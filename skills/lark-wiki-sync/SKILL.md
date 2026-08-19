---
name: lark-wiki-sync
description: >
  通过 lark-cli 将本地 Markdown 文档（CHANGELOG、README 等）批量同步到飞书知识库 wiki 文档。
  以 bot 身份写入，支持 monorepo 多文档场景。涉及 lark-wiki-sync.config.json、
  sync:wiki、飞书文档同步、wiki token 时使用。
---

# 文档飞书同步

通过 lark-cli 将本地任意 Markdown 文档批量同步到飞书知识库 wiki 文档。不限于 CHANGELOG，也可以同步 README、技术文档等任意 `.md` 文件。

## 何时使用

- 用户要同步 Markdown 文档（CHANGELOG、README 等）到飞书
- 用户新增了文档，需要配置飞书同步
- 用户提到 `lark-wiki-sync.config.json` 或 `sync:wiki`
- 飞书文档权限问题导致同步失败

## 前置条件

1. **lark-cli 已安装并配置应用**（`lark-cli config init`）
2. **bot 已被添加为飞书知识库成员**（需 admin 权限以编辑文档）
3. 如果 bot 未加入知识库，以 user 身份执行：
   ```bash
   # 先获取 space_id
   lark-cli wiki +node-get --node-token "https://<domain>.feishu.cn/wiki/<wikiToken>" --as user
   # 再添加 bot 为成员
   lark-cli wiki +member-add --space-id <space_id> \
     --member-id <appId> --member-type appid --member-role admin --as user
   ```

## 文件结构

```
.agents/skills/lark-wiki-sync/
├── SKILL.md                              # 本文档
├── scripts/sync-wiki.mjs                 # 同步脚本（通用）
└── lark-wiki-sync.config.template.json   # 配置模板
```

项目根目录放置配置文件：
```
your-project/
├── lark-wiki-sync.config.json            # 项目配置（从模板复制后填写）
├── lark-wiki-sync.state.json             # 同步状态（脚本自动维护，加入 .gitignore）
└── package.json
```

## 配置文件

从 `lark-wiki-sync.config.template.json` 复制到项目根目录，改名为 `lark-wiki-sync.config.json`：

```json
{
  "feishuDomain": "your-tenant.feishu.cn",
  "notifyChatIds": ["oc_xxxxxxxxxxxxxxxx"],
  "docs": [
    {
      "name": "文档显示名",
      "path": "apps/your-app/CHANGELOG.md",
      "wikiToken": "从飞书wiki文档URL中提取的token"
    },
    {
      "name": "README",
      "path": "README.md",
      "wikiToken": "另一个wikiToken",
      "title": "项目说明文档"
    }
  ]
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `feishuDomain` | 是 | 飞书租户域名（如 `xxx.feishu.cn`） |
| `notifyChatIds` | 否 | 通知群聊的 chat_id 数组（`oc_xxx`），可配置多个。配置后，每次有文档实际更新时，AI 会总结变更并发送摘要到这些群。留空数组 `[]` 则不通知 |
| `docs[].name` | 是 | 显示名，用于日志输出和默认文档标题 |
| `docs[].path` | 是 | 相对于项目根目录的 Markdown 文件路径 |
| `docs[].wikiToken` | 是 | 飞书 wiki 节点 token（URL 中 `/wiki/` 后的部分），空字符串表示跳过 |
| `docs[].title` | 否 | 文档标题，默认使用 `name` 的值 |

## 接入步骤

### 1. 安装 skill

将本 skill 目录放入项目的 `.agents/skills/lark-wiki-sync/`。

### 2. 创建配置文件

```bash
cp .agents/skills/lark-wiki-sync/lark-wiki-sync.config.template.json lark-wiki-sync.config.json
```

编辑 `lark-wiki-sync.config.json`，填入飞书域名和各文档的 path 与 wikiToken。

### 3. 添加 package.json 脚本

```json
{
  "scripts": {
    "sync:wiki": "node .agents/skills/lark-wiki-sync/scripts/sync-wiki.mjs"
  }
}
```

### 4. 运行

```bash
# 同步所有配置的文档（内容未变化的自动跳过）
pnpm sync:wiki

# 只同步名称或路径匹配的文档
pnpm sync:wiki -- --filter 象州

# 预览不写入
pnpm sync:wiki -- --dry-run

# 忽略本地状态，强制全量同步
pnpm sync:wiki -- --force
```

## Index 导航页维护

当配置文件中有 `indexWikiToken` 时，每次"同步文档到飞书"且本次有文档实际更新时，还必须同时更新 Index 导航页。Index 页不走 `sync:wiki` 脚本（它包含飞书特有的引用、图片等内容，不适合 overwrite），而是通过 `lark-doc` skill 增量编辑。

### 标准同步流程

当用户说"同步文档到飞书"时，AI 应执行以下三步：

1. **运行 `pnpm sync:wiki`** - 同步所有 Markdown 文档（增量：未变化的自动跳过）
2. **更新 Index 导航页** - 仅当本次有实际同步（输出中"成功"数量 > 0）时执行：更新顶部时间戳，并检查项目信息是否需要变更；全部"未变化"时跳过此步
3. **总结变更并通知群聊** - 仅当本次有实际同步（"成功"数量 > 0）且配置了 `notifyChatIds` 时执行：AI 总结本次更新的文档内容，发送摘要到配置的群聊；详见下方「总结变更并通知群聊」

### 更新 Index 页时间戳

1. 通过 `lark-cli docs +fetch --detail with-ids` 获取 Index 页的 block 结构
2. 找到顶部的 `<blockquote>` block，用 `lark-cli docs +update --command block_replace` 更新时间戳
3. 内容格式：`<blockquote><p>本导航页由 AI 助手自动维护 · 最后更新于 {YYYY-MM-DD HH:mm:ss}</p></blockquote>`（本地时间，含秒，与各文档页内的时间戳格式一致）

### 检查项目信息

同步时应检查 Index 页中本仓库项目的链接和地址是否需要更新：

- 变更日志引用链接的标题是否与配置文件中的 `name` 一致
- 生产/测试环境地址是否与项目中的实际配置一致
- 如有变更，用 `block_replace` 更新对应 block

**注意**：Index 页可能包含不在本仓库中的项目（其他团队的项目），这些项目的信息不要修改，只更新本仓库管理的项目。

### 新增文档时更新 Index 页

新增文档时，在对应项目的 `<h2>` 标题下的 `<ul>` 列表中用 `lark-cli docs +update --command block_insert_after` 插入引用链接：
- 引用链接使用 `<cite>` 标签：`<cite doc-id="<wikiToken>" file-type="wiki" title="<name>" type="doc"></cite>`

### 配置

Index 页的 wikiToken 记录在配置文件中：
```json
{
  "feishuDomain": "xxx.feishu.cn",
  "indexWikiToken": "Index导航页的wikiToken",
  "docs": [...]
}
```

## 总结变更并通知群聊

当配置文件中有 `notifyChatIds`（非空数组）且本次有文档实际更新（同步成功数量 > 0）时，同步完成后 AI 需总结本次变更并发送摘要到配置的群聊。全部"未变化"时跳过此步。

### 前置条件

- **bot 已加入所有目标群**：以 `--as bot` 发送，bot 必须已是每个目标群的成员，否则对应群发送失败
- **目标群 chat_id**：即 `notifyChatIds` 中的每一项，格式 `oc_xxx`

### 获取群 chat_id

若只知道群名，可用 lark-im 查询 chat_id：

```bash
# 按群名搜索
lark-cli im +chat-search --query "群名关键词" --as user
# 或列出 bot 已加入的群
lark-cli im +chat-list --as bot
```

### 通知流程

1. **确定已更新的文档**：从 `pnpm sync:wiki` 输出中解析 `ok     {name} - 同步成功` 行，得到本次实际更新的文档列表
2. **读取并总结变更**：逐个读取已更新文档的本地 Markdown 文件，生成简洁的中文摘要
   - CHANGELOG 类文档：聚焦最新版本条目，提炼新增 / 修复 / 优化等要点
   - 其他文档：概述本次主要变更内容
3. **组装摘要消息**：用 Markdown 组织消息，包含：
   - 标题（如「文档更新摘要 · {YYYY-MM-DD HH:mm}」）
   - 每个已更新文档的小标题 + 变更要点（控制在 3~6 条以内）
   - 文档的飞书访问链接：`https://{feishuDomain}/wiki/{wikiToken}`
4. **发送到所有配置群**：对 `notifyChatIds` 中每个 chat_id 各发一条：
   ```bash
   lark-cli im +messages-send --chat-id <notifyChatId> --markdown '<摘要内容>' --as bot
   ```

### 示例消息

```markdown
## 文档更新摘要 · 2026-08-19 14:30

### 象州客户端 CHANGELOG
- 新增「一键导出」功能
- 修复低版本 iOS 表格滚动卡顿
- 优化首屏加载速度

### README
- 补充环境变量配置说明
- 更新部署架构图

文档链接：
- [象州客户端 CHANGELOG](https://xxx.feishu.cn/wiki/xxxx)
- [README](https://xxx.feishu.cn/wiki/yyyy)
```

> 发送前可先将摘要内容交用户确认；若希望全自动，配置 `notifyChatIds` 并触发同步即视为已授权直接发送。

## 脚本工作原理

1. 从 cwd 向上查找 `lark-wiki-sync.config.json`
2. 对每个文档条目：
   - 读取 Markdown 文件，将第一行 `# xxx` 替换为 `# {title 或 name}`
   - 对处理后的内容（**不含时间戳标记行**，换行符已归一化为 LF）计算 sha256 哈希
   - 与状态文件中记录的哈希对比：内容与 wikiToken 均未变化则跳过，不发任何 API 请求
   - 在标题后插入引用块：`<blockquote>本文档由 AI 助手自动同步 · 最后更新于 {时间}</blockquote>`
   - 通过 `lark-cli wiki +node-get` 解析 wikiToken 得到实际 doc token（obj_token）
   - 通过 `lark-cli docs +update --command overwrite --doc-format markdown` 以 bot 身份覆盖文档
   - **同步成功后**才将内容哈希写入状态文件；失败保留旧状态，下次自动重试
3. 输出同步结果摘要（成功 / 未变化 / 跳过 / 失败）

## 增量同步状态文件

脚本自动在配置文件同目录维护 `lark-wiki-sync.state.json`（如配置为 `custom.json` 则为 `custom.state.json`），**无需手动编辑**：

```json
{
  "docs": {
    "apps/your-app/CHANGELOG.md": {
      "contentHash": "sha256 哈希",
      "wikiToken": "上次同步使用的 wikiToken",
      "syncedAt": "2026-08-17 10:00:00"
    }
  }
}
```

- 以 `docs[].path` 为 key，内容或 wikiToken 变化才会重新同步
- 建议加入 `.gitignore`（本机状态，无需提交）
- 状态文件损坏或被删除时自动视为空状态，退化为全量同步，安全无副作用
- 需要"无论如何都全量推送一次"时使用 `--force`

## 注意事项

- **bot 身份写入**：以 bot 身份操作，便于在飞书文档历史中区分人工编辑和自动同步
- **增量同步**：内容未变化的文档自动跳过（不发 API 请求），只有内容或 wikiToken 变化时才 overwrite
- **overwrite 模式**：实际同步时会清空文档后重写（飞书自身的版本历史仍可回溯）
- **Windows 兼容**：脚本在 Windows 上使用 `shell: true` 调用 lark-cli（`.cmd` 文件需要）
- **任意文档**：不限于 CHANGELOG，任何 Markdown 文件都可以同步
- **Index 页同步**：当配置文件有 `indexWikiToken` 且本次有文档实际更新时，同步文档后必须同时更新 Index 导航页（时间戳 + 项目信息检查）；全部未变化时跳过
- **群聊通知**：当配置文件有 `notifyChatIds`（非空）且本次有文档实际更新时，同步后 AI 会总结变更并发送摘要到这些群；bot 需已加入每个目标群。留空数组 `[]` 则不通知
