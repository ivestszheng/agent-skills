# Agent Skills - agent-skills 项目

## 版本管理

此项目使用 `standard-version` 进行版本管理和发布。

- 请使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 规范提交代码
- 提交类型包括：`feat:`（新功能）、`fix:`（修复）、`docs:`（文档）、`style:`（格式）、`refactor:`（重构）、`test:`（测试）、`chore:`（构建/工具）等
- 当代码推送到 `main` 分支时，CI 会自动运行 `standard-version` 来：
  - 根据提交历史自动升级版本号
  - 生成 `CHANGELOG.md`
  - 创建 git tag
  - 提交并推送变更

## Git 提交信息

**所有 git 提交信息必须使用中文**，包括：
- 提交的标题（subject）
- 提交的详细描述（body）
- 关闭 issue 的信息（footer）

示例：
```
feat: 添加 standard-version 版本管理配置
- 配置 package.json 中的 standard-version 脚本
- 添加 GitHub Actions CI 工作流
- 在 main 分支推送时自动触发版本发布
```
