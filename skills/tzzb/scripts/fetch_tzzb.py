# -*- coding: utf-8 -*-
"""从同花顺投资账本（tzzb.10jqka.com.cn）抓取投资实时数据 → JSON 文件。

通道：browser-skill（bsk CLI + 浏览器扩展，走用户已登录 Chrome，无 CDP 授权弹窗）。
数据源：「汇总持仓」视图（股票+基金全量，钧少 2026-10-09 确认此 tab 必有）。
口径：钱迹「汇总账户」快照负责市值（月度同步）；本脚本产出持仓明细与盈亏，
供月度体检做投资分析与持仓集中度。

反调试策略（2026-10-09 实测定稿）：
- 同花顺检测 debugger 附加即在持久存储写标记 → 所有加载渲染「不支持开发者工具」提示页；
- get-html/observe/snapshot 走 content script **不触发**，evaluate（chrome.debugger）随机触发；
- 因此表格抓取全程用 get-html，evaluate 仅用于清标记恢复与点击 tab 兜底。

用法：
    python fetch_tzzb.py [--out 输出路径.json]

退出码：0 成功；2 环境失败（daemon/扩展/页面/反调试不可用）——调用方应降级，勿反复重试。
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

BSK = os.path.expanduser("~/.local/bin/bsk.exe")
PAGE_URL = "https://tzzb.10jqka.com.cn/pc/index.html#/myAccount"
CODE_RE = re.compile(r"^\d{5,6}$")

CLICK_JS = """
(()=>{const els=[...document.querySelectorAll('div,span,a,li')]
 .filter(e=>e.innerText&&e.innerText.trim()==='%s'&&e.children.length===0);
 if(els.length){els[0].click();return 'ok'}return 'missing'})()
"""

CLEAR_JS = """
(()=>{try{localStorage.clear();sessionStorage.clear();
document.cookie.split(';').forEach(c=>{document.cookie=c.split('=')[0].trim()+'=;expires=Thu,01 Jan 1970 00:00:00 GMT;path=/'});return 'cleared'}catch(e){return 'err'}})()
"""


def bsk(args, timeout=60):
    env = dict(os.environ, BSK_AUTO_START="0")
    r = subprocess.run([BSK] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout, env=env)
    if r.returncode != 0 and not r.stdout.strip():
        raise RuntimeError("bsk %s failed: %s" % (args[0], r.stderr.strip()[:200]))
    return r.stdout


def bsk_json(args, timeout=60):
    out = bsk(args, timeout).strip()
    return json.loads(out)


def ensure_daemon():
    """daemon 活着就复用；否则本进程内拉起（脚本退出后由宿主回收，下次再起）。"""
    try:
        bsk_json(["status", "--json"], timeout=10)
        return None
    except Exception:
        pass
    proc = subprocess.Popen(
        [BSK, "daemon", "start", "--foreground"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    for _ in range(15):
        time.sleep(1)
        try:
            bsk_json(["status", "--json"], timeout=10)
            return proc
        except Exception:
            continue
    raise RuntimeError("bsk daemon 无法启动/连接")


def num(s):
    if not s:
        return None
    s = s.strip().replace(",", "").replace("+", "")
    m = re.match(r"^(-?[\d.]+)万$", s)
    if m:
        return round(float(m.group(1)) * 10000, 2)
    try:
        return float(s)
    except ValueError:
        return None


def get_html(session):
    """整页 HTML（content script 通道，不触发同花顺反调试）。"""
    return bsk_json(["get-html", "--session", session, "--json"]).get("html", "") or ""


def page_text(html):
    """HTML → 纯文本（去 script/style/标签），用于检测提示页与视图状态。"""
    t = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t)


def parse_view_hashes(html):
    """读各视图 tab 的 hash 映射：{视图名: hash}。hash 每次 SPA 加载随机分配。"""
    out = {}
    for m in re.finditer(
            r'class="SumAccountTab_accountListView[^"]*SumAccountTab_accountListView_([A-Za-z0-9]+)"[^>]*>([^<]{0,20})',
            html):
        name = m.group(2).strip()
        if name:
            out[name] = m.group(1)
    return out


def parse_html_table(html):
    """从 HTML 解析持仓表 → 行结构（与 DOM innerText 方案同构）。"""
    rows = []
    for tr in re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", html, flags=re.I):
        cells = []
        for td in re.findall(r"<t[dh][^>]*>([\s\S]*?)</t[dh]>", tr, flags=re.I):
            txt = re.sub(r"<[^>]+>", "", td)
            txt = re.sub(r"\s+", "", txt)  # 单元格内部不留空白（HTML 版无换行）
            cells.append(txt)
        # HTML 里整行可能在单个单元格文本里，或按列拆分；两种都归一成列表
        joined = [c for c in cells if c]
        if len(joined) <= 1 and cells:
            # 整行文本挤在一个单元格里：按已知模式切分
            txt = cells[0] if cells else ""
            # 行首是代码或「汇总」
            if CODE_RE.match(txt[:6]):
                # 代码(6) + 名称(非数字开头) + 后续数字/百分比串
                rows.append(txt)
            elif txt.startswith("汇总"):
                rows.append(txt)
            continue
        first = joined[0] if joined else ""
        if CODE_RE.match(first) or first == "汇总":
            rows.append(joined)
    # 统一：行可能是字符串（单格挤一行）或列表（多单元格）
    out = []
    for r in rows:
        if isinstance(r, str):
            # 拆出代码/名称/数字序列
            m = re.match(r"^(\d{5,6})([\u4e00-\u9fffA-Za-z0-9]+?)(\d[\d,.]*.*)$", r)
            if m:
                cells = [m.group(1), m.group(2)] + re.findall(
                    r"[+-]?\d[\d,]*(?:\.\d+)?(?:万)?|[+-]?\d+\.\d+%", m.group(3))
                out.append(cells)
            elif r.startswith("汇总"):
                cells = ["汇总"] + re.findall(
                    r"[+-]?\d[\d,]*(?:\.\d+)?(?:万)?|[+-]?\d+\.\d+%", r)
                out.append(cells)
        else:
            out.append(r)
    return out


def parse_rows(rows):
    positions, summary = [], None
    for c in rows:
        if c[0] == "汇总":
            # 汇总行少列：市值/当日/当日率/持有盈亏/持有率/本周/本月/今年/仓位
            summary = {
                "amount": num(c[1]) if len(c) > 1 else None,
                "day_pnl": num(c[2]) if len(c) > 2 else None,
                "day_pct": c[3] if len(c) > 3 else None,
                "hold_pnl": num(c[4]) if len(c) > 4 else None,
                "hold_pct": c[5] if len(c) > 5 else None,
                "month_pnl": num(c[7]) if len(c) > 7 else None,
                "year_pnl": num(c[8]) if len(c) > 8 else None,
                "weight": c[9] if len(c) > 9 else None,
            }
            continue
        positions.append({
            "code": c[0], "name": c[1] if len(c) > 1 else "",
            "amount": num(c[2]) if len(c) > 2 else None,
            "day_pnl": num(c[3]) if len(c) > 3 else None,
            "day_pct": c[4] if len(c) > 4 else None,
            "hold_pnl": num(c[5]) if len(c) > 5 else None,
            "hold_pct": c[6] if len(c) > 6 else None,
            "total_pnl": num(c[7]) if len(c) > 7 else None,
            "month_pnl": num(c[10]) if len(c) > 10 else None,
            "year_pnl": num(c[11]) if len(c) > 11 else None,
            "weight": c[12] if len(c) > 12 else None,
        })
    return positions, summary


def main():
    ap = argparse.ArgumentParser(description="抓取同花顺投资账本数据")
    ap.add_argument("--out", default="invest-tzzb.json",
                    help="输出 JSON 路径（默认当前目录 invest-tzzb.json）")
    args = ap.parse_args()
    out_path = os.path.abspath(args.out)

    session = None
    try:
        ensure_daemon()
        session = bsk_json(["session", "start", "--no-focus", "--json"]).get("session_id")
        if not session:
            print("SESSION_FAIL")
            return 2
        bsk(["navigate", PAGE_URL, "--session", session])
        time.sleep(12)

        # 提示页检测 + 恢复（get-html 通道检测，不触发反调试）
        html = get_html(session)
        if "不支持开发者工具" in html:
            bsk(["evaluate", "--session", session, "--json", CLEAR_JS])
            bsk(["navigate", PAGE_URL, "--session", session])
            time.sleep(12)
            html = get_html(session)
        if "不支持开发者工具" in html:
            print("BLOCKED_FAIL 反调试提示页无法恢复")
            return 2

        # 从 HTML 读视图 hash 映射，直达「汇总持仓」
        hashes = parse_view_hashes(html)
        target = hashes.get("汇总持仓")
        if not target:
            # 兜底：evaluate 点击 tab（可能触发标记，事后恢复）
            bsk(["evaluate", "--session", session, "--json", CLICK_JS % "汇总持仓"])
            time.sleep(6)
            html = get_html(session)
            hashes = parse_view_hashes(html)
            active = re.search(r'accountListView_active[^"]*_([A-Za-z0-9]+)"', html)
            target = (active.group(1) if active else None)
        if not target:
            print("VIEW_FAIL 未找到「汇总持仓」视图 hash | 前200字: %r"
                  % page_text(html)[:200])
            return 2
        bsk(["navigate", "https://tzzb.10jqka.com.cn/pc/index.html#/myAccount/a/" + target,
             "--session", session])

        # 轮询等表格渲染（全程 get-html，零 evaluate）
        rows = []
        for i in range(8):
            time.sleep(8)
            html = get_html(session)
            if "不支持开发者工具" in html:
                print("DATA_FAIL 抓取中触发反调试提示页")
                break
            rows = parse_html_table(html)
            if rows:
                break
        if not rows:
            print("DATA_FAIL 持仓表未渲染（可能未登录或页面异常）| 前200字: %r"
                  % page_text(html)[:200])
            try:  # 恢复：清掉标记，避免窗口留在提示页状态
                bsk(["evaluate", "--session", session, "--json", CLEAR_JS])
            except Exception:
                pass
            return 2

        positions, summary = parse_rows(rows)
        if not summary or not summary.get("amount"):
            print("DATA_FAIL 缺少汇总行 | rows=%r" % rows[:2])
            return 2

        result = {
            "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "view": "汇总持仓",
            "summary": summary,
            "positions": positions,
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
        print("OK %s | 持仓市值 %s | %d 只 | 今年盈亏 %s" % (
            out_path, summary["amount"], len(positions), summary.get("year_pnl")))
        return 0
    except Exception as e:
        print("FAIL %s: %s" % (type(e).__name__, e))
        return 2
    finally:
        if session:
            try:
                bsk(["session", "stop", session], timeout=30)
            except Exception:
                pass
        # daemon 保持运行（长驻，后续任务复用），不主动杀


if __name__ == "__main__":
    sys.exit(main())
