<!--
  文件名: chat-loading-example-text.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-loading#带文案描述的加载组件
  场景: 带文案描述的加载组件
  描述: 演示 ChatLoading 配合 text 属性展示带文案描述的加载状态。
  依赖组件: t-chat-loading
  关键特性: 加载文案, text属性, dots动画
-->

# ChatLoading 代码演示-带文案描述的加载组件

```wxml
<view class="chat-example">
  <view class="chat-example-block">
    <t-chat-loading animation="dots" text="加载中..." />
  </view>
</view>
```

```js
Component({
  data: {},
});
```

```css
.chat-example {
  background-color: var(--td-bg-color-container);
  padding: 32rpx;
}
```

```json
{
  "usingComponents": {
    "t-chat-loading": "tdesign-miniprogram/chat-loading/chat-loading"
  }
}
```