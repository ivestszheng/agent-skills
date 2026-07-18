<!--
  文件名: chat-thinking-example-status-complete.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-thinking#思考完成
  场景: 思考完成
  描述: 演示 ChatThinking 思考完成后的状态展示，面板默认收起。
  依赖组件: t-chat-thinking
  关键特性: 思考完成状态, status:complete, 面板收起
-->

# ChatThinking 代码演示-思考完成

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
    status: 'complete',
    content: {
      text: '嗯，用户问牛顿第一定律是不是适用于所有参考系。首先，我得先回忆一下牛顿第一定律的内容。牛顿第一定律，也就是惯性定律，说物体在没有外力作用时会保持静止或匀速直线运动。也就是说， 保持原来的运动状态。',
      title: '已深度思考(用时19秒)',
    },
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
    "t-chat-thinking": "tdesign-miniprogram/chat-thinking/chat-thinking",
    "t-radio": "tdesign-miniprogram/radio/radio",
    "t-radio-group": "tdesign-miniprogram/radio-group/radio-group"
  }
}
```