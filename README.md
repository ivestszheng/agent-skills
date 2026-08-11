# agent-skills

[![npm version](https://img.shields.io/npm/v/agent-skills)](https://www.npmjs.com/package/agent-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub last commit](https://img.shields.io/github/last-commit/ivestszheng/agent-skills)](https://github.com/ivestszheng/agent-skills)
[![GitHub stars](https://img.shields.io/github/stars/ivestszheng/agent-skills?style=social)](https://github.com/ivestszheng/agent-skills)

LLM 智能体专属行为规则库 —— 收录面向 [Trae](https://trae.ai/)、飞书 lark-cli、TDesign 小程序等场景的 Rules 与 Skills。

Skills 是由指令（SKILL.md）、脚本（scripts/）和参考文档（references/）组成的文件夹，LLM 智能体在匹配到触发条件时会动态加载对应内容。Rules 是全局生效的行为规范，用于约束代码风格与提交习惯。

## 目录结构

```
agent-skills/
├── rules/                          # 全局行为规则
│   ├── trae/                       # Trae IDE 规则
│   │   ├── global.md               # 代码格式与符号规范
│   │   └── git-commit-message.md   # Git 提交信息规则
│   └── turborepo_rules.md          # Turborepo monorepo 规范
├── skills/                         # 智能体技能
│   ├── lark-wiki-sync/             # 飞书知识库文档同步
│   ├── tdesign-miniprogram/        # TDesign 小程序基础组件
│   └── tdesign-miniprogram-chat/   # TDesign 小程序 AI Chat 组件
├── .trae/rules/                    # Trae IDE 项目级规则（与 rules/ 同步）
├── AGENTS.md                       # 版本管理与提交规范
├── CHANGELOG.md                    # 变更日志
└── package.json                    # 项目配置（standard-version）
```

## 安装与使用

### 安装 Skill 到项目

将对应 skill 目录复制到项目的 `.agents/skills/` 下即可：

```bash
# 示例：安装 tdesign-miniprogram skill
cp -r skills/tdesign-miniprogram  your-project/.agents/skills/
```

### 安装 Rule 到 Trae 项目

将 `rules/trae/` 下的规则文件复制到项目的 `.trae/rules/` 目录，Trae IDE 会自动加载：

```bash
cp -r rules/trae/*  your-project/.trae/rules/
```

## Skill 结构

每个 Skill 遵循统一结构：

```
skill-name/
├── SKILL.md           # 技能入口文件（含 frontmatter + 指令）
├── references/        # 参考文档（按需加载）
└── scripts/           # 脚本工具（按需调用）
```

`SKILL.md` 的 frontmatter 定义技能元数据：

```yaml
---
name: skill-name
description: >
  技能描述与触发条件，当用户提及 xxx 时使用。
---
```

## License

[MIT](https://opensource.org/licenses/MIT)


## Rules

全局行为规则，始终加载、约束所有会话。

| 规则 | 文件路径 | 说明 |
|------|----------|------|
| **代码格式与符号规范** | [rules/trae/global.md](rules/trae/global.md) | 禁止将代码中的 `<` `>` 转义为 HTML 实体，确保泛型、JSX/TSX 标签、比较运算符等语法的正确性 |
| **Git 提交信息规则** | [rules/trae/git-commit-message.md](rules/trae/git-commit-message.md) | 所有 Git 提交信息必须使用中文 |
| **Turborepo 规范** | [rules/turborepo_rules.md](rules/turborepo_rules.md) | Turborepo monorepo 构建系统指导，含可用 Skills、Packages 索引 |

## Skills

智能体技能，按触发条件动态加载。每个 Skill 的详细用法见对应目录下的 `SKILL.md`。

| Skill | 目录 | 说明 |
|-------|------|------|
| **lark-wiki-sync** | [skills/lark-wiki-sync](skills/lark-wiki-sync/SKILL.md) | 通过 lark-cli 将本地 Markdown 文档批量同步到飞书知识库 wiki，支持 monorepo 多文档场景 |
| **tdesign-miniprogram** | [skills/tdesign-miniprogram](skills/tdesign-miniprogram/SKILL.md) | TDesign 微信小程序基础组件库开发指南，涵盖基础布局、导航、输入、数据展示等完整组件体系 |
| **tdesign-miniprogram-chat** | [skills/tdesign-miniprogram-chat](skills/tdesign-miniprogram-chat/SKILL.md) | TDesign 微信小程序 AI 聊天组件库开发指南，含消息列表、Markdown 渲染、SSE 流式输出、附件管理等 |
