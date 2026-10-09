#!/usr/bin/env python3
"""同花顺投资账本抓取 —— HTTP API 直连模式（首选，无需浏览器/bsk，零反调试风险）。

接口来源：钧少 2026-10-09 提供的 DevTools 抓包（tzzb.10jqka.com.cn/caishen_httpserver）。
会话凭证：../session_cookies.json（sess_tk 约 7 天过期，过期后按 SKILL.md 说明更新）。

用法:
    PYTHONIOENCODING=utf-8 python fetch_tzzb_api.py --out <输出路径>.json
退出码: 0=成功; 2=环境失败(会话过期/网络/风控) → 调用方应降级，勿重试超过 1 次

输出 JSON 与旧版（网页抓取）结构完全一致，消费方（monthly_report.py）无需改动:
{
  "fetched_at": "...", "view": "汇总持仓（API）",
  "summary": {"amount", "day_pnl", "day_pct", "hold_pnl", "hold_pct", "month_pnl", "year_pnl", "weight"},
  "positions": [{"code","name","amount","day_pnl","day_pct","hold_pnl","hold_pct",
                 "total_pnl","month_pnl","year_pnl","weight"}]
}
amount 为持仓市值（股票+基金，不含现金）；现金在响应 money_remain，单独输出为 cash。
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://tzzb.10jqka.com.cn/caishen_httpserver/tzzb/caishen_fund"
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSION_FILE = os.path.join(SKILL_DIR, "session_cookies.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36")


def load_session():
    with open(SESSION_FILE, encoding="utf-8") as f:
        s = json.load(f)
    ck = s["cookies"]
    p = s.get("params", {})
    uid = ck.get("userid") or p.get("userid")
    return "; ".join(f"{k}={v}" for k, v in ck.items()), uid, p


def call(cookie_hdr, path, body):
    req = urllib.request.Request(f"{BASE}/{path}", data=body.encode(), method="POST")
    for k, v in [
        ("Content-Type", "application/x-www-form-urlencoded"),
        ("Cookie", cookie_hdr),
        ("Origin", "https://tzzb.10jqka.com.cn"),
        ("Referer", "https://tzzb.10jqka.com.cn/pc/index.html"),
        ("User-Agent", UA),
        ("Accept", "application/json, text/plain, */*"),
        ("Accept-Encoding", "identity"),
    ]:
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8", "replace")
    d = json.loads(text)
    if str(d.get("error_code")) != "0":
        raise RuntimeError(f"{path} -> error_code={d.get('error_code')} {d.get('error_msg')}")
    return d.get("ex_data") or {}


def pct(x):
    return "%+.2f%%" % (x * 100)


def main():
    out_path = None
    args = sys.argv[1:]
    if "--out" in args:
        out_path = args[args.index("--out") + 1]
    try:
        cookie_hdr, uid, params = load_session()
        common = {"terminal": "1", "version": "0.0.0", "userid": uid, "user_id": uid}
        positions = []

        # ---- 股票持仓 ----
        body = urllib.parse.urlencode({**common, "manual_id": "",
                                       "fund_key": params.get("fund_key", ""),
                                       "rzrq_fund_key": "", "is_merge": "1"})
        sp = call(cookie_hdr, "pc/asset/v1/stock_position", body)
        cash = float(sp.get("money_remain") or 0)
        for it in sp.get("position") or []:
            value = float(it.get("value") or 0)
            if value <= 0:
                continue
            hold = float(it.get("hold_profit") or 0)
            cost = value - hold  # 成本≈市值-持仓盈亏
            positions.append({
                "code": it.get("code") or "",
                "name": it.get("name") or "",
                "amount": round(value, 2),
                "day_pnl": round(float(it.get("pre_profit") or 0), 2),
                "day_pct": pct(float(it.get("pre_rate") or 0)),
                "hold_pnl": round(hold, 2),
                "hold_pct": pct(hold / cost) if cost else "",
                "total_pnl": round(hold, 2),
                "month_pnl": round(float(it.get("m_profit") or 0), 2),
                "year_pnl": round(float(it.get("y_profit") or 0), 2),
                "weight": "%.2f%%" % (float(it.get("position_rate") or 0) * 100),
            })

        # ---- 基金持仓 ----
        body = urllib.parse.urlencode({**common, "from_id": "pcweb",
                                       "custid": params.get("custid", ""), "fundid": ""})
        mf = call(cookie_hdr, "fund/v1/merge_fund", body)
        for it in (mf.get("fund") or []):
            value = float(it.get("fundvalue") or 0)
            if value <= 0:
                continue
            hold = float(it.get("posprofit") or 0)
            cost = float(it.get("fundcost") or 0)
            positions.append({
                "code": str(it.get("fundcode") or ""),
                "name": it.get("fundname") or "",
                "amount": round(value, 2),
                "day_pnl": round(float(it.get("pre_profit") or 0), 2),
                "day_pct": pct(float(it.get("pre_rate") or 0)),
                "hold_pnl": round(hold, 2),
                "hold_pct": pct(hold / cost) if cost else "",
                "total_pnl": round(float(it.get("all_profit") or 0), 2),
                "month_pnl": round(float(it.get("m_profit") or 0), 2),
                "year_pnl": round(float(it.get("y_profit") or it.get("h_y_profit") or 0), 2),
                "weight": "%.2f%%" % (float(it.get("pospercent") or 0) * 100),
            })

        amount = round(sum(p["amount"] for p in positions), 2)
        s_day = round(sum(p["day_pnl"] for p in positions), 2)
        s_hold = round(sum(p["hold_pnl"] for p in positions), 2)
        s_month = round(sum(p["month_pnl"] for p in positions), 2)
        s_year = round(sum(p["year_pnl"] for p in positions), 2)
        total = amount + cash
        data = {
            "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "view": "汇总持仓（API）",
            "cash": round(cash, 2),
            "summary": {
                "amount": amount,
                "day_pnl": s_day,
                "day_pct": pct(s_day / (amount - s_day)) if amount - s_day else "",
                "hold_pnl": s_hold,
                "hold_pct": pct(s_hold / (amount - s_hold)) if amount - s_hold else "",
                "month_pnl": s_month,
                "year_pnl": s_year,
                "weight": ("%.2f%%" % (amount / total * 100)) if total else "",
            },
            "positions": positions,
        }
        if out_path:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        print("OK %s ｜ 持仓 %d 笔 市值 %.2f 现金 %.2f" % (
            out_path or "(stdout)", len(positions), amount, cash))
        return 0
    except urllib.error.HTTPError as e:
        print("API_FAIL HTTP %s（可能登录态过期，更新 session_cookies.json）" % e.code)
        return 2
    except Exception as e:
        print("API_FAIL %s" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
