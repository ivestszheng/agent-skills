---
name: "tdesign-miniprogram-chat"
description: >
  TDesign 微信小程序 AI 聊天组件库（tdesign-miniprogram-chat）完整开发指南。
  当用户在微信小程序中开发 AI 对话/聊天界面、使用 TDesign Chat 组件、
  接入 SSE 流式输出、或提及 t-chat / chat-list / chat-message / chat-sender / chat-actionbar / chat-markdown / chat-thinking / chat-loading / attachments / chat-content 时使用。
---

# TDesign 微信小程序 AI Chat 组件

TDesign Miniprogram Chat 是腾讯 TDesign 团队为微信小程序 AI 聊天场景打造的专业组件库，基于 `tdesign-miniprogram` 包，提供从消息列表、输入框、消息体、Markdown 渲染到思考过程、加载动画、附件管理等完整组件体系。

## 快速导航

| 场景 | 参考文档 |
|------|----------|
| 安装配置与快速上手 | [$getting-started](references/getting-started.md) |
| SSE 流式输出接入 | [$sse-streaming](references/sse-streaming.md) |
| ChatList 对话列表 | [$chat-list](references/chat-list.md) |
| ChatSender 对话输入框 | [$chat-sender](references/chat-sender.md) |
| ChatMessage 对话消息体 | [$chat-message](references/chat-message.md) |
| ChatActionbar 对话操作栏 | [$chat-actionbar](references/chat-actionbar.md) |
| ChatMarkdown Markdown 渲染 | [$chat-markdown](references/chat-markdown.md) |
| ChatThinking 思考过程 | [$chat-thinking](references/chat-thinking.md) |
| ChatLoading 加载动画 | [$chat-loading](references/chat-loading.md) |
| Attachments 文件附件 | [$attachments](references/attachments.md) |
| ChatContent 对话正文 | [$chat-content](references/chat-content.md) |

## 核心概念

### 消息数据结构

每条消息遵循统一的数据结构：

```typescript
interface ChatMessage {
  chatId: string;        // 唯一标识
  role: 'user' | 'assistant' | 'system';  // 角色
  content: TdChatContentType[];  // 内容数组
  avatar?: string;       // 头像 URL
  name?: string;         // 昵称
  datetime?: string;     // 时间
  status?: 'pending' | 'complete' | 'error';  // 状态
  comment?: string;      // 备注/评注
}

interface TdChatContentType {
  type: 'text' | 'markdown';
  data: string;
}
```

### 组件协作关系

```
t-chat (ChatList)              -- 消息列表容器
├── t-chat-message             -- 单条消息
│   ├── t-chat-content         -- 正文内容（自动根据 role 切换样式）
│   │   └── t-chat-markdown    -- Markdown 渲染（assistant 角色时自动使用）
│   ├── t-chat-thinking        -- 思考过程面板
│   ├── t-chat-loading        -- 加载动画
│   ├── t-attachments         -- 文件附件展示
│   └── t-chat-actionbar       -- 操作栏（复制/引用/分享等）
└── t-chat-sender (footer)     -- 底部输入框
```

### 典型使用流程

1. 安装 `tdesign-miniprogram` 并构建 npm
2. 在页面 JSON 中引入所需组件
3. 构建 `chatList` 数据数组
4. 监听 `t-chat-sender` 的 `send` 事件，将用户消息插入列表
5. 发起 SSE 请求，通过 `onChunkReceived` 逐步更新助手消息
6. 流式完成后，更新消息 `status` 为 `complete`

## 路由规则

- **安装/配置问题** → 加载 [$getting-started](references/getting-started.md)
- **SSE 流式接入/大模型对接** → 加载 [$sse-streaming](references/sse-streaming.md)
- **使用 ChatList 组件** → 加载 [$chat-list](references/chat-list.md)
- **使用 ChatSender 输入框** → 加载 [$chat-sender](references/chat-sender.md)
- **使用 ChatMessage 消息体** → 加载 [$chat-message](references/chat-message.md)
- **使用 ChatActionbar 操作栏** → 加载 [$chat-actionbar](references/chat-actionbar.md)
- **使用 ChatMarkdown 渲染** → 加载 [$chat-markdown](references/chat-markdown.md)
- **使用 ChatThinking 思考过程** → 加载 [$chat-thinking](references/chat-thinking.md)
- **使用 ChatLoading 加载动画** → 加载 [$chat-loading](references/chat-loading.md)
- **使用 Attachments 附件** → 加载 [$attachments](references/attachments.md)
- **使用 ChatContent 正文** → 加载 [$chat-content](references/chat-content.md)

## Scripts 脚本工具

`scripts/` 目录提供了开发过程中的实用脚本，加速项目搭建和调试。

| 脚本 | 用途 |
|------|------|
| `scripts/init-project.ps1` | 初始化小程序项目：安装 tdesign-miniprogram、修复 app.json 配置、复制 sse-client.js |
| `scripts/create-chat-page.js` | 一键生成完整聊天页面模板（wxml/wxss/js/json 四件套） |
| `scripts/sse-client.js` | 微信小程序 SSE 客户端封装：流式请求、消息创建、ID 生成 |
| `scripts/mock-server.py` | Python SSE 模拟服务端：本地调试流式对话无需真实后端 |

### 快速开始

```bash
# 1. 初始化项目（PowerShell）
pwsh -File scripts/init-project.ps1

# 2. 生成聊天页面
node scripts/create-chat-page.js pages/chat/chat

# 3. 启动模拟服务端（需先 pip install fastapi uvicorn sse-starlette）
python scripts/mock-server.py

# 4. 在微信开发者工具中构建 npm 并预览
```

### SSE 客户端用法

```javascript
const { createSSEClient, createAssistantMessage, createUserMessage } = require('./sse-client');

const assistantMsg = createAssistantMessage({ avatar: 'https://tdesign.gtimg.com/site/chat-avatar.png' });
const userMsg = createUserMessage('你好');

this.setData({ chatList: [assistantMsg, userMsg, ...this.data.chatList] });

const sse = createSSEClient({
  url: 'https://your-api/chat',
  method: 'POST',
  data: { prompt: '你好' },
  onMessage(content) { this._appendStreamContent(content, assistantMsg.chatId); },
  onComplete() { this._completeStream(assistantMsg.chatId); },
  onError(err) { console.error(err); },
});

// 需要中止时
sse.abort();
```

## 官方资源

- 官方文档：https://tdesign.tencent.com/miniprogram-chat/overview
- GitHub：https://github.com/Tencent/tdesign-miniprogram
- NPM：https://www.npmjs.com/package/tdesign-miniprogram
