# 项目规则

你已经加载 [vercel skills](https://www.skills.sh) 技能框架。

## 可用 Skills

| Skill         | 触发条件                                                     |
| ------------- | ------------------------------------------------------------ |
| brainstorming | 在任何创造性工作之前必须使用此技能——创建功能、构建组件、添加功能或修改行为。在实现之前先探索用户意图、需求和设计。 |
| ai-elements | 使用 ai-elements 组件构建 AI 聊天界面（对话、消息、工具展示、提示输入等）。当用户想构建聊天机器人、AI 助手 UI 或任何 AI 驱动的聊天界面时使用。 |
| building-components | 构建现代、可访问且可组合的 UI 组件指南。在构建新组件、实现可访问性（ARIA、键盘导航、焦点管理）、创建可组合 API、设置设计 tokens 与主题系统、发布组件到 npm/registry 或编写组件文档时使用。 |
| shadcn | 管理 shadcn 组件与项目——添加、搜索、修复、调试、样式化和组合 UI。在处理 shadcn/ui、组件注册表、`--preset` 代码、或任何含 `components.json` 的项目时应用；也在 "shadcn init"、"用 --preset 创建应用" 或 "切换 --preset" 时触发。 |
| streamdown | 实现、配置和自定义 Streamdown——一种针对流式渲染优化的 React Markdown 渲染器，支持语法高亮、Mermaid 图、数学渲染和 CJK。在 Streamdown 安装与配置、插件（code/mermaid/math/cjk）、样式、安全配置、与 AI 流式集成（如 Vercel AI SDK）、caret 静态模式或自定义组件、以及排查 Tailwind/Shiki/Vite 问题时使用。 |
| turborepo | Turborepo monorepo 构建系统指导。在 `turbo.json`、任务管道、`dependsOn`、缓存、远程缓存、`turbo` CLI、`--filter`、`--affected`、CI 优化、环境变量、内部 packages、monorepo 结构与最佳实践、以及边界管理时触发。 |
| next-best-practices | Next.js 最佳实践——文件约定、RSC 边界、数据模式、异步 API、metadata、错误处理、路由处理器、图像/字体优化、打包。 |
| vercel-react-best-practices | 来自 Vercel 工程团队的 React 与 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码以确保最优性能模式时使用。涉及 React 组件、Next.js 页面、数据获取、bundle 优化或性能改进等任务时触发。 |
| web-design-guidelines | 审查 UI 代码是否符合 Web Interface Guidelines。在被要求 "审查我的 UI"、"检查可访问性"、"审计设计"、"审查 UX" 或 "按最佳实践检查我的站点" 时使用。 |
| taro-miniprogram-dev | Taro + React + TypeScript 微信小程序开发框架技能。适用于：(1) 从零初始化 Taro 项目并编译为微信小程序；(2) 创建页面、组件、样式；(3) 搭建 services 请求层（接入真实后端或 Mock 数据）；(4) 配置 TabBar、页面路由、设计系统。触发关键词：小程序开发、Taro开发、微信小程序、mini program、Taro框架、项目初始化。 |

## 可用 Packages

| Package | 使用场景 |
| ------- | -------- |
| `@repo/ui` | 共享 Wev UI 组件库——基于 shadcn/ui 扩展的 React/TypeScript 组件集合，包含 `Button`、`Card`、`Dialog`、`Input`、`Avatar`、`Conversation`、`Message` 等 80+ 组件，以及 `src/styles/globals.css` 全局样式和 `lib/utils.ts` 工具函数。 |
| `@repo/utils` | 通用工具函数库——提供 `log`（日志与 debug 输出）和 `AuthUtils`（认证相关）。组件开发、业务代码中需要统一的日志或鉴权时使用。 |
| `@repo/typescript-config` | 共享 TypeScript 配置——预置 `base.json`、`nextjs.json`、`react-library.json`、`taro.json` 四套 tsconfig 配置。新项目在根 `tsconfig.json` 中通过 `extends` 引用，即可获得统一的编译目标与路径别名。 |
| `@repo/eslint-config` | 共享 ESLint 配置——提供 `./base`、`./next-js`、`./react-internal` 三套预设，涵盖 `@typescript-eslint`、`eslint-plugin-react`、`eslint-plugin-react-hooks`、`eslint-plugin-turbo` 等插件。新项目直接引用即可获得一致的代码规范。 |
| `docker` | Docker 镜像构建方案——包含 `Dockerfile.nextjs`（Next.js 项目）、`Dockerfile.vite`（Vite 静态项目）以及 `build-helper.js`（分析 app 依赖 packages）。支持 `APP_NAME`、`PORT`、`BUILD_MODE` 三个构建参数，`README.md` 中有完整使用示例。 |
| `nginx-config` | 共享 Nginx 配置——`base.conf` 为基础站点模板，内置 `try_files` 解决前端框架路由刷新 404 问题。Vite/Next.js 静态部署时可直接作为容器的 `/etc/nginx/conf.d/default.conf`。 |
