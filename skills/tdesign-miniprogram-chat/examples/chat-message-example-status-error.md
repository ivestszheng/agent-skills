<!--
  文件名: chat-message-example-status-error.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-message#出错状态
  场景: 出错状态
  描述: 演示 status 为 error 时的消息展示。
  依赖组件: t-chat-message, t-chat-actionbar
  关键特性: status错误状态, error展示
-->

# ChatMessage 代码演示-错误状态

```wxml
<view class="chat-example">
  <view class="chat-example-block">
    <t-chat-message
      avatar="https://tdesign.gtimg.com/site/chat-avatar.png"
      content="{{message.content}}"
      role="{{message.role}}"
      status="error"
    ></t-chat-message>
  </view>
</view>
```

```js
Component({
  data: {
    message: {
      role: 'assistant',
      status: 'error',
      content: [
        {
          type: 'text',
          data: '´• •`!!!请求出错',
        },
      ],
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