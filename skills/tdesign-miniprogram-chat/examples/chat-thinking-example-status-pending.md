<!--
  文件名: chat-thinking-example-status-pending.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-thinking#_思考中
  场景: 思考中
  描述: 演示 ChatThinking 思考中的状态，展示加载动效。
  依赖组件: t-chat-thinking
  关键特性: 思考中状态, status:pending, 加载动效
-->

# ChatThinking 代码演示-思考中

思考中 

```wxml
<view class="chat-example-block">
  <t-chat-thinking
    content="{{content}}"
    layout="block"
    status="{{status}}"
    bind:collapsedChange="handleCollapsedChange"
  />
</view>
```

```js
Component({
  data: {
    animation: 'moving',
    content: {
      text: '嗯，用户问牛顿第一定律是不是适用于所有参考系。首先，我得先回忆一下牛顿第一定律的内容。牛顿第一定律',
      title: '思考中···',
    },
    status: 'pending',
  },
  methods: {
    handleCollapsedChange(e) {
      console.log('展开状态变化:', e.detail);
    },
  },
});
```

```css
.chat-example-block {
  background-color: var(--td-bg-color-container);
  padding: 32rpx;
}
```

```json
{
  "usingComponents": {
    "t-chat-thinking": "tdesign-miniprogram/chat-thinking/chat-thinking"
  }
}
```