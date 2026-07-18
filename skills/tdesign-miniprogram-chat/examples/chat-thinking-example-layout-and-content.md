<!--
  文件名: chat-thinking-example-layout-and-content.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-thinking#_03-组件样式
  场景: 组件样式
  描述: 演示 ChatThinking 的 layout 布局方式（block/border）和 content 插槽自定义。
  依赖组件: t-chat-thinking
  关键特性: layout布局, block/border样式, content插槽自定义
-->

# ChatThinking 代码演示-组件样式

支持通过`layout`来设置思考过程的布局方式 支持通过`content`插槽自定义思考过程显示内容

```wxml
<block>
  <view class="chat-example-desc">block 样式</view>
  <view class="chat-example-block">
    <t-chat-thinking layout="block" content="{{title2}}" status="{{status}}" animation="{{animation}}">
      <view slot="content"> {{text2}} </view>
    </t-chat-thinking>
  </view>

  <view class="chat-example-desc">border 样式</view>
  <view class="chat-example-block">
    <t-chat-thinking layout="border" content="{{content}}" status="{{status}}" animation="{{animation}}" />
  </view>
</block>
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
    title2: {
      title: '已深度思考(用时19秒)',
    },
    text2:
      '嗯，用户问牛顿第一定律是不是适用于所有参考系。首先，我得先回忆一下牛顿第一定律的内容。牛顿第一定律，也就是惯性定律，说物体在没有外力作用时会保持静止或匀速直线运动。也就是说， 保持原来的运动状态。',
  },
});
```

```css
.chat-example-desc {
  margin: var(--td-spacer-3) var(--td-spacer-2) var(--td-spacer-2);
  font-size: var(--td-font-size-base);
  white-space: pre-line;
  color: var(--bg-color-demo-desc);
  line-height: 22px;
}

.chat-example-desc:first-child {
  margin-top: -8px;
}

.chat-example-block {
  background-color: var(--td-bg-color-container);
  padding: var(--td-spacer-2);
}
```

```json
{
  "usingComponents": {
    "t-chat-thinking": "tdesign-miniprogram/chat-thinking/chat-thinking"
  }
}
```