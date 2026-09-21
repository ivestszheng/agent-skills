# -*- coding: utf-8 -*-
"""钱迹本地数据库读取工具。

仅使用 Python 标准库（sqlite3 / json / shutil），无第三方依赖。

钱迹 Windows 桌面版会在本地保存一份完整的 SQLite 库：
    %APPDATA%\\com.mutangtech.qianji.win\\qianji_flutter\\qianjiapp.db
客户端运行时会独占该文件，因此本模块默认先复制到临时目录再只读打开。

用法::

    from qianji import Qianji

    q = Qianji()                    # 自动定位 + 复制
    q.balance_sheet()               # 资产 / 负债 / 净资产
    q.summary(2026)                 # 收支概览 + 月度明细
    q.category_spend(2026)          # 分类支出排行
    q.close()                       # 清理临时副本

命令行自测::

    python qianji.py                # 打印发现路径 + 各表行数 + 收支概览
"""

from __future__ import annotations

import collections
import datetime
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile

__all__ = ["Qianji", "find_db", "candidate_paths", "NOT_BALANCE", "fmt", "wan",
           "INVEST_STYPES", "mask_text", "mask_path", "MASKED_FIELDS"]

# ---------------------------------------------------------------- 常量

#: 过滤「平账」分录的统一条件。资产余额校准会生成 remark 形如
#: ``平账(旧值 ~ 新值)`` 的流水，但分类挂在「日常」/「其它收益」下，
#: 必须排除否则会把资产浮盈浮亏算成收支。
NOT_BALANCE = "(remark IS NULL OR remark NOT LIKE '平账%')"

BILL_TYPE_NAMES = {
    0: "支出",
    1: "收入",
    2: "转账",
    3: "还信用卡",
    5: "借出/借入",
    6: "借出",
    9: "借出收回",
    20: "退款",
    21: "报销收款",
}

ASSET_TYPE_NAMES = {
    1: "资金账户",
    2: "信用卡",
    3: "押金",
    4: "投资",
    5: "借入借出",
}

# 资产 stype 分组（用于生成资产配置）
GROUP_RULES = [
    ("股票/权益", {41, 42, 43}),
    ("债券/理财", {48, 49}),
    ("固定收益/储蓄险", {47}),
    ("现金活期", {11, 12, 13, 14, 102, 107}),
    ("公积金/医保", {17, 18}),
    ("押金", {35}),
]
GROUP_FALLBACK = "其他"

#: 投资类 stype —— 只有这几类的 ``money - initmoney`` 才是真正的浮动盈亏。
#: 银行卡/公积金等账户的 ``initmoney`` 只是记录起点余额，差额是资金进出，
#: 不是盈亏，展示时要显示为 “-”。
INVEST_STYPES = {41, 42, 43, 47, 48, 49}


def candidate_paths():
    """返回候选数据库路径（按优先级）。"""
    paths = []
    appdata = os.environ.get("APPDATA")
    if appdata:
        paths.append(
            os.path.join(
                appdata, "com.mutangtech.qianji.win", "qianji_flutter", "qianjiapp.db"
            )
        )
    local = os.environ.get("LOCALAPPDATA")
    if local:
        paths.append(
            os.path.join(
                local, "com.mutangtech.qianji.win", "qianji_flutter", "qianjiapp.db"
            )
        )
    # macOS / Linux 下的可能位置（非官方桌面版，仅作兜底）
    home = os.path.expanduser("~")
    paths += [
        os.path.join(home, "Documents", "qianjiapp.db"),
        os.path.join(home, "Downloads", "qianjiapp.db"),
    ]
    return paths


def find_db():
    """自动定位钱迹数据库，找不到返回 None。"""
    for p in candidate_paths():
        if os.path.isfile(p):
            return p
    return None


def fmt(x):
    """金额千分位格式化。"""
    try:
        return "{:,.2f}".format(float(x))
    except (TypeError, ValueError):
        return str(x)


def wan(x):
    """金额转「万」为单位的紧凑显示。"""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    if abs(v) >= 10000:
        return "{:.2f} 万".format(v / 10000)
    return "{:,.0f}".format(v)


def _ts(t, f="%Y-%m-%d"):
    try:
        return datetime.datetime.fromtimestamp(t).strftime(f)
    except (TypeError, ValueError, OSError, OverflowError):
        return str(t)


# ---------------------------------------------------------------- 脱敏
#
# 原则：库层（Qianji）返回**原始数据**，只在「渲染给用户看」的地方套脱敏，
# 避免过滤掉数据本身影响统计。以下两个函数是唯一的脱敏入口，任何写入
# 报告 / Markdown / JSON 的文本都应先过一遍。
#
# 高敏字段（务必不要输出原文）：
#   user_card.cardno  银行卡/证券账号明文
#   user_card.owner   持卡人姓名
#   user_card.images  卡面图片（base64 或本地文件路径）
#   user_card.userid / user_book2.userid / user_book2.memberid  账号标识
#   book_member.name  账本成员昵称
#   数据库文件路径     含操作系统登录用户名

#: 明确不应出现在任何输出里的字段名
MASKED_FIELDS = ("cardno", "owner", "images", "userid", "memberid")

_RE_IDCARD = re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")
_RE_MOBILE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
_RE_LONGCARD = re.compile(r"(?<!\d)\d{15,19}(?!\d)")
_RE_USERDIR = re.compile(r"([\\/])[Uu]sers\1[^\\/]+")


def mask_text(s):
    """对任意文本里的身份证、手机号、长数字串（卡号）做脱敏。

    只用于输出渲染，不改变查询结果。
    """
    if s is None:
        return s
    s = str(s)
    if not s:
        return s
    s = _RE_IDCARD.sub(lambda m: m.group()[:3] + "*" * 11 + m.group()[-4:], s)
    s = _RE_MOBILE.sub(lambda m: m.group()[:3] + "****" + m.group()[-4:], s)
    s = _RE_LONGCARD.sub(lambda m: m.group()[:2] + "****" + m.group()[-2:], s)
    return s


def mask_path(p):
    """把路径里的操作系统登录用户名抹掉（`C:\\Users\\xxx\\...` → `~\\...`）。"""
    if not p:
        return p
    p = str(p)
    home = os.path.expanduser("~")
    if home and home not in ("~", "/") and p.lower().startswith(home.lower()):
        return "~" + p[len(home):]
    return _RE_USERDIR.sub(lambda m: m.group(1) + "Users" + m.group(1) + "***", p)


class Qianji:
    """钱迹本地库的只读访问对象。"""

    def __init__(self, db_path=None, live=False, workdir=None):
        """
        :param db_path: 指定数据库路径；None 时自动定位
        :param live: True 则直接读原库（客户端未运行时才可用，不会复制）
        :param workdir: 临时副本存放目录，默认系统临时目录
        """
        src = db_path or find_db()
        if not src:
            raise FileNotFoundError(
                "未找到钱迹数据库，请用 db_path 显式指定。已尝试：\n  "
                + "\n  ".join(mask_path(p) for p in candidate_paths())
            )
        if not os.path.isfile(src):
            raise FileNotFoundError("数据库不存在：{}".format(mask_path(src)))

        self.source = os.path.abspath(src)
        self._tmpdir = None
        if live:
            target = self.source
        else:
            self._tmpdir = tempfile.mkdtemp(prefix="qianji-", dir=workdir)
            target = os.path.join(self._tmpdir, "qianjiapp.db")
            shutil.copy2(self.source, target)

        # 只读打开，避免误写
        self.conn = sqlite3.connect("file:{}?mode=ro".format(target), uri=True)
        self.conn.row_factory = sqlite3.Row
        self._cats = None
        self._atypes = None

    # ------------------------------------------------------------ 基础

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass
        if self._tmpdir and os.path.isdir(self._tmpdir):
            shutil.rmtree(self._tmpdir, ignore_errors=True)
            self._tmpdir = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def rows(self, sql, args=()):
        return [dict(r) for r in self.conn.execute(sql, args)]

    def one(self, sql, args=()):
        r = self.conn.execute(sql, args).fetchone()
        return dict(r) if r else None

    # ------------------------------------------------------ 字典 / 元数据

    @property
    def categories(self):
        """{分类id: 分类字典}"""
        if self._cats is None:
            self._cats = {r["id"]: r for r in self.rows("SELECT * FROM category")}
        return self._cats

    def category_name(self, cid):
        c = self.categories.get(cid)
        return c["name"] if c else str(cid)

    @property
    def asset_types(self):
        """{(type, stype): 类别中文名}，来自 asset_type.type 里的 JSON。"""
        if self._atypes is None:
            d = {}
            for r in self.rows("SELECT name, type FROM asset_type"):
                if not r["type"]:
                    continue
                try:
                    j = json.loads(r["type"])
                except (ValueError, TypeError):
                    continue
                if not isinstance(j, dict) or not j.get("name"):
                    continue
                d[(j.get("type"), j.get("stype"))] = j["name"]
            self._atypes = d
        return self._atypes

    def books(self, safe=True):
        """账本列表。

        :param safe: True 时剔除 `userid` / `memberid` 等账号标识字段
        """
        rows = self.rows("SELECT * FROM user_book2")
        if not safe:
            return rows
        return [
            {k: v for k, v in r.items() if k not in ("userid", "memberid")}
            for r in rows
        ]

    def available_years(self):
        return [
            r["y"]
            for r in self.rows(
                "SELECT DISTINCT strftime('%Y', time, 'unixepoch', 'localtime') y "
                "FROM user_bill ORDER BY y"
            )
            if r["y"]
        ]

    def date_range(self):
        r = self.one("SELECT MIN(time) a, MAX(time) b, COUNT(*) c FROM user_bill")
        return {
            "start": _ts(r["a"]),
            "end": _ts(r["b"]),
            "count": r["c"],
        }

    def cards(self, mask=True):
        """银行卡 / 证券账户。

        默认做三件事：卡号只留前 4 后 4、持卡人姓名只留姓氏、剔除
        `userid` 与 `images`（卡面图片，可能是 base64 或本地图片路径）。
        """
        out = []
        for row in self.rows("SELECT * FROM user_card"):
            r = dict(row)
            no = (r.get("cardno") or "").replace(" ", "")
            r["cardno"] = (no[:4] + "****" + no[-4:]) if (mask and len(no) > 8) else no
            owner = r.get("owner")
            if mask and owner:
                owner = str(owner)
                r["owner"] = owner[0] + "*" * (len(owner) - 1)
            if mask:
                if r.get("remark"):
                    r["remark"] = mask_text(r["remark"])
                for k in ("userid", "images"):
                    r.pop(k, None)
            out.append(r)
        return out

    # -------------------------------------------------------------- 流水

    def _year_clause(self, year, args):
        if year is None:
            return "1=1"
        args.append(str(year))
        return "strftime('%Y', time, 'unixepoch', 'localtime') = ?"

    def bills(self, year=None, exclude_balance=True, types=None):
        """查询流水。默认剔除平账分录。"""
        args = []
        where = [self._year_clause(year, args)]
        if exclude_balance:
            where.append(NOT_BALANCE)
        if types:
            where.append("type IN ({})".format(",".join("?" * len(types))))
            args.extend(types)
        sql = "SELECT * FROM user_bill WHERE {} ORDER BY time".format(" AND ".join(where))
        return self.rows(sql, args)

    def summary(self, year=None):
        """收支概览：总额 + 逐月明细。

        - ``expense`` 为毛支出（type=0，剔除平账）
        - ``net_expense`` = expense - refund（type=20）
        - ``income`` 已剔除收入侧平账
        """
        args = []
        where = self._year_clause(year, args)
        r = self.one(
            """SELECT
                SUM(CASE WHEN type=0 AND {nb} THEN money ELSE 0 END) expense,
                SUM(CASE WHEN type=0 AND {nb} THEN 1 ELSE 0 END) expense_count,
                SUM(CASE WHEN type=1 AND {nb} THEN money ELSE 0 END) income,
                SUM(CASE WHEN type=1 AND {nb} THEN 1 ELSE 0 END) income_count,
                SUM(CASE WHEN type=20 THEN money ELSE 0 END) refund,
                SUM(CASE WHEN type=1 AND remark LIKE '平账%' THEN money ELSE 0 END) income_adjust,
                SUM(CASE WHEN type=0 AND remark LIKE '平账%' THEN money ELSE 0 END) expense_adjust
               FROM user_bill WHERE {w}""".format(nb=NOT_BALANCE, w=where),
            args,
        )
        income = r["income"] or 0.0
        expense = r["expense"] or 0.0
        refund = r["refund"] or 0.0
        net = expense - refund

        margs = []
        mwhere = self._year_clause(year, margs)
        months = []
        for m in self.rows(
            """SELECT strftime('%Y-%m', time, 'unixepoch', 'localtime') m,
                SUM(CASE WHEN type=0 AND {nb} THEN money ELSE 0 END) expense,
                SUM(CASE WHEN type=20 THEN money ELSE 0 END) refund,
                SUM(CASE WHEN type=1 AND {nb} THEN money ELSE 0 END) income,
                COUNT(*) cnt
               FROM user_bill WHERE {w} GROUP BY m ORDER BY m""".format(
                nb=NOT_BALANCE, w=mwhere
            ),
            margs,
        ):
            e = m["expense"] or 0.0
            i = m["income"] or 0.0
            rf = m["refund"] or 0.0
            months.append(
                {
                    "month": m["m"],
                    "expense": e,
                    "refund": rf,
                    "net_expense": e - rf,
                    "income": i,
                    "surplus": i - (e - rf),
                    "count": m["cnt"],
                }
            )

        return {
            "year": year,
            "income": income,
            "income_count": r["income_count"] or 0,
            "expense": expense,
            "expense_count": r["expense_count"] or 0,
            "refund": refund,
            "net_expense": net,
            "surplus": income - net,
            "savings_rate": (income - net) / income * 100 if income else 0.0,
            "balance_adjust_income": r["income_adjust"] or 0.0,
            "balance_adjust_expense": r["expense_adjust"] or 0.0,
            "months": months,
        }

    def category_spend(self, year=None, net=True):
        """分类支出排行。net=True 时按毛支出统计（退款不逐项冲减分类）。"""
        args = []
        where = [self._year_clause(year, args), NOT_BALANCE, "type=0"]
        rows = self.rows(
            "SELECT cateid, SUM(money) s, COUNT(*) c FROM user_bill "
            "WHERE {} GROUP BY cateid ORDER BY s DESC".format(" AND ".join(where)),
            args,
        )
        return [
            {"category": self.category_name(r["cateid"]), "amount": r["s"], "count": r["c"]}
            for r in rows
        ]

    def income_by_category(self, year=None):
        args = []
        where = [self._year_clause(year, args), NOT_BALANCE, "type=1"]
        rows = self.rows(
            "SELECT cateid, SUM(money) s, COUNT(*) c FROM user_bill "
            "WHERE {} GROUP BY cateid ORDER BY s DESC".format(" AND ".join(where)),
            args,
        )
        total = sum(r["s"] for r in rows) or 1
        return [
            {
                "category": self.category_name(r["cateid"]),
                "amount": r["s"],
                "count": r["c"],
                "share": r["s"] / total * 100,
            }
            for r in rows
        ]

    def balance_adjustments(self):
        """所有平账分录（用于向用户解释口径）。"""
        return self.rows(
            "SELECT * FROM user_bill WHERE remark LIKE '平账%' ORDER BY time"
        )

    # -------------------------------------------------------------- 资产

    def assets(self):
        """资产明细，附中文类别与浮动盈亏。"""
        out = []
        for r in self.rows("SELECT * FROM user_asset ORDER BY type, stype, money DESC"):
            extra = {}
            if r.get("extra"):
                try:
                    extra = json.loads(r["extra"])
                except (ValueError, TypeError):
                    extra = {}
            if not isinstance(extra, dict):
                extra = {}
            credit = {}
            if r.get("credit"):
                try:
                    credit = json.loads(r["credit"])
                except (ValueError, TypeError):
                    credit = {}
            if not isinstance(credit, dict):
                credit = {}
            loan = {}
            if r.get("loan"):
                try:
                    loan = json.loads(r["loan"])
                except (ValueError, TypeError):
                    loan = {}
            if not isinstance(loan, dict):
                loan = {}
            cost = extra.get("initmoney")
            r = dict(r)
            r.pop("userid", None)
            # 账户名与备注可能被人为写进卡号 / 手机号 / 姓名，输出前统一过一遍
            r["name"] = mask_text(r["name"])
            r["remark"] = mask_text(r["remark"])
            r["type_name"] = ASSET_TYPE_NAMES.get(r["type"], str(r["type"]))
            r["stype_name"] = self.asset_types.get((r["type"], r["stype"])) or ""
            r["cost"] = cost
            r["pnl"] = (r["money"] - cost) if (cost and r["stype"] in INVEST_STYPES) else None
            r["extra_json"] = extra
            r["credit_json"] = credit
            r["loan_json"] = loan
            out.append(r)
        return out

    def group_of(self, asset):
        for name, stypes in GROUP_RULES:
            if asset["stype"] in stypes:
                return name
        return GROUP_FALLBACK

    def balance_sheet(self, include_cleared=False):
        """资产负债表。

        :param include_cleared: 是否包含「借入借出」这类已结清（money=0）账户
        """
        groups = collections.OrderedDict((n, []) for n, _ in GROUP_RULES)
        groups[GROUP_FALLBACK] = []
        liabilities = []
        for a in self.assets():
            if a["type"] == 2:  # 信用卡等负债
                liabilities.append(a)
                continue
            if a["type"] == 5:  # 借入借出
                if include_cleared or a["money"]:
                    groups.setdefault("借入借出", []).append(a)
                continue
            groups[self.group_of(a)].append(a)

        if not include_cleared:
            groups = collections.OrderedDict(
                (k, v) for k, v in groups.items() if v
            )
        total = sum(a["money"] for v in groups.values() for a in v)
        debt = sum(a["money"] for a in liabilities if a["money"] > 0)
        return {
            "groups": groups,
            "assets": total,
            "liabilities": debt,
            "net": total - debt,
            "liability_accounts": liabilities,
        }

    # -------------------------------------------------------------- 预算

    def budgets(self, year):
        return self.rows(
            "SELECT * FROM user_budget WHERE typeinfo LIKE ? ORDER BY type, flag, money DESC",
            ("{}%".format(year),),
        )

    def budget_execution(self, year):
        """年度分类预算执行情况。实际值取该分类毛支出（剔除平账）。"""
        rows = self.rows(
            "SELECT * FROM user_budget WHERE type=2 AND flag=2 AND typeinfo=?",
            (str(year),),
        )
        total_row = self.one(
            "SELECT money FROM user_budget WHERE type=2 AND flag=1 AND typeinfo=?",
            (str(year),),
        )
        spend = {x["category"]: x["amount"] for x in self.category_spend(year)}
        items = []
        for r in rows:
            name = self.category_name(r["cateid"])
            actual = spend.get(name, 0.0)
            items.append(
                {
                    "category": name,
                    "budget": r["money"],
                    "actual": actual,
                    "rate": actual / r["money"] * 100 if r["money"] else 0.0,
                    "remain": r["money"] - actual,
                }
            )
        items.sort(key=lambda x: -x["budget"])
        budget_total = sum(i["budget"] for i in items)
        actual_total = sum(i["actual"] for i in items)
        return {
            "year": year,
            "declared_total": total_row["money"] if total_row else None,
            "budget_total": budget_total,
            "actual_total": actual_total,
            "rate": actual_total / budget_total * 100 if budget_total else 0.0,
            "items": items,
        }

    def operation_log(self):
        return self.rows("SELECT * FROM user_log ORDER BY time")


# ---------------------------------------------------------------- 自测

def _main():
    q = Qianji()
    print("数据库：", mask_path(q.source))
    r = q.date_range()
    print("记录区间：{} ~ {}，共 {} 笔".format(r["start"], r["end"], r["count"]))
    print("账本：", [b["name"] for b in q.books()])
    print("年份：", q.available_years())
    bs = q.balance_sheet()
    print("净资产：{} 元（资产 {} / 负债 {}）".format(
        fmt(bs["net"]), fmt(bs["assets"]), fmt(bs["liabilities"])))
    for name, items in bs["groups"].items():
        print("  {:<12}{:>14} 元  {}".format(
            name, fmt(sum(a["money"] for a in items)),
            "、".join(a["name"] for a in items)))
    for y in q.available_years():
        s = q.summary(y)
        print("[{}] 收入 {} / 净支出 {} / 结余 {} / 储蓄率 {:.1f}%".format(
            y, fmt(s["income"]), fmt(s["net_expense"]),
            fmt(s["surplus"]), s["savings_rate"]))
    adj = q.balance_adjustments()
    print("平账分录 {} 笔，合计 {:.2f} 元（已从统计中剔除）".format(
        len(adj), sum(a["money"] for a in adj)))
    q.close()


if __name__ == "__main__":
    _main()
