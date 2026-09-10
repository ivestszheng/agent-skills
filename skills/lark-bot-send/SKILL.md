---
name: "lark-bot-send"
description: "以 bot 身份通过飞书发送消息，自动处理凭据注入和 strict-mode 绕过。当需要以机器人身份向飞书群或个人发送消息时调用。"
---

# Lark Bot Send

以飞书机器人（bot）身份发送消息到指定群聊或个人。自动完成凭据读取、tenant_access_token 获取、环境变量注入和 strict-mode 绕过，调用方只需提供消息内容和目标。

## 何时调用

- 用户要求以 bot / 机器人 / 工作助手身份发送飞书消息
- 定时自动化任务中需要以 bot 身份发送飞书消息
- 用户反馈 user 身份发的消息收不到新消息提示（需要 bot 身份才会触发提醒）

## 凭据文件

路径：`C:\Users\ives\lark_bot_srcret.json`

结构（JSON，键名大小写敏感）：

```json
{
    "AppID": "<app_id>",
    "AppSecret": "<app_secret>"
}
```

**禁止在对话中明文输出 AppSecret 的值。** 读取文件后直接赋给变量使用，不要打印。

## 发送流程

以下为单次发送的完整命令模板（PowerShell）。将 `<CHAT_ID>`、`<MESSAGE_CONTENT>` 替换为实际值：

```powershell
# 1. 读取凭据文件（不打印密钥）
$cfg = Get-Content "C:\Users\ives\lark_bot_srcret.json" -Raw | ConvertFrom-Json

# 2. 调用飞书 API 获取 tenant_access_token
$body = @{ app_id = $cfg.AppID; app_secret = $cfg.AppSecret } | ConvertTo-Json
$resp = Invoke-RestMethod -Uri "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" -Method Post -ContentType "application/json; charset=utf-8" -Body $body

# 3. 设置环境变量（三个缺一不可）
$env:LARKSUITE_CLI_APP_ID = $cfg.AppID
$env:LARKSUITE_CLI_TENANT_ACCESS_TOKEN = $resp.tenant_access_token
$env:LARKSUITE_CLI_STRICT_MODE = "off"

# 4. 以 bot 身份发送消息
$msg = @'
<MESSAGE_CONTENT>
'@
lark-cli im +messages-send --chat-id <CHAT_ID> --markdown $msg --as bot
```

## 环境变量说明

| 变量 | 作用 |
|------|------|
| `LARKSUITE_CLI_APP_ID` | 覆盖为凭据文件中的 AppID（系统注入的可能是不同的 app） |
| `LARKSUITE_CLI_TENANT_ACCESS_TOKEN` | bot 身份所需的租户令牌，通过飞书 API 获取 |
| `LARKSUITE_CLI_STRICT_MODE=off` | 绕过 strict-mode 策略锁（系统默认锁为 user） |

三个变量缺一不可：
- 缺 `APP_ID`：CLI 用错误的 app，bot 令牌与 app 不匹配
- 缺 `TENANT_ACCESS_TOKEN`：报 `token_missing`，bot 无可用令牌
- 缺 `STRICT_MODE=off`：报 `strict mode is "user"`，bot 命令被拦截

## 发送到个人

将 `--chat-id <CHAT_ID>` 替换为 `--user-id <OPEN_ID>`（如 `ou_xxx`）。

## 消息格式

- `--markdown`：适合带标题、列表、链接的格式化消息（推荐默认）
- `--text`：纯文本，保留原始格式
- `--content`：精确控制 JSON payload

## 注意事项

- 凭据文件路径 `C:\Users\ives\lark_bot_srcret.json` 是硬编码的，路径变更时需更新此 skill
- JSON 键名为 `AppID`（大写 D）和 `AppSecret`，大小写敏感
- tenant_access_token 有效期 7200 秒（2小时），定时任务每次执行时重新获取即可
- 发送前需确认 bot 已在目标群中（或与目标用户有私聊关系）
