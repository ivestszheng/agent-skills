# 钱迹数据库结构与字段口径

数据库文件：`qianjiapp.db`（SQLite 3），由钱迹 Windows 桌面版（Flutter）维护。
位置：`%APPDATA%\com.mutangtech.qianji.win\qianji_flutter\qianjiapp.db`

> 客户端运行时该文件被独占锁，**必须先复制再打开**，否则报 `database is locked`。

## 表清单

| 表 | 说明 | 敏感度 |
|---|---|---|
| `user_bill` | 流水（核心表） | 含备注/图片，需过滤 |
| `user_asset` | 资产/账户余额 | 账户名可能含敏感串 |
| `asset_type` | 资产分类字典 | — |
| `asset_group` | 资产分组 | — |
| `asset_snapshot` | 资产历史快照（多数版本为空） | — |
| `user_budget` | 预算（年度 / 月度） | — |
| `category` | 分类（用户可见） | — |
| `category_icon` | 分类图标库（内置） | — |
| `user_book2` | 账本 | 含 `userid` / `memberid` |
| `book_member` | 账本成员（含昵称、VIP 到期） | **含昵称，勿输出** |
| `book_type` | 账本类型字典 | — |
| `user_card` | 银行卡 / 证券账户 | **含完整卡号、持卡人、卡面图，必须脱敏** |
| `user_installment` | 分期 | — |
| `user_repeattask` | 周期记账任务 | — |
| `saving_plan` / `saving_transaction` | 存钱计划 | — |
| `bill_tags8` / `bill_tag_groups` | 标签 | — |
| `user_log` | **操作日志（资产校准 / 改单 / 删单）** | 含余额旧值新值 |
| `currency3` / `bank` / `common_question` / `feedmatter_faq` | 字典表 | — |
| `key_value` / `sqlite_sequence` | 内部表 | — |

> 行数随记账量变化，用 `SELECT COUNT(*) FROM user_bill` 之类现查，不要依赖固定值。

## user_bill（流水）

| 字段 | 含义 |
|---|---|
| `id` | 主键，19 位数字（时间戳 + 随机后缀），每条不同，不要写死样例值 |
| `userid` | 用户 ID（微信 openid 形式） |
| `type` | **单据类型，见下表** |
| `money` | 金额，**单位=元**，浮点 |
| `remark` | 备注。**平账分录在此处写 `平账(旧值 ~ 新值)`** |
| `cateid` | 分类 ID，关联 `category.id` |
| `time` | 记账时间，**秒级 unix 时间戳** |
| `createtime` / `updatetime` | 创建/修改时间戳 |
| `assetid` | 关联资产（`-1` = 未指定账户） |
| `fromid` / `targetid` | 转账、还款的转出/转入资产 |
| `descinfo` | 展示文案（转账对象、平账描述等） |
| `extra` | JSON 字符串，常见键：`baoxiaoed`（已报销额）、`baoxiaov`、`refundsid`（退款源单 ID）、`transfee`（手续费）、`tags` |
| `bookid` | 账本 ID，默认 `-1`（钱迹默认账本） |
| `status` | `1` = 正常 |
| `platform` | 录入来源：`0` 手动、`122`/`66`/`102` 等为导入/自动记账 |

### type 枚举

| type | 含义 | 是否计入收支 |
|---|---|---|
| `0` | 支出 | ✅ 计入支出 |
| `1` | 收入 | ✅ 计入收入 |
| `2` | 转账（资产间） | ❌ 不计 |
| `3` | 信用卡还款 | ❌ 不计 |
| `5` | 借出/借入（支出方向） | ❌ 不计 |
| `6` | 借出（资产为债权账户） | ❌ 不计 |
| `9` | 借出收回 | ❌ 不计 |
| `20` | **退款** | ⚠️ 用于**冲减**支出口径 |
| `21` | 报销收款 | ⚠️ 通常与 `5` 成对，计入收入侧需谨慎 |

> 只统计 `type IN (0, 1)` 才是标准收支口径；退款单独取 `type=20` 做冲减。

## category（分类）

| 字段 | 含义 |
|---|---|
| `id` | 分类 ID |
| `name` | 分类名 |
| `type` | **`0` = 支出分类，`1` = 收入分类** |
| `parentid` | `-1` = 一级分类；否则为父分类 ID |
| `level` | `1` 一级 / `2` 二级 |
| `sort` | 排序；`500` 一般为用户新建的分类 |
| `editable` | **`0` = 钱迹内置分类，删不掉也改不了名**（如「日常」「其它收益」） |

统计时注意：

- `user_bill.cateid` 可能是**二级分类**的 id，若要按一级汇总需回溯 `parentid`。
- 内置分类「日常」「其它收益」是资产校准分录的默认落点，是统计被污染的源头。

## user_asset（资产）

| 字段 | 含义 |
|---|---|
| `money` | 当前余额/市值，单位=元（**信用卡、借出为负/正按 type 语义**） |
| `type` | **`1` 资金账户、`2` 信用卡（负债）、`3` 押金、`4` 投资、`5` 借入借出** |
| `stype` | 二级类型，见 `asset_type` 字典 |
| `extra` | JSON，`initmoney` = **记录成本**（可用于算浮动盈亏）；`bank` = 银行名 |
| `credit` | JSON，信用卡专用：`limit`（额度）、`statedate`（账单日）、`paydate2`（还款日） |
| `loan` | JSON，借贷专用：`money`、`totalpay`、`startdate`、`enddate` |
| `incount` | `1` 表示计入总资产 |
| `status` | `0` = 正常 |

### asset_type 字典

`asset_type.name` 列几乎为空，中文名藏在 `asset_type.type` 的 **JSON 字符串**里：

```json
{"icon":"http://res3.qianjiapp.com/assetv2/asset_icon_cash.png",
 "name":"现金","type":1,"stype":11,"c":"E45644"}
```

用 `(type, stype)` 组 key 建字典即可把 `user_asset` 翻成中文类别。
常见 stype（取自钱迹内置 `asset_type` 字典）：`12` 银行卡、`17` 公积金、`18` 医保、
`21` 信用卡、`35` 押金、`41` 股票、`47` 固定收益、`48` 债券、`51` 借入借出、
`102` 微信零钱通、`107` 小荷包。实际以用户库里的字典表为准，不要写死。

## user_card（银行卡 / 证券账户）—— 高敏表

| 字段 | 含义 | 敏感度 |
|---|---|---|
| `cardno` | 卡号 / 证券账号 **明文** | 🔴 只留前 4 后 4 |
| `owner` | 持卡人姓名 | 🔴 只留姓氏 |
| `images` | 卡面图片（base64 或本地文件路径） | 🔴 直接丢弃 |
| `userid` | 账号标识 | 🟠 丢弃 |
| `bank` | 银行名 | 🟡 一般可保留 |
| `type` | 卡类型 | — |
| `remark` | 备注，用户可能手写卡号/手机号 | 🟡 过 `mask_text()` |

`Qianji.cards()` 已按上表默认脱敏；`mask=False` 会返回原文，**仅在用户明确要求时使用**。

## user_budget（预算）

| 字段 | 含义 |
|---|---|
| `type` | `1` = 月度预算，`2` = 年度预算 |
| `typeinfo` | `'2026'`（年度）或 `'2026,9'`（2026 年 9 月） |
| `flag` | `1` = 总预算，`2` = 分类预算 |
| `cateid` | 分类 ID（`flag=2` 时有效） |
| `money` | 预算金额，单位=元 |

> `flag=1` 的总预算通常等于 `flag=2` 各项之和，**不要重复累加**。

## user_log（操作日志）

排查口径异常时最有用，`message` 里带 `tag`：

- `ASSET-DIFF` / `AssetDiff`：资产余额校准。含
  `oldValue` / `newValue` / `diff` / **`generateDiffBill=true|false`**。
  `true` 表示生成了一条平账流水（会污染分类统计），`false` 表示静默调整（不产生流水）。
- `AssetDelete`：删除资产。
- `BillModify`：改单，`fields` 是 JSON，例如 `{"cateid":<分类ID>}`。
- `BillDelete`：删单。

## ⚠️ 头号陷阱：平账分录

余额校准时钱迹会生成

```
remark = "平账(旧值 ~ 新值)"
```

的流水，**分类却挂到「日常」（支出方向）或「其它收益」（收入方向）**。
「平账」这个身份**只写在 `remark` 里，不进 `cateid`**；
而 App 内的分类统计 / 排行榜 / 预算执行**全部按 `cateid` 聚合，不认 `remark`**。

后果：一笔几万元的股票市值校准，会在「日常」里显示成几万元的日用品消费，
月度支出被整笔撑大。

处理方式：

```sql
-- 统一过滤常量
(remark IS NULL OR remark NOT LIKE '平账%')
```

```sql
-- 统计真实收入时还要扣掉收入侧的平账
SUM(CASE WHEN type=1 AND remark LIKE '平账%' THEN money ELSE 0 END)
```

给用户的口径建议：

1. **最干净**：校准时选**不生成账单**（`generateDiffBill=false`），余额照常更新、零流水。
2. **要留痕**：支出侧、收入侧**各建一个「平账」分类**（只建支出侧没用，
   收入方向的校准分录只会落到「其它收益」），并且**不给它设预算**。
3. 「日常」「其它收益」是内置分类（`editable=0`），删不掉、改不了名。

## 其他常见坑

1. 时间戳转本地时间忘了 `'localtime'` → 跨月分录错位。
   正确写法：`strftime('%Y-%m', time, 'unixepoch', 'localtime')`。
2. 忘了解析 `asset_type.type` 的 JSON → 资产类别显示成 `?4/41`。
3. 漏记工资/公积金会让某年结余为负，先核对收入笔数是否按月齐全再下结论。
4. 直接 `sqlite3.connect()` 原库 → `database is locked`，一律先 `shutil.copy2`。
5. `user_card.cardno` 是明文完整卡号，`owner` 是持卡人姓名，`images` 是卡面图，
   **三者输出前必须处理**（见上文 user_card 表），报告路径里的操作系统用户名也要抹掉。
