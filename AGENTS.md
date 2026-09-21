# Agent Skills - agent-skills 项目

## 版本管理

本仓库**不做仓库级发版**：不使用 standard-version，不打 tag，`package.json` 的 `version` 不再随提交变化，`CHANGELOG.md` 停更并保留为历史记录。版本号只存在于每个 Skill 自己的 `SKILL.md` 里。

提交仍需遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/)：提交类型包括 `feat:`（新功能）、`fix:`（修复）、`docs:`（文档）、`style:`（格式）、`refactor:`（重构）、`test:`（测试）、`chore:`（构建/工具）等——Skill 版本号就是据此推导的。

### Skill 版本（`skills/<name>/SKILL.md`）

每个 Skill 自带独立版本号，写在各自 `SKILL.md` frontmatter 的 `version` 字段里，用于发布到 SkillHub 等平台。

- **自动更新**：推送到 `main` 时由 `.github/workflows/release.yml` 的 `Bump skill versions` 步骤完成
  - 按 `github.event.before..github.sha` 范围找出**本次推送改动到的 Skill**，只 bump 这些
  - 以 `chore: 自动更新 skill 版本号` 单独提交后推回 `main`
  - 不用本地 git 钩子：版本号代表「已合入 main 的内容」，避免 WIP 提交让版本号反复跳
  - bump 前会先跑 `node scripts/validate-skills.mjs`，frontmatter 不合规则整个 workflow 失败、不会 bump
- **幂等**：若某 Skill 的版本相对基线已变过（例如本地手动 bump 过），脚本会跳过，不会重复 bump
- **bump 级别**由本次提交信息推导：`fix:` 等 → patch，`feat:` → minor，`BREAKING CHANGE` / `feat!:` → major（版本低于 `1.0.0` 时降级为 minor）
- **手动命令**：
  - `pnpm skill:bump` 按工作区改动 bump（加 `--dry-run` 只预览）
  - `pnpm skill:bump:all` 所有 Skill 各 bump 一次
  - `pnpm skill:check` 校验「改了 Skill 却没 bump 版本号」
  - `pnpm skill:validate [skill-name...]` 校验 frontmatter 是否满足发布要求
  - `node scripts/bump-skill-versions.mjs --help` 查看全部参数
- **可选本地钩子**：`pnpm hooks:install` 启用 `scripts/hooks/pre-commit`，适合想「提交即带版本号」的场景；依赖上面的幂等逻辑，与 CI 同时存在也不会重复 bump
- 新增 Skill 时在 frontmatter 补 `slug`、`displayName`、`version` 三个字段（`slug` 在 SkillHub 全网唯一），脚本首次运行会补上 `version: 0.1.0`

### frontmatter 字段

两套规范叠加在同一个 `SKILL.md` 上，校验脚本 `scripts/validate-skills.mjs` 按此逐项检查：

| 字段 | 来源 | 要求 |
|---|---|---|
| `name` | Agent Skills 标准 | 必填，≤64 字符、kebab-case、必须与父目录名一致 |
| `description` | Agent Skills 标准 | 必填，≤1024 字符，写清「做什么 + 何时用」 |
| `license` / `compatibility` / `metadata` / `allowed-tools` | Agent Skills 标准 | 可选 |
| `slug` | SkillHub | 必填，2-128 位 kebab-case |
| `displayName` | SkillHub | 必填 |
| `version` | SkillHub | 必填，合法 SemVer |
| `summary` / `tags` / `homepage` | SkillHub | 建议填写，缺失只提醒不阻断 |

标准明确「未知顶层字段会被忽略」，因此 SkillHub 专有字段与标准字段可以共存，不影响其他客户端加载。**`version` 必须写在顶层**——`bump-skill-versions.mjs` 只匹配顶层 `version:` 行，写进 `metadata` 会导致自动 bump 失效。

## Git 提交信息

**所有 git 提交信息必须使用中文**，包括：
- 提交的标题（subject）
- 提交的详细描述（body）
- 关闭 issue 的信息（footer）

示例：
```
feat(qianji): 新增预算执行分析
- 解析预算表并计算执行率
- 报告中新增月度对比区块
```
