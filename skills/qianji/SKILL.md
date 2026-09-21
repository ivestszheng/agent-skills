---
name: qianji
description: >
  读取本机「钱迹」App 的本地 SQLite 数据库（qianjiapp.db），做个人财务分析并生成
  自包含 HTML 报告。当用户提到钱迹、记账数据、我的财务状况、收支分析、这个月花了多少、
  净资产、月度/年度账单复盘、资产配置、预算执行时使用。
slug: qianji
displayName: 钱迹财务分析
summary: 读取本机钱迹 App 的本地数据库，做个人财务分析并生成自包含 HTML 报告
version: 0.1.0
license: MIT
tags: [记账, 个人财务, 收支分析, 资产配置, sqlite]
homepage: https://github.com/ivestszheng/agent-skills/tree/main/skills/qianji
---

# 钱迹财务分析

读取本机「钱迹」客户端的本地数据库，做个人财务分析、生成报告。

钱迹（木糖科技）的移动端数据在云端，但 **Windows 桌面版会在本地存一份完整的 SQLite 库**
（`com.mutangtech.qianji.win/qianji_flutter/qianjiapp.db`），流水、资产、预算、分类、银行卡、改单日志全在，
因此不需要登录、不需要联网、不需要导出 CSV，直接离线读库即可。

## 何时使用

- 用户问「我这个月/今年花了多少」「我的收支情况」「净资产多少」
- 用户要复盘账本、看消费结构、看预算执行、看资产配置
- 用户提到 钱迹 / qianjiapp.db / 记账数据 / 账单分析
- 需要把记账数据导出成报告、图表、Markdown

## 前置条件

- 本机装过 **钱迹 Windows 桌面版**（`C:\Program Files (x86)\qianji\qianji.exe`）
- Python 3.8+（只用标准库 `sqlite3`，无需任何第三方依赖）
- 钱迹客户端可能正在运行，数据库会被锁 —— 脚本会自动**先复制到临时目录再只读打开**

数据库位置（按顺序探测）：

| 平台 | 路径 |
|------|------|
| Windows | `%APPDATA%\com.mutangtech.qianji.win\qianji_flutter\qianjiapp.db` |
| Windows | `%LOCALAPPDATA%\com.mutangtech.qianji.win\qianji_flutter\qianjiapp.db` |
| 备选 | 用户用钱迹导出的 `.db` / `.sqlite` 文件（用 `--db` 显式指定） |

## 文件结构

```
qianji/
├── SKILL.md                     # 本文档
├── references/
│   ├── database-schema.md       # 表结构、字段口径、type 枚举、平账陷阱
│   └── analysis-conventions.md  # 指标定义与常见统计口径
└── scripts/
    ├── qianji.py                # 核心库（定位 DB、连接、查询封装）
    ├── analyze.py               # CLI：输出 Markdown / JSON 分析摘要
    └── report.py                # CLI：生成自包含 HTML 报告（含图表）
```

## 使用方式

### 1. 快速分析（Markdown 摘要）

```bash
python scripts/analyze.py                      # 分析全部年份
python scripts/analyze.py --year 2026          # 只看 2026
python scripts/analyze.py --year 2026 --md 报告.md
python scripts/analyze.py --year 2026 --json data.json
```

### 2. 生成 HTML 报告

```bash
python scripts/report.py --year 2026 --out 钱迹财务分析报告.html
```

产物是**自包含 HTML**（内联 SVG 环形图 + 纯 CSS 柱状图，不引用任何 CDN），
双击即可离线打开。生成后在对话里用 `present_files` 展示。

### 3. 作为库调用

```python
import sys; sys.path.insert(0, "scripts")
from qianji import Qianji

q = Qianji()                      # 自动定位并复制数据库
print(q.balance_sheet())          # 资产/负债/净资产
print(q.summary(2026))            # 收支与月度明细
print(q.category_spend(2026))     # 分类支出排行
q.close()
```

`Qianji(db_path=...)` 可指定数据库；`Qianji(live=False)` 直接读原库（不复制，慎用）。

## 核心口径（务必先读）

1. **金额单位是「元」**（不是分），浮点数存储。
2. **必须剔除「平账」分录**：资产余额校准会生成 `remark LIKE '平账(旧值 ~ 新值)'` 的流水，
   且挂在「日常」「其它收益」这类普通分类下。不剔除会把资产浮盈浮亏当成收支。
   本库统一用 `NOT_BALANCE` 常量过滤，统计收入时还要再减去收入侧的平账金额。
3. **`user_bill.type` 枚举**：`0` 支出、`1` 收入、`2` 转账、`3` 还信用卡、
   `20` 退款、`21` 报销收款、`5/6/9` 借入借出。默认 `0/1` 才算收支。
4. **退款要冲减支出**：净支出 = 支出 − 退款（type=20）。
5. **某年收入明显偏低时先别下结论**：用户常漏记工资/公积金，先检查收入笔数按月是否齐全。

更完整的表结构、字段含义、常见坑见
[references/database-schema.md](references/database-schema.md)，
指标定义见 [references/analysis-conventions.md](references/analysis-conventions.md)。

## 输出建议

- 对话里先给**结论**：净资产、储蓄率、最大风险、可执行动作；数字要给量级（万/元），别堆表格。
- 报告文件里再放完整明细：资产配置、月度收支、分类排行、预算执行、风险清单。
- 资产配置要按「股票/债券/储蓄险/现金活期/公积金医保/押金」分组，并单列浮动盈亏。

## 隐私与脱敏（硬性要求）

全程**只读、离线**，不联网、不上传；分析结束后清理临时复制的数据库副本。

库层 `qianji.py` 默认已做基础防护（`cards()` 自动脱敏并剔除敏感字段、`books()` 剔除账号标识、
`assets()` 过滤账户名与备注），但**把数据交给用户之前仍要自己检查一遍**，遵守以下规则：

| 字段 | 位置 | 处理 |
|---|---|---|
| `cardno` | `user_card` | 银行卡/证券账号明文 → 只留前 4 后 4 |
| `owner` | `user_card` | 持卡人姓名 → 只留姓氏 |
| `images` | `user_card` | 卡面图片（base64 / 本地路径）→ **直接丢弃** |
| `userid` / `memberid` | `user_book2`、`user_bill`、`user_card` | 账号标识 → 丢弃 |
| `name` | `book_member` | 账本成员昵称 → 不输出 |
| `remark` / `descinfo` | `user_bill`、`user_asset`、`user_card` | 用户手写，可能夹带卡号/手机号/身份证/姓名 → 过 `mask_text()` |
| 数据库文件路径 | 脚本内部 | 含操作系统登录用户名 → 过 `mask_path()` |

两个统一入口（写任何文件、往对话里贴任何数字之前都用它们）：

```python
from qianji import mask_text, mask_path

mask_path(r"C:\Users\<用户名>\AppData\Roaming\com.mutangtech.qianji.win\...\qianjiapp.db")
# 当前登录用户 → ~\AppData\Roaming\com.mutangtech.qianji.win\...\qianjiapp.db
# 其它用户名   → C:\Users\***\AppData\Roaming\...

mask_text("卡号 6222000000000000，手机 13800000000，身份证 110101199001010000")
# → 卡号 62****00，手机 138****0000，身份证 110***********0000
```

> 演示用的号码全是占位（全 0），不指向任何真实账户。

- `mask_text()` 处理身份证（18 位）、手机号（11 位）、长数字串（15~19 位，含卡号与单据 id）。
- 报告与 Markdown 里的**登录用户名、卡号、姓名不应出现原文**；报告末尾已自动声明脱敏范围。
- 若用户明确要求导出原始数据（例如完整卡号），先说明风险，不要默默写进文件。
