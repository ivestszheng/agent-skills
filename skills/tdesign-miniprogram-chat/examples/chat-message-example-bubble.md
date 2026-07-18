<!--
  文件名: chat-message-example-bubble.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-message#气泡样式
  场景: 气泡样式
  描述: 演示 variant 属性的不同气泡样式：text、base、outline。
  依赖组件: t-chat-message, t-chat-actionbar
  关键特性: variant气泡样式, text/base/outline三种变体
-->

# ChatMessage 代码演示-气泡样式

```wxml
<view class="chat-example">
  <view class="chat-example-block"
    ><t-chat-message content="{{userMessage.content}}" role="{{userMessage.role}}" variant="text"></t-chat-message
  ></view>
  <view class="chat-example-block"
    ><t-chat-message content="{{userMessage.content}}" role="{{userMessage.role}}" variant="base"></t-chat-message
  ></view>
  <view class="chat-example-block"
    ><t-chat-message content="{{userMessage.content}}" role="{{userMessage.role}}" variant="outline"></t-chat-message
  ></view>
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
  "styleIsolation": "shared",
  "usingComponents": {
    "t-chat-message": "tdesign-miniprogram/chat-message/chat-message",
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar"
  }
}
```