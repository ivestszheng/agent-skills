# ChatMessage 对话消息体

单条聊天消息组件，展示头像、昵称、时间、消息内容和操作栏。

## 引入

```json
{
  "usingComponents": {
    "t-chat-message": "tdesign-miniprogram/chat-message/chat-message",
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar"
  }
}
```

## 基础用法

```xml
<t-chat-message
  content="{{userMessage.content}}"
  role="{{userMessage.role}}"
/>
```

## Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `avatar` | String | - | 头像 URL |
| `name` | String | - | 昵称 |
| `datetime` | String | - | 时间文本 |
| `content` | Array | `[]` | 消息内容数组，每项 `{ type: 'text'\|'markdown', data: string }` |
| `role` | String | `'user'` | 角色：`user` / `assistant` / `system` |
| `placement` | String | - | 对齐方式：`'left'` / `'right'` |
| `status` | String | `''` | 消息状态：`'pending'` / `'complete'` / `'error'` |
| `chat-id` | String | - | 消息唯一标识 |
| `chatContentProps` | Object | - | 传递给 t-chat-content 的额外属性 |
| `variant` | String | - | 变体样式：`'text'` 等 |

## Slots

| 插槽名 | 说明 |
|--------|------|
| `avatar` | 自定义头像 |
| `name` | 自定义昵称区域 |
| `actionbar` | 操作栏插槽（放 t-chat-actionbar） |
| `content` | 自定义内容（默认使用 t-chat-content） |

## 可配置头像、昵称、对齐方式

```xml
<!-- 用户消息，右侧 -->
<t-chat-message
  datetime="16:38"
  name="张三"
  content="{{message.content}}"
  role="{{message.role}}"
/>

<!-- 助手消息，左侧带头像 -->
<t-chat-message
  avatar="https://tdesign.gtimg.com/site/chat-avatar.png"
  datetime="16:38"
  name="TDesignAI"
  content="{{message.content}}"
  role="{{message.role}}"
/>

<!-- 自定义 name 插槽 -->
<t-chat-message content="{{message.content}}" role="{{message.role}}" datetime="16:38">
  <view slot="name" class="name-block">
    <image src="https://tdesign.gtimg.com/site/chat-avatar.png" />
    <view>Canxuan</view>
  </view>
</t-chat-message>
```

## 附件消息

```xml
<t-chat-message
  content="{{pic.content}}"
  role="{{pic.role}}"
  chatContentProps="{{chatContentProps}}"
/>
```

## 思考过程消息

```xml
<t-chat-message
  content="{{aiMessage.content}}"
  role="{{aiMessage.role}}"
  status="{{aiMessage.status}}"
  variant="text"
>
  <t-chat-actionbar slot="actionbar" />
</t-chat-message>
```

## 事件

| 事件名 | 说明 |
|--------|------|
| `bind:message-longpress` | 消息长按 |
| `bind:click` | 消息点击 |

## content 插槽使用建议

- 渲染聊天消息统一用 `t-chat-content`
- 仅在需要"单独使用 Markdown 组件"时使用 `t-chat-markdown`
- 也可选择其他第三方 markdown 渲染库
