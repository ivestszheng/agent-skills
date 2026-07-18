<!--
  文件名: chat-thinking-example-type.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-thinking#_01-组件类型
  场景: 组件类型
  描述: 演示 ChatThinking 的基础类型，支持打字机效果和多种加载动效。
  依赖组件: t-chat-thinking
  关键特性: 组件类型, 打字机效果, 动效类型, collapsed控制
-->

# ChatThinking 代码演示-组件类型

支持多种加载动效类型，包括`gradient`、`moving`、`dots`


```wxml
<view class="chat-example-block">
  <t-chat-thinking
    content="{{content}}"
    layout="block"
    status="{{status}}"
    animation="moving"
    bind:collapsedChange="handleCollapsedChange"
  />
</view>
```

```js
Component({
  data: {
    thinking: true,
    fullText:
      '嗯，用户问牛顿第一定律是不是适用于所有参考系。首先，我得先回忆一下牛顿第一定律的内容。牛顿第一定律，也就是惯性定律，说物体在没有外力作用时会保持静止或匀速直线运动。也就是说， 保持原来的运动状态。',
    currentText: '',
    isTyping: true,
    content: {
      text: '',
      title: '思考过程',
    },
    typeSpeed: 50,
    status: 'pending',
    startTime: 0,
  },

  lifetimes: {
    attached() {
      this.setData({
        startTime: Date.now(),
      });
      this.startTyping();
    },

    detached() {
      if (this.typingTimer) {
        clearTimeout(this.typingTimer);
      }
    },
  },

  methods: {
    startTyping() {
      const { fullText, typeSpeed } = this.data;
      let currentIndex = 0;
      const typeNextChar = () => {
        if (currentIndex <= fullText.length) {
          const currentText = fullText.substring(0, currentIndex);
          // 检查是否已经完成打字
          if (currentIndex === fullText.length) {
            const endTime = Date.now();
            const duration = Math.round((endTime - this.data.startTime) / 1000);
            this.setData({
              currentText,
              content: {
                text: currentText,
                title: `已完成思考（耗时${duration}秒）`,
              },
              isTyping: false,
              status: 'complete',
            });
            return; // 直接返回，不再继续执行
          }
          // 正常打字过程
          this.setData({
            currentText,
            content: {
              text: currentText,
              title: '思考过程',
            },
            isTyping: currentIndex < fullText.length,
          });
          if (currentIndex < fullText.length) {
            this.typingTimer = setTimeout(typeNextChar, typeSpeed);
          }
          currentIndex += 1;
        }
      };
      typeNextChar();
    },
    replayTyping() {
      if (this.typingTimer) {
        clearTimeout(this.typingTimer);
      }
      this.setData({
        currentText: '',
        content: {
          text: '',
          title: '思考过程',
        },
        isTyping: true,
        startTime: Date.now(),
      });
      this.startTyping();
    },
    onStop() {
      console.log('停止思考');
      this.setData({
        thinking: false,
      });
      wx.showToast({
        title: '已停止思考',
        icon: 'success',
      });
    },
    toggleThinking() {
      this.setData({
        thinking: !this.data.thinking,
      });
    },
    resetThinking() {
      this.setData({
        thinking: true,
      });
      wx.showToast({
        title: '已重置',
        icon: 'success',
      });
    },
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
  },
  "component": true
}
```

支持通过collapsed来控制面板是否折叠，示例中展示了当内容输出结束时自动收起的效果

```wxml
<view class="chat-example-block">
  <t-chat-thinking
    content="{{content}}"
    layout="block"
    status="{{status}}"
    animation="moving"
    bind:collapsedChange="handleCollapsedChange"
    collapsed="{{collapsed}}"
  />
</view>
```

```js
Component({
  data: {
    thinking: true,
    collapsed: false,
    fullText:
      '嗯，用户问牛顿第一定律是不是适用于所有参考系。首先，我得先回忆一下牛顿第一定律的内容。牛顿第一定律，也就是惯性定律，说物体在没有外力作用时会保持静止或匀速直线运动。也就是说， 保持原来的运动状态。',
    currentText: '',
    isTyping: true,
    content: {
      text: '',
      title: '思考过程',
    },
    typeSpeed: 50,
    status: 'pending',
    startTime: 0,
  },

  observers: {
    status(val) {
      if (val === 'complete') {
        this.setData({ collapsed: true });
      }
    },
  },

  lifetimes: {
    attached() {
      this.setData({
        startTime: Date.now(),
      });
      this.startTyping();
    },

    detached() {
      if (this.typingTimer) {
        clearTimeout(this.typingTimer);
      }
    },
  },

  methods: {
    startTyping() {
      const { fullText, typeSpeed } = this.data;
      let currentIndex = 0;
      const typeNextChar = () => {
        if (currentIndex <= fullText.length) {
          const currentText = fullText.substring(0, currentIndex);
          // 检查是否已经完成打字
          if (currentIndex === fullText.length) {
            const endTime = Date.now();
            const duration = Math.round((endTime - this.data.startTime) / 1000);
            this.setData({
              currentText,
              content: {
                text: currentText,
                title: `已完成思考（耗时${duration}秒）`,
              },
              isTyping: false,
              status: 'complete',
            });
            return; // 直接返回，不再继续执行
          }
          // 正常打字过程
          this.setData({
            currentText,
            content: {
              text: currentText,
              title: '思考过程',
            },
            isTyping: currentIndex < fullText.length,
          });
          if (currentIndex < fullText.length) {
            this.typingTimer = setTimeout(typeNextChar, typeSpeed);
          }
          currentIndex += 1;
        }
      };
      typeNextChar();
    },
    replayTyping() {
      if (this.typingTimer) {
        clearTimeout(this.typingTimer);
      }
      this.setData({
        currentText: '',
        content: {
          text: '',
          title: '思考过程',
        },
        isTyping: true,
        startTime: Date.now(),
      });
      this.startTyping();
    },
    onStop() {
      console.log('停止思考');
      this.setData({
        thinking: false,
      });
      wx.showToast({
        title: '已停止思考',
        icon: 'success',
      });
    },
    toggleThinking() {
      this.setData({
        thinking: !this.data.thinking,
      });
    },
    resetThinking() {
      this.setData({
        thinking: true,
      });
      wx.showToast({
        title: '已重置',
        icon: 'success',
      });
    },
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
  },
  "component": true
}
```
