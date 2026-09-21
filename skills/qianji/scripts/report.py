# -*- coding: utf-8 -*-
"""生成钱迹财务分析报告（自包含 HTML，无外部依赖）。

用法::

    python report.py                                  # 默认输出到当前目录
    python report.py --year 2026 --out 报告.html
    python report.py --db D:\\export\\qianjiapp.db --open

产物为单个 HTML 文件：内联 SVG 环形图 + 纯 CSS 柱状图，不引用任何 CDN，
双击即可离线打开。
"""

from __future__ import annotations

import argparse
import datetime
import html
import math
import os
import sys
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from qianji import Qianji, fmt, wan, mask_path, mask_text  # noqa: E402

PALETTE = ["#4C6FFF", "#8B5CF6", "#F59E0B", "#10B981", "#06B6D4",
           "#94A3B8", "#EF4444", "#EC4899"]

STYLE = """
:root{--bg:#0f1117;--card:#171a23;--line:#2a2f3c;--fg:#e8ecf3;--mut:#8b93a7;
--blue:#4C6FFF;--green:#10B981;--red:#EF4444;--amber:#F59E0B}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.7 -apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:32px 22px 64px}
h1{font-size:26px;margin:0 0 6px}
h2{font-size:18px;margin:38px 0 14px;padding-left:11px;border-left:3px solid var(--blue)}
h3{font-size:15px;margin:20px 0 8px;color:var(--mut);font-weight:600}
.sub{color:var(--mut);font-size:13px;margin-bottom:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:12px;margin-top:16px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.kpi .l{font-size:12px;color:var(--mut)}
.kpi .v{font-size:22px;font-weight:700;margin-top:4px;letter-spacing:-.4px}
.kpi .d{font-size:12px;color:var(--mut);margin-top:2px}
.blue{color:var(--blue)}.green{color:var(--green)}.red{color:var(--red)}.amber{color:var(--amber)}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin-top:14px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;color:var(--mut);font-weight:600;font-size:12px;padding:8px 6px;border-bottom:1px solid var(--line)}
td{padding:8px 6px;border-bottom:1px solid rgba(42,47,60,.5)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.donutwrap{display:flex;gap:26px;align-items:center;flex-wrap:wrap}
.legend{flex:1;min-width:260px}
.lg{display:flex;align-items:center;gap:9px;padding:5px 0;font-size:13.5px}
.dot{width:11px;height:11px;border-radius:3px;flex:none;display:inline-block}
.lg .amt{margin-left:auto;font-variant-numeric:tabular-nums;color:var(--mut)}
.chart{display:flex;gap:12px;align-items:flex-end;padding:14px 4px 0;overflow-x:auto}
.bcol{flex:1;min-width:52px;text-align:center}
.bwrap{display:flex;gap:3px;align-items:flex-end;justify-content:center;height:158px;border-bottom:1px solid var(--line)}
.bar{width:15px;border-radius:3px 3px 0 0;position:relative}
.bar.inc{background:linear-gradient(180deg,#34d399,#10B981)}
.bar.exp{background:linear-gradient(180deg,#f87171,#EF4444)}
.bar span{position:absolute;top:-17px;left:50%;transform:translateX(-50%);font-size:10px;color:var(--mut);white-space:nowrap}
.blab{font-size:11.5px;color:var(--mut);margin-top:6px}
.crow{display:flex;align-items:center;gap:11px;margin:7px 0}
.cname{width:96px;font-size:13px;flex:none;text-align:right;color:#c9d1e0}
.ctrack{flex:1;height:17px;background:#12151d;border-radius:5px;overflow:hidden}
.cfill{height:100%;border-radius:5px}
.cval{width:150px;font-size:12.5px;font-variant-numeric:tabular-nums;flex:none}
.cpct{color:var(--mut);margin-left:7px;font-size:11.5px}
.ptrack{height:7px;background:#12151d;border-radius:4px;overflow:hidden;min-width:80px}
.pfill{height:100%}
.pfill.ok{background:var(--green)}.pfill.warn{background:var(--amber)}.pfill.over{background:var(--red)}
.up{color:var(--green)}.down{color:var(--red)}
.warn-t{color:var(--amber)}.over{color:var(--red)}.ok{color:var(--green)}
ul{margin:8px 0;padding-left:20px}li{margin:6px 0}
.tag{display:inline-block;padding:2px 9px;border-radius:20px;font-size:11.5px;margin-right:6px}
.t-red{background:rgba(239,68,68,.14);color:#fca5a5}
.t-amber{background:rgba(245,158,11,.14);color:#fcd34d}
.t-green{background:rgba(16,185,129,.14);color:#6ee7b7}
.t-blue{background:rgba(76,111,255,.16);color:#a5b8ff}
.note{font-size:12.5px;color:var(--mut);margin-top:10px;line-height:1.6}
.rem{color:var(--mut);font-size:12px}
"""


def esc(x):
    return html.escape(str(x if x is not None else ""))


def build_html(q, year=None, suggest=True):
    """组装 HTML 报告字符串。"""
    rng = q.date_range()
    bs = q.balance_sheet()
    years = q.available_years()
    if year is None:
        year = years[-1] if years else None
    year = str(year) if year else None

    s = q.summary(year) if year else q.summary(None)
    cats = q.category_spend(year) if year else q.category_spend(None)
    incomes = q.income_by_category(year) if year else q.income_by_category(None)
    budget = q.budget_execution(year) if year else None
    adj = q.balance_adjustments()

    total_assets = bs["assets"]
    net = bs["net"]
    months = s["months"]
    monthly_avg = s["net_expense"] / len(months) if months else 0

    # ---- 资产配置环形图
    alloc = [(name, sum(a["money"] for a in items))
             for name, items in bs["groups"].items()]
    alloc = [x for x in alloc if x[1]]
    alloc.sort(key=lambda x: -x[1])
    R, C = 76, 2 * math.pi * 76
    off, segs = 0.0, []
    for i, (k, v) in enumerate(alloc):
        frac = v / total_assets if total_assets else 0
        dash = frac * C
        segs.append(
            '<circle cx="100" cy="100" r="{}" fill="none" stroke="{}" stroke-width="26" '
            'stroke-dasharray="{:.2f} {:.2f}" stroke-dashoffset="{:.2f}" '
            'transform="rotate(-90 100 100)"><title>{} {} 元 {:.1f}%</title></circle>'.format(
                R, PALETTE[i % len(PALETTE)], max(dash - 2, 0), C - dash + 2,
                -off, esc(k), fmt(v), frac * 100))
        off += dash
    donut = "".join(segs)
    legend = "".join(
        '<div class="lg"><span class="dot" style="background:{}"></span>{}'
        '<span class="amt">{} 元 · {:.1f}%</span></div>'.format(
            PALETTE[i % len(PALETTE)], esc(k), fmt(v),
            (v / total_assets * 100) if total_assets else 0)
        for i, (k, v) in enumerate(alloc))

    # ---- 资产明细表
    asset_rows = []
    for gname, items in bs["groups"].items():
        for a in sorted(items, key=lambda x: -x["money"]):
            pnl = "-"
            if a["pnl"] is not None:
                cls = "up" if a["pnl"] >= 0 else "down"
                pnl = '<span class="{}">{:+,.0f}</span>'.format(cls, a["pnl"])
            asset_rows.append(
                "<tr><td>{}</td><td>{}</td><td class=\"num\">{}</td>"
                "<td class=\"num\">{}</td><td class=\"rem\">{}</td></tr>".format(
                    esc(a["name"]), esc(gname), fmt(a["money"]), pnl,
                    esc(a["remark"] or "")))
    asset_table = "".join(asset_rows)

    stock = [a for n, items in bs["groups"].items() if n == "股票/权益"
             for a in items]
    stock_val = sum(a["money"] for a in stock)
    priced = [a for a in stock if a["pnl"] is not None]
    stock_cost = sum(a["cost"] for a in priced)
    stock_pnl = sum(a["pnl"] for a in priced)

    cash = sum(a["money"] for n, items in bs["groups"].items() if n == "现金活期"
               for a in items)
    cover = cash / monthly_avg if monthly_avg else 0

    liab_note = "；".join(
        "{}（额度 {}）".format(
            esc(a["name"]),
            fmt((a.get("credit_json") or {}).get("limit", 0)))
        for a in bs["liability_accounts"]) or "无负债账户"

    # ---- 月度柱状图
    mx = max([m["income"] for m in months] + [m["net_expense"] for m in months] + [1])
    bars = []
    for m in months:
        hi, he = m["income"] / mx * 150, m["net_expense"] / mx * 150
        bars.append(
            '<div class="bcol"><div class="bwrap">'
            '<div class="bar inc" style="height:{:.1f}px" title="收入 {}"><span>{}</span></div>'
            '<div class="bar exp" style="height:{:.1f}px" title="净支出 {}"><span>{}</span></div>'
            '</div><div class="blab">{}月</div></div>'.format(
                hi, fmt(m["income"]), wan(m["income"]), he, fmt(m["net_expense"]),
                wan(m["net_expense"]), m["month"][5:]))
    monthly_chart = "".join(bars)

    month_rows = "".join(
        '<tr><td>{}</td><td class="num">{}</td><td class="num">{}</td>'
        '<td class="num {}">{}</td></tr>'.format(
            m["month"], fmt(m["net_expense"]), fmt(m["income"]),
            "green" if m["surplus"] >= 0 else "red", fmt(m["surplus"]))
        for m in months)

    # ---- 分类支出条形
    cmax = max([c["amount"] for c in cats] + [1])
    ctotal = sum(c["amount"] for c in cats) or 1
    cat_bars = "".join(
        '<div class="crow"><div class="cname">{}</div>'
        '<div class="ctrack"><div class="cfill" style="width:{:.1f}%;background:{}"></div></div>'
        '<div class="cval">{}<span class="cpct">{:.1f}% · {}笔</span></div></div>'.format(
            esc(c["category"]), c["amount"] / cmax * 100,
            PALETTE[i % len(PALETTE)], fmt(c["amount"]),
            c["amount"] / ctotal * 100, c["count"])
        for i, c in enumerate(cats))

    inc_rows = "".join(
        '<tr><td>{}</td><td class="num">{}</td><td class="num">{:.1f}%</td>'
        '<td class="num">{}</td></tr>'.format(
            esc(c["category"]), fmt(c["amount"]), c["share"], c["count"])
        for c in incomes)

    # ---- 预算
    bud_html = ""
    if budget and budget["items"]:
        rows = []
        for i in budget["items"]:
            cls = "over" if i["rate"] >= 100 else ("warn" if i["rate"] >= 85 else "ok")
            rows.append(
                '<tr><td>{}</td><td class="num">{}</td><td class="num">{}</td>'
                '<td class="num {}">{:.1f}%</td>'
                '<td><div class="ptrack"><div class="pfill {}" style="width:{:.1f}%"></div></div></td>'
                '<td class="num">{}</td></tr>'.format(
                    esc(i["category"]), fmt(i["budget"]), fmt(i["actual"]), cls,
                    i["rate"], cls, min(i["rate"], 130) / 130 * 100, fmt(i["remain"])))
        bud_html = """
<h2>预算执行</h2>
<div class="card">
  <div class="sub">年度预算 {} 元 · 已执行 {:.1f}%</div>
  <table>
    <tr><th>分类</th><th class="num">年度预算</th><th class="num">已花</th>
        <th class="num">执行率</th><th>进度</th><th class="num">剩余</th></tr>
    {}
    <tr style="font-weight:700"><td>合计</td><td class="num">{}</td>
        <td class="num">{}</td><td class="num">{:.1f}%</td><td></td>
        <td class="num">{}</td></tr>
  </table>
</div>""".format(
            fmt(budget["declared_total"] or budget["budget_total"]),
            budget["rate"], "".join(rows), fmt(budget["budget_total"]),
            fmt(budget["actual_total"]), budget["rate"],
            fmt(budget["budget_total"] - budget["actual_total"]))

    # ---- 结论
    adv = []
    pos = []
    if s["savings_rate"] >= 25:
        pos.append("现金流为正，本期结余 <b>{} 元</b>，储蓄率 <b>{:.1f}%</b>，属于健康区间。".format(
            fmt(s["surplus"]), s["savings_rate"]))
    else:
        adv.append("期储蓄率仅 <b>{:.1f}%</b>，建议先定位可压缩的弹性支出。".format(s["savings_rate"]))
    if bs["liabilities"] <= 0:
        pos.append("无负债：{}。".format(liab_note))
    else:
        adv.append("存在负债 {} 元（{}），注意还款节奏。".format(
            fmt(bs["liabilities"]), liab_note))
    if cover < 3:
        adv.append("应急金不足：现金活期仅 <b>{} 元</b>，约覆盖 <b>{:.1f} 个月</b>支出"
                   "（月均 {} 元），建议补到 3~6 个月。".format(
                       fmt(cash), cover, fmt(monthly_avg)))
    else:
        pos.append("应急金覆盖率约 <b>{:.1f} 个月</b>，缓冲充足。".format(cover))
    top = max(stock, key=lambda x: x["money"], default=None)
    if top and total_assets and top["money"] / total_assets > 0.25:
        adv.append("持仓集中：<b>{}</b> 一只占总资产 <b>{:.1f}%</b>，建议设仓位上限。".format(
            esc(top["name"]), top["money"] / total_assets * 100))
    over = [i for i in (budget["items"] if budget else []) if i["rate"] >= 100]
    warn = [i for i in (budget["items"] if budget else []) if 85 <= i["rate"] < 100]
    if over:
        adv.append("预算超支：{}。".format("、".join(
            "{}（{:.0f}%）".format(esc(i["category"]), i["rate"]) for i in over)))
    if warn:
        adv.append("接近预算上限：{}。".format("、".join(
            "{}（{:.0f}%）".format(esc(i["category"]), i["rate"]) for i in warn)))
    if adj:
        adv.append("口径提醒：已剔除 <b>{} 笔</b>资产余额校准「平账」分录"
                   "（合计 {} 元），否则会被算成收支。建议校准时选「不生成账单」，"
                   "或把分类改为专门的「平账」分类。".format(len(adj), fmt(
                       sum(a["money"] for a in adj))))

    def ul(items, empty):
        if not items:
            return '<div class="note">{}</div>'.format(empty)
        return "<ul>" + "".join("<li>{}</li>".format(x) for x in items) + "</ul>"

    conclusion = ""
    if suggest:
        conclusion = """
<h2>结论与建议</h2>
<div class="card">
  <h3>健康项</h3>
  {}
  <h3>风险点与可执行动作</h3>
  {}
</div>""".format(ul(pos, "—"), ul(adv, "暂无显著风险项。"))

    adj_note = ""
    if adj:
        adj_note = ("<br>已剔除 {} 笔资产余额校准「平账」分录（合计 {} 元）。"
                    .format(len(adj), fmt(sum(a["money"] for a in adj))))

    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>钱迹财务分析报告 {year}</title>
<style>{style}</style></head><body><div class="wrap">

<h1>钱迹财务分析报告</h1>
<div class="sub">数据来源：本机 钱迹数据库 <code>{src}</code><br>
记录区间 {start} ~ {end}，共 {cnt} 笔 · 账本：{books} · 生成时间 {gen}</div>

<div class="grid">
  <div class="kpi"><div class="l">净资产</div><div class="v blue">{net}</div>
    <div class="d">总资产 {assets} · 负债 {liab}</div></div>
  <div class="kpi"><div class="l">{year} 年收入</div><div class="v">{income}</div>
    <div class="d">{inc_cnt} 笔 · 月均 {inc_avg}</div></div>
  <div class="kpi"><div class="l">{year} 年净支出</div><div class="v amber">{net_exp}</div>
    <div class="d">月均 {mon_avg}</div></div>
  <div class="kpi"><div class="l">{year} 年结余</div><div class="v {sur_cls}">{surplus}</div>
    <div class="d">储蓄率 {rate:.1f}%</div></div>
</div>

<h2>资产配置</h2>
<div class="card">
  <div class="donutwrap">
    <svg viewBox="0 0 200 200" width="200" height="200" style="flex:none">
      {donut}
      <text x="100" y="94" text-anchor="middle" fill="#8b93a7" font-size="11">净资产</text>
      <text x="100" y="116" text-anchor="middle" fill="#e8ecf3" font-size="19" font-weight="700">{net}</text>
    </svg>
    <div class="legend">{legend}</div>
  </div>
  <table style="margin-top:18px">
    <tr><th>账户</th><th>类别</th><th class="num">当前金额</th>
        <th class="num">浮动盈亏</th><th>备注</th></tr>
    {asset_table}
  </table>
  <div class="note">股票/权益合计 {stock_val} 元，其中有成本记录的持仓成本 {stock_cost} 元，
    浮动 <b>{stock_pnl:+,.0f}</b> 元（其余为账户内可用资金，不计盈亏）。{liab_note}。
    现金活期 {cash} 元 ≈ <b>{cover:.1f} 个月</b>支出。</div>
</div>

<h2>月度收支</h2>
<div class="card">
  <div class="sub"><span class="dot" style="background:#10B981"></span> 收入　
    <span class="dot" style="background:#EF4444;margin-left:12px"></span> 净支出（已抵扣退款）</div>
  <div class="chart">{monthly_chart}</div>
  <table style="margin-top:20px">
    <tr><th>月份</th><th class="num">净支出</th><th class="num">收入</th><th class="num">结余</th></tr>
    {month_rows}
    <tr style="font-weight:700"><td>合计</td><td class="num">{net_exp_f}</td>
        <td class="num">{income_f}</td><td class="num">{surplus_f}</td></tr>
  </table>
  <div class="note">毛支出 {expense} 元，退款 {refund} 元，净支出 {net_exp_f} 元。</div>
</div>

<h2>支出结构</h2>
<div class="card">{cat_bars}
  <div class="note">按毛支出统计，合计 {expense} 元；退款 {refund} 元未逐项冲减分类。</div>
</div>

<h2>收入结构</h2>
<div class="card">
  <table>
    <tr><th>来源</th><th class="num">金额</th><th class="num">占比</th><th class="num">笔数</th></tr>
    {inc_rows}
    <tr style="font-weight:700"><td>合计</td><td class="num">{income}</td>
        <td class="num">100%</td><td class="num">{inc_cnt}</td></tr>
  </table>
</div>

{bud}

{conclusion}

<div class="note" style="margin-top:26px">
说明：本报告基于本机钱迹本地数据库离线读取生成，不联网、不上传，金额单位均为人民币元。{adj_note}
已自动脱敏：银行卡号（仅保留前 4 后 4）、持卡人姓名、身份证号、手机号、账号标识与本地登录用户名；
卡面图片、`userid` 等字段不纳入报告。所有统计均已剔除资产余额校准「平账」分录。
</div>

</div></body></html>""".format(
        year=esc(year or "全部"),
        style=STYLE,
        src=esc(mask_path(q.source)),
        start=rng["start"], end=rng["end"], cnt=rng["count"],
        books=esc("、".join(b["name"] for b in q.books())),
        gen=generated,
        net=wan(net), assets=wan(total_assets), liab=wan(bs["liabilities"]),
        income=wan(s["income"]),
        inc_cnt=s["income_count"],
        inc_avg=wan(s["income"] / len(months)) if months else "-",
        net_exp=wan(s["net_expense"]),
        net_exp_f=fmt(s["net_expense"]),
        income_f=fmt(s["income"]),
        surplus_f=fmt(s["surplus"]),
        mon_avg=wan(monthly_avg),
        surplus=wan(s["surplus"]),
        sur_cls="green" if s["surplus"] >= 0 else "red",
        rate=s["savings_rate"],
        donut=donut, legend=legend, asset_table=asset_table,
        stock_val=fmt(stock_val), stock_cost=fmt(stock_cost),
        stock_pnl=stock_pnl, liab_note=liab_note,
        cash=fmt(cash), cover=cover,
        monthly_chart=monthly_chart, month_rows=month_rows,
        expense=fmt(s["expense"]), refund=fmt(s["refund"]),
        cat_bars=cat_bars, inc_rows=inc_rows,
        bud=bud_html, conclusion=conclusion, adj_note=adj_note,
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description="生成钱迹财务分析 HTML 报告")
    ap.add_argument("--db", help="数据库路径（默认自动定位）")
    ap.add_argument("--year", help="报告年份，默认最新有数据的年份")
    ap.add_argument("--out", help="输出 HTML 路径")
    ap.add_argument("--open", action="store_true", help="生成后用浏览器打开")
    ap.add_argument("--live", action="store_true", help="直接读原库（不复制）")
    args = ap.parse_args(argv)

    q = Qianji(db_path=args.db, live=args.live)
    try:
        doc = build_html(q, args.year)
        default_name = "钱迹财务分析报告{}.html".format(
            "-" + args.year if args.year else "")
        out = os.path.abspath(args.out or default_name)
    finally:
        q.close()

    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print("已生成：{}".format(out))
    if args.open:
        webbrowser.open("file:///" + out.replace("\\", "/"))


if __name__ == "__main__":
    main()
