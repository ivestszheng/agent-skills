<!--
  文件名: chat-message-example-avatar.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-message#可配置昵称、头像、对齐方式
  场景: 可配置昵称、头像、对齐方式
  描述: 演示 avatar、name、placement 属性的配置，以及 name 插槽自定义。
  依赖组件: t-chat-message, t-chat-actionbar, t-divider
  关键特性: avatar/name配置, placement对齐, name插槽自定义
-->

# ChatMessage 代码演示-可配置昵称、头像、对齐方式

支持`avatar`,`name`插槽自定义

```wxml
<view class="chat-example">
  <view class="chat-example-block">
    <t-chat-message datetime="16:38" name="张三" content="{{message.content}}" role="{{message.role}}"></t-chat-message>
  </view>
  <view class="chat-example-block">
    <t-chat-message
      avatar="https://tdesign.gtimg.com/site/chat-avatar.png"
      datetime="16:38"
      name="TDesignAI"
      content="{{message.content}}"
      role="{{message.role}}"
    ></t-chat-message>
  </view>
  <view class="chat-example-block">
    <t-chat-message
      avatar="https://tdesign.gtimg.com/site/chat-avatar.png"
      datetime="16:38"
      name="TDesignAI"
      content="{{message.content}}"
      role="{{message.role}}"
      placement="right"
    ></t-chat-message>
  </view>
  <view class="chat-example-block">
    <t-chat-message content="{{message.content}}" role="{{message.role}}" datetime="16:38">
      <view slot="name" class="name-block">
        <image src="https://tdesign.gtimg.com/site/chat-avatar.png" />
        <view>Canxuan</view>
      </view>
    </t-chat-message>
  </view>
</view>
```

```js
Component({
  data: {
    message: {
      role: 'system',
      content: [
        {
          type: 'text',
          data: '牛顿第一定律是否适用于所有参考系？',
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

.name-block {
  display: flex;
  align-items: center;
  margin-right: 16rpx;
}

.name-block image {
  margin-right: 16rpx;
  width: 40rpx;
  height: 40rpx;
}
```

```json
{
  "component": true,
  "usingComponents": {
    "t-chat-message": "tdesign-miniprogram/chat-message/chat-message",
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar",
    "t-divider": "tdesign-miniprogram/divider/divider"
  }
}
```