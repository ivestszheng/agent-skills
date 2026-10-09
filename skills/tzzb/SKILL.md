---
name: tzzb
description: >
  同花顺投资账本（tzzb.10jqka.com.cn）数据抓取：股票+基金持仓明细、汇总市值、
  当日/本月/今年盈亏、仓位占比、日频资产趋势。当用户提到投资账本、同花顺持仓、
  抓取持仓、更新投资数据、tzzb、投资明细时使用。输出 JSON 供财务分析/月度体检消费。
slug: tzzb
displayName: 同花顺投资账本抓取
summary: 通过 HTTP API 直连同花顺投资账本，抓取股票+基金持仓与资产趋势，零浏览器零反调试
version: 0.1.0
license: MIT
tags: [投资, 同花顺, 持仓, 数据抓取, 财务分析]
homepage: https://github.com/ivestszheng/agent-skills/tree/main/skills/tzzb
---

# 同花顺投资账本抓取（tzzb）

从同花顺投资账本（tzzb.10jqka.com.cn）抓取投资实时数据，输出 JSON。
全程只读站点数据，不写任何站点数据。

## 方案 A：HTTP API 直连（首选）

**不需要浏览器、不依赖任何扩展、不触发反调试**。登录态通过本地会话文件注入，直接 POST 会话接口。

```bash
PYTHONIOENCODING=utf-8 python scripts/fetch_tzzb_api.py --out <输出路径>.json
# 退出码 0=成功；2=环境失败（会话过期/网络）→ 调用方应降级，勿重试超过 1 次
```

### 首次配置（获取会话凭证）

1. 浏览器登录 `https://tzzb.10jqka.com.cn/pc/index.html`；
2. DevTools → Network → 随便选一个 `/caishen_httpserver/` 开头的请求 → *Copy as PowerShell*；
3. 从中提取全部 `Cookie("名字", "值", ...)` 对，写入本 skill 目录下的 `session_cookies.json`
   （格式见 `session_cookies.example.json`；`v` 等 Cookie 逐请求变化，任取一份即可）；
4. 同文件 `params` 里补上 `fund_key`（股票账户键，来自请求体）、`custid`（爱基金 cust_id）、`userid`。

> ⚠️ `session_cookies.json` 是**真实登录态**，只放本机用户目录，严禁提交到仓库或对外分享。
> 建议在本仓库 `.gitignore` 确认覆盖（本仓库默认不含该文件）。

### 会话有效期与续期

- `sess_tk`（JWT）约 **7 天**过期（payload 的 `exp` 可直接解出来）；
- 过期后重抓会退出码 2：重新 *Copy as PowerShell* 更新 `session_cookies.json` 的 Cookie 即可。

### 接口清单（POST，form-urlencoded，公共参数 `terminal=1&version=0.0.0&userid=&user_id=`）

注意**两种参数形态**：股票侧 `fund_key=<股票账户键>&custid=`，基金侧 `fund_key=&custid=<爱基金cust_id>`：

| 接口 | 参数形态 | 返回 |
|---|---|---|
| `pc/asset/v1/stock_position` | 股票侧 +`manual_id&is_merge=1` | 股票持仓 `ex_data.position[]`（code/name/value/price/hold_profit/hold_rate/position_rate/m_profit/y_profit…）+ `money_remain` 现金 |
| `fund/v1/merge_fund` | `from_id=pcweb&custid=…&fundid=` | 基金持仓 `ex_data.fund[]`（fundcode/fundname/fundvalue/fundcost/posprofit/pospercent）+ `account.total_asset` |
| `pc/asset/v1/asset_trend` | 两侧各调一次 | **日频资产趋势** `total_asset[]{date(YYYYMMDD), asset, profit, fundIn, fundOut, zczs}` + `month_init_zczs/year_init_zczs`；两侧合并即全口径资产曲线，适合画历史曲线、替代手动快照 |
| `pc/account/v1/merge_day_trading` | 股票侧 | 当日交易 `data[]`（无交易为空） |
| `pc/asset/v1/query_bank_history` | 股票侧 | 银证流水 `{"stock":[]}` |
| `invest/v1/pass_quotes` | `code=1:002594,2:601398&date=YYYYMMDD` | 指定行情（`1:`=SZ `2:`=SH） |

其余 `pc/account/v1/init|status|stock_card|fund_card`、`pc/asset/v1/time_share|merge_compare`、
`through_stock/v1/through_time_share` 为页面配套接口，按需扩展。

响应统一信封：`{"error_code":"0","error_msg":"success","ex_data":{...}}`。

## 方案 B：bsk 浏览器扩展（备用）

仅当 API 会话过期且不能马上续期时考虑。需要 [bsk CLI](https://github.com/Tencent/BrowserSkill) + Chrome 扩展：

- `bsk status --json` 的 `browsers` 非空=扩展已连接；daemon 用托管后台任务拉起（`BSK_AUTO_START=0 bsk daemon start --foreground`）；
- 老脚本 `scripts/fetch_tzzb.py` 退出码 0=成功；2=反调试提示页（持久存储被写标记，重试无效），调用方降级勿硬重试；
- ⚠️ 同花顺反调试：CDP/debugger 附加会在持久存储写标记 → 此站**禁用一切 CDP 通道**；恢复=清 localStorage+sessionStorage+cookie 后重新导航；
- bsk 抓数据优先 `get-html`/`observe`/`snapshot`（content script 通道）；视图 tab 的 URL hash 每次加载随机分配，需从 HTML 读 `SumAccountTab_accountListView ..._<hash>` 映射再 navigate。

## 输出 JSON 结构（fetch_tzzb_api.py）

```json
{
  "fetched_at": "YYYY-MM-DD HH:MM:SS",
  "view": "汇总持仓（API）",
  "cash": 15153.62,
  "summary": {"amount": 220423.92, "day_pnl": -1917.08, "day_pct": "-0.86%",
               "hold_pnl": -28420.77, "hold_pct": "-11.42%",
               "month_pnl": 2012.92, "year_pnl": -17046.08, "weight": "93.57%"},
  "positions": [{"code", "name", "amount", "day_pnl", "day_pct", "hold_pnl", "hold_pct",
                 "total_pnl", "month_pnl", "year_pnl", "weight"}]
}
```

- `amount` 是**持仓市值**（股票+基金，不含现金）；现金在 `cash` 字段；
- `summary.weight` = 持仓市值 ÷（市值+现金），即权益仓位占比。

## 与记账 App 的口径建议（实践沉淀）

- 若同时用记账 App（如钱迹）管理「汇总账户」：App 内快照=市值+现金，**每月手动同步一次**，作为市值/FIRE 等长期计算的权威来源；本 skill 数据只做明细分析、持仓集中度、盈亏结构，不覆盖快照；
- 快照明显低于持仓市值说明未同步，先补快照再算。

## 脱敏（硬性要求）

抓取结果含真实持仓与金额：仅写入本机指定路径或展示给用户本人；
**进公开仓库/对外报告前必须脱敏**（金额→占位符、持仓名→示例代码）。
