<!--
  文件名: chat-loading-example-animation.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-loading#_01-组件类型
  场景: 动画样式
  描述: 演示 ChatLoading 的多种动效类型：gradient、moving、dots。
  依赖组件: t-chat-loading
  关键特性: 动画样式, gradient/moving/dots, 动效切换
-->

# ChatLoading 代码演示-动画样式

```wxml
<view class="chat-example">
  <!-- <view class="chat-example-block">
    <t-chat-loading animation="skeleton" />
  </view> -->
  <view class="chat-example-block">
    <t-chat-loading animation="gradient" />
  </view>
  <view class="chat-example-block">
    <t-chat-loading animation="moving" />
  </view>
  <view class="chat-example-block">
    <t-chat-loading animation="dots" />
  </view>
</view>
```

```js
Component({
  data: {
    currentAnimation: 'skeleton',
    loadingText: '',
    animations: [
      { key: 'moving', text: '正在理解中...' },
      { key: 'gradient', text: '深度思考中...' },
      { key: 'circle', text: '加载中...' },
      { key: 'skeleton', text: '' },
    ],
  },

  onLoad() {
    // 模拟动画切换
    this.startAnimationCycle();
  },

  startAnimationCycle() {
    let index = 0;
    this.animationTimer = setInterval(() => {
      const animation = this.data.animations[index];
      this.setData({
        currentAnimation: animation.key,
        loadingText: animation.text,
      });

      index = (index + 1) % this.data.animations.length;
    }, 2000); // 每2秒切换一次动画
  },

  onUnload() {
    // 清理定时器
    if (this.animationTimer) {
      clearInterval(this.animationTimer);
    }
  },

  // 手动切换动画类型
  switchAnimation(e) {
    const { animation } = e.currentTarget.dataset;
    const animationData = this.data.animations.find((item) => item.key === animation);

    if (animationData) {
      this.setData({
        currentAnimation: animationData.key,
        loadingText: animationData.text,
      });
    }
  },
});
```

```css
.chat-example {
  background-color: var(--td-bg-color-container);
  padding: 32rpx;
  display: flex;
  align-items: center;
  gap: 48rpx;
}
```

```json
{
  "usingComponents": {
    "t-chat-loading": "tdesign-miniprogram/chat-loading/chat-loading",
    "t-col": "tdesign-miniprogram/col/col",
    "t-row": "tdesign-miniprogram/row/row"
  }
}
```