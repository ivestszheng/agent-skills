# -*- coding: utf-8 -*-
"""钱迹账本分析 —— 输出 Markdown / JSON 摘要。

用法::

    python analyze.py                        # 全量概览
    python analyze.py --year 2026            # 指定年份
    python analyze.py --year 2026 --md 报告.md
    python analyze.py --year 2026 --json data.json
    python analyze.py --db D:\\export\\qianjiapp.db
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qianji import Qianji, fmt, wan, mask_path, mask_text  # noqa: E402


def build(q, year=None, top=12):
    """把分析结果整理成一个纯数据 dict。

    输出前统一脱敏：路径抹掉登录用户名，账户名 / 备注过敏感串过滤，
    信用卡只保留额度等必要字段，不含卡号、持卡人、userid。
    """
    bs = q.balance_sheet()
    rng = q.date_range()
    data = {
        "source": mask_path(q.source),
        "range": rng,
        "books": [b["name"] for b in q.books()],
        "balance_sheet": {
            "assets": bs["assets"],
            "liabilities": bs["liabilities"],
            "net": bs["net"],
            "groups": [
                {
                    "name": name,
                    "amount": sum(a["money"] for a in items),
                    "accounts": [
                        {
                            "name": a["name"],
                            "stype": a["stype_name"],
                            "money": a["money"],
                            "cost": a["cost"],
                            "pnl": a["pnl"],
                            "remark": a["remark"],
                        }
                        for a in sorted(items, key=lambda x: -x["money"])
                    ],
                }
                for name, items in bs["groups"].items()
            ],
            "liability_accounts": [
                {
                    "name": mask_text(a["name"]),
                    "money": a["money"],
                    "limit": (a.get("credit_json") or {}).get("limit"),
                    "statedate": (a.get("credit_json") or {}).get("statedate"),
                    "paydate": (a.get("credit_json") or {}).get("paydate2"),
                }
                for a in bs["liability_accounts"]
            ],
        },
        "years": [],
        "balance_adjustments": {
            "count": len(q.balance_adjustments()),
            "amount": sum(a["money"] for a in q.balance_adjustments()),
        },
    }
    for y in (q.available_years() if year is None else [str(year)]):
        s = q.summary(y)
        data["years"].append(
            {
                "year": y,
                "summary": s,
                "category_spend": q.category_spend(y)[:top],
                "income_by_category": q.income_by_category(y),
                "budget": q.budget_execution(y),
            }
        )
    return data


def to_markdown(data, top=12):
    o = []
    a = o.append
    a("# 钱迹账本分析")
    a("")
    a("- 数据来源：`{}`".format(data["source"]))
    a("- 记录区间：{} ~ {}，共 {} 笔".format(
        data["range"]["start"], data["range"]["end"], data["range"]["count"]))
    a("- 账本：{}".format("、".join(data["books"])))
    a("")

    bs = data["balance_sheet"]
    a("## 资产与净资产")
    a("")
    a("| 项目 | 金额（元） |")
    a("|---|---:|")
    for g in bs["groups"]:
        a("| {} | {} |".format(g["name"], fmt(g["amount"])))
    a("| **总资产** | **{}** |".format(fmt(bs["assets"])))
    a("| 负债 | {} |".format(fmt(bs["liabilities"])))
    a("| **净资产** | **{}** |".format(fmt(bs["net"])))
    a("")
    for g in bs["groups"]:
        a("### {}".format(g["name"]))
        a("")
        a("| 账户 | 类别 | 当前金额 | 记录成本 | 浮动盈亏 | 备注 |")
        a("|---|---|---:|---:|---:|---|")
        for acc in g["accounts"]:
            is_invest = acc["pnl"] is not None
            a("| {} | {} | {} | {} | {} | {} |".format(
                acc["name"], acc["stype"], fmt(acc["money"]),
                fmt(acc["cost"]) if is_invest else "-",
                ("{:+,.2f}".format(acc["pnl"]) if is_invest else "-"),
                acc["remark"] or ""))
        a("")

    for y in data["years"]:
        s = y["summary"]
        a("## {} 年收支".format(y["year"]))
        a("")
        a("- 收入：{} 元（{} 笔）".format(fmt(s["income"]), s["income_count"]))
        a("- 毛支出：{} 元（{} 笔）".format(fmt(s["expense"]), s["expense_count"]))
        a("- 退款：{} 元".format(fmt(s["refund"])))
        a("- **净支出：{} 元**".format(fmt(s["net_expense"])))
        a("- **结余：{} 元（储蓄率 {:.1f}%）**".format(
            fmt(s["surplus"]), s["savings_rate"]))
        if s["months"]:
            a("- 月均净支出：{} 元".format(
                fmt(s["net_expense"] / len(s["months"]))))
        a("")
        a("| 月份 | 毛支出 | 退款 | 净支出 | 收入 | 结余 | 笔数 |")
        a("|---|---:|---:|---:|---:|---:|---:|")
        for m in s["months"]:
            a("| {} | {} | {} | {} | {} | {} | {} |".format(
                m["month"], fmt(m["expense"]), fmt(m["refund"]),
                fmt(m["net_expense"]), fmt(m["income"]),
                fmt(m["surplus"]), m["count"]))
        a("| **合计** | **{}** | **{}** | **{}** | **{}** | **{}** | {} |".format(
            fmt(s["expense"]), fmt(s["refund"]), fmt(s["net_expense"]),
            fmt(s["income"]), fmt(s["surplus"]),
            sum(m["count"] for m in s["months"])))
        a("")

        a("### 支出分类 TOP {}".format(top))
        a("")
        a("| 分类 | 金额 | 笔数 | 占比 |")
        a("|---|---:|---:|---:|")
        total = sum(c["amount"] for c in y["category_spend"]) or 1
        for c in y["category_spend"]:
            a("| {} | {} | {} | {:.1f}% |".format(
                c["category"], fmt(c["amount"]), c["count"],
                c["amount"] / total * 100))
        a("")

        a("### 收入结构")
        a("")
        a("| 来源 | 金额 | 占比 | 笔数 |")
        a("|---|---:|---:|---:|")
        for c in y["income_by_category"]:
            a("| {} | {} | {:.1f}% | {} |".format(
                c["category"], fmt(c["amount"]), c["share"], c["count"]))
        a("")

        b = y["budget"]
        if b["items"]:
            a("### 预算执行（年度预算 {} 元）".format(
                fmt(b["declared_total"] or b["budget_total"])))
            a("")
            a("| 分类 | 预算 | 已花 | 执行率 | 剩余 |")
            a("|---|---:|---:|---:|---:|")
            for i in b["items"]:
                flag = " ⚠️超支" if i["rate"] >= 100 else ""
                a("| {}{} | {} | {} | {:.1f}% | {} |".format(
                    i["category"], flag, fmt(i["budget"]), fmt(i["actual"]),
                    i["rate"], fmt(i["remain"])))
            a("| **合计** | **{}** | **{}** | **{:.1f}%** | **{}** |".format(
                fmt(b["budget_total"]), fmt(b["actual_total"]), b["rate"],
                fmt(b["budget_total"] - b["actual_total"])))
            a("")

    adj = data["balance_adjustments"]
    if adj["count"]:
        a("## 口径说明")
        a("")
        a("已从统计中剔除 {} 笔资产余额校准「平账」分录（合计 {} 元）。".format(
            adj["count"], fmt(adj["amount"])))
        a("这类分录备注形如 `平账(旧值 ~ 新值)`，但分类会落到「日常」/「其它收益」，")
        a("若不过滤会把资产浮盈浮亏当成收支。")
        a("")
    return "\n".join(o)


def main(argv=None):
    ap = argparse.ArgumentParser(description="钱迹账本分析")
    ap.add_argument("--db", help="数据库路径（默认自动定位）")
    ap.add_argument("--year", help="只分析指定年份，如 2026")
    ap.add_argument("--md", help="Markdown 输出路径")
    ap.add_argument("--json", dest="json_out", help="JSON 输出路径")
    ap.add_argument("--top", type=int, default=12, help="分类排行条数，默认 12")
    ap.add_argument("--live", action="store_true", help="直接读原库（不复制）")
    args = ap.parse_args(argv)

    q = Qianji(db_path=args.db, live=args.live)
    try:
        data = build(q, args.year, args.top)
    finally:
        q.close()

    md = to_markdown(data, args.top)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as f:
            f.write(md)
        print("已写入 Markdown：{}".format(os.path.abspath(args.md)))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("已写入 JSON：{}".format(os.path.abspath(args.json_out)))
    if not args.md and not args.json_out:
        sys.stdout.write(md)


if __name__ == "__main__":
    main()
