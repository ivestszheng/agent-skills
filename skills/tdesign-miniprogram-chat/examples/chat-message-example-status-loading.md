<!--
  文件名: chat-message-example-status-loading.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-message#加载状态
  场景: 加载状态
  描述: 演示 status 为 pending 时的加载动画，支持 gradient 和 skeleton 两种 animation。
  依赖组件: t-chat-message, t-chat-actionbar
  关键特性: status加载状态, animation动画, gradient/skeleton
-->

# ChatMessage 代码演示-加载状态

```wxml
<view class="chat-example">
  <view class="chat-example-block">
    <t-chat-message
      avatar="https://tdesign.gtimg.com/site/chat-avatar.png"
      content="{{message.content}}"
      role="{{message.role}}"
      animation="gradient"
      status="{{message.status}}"
    ></t-chat-message>
  </view>
  <view class="chat-example-block">
    <t-chat-message
      avatar="https://tdesign.gtimg.com/site/chat-avatar.png"
      content="{{message.content}}"
      role="{{message.role}}"
      animation="skeleton"
      status="{{message.status}}"
    ></t-chat-message>
  </view>
</view>
```

```js
Component({
  data: {
    message: {
      role: 'assistant',
      status: 'pending',
      content: [
        {
          type: 'text',
          data: '牛顿第一定律并不适用于所有参考系，它只适用于惯性参考系。在质点不受外力作用时，能够判断出质点静止或作匀速直线运动的参考系一定是惯性参考系，因此只有在惯性参考系中牛顿第一定律才适用。',
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