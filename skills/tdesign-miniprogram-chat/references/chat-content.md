# ChatContent 对话正文

聊天消息正文内容组件，根据角色自动选择渲染方式：用户消息用纯文本（HTML 转义），助手消息用 Markdown 渲染。

## 引入

```json
{
  "usingComponents": {
    "t-chat-content": "tdesign-miniprogram/chat-content/chat-content"
  }
}
```

## Props

| 名称 | 类型 | 默认值 | 说明 | 必传 |
|------|------|--------|------|------|
| `content` | Object | - | 聊天内容对象 | **Y** |
| `role` | String | - | 消息角色：`user` / `assistant` / `system` | **Y** |
| `markdown-props` | Object | - | marked 解析器配置选项（透传给 t-chat-markdown） | N |
| `status` | String | - | 正文状态：`'error'` / `''` | N |

### TdChatContentType 类型

```typescript
interface TdChatContentType {
  type: 'text' | 'markdown';
  data: string;
}
```

> 类型定义详见：[type.ts](https://github.com/Tencent/tdesign-miniprogram/blob/develop/packages/pro-components/chat/chat-content/type.ts)

## 事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `bindclick` | 内容节点点击 | `{ node: { type, href, text } }` |

## 渲染规则

- **用户消息（role=user）**：纯文本内容，自动做 HTML 转义并用 `rich-text` 渲染
- **助手消息（role=assistant）**：自动调用内置 `t-chat-markdown` 组件渲染 Markdown

## 基础用法

```xml
<!-- 用户消息：纯文本 -->
<t-chat-content content="{{userContent}}" role="user" />

<!-- 助手消息：Markdown -->
<t-chat-content content="{{assistantContent}}" role="assistant" bindclick="onClick" />
```

```javascript
import markdownData from './mock.js';

Component({
  data: {
    userContent: {
      type: 'text',
      data: '这是用户发送的普通文本内容',
    },
    assistantContent: {
      type: 'markdown',
      data: markdownData,
    },
  },
  methods: {
    onClick(e) {
      const { node } = e.detail;
      console.log('点击节点', node);
    },
  },
});
```

## 在 ChatMessage 中自动使用

当使用 `t-chat-message` 组件时，如果未提供自定义 `content` 插槽，组件内部会自动使用 `t-chat-content` 进行渲染。因此通常不需要直接使用 `t-chat-content`，除非需要单独控制渲染行为。

## content 插槽使用建议

- **推荐**：渲染聊天消息统一使用 `t-chat-content`（它会根据 type 自动选择 text 或 markdown 渲染）
- **单独使用**：仅在需要直接使用 Markdown 渲染组件时，使用 `t-chat-markdown`
- **自定义**：也可选择其他第三方 markdown 渲染库，自行替换

## Markdown 数据示例

```javascript
const mockMarkdownData = `# Markdown功能测试

## 基础语法测试

### 列表测试
- 无序列表项1
- 无序列表项2
  - 缩进列表项1
  - 缩进列表项2

### 代码块测试
\`\`\`javascript
function greet(name) {
  console.log(\`Hello, \${name}!\`);
}
greet('Markdown');
\`\`\`

> 引用文本块

**加粗文字** _斜体文字_ ~~删除线~~

这是一个链接 [TDesign](https://tdesign.tencent.com)。
`;
```
