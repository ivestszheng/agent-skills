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
└── package.json
```

## 配置文件

从 `lark-wiki-sync.config.template.json` 复制到项目根目录，改名为 `lark-wiki-sync.config.json`：

```json
{
  "feishuDomain": "your-tenant.feishu.cn",
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
# 同步所有配置的文档
pnpm sync:wiki

# 只同步名称或路径匹配的文档
pnpm sync:wiki -- --filter 象州

# 预览不写入
pnpm sync:wiki -- --dry-run
```

## 新增文档流程

1. 在飞书知识库中创建一个 wiki 文档
2. 从 wiki 文档 URL 中提取 token（`/wiki/` 后的部分）
3. 在 `lark-wiki-sync.config.json` 的 `docs` 数组中添加一项
4. 如果项目有 Index 导航页，通过 `lark-doc` skill 在 Index 页中对应标题下插入新文档的引用链接
5. 运行 `pnpm sync:wiki -- --dry-run` 验证

### 更新 Index 导航页（可选）

如果项目在飞书知识库中有一个 Index 导航页（汇总各文档的链接），新增文档后应同步更新。Index 页不走 `sync:wiki` 脚本（它包含飞书特有的引用、图片等内容，不适合 overwrite），而是通过 `lark-doc` skill 增量编辑：

1. 通过 `lark-cli docs +fetch --detail with-ids` 获取 Index 页的 block 结构
2. 找到对应标题 block，在其后的列表中用 `lark-cli docs +update --command block_insert_after` 插入引用链接
3. 引用链接使用 `<cite>` 标签：`<cite doc-id="<wikiToken>" file-type="wiki" title="<name>" type="doc"></cite>`

Index 页的 wikiToken 可记录在配置文件中以便 AI 查找：
```json
{
  "feishuDomain": "xxx.feishu.cn",
  "indexWikiToken": "可选，Index导航页的wikiToken",
  "docs": [...]
}
```

## 脚本工作原理

1. 从 cwd 向上查找 `lark-wiki-sync.config.json`
2. 对每个文档条目：
   - 读取 Markdown 文件，将第一行 `# xxx` 替换为 `# {title 或 name}`
   - 在标题后插入引用块：`<blockquote>本文档由 AI 助手自动同步 · 最后更新于 {时间}</blockquote>`
   - 通过 `lark-cli wiki +node-get` 解析 wikiToken 得到实际 doc token（obj_token）
   - 通过 `lark-cli docs +update --command overwrite --doc-format markdown` 以 bot 身份覆盖文档
3. 输出同步结果摘要

## 注意事项

- **bot 身份写入**：以 bot 身份操作，便于在飞书文档历史中区分人工编辑和自动同步
- **overwrite 模式**：每次同步会清空文档后重写（飞书自身的版本历史仍可回溯）
- **Windows 兼容**：脚本在 Windows 上使用 `shell: true` 调用 lark-cli（`.cmd` 文件需要）
- **任意文档**：不限于 CHANGELOG，任何 Markdown 文件都可以同步
