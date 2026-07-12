# ChatActionbar 对话操作栏

消息操作栏组件，提供复制、引用、分享等快捷操作。

## 引入

```json
{
  "usingComponents": {
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar"
  }
}
```

## 基础用法

### 作为 ChatMessage 子组件（内嵌模式）

```xml
<t-chat-message
  content="{{item.content}}"
  role="{{item.role}}"
>
  <t-chat-actionbar slot="actionbar" />
</t-chat-message>
```

### 在 ChatList 中使用（悬浮/长按模式）

```xml
<t-chat-actionbar
  class="popover-actionbar"
  placement="longpress"
  bind:actions="handlePopoverAction"
  longPressPosition="{{longPressPosition}}"
  action-bar="{{['quote', 'copy', 'share']}}"
/>
```

### 手动初始化状态

可通过编程方式手动初始化操作栏的状态和位置。

## Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `placement` | String | `'end'` | 展示位置：`'end'`（消息末尾）/ `'longpress'`（长按弹出） |
| `chat-id` | String | - | 关联的消息 ID |
| `comment` | String | `''` | 备注/评注内容 |
| `action-bar` | Array | - | 操作项列表，如 `['quote', 'copy', 'share']` |
| `longPressPosition` | Object | `null` | 长按弹出的位置坐标 |

## 事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `bind:actions` | 点击操作项时触发 | `{ action: string, chatId: string }` |

## 事件处理示例

```javascript
handleAction(e) {
  const { action, chatId } = e.detail;
  switch (action) {
    case 'copy':
      wx.setClipboardData({ data: '消息内容' });
      break;
    case 'quote':
      // 设置引用内容到输入框
      this.setData({ quotedContent: '...' });
      break;
    case 'share':
      // 分享逻辑
      break;
  }
}
```
