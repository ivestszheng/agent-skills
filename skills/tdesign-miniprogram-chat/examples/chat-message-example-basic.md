<!--
  文件名: chat-message-example-basic.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-message#基础类型
  场景: 基础类型
  描述: 演示 ChatMessage 的基础用法，展示单条文本消息。
  依赖组件: t-chat-message, t-chat-actionbar
  关键特性: 基础文本消息, content/role属性
-->

# ChatMessage 代码演示-基础类型

```wxml
<view class="chat-example">
  <view class="chat-example-block">
    <t-chat-message content="{{userMessage.content}}" role="{{userMessage.role}}"></t-chat-message>
  </view>
</view>
```

```js
Component({
  properties: {
    userMessage: {
      type: Object,
      value: {
        role: 'user',
        content: [
          {
            type: 'text',
            data: '牛顿第一定律是否适用于所有参考系？',
          },
        ],
      },
    },
  },
});
```

```css
.chat-example {
  display: flex;
  flex-direction: column;
  gap: 32rpx;
}

.chat-example-block {
  background-color: var(--td-bg-color-container);
  padding: 32rpx 32rpx 0 32rpx;
}
```

```json
{
  "component": true,
  "usingComponents": {
    "t-chat-message": "tdesign-miniprogram/chat-message/chat-message",
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar"
  }
}
```