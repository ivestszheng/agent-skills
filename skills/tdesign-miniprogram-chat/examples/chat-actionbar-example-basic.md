<!--
  文件名: chat-actionbar-example-basic.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-actionbar#基础类型
  场景: 基础用法
  描述: 演示 ChatActionbar 的基础用法，包含复制、点赞、点踩、分享等操作。
  依赖组件: t-chat-actionbar, t-toast
  关键特性: 基础操作栏, actions事件, copy/good/bad/share操作
-->

# ChatActionbar 代码演示-基础用法

```wxml
<t-toast id="t-toast" />
<view class="container">
  <t-chat-actionbar content="{{content}}" bind:actions="handleAction" />
</view>
```

```js
import Toast from 'tdesign-miniprogram/toast';

Component({
  data: {
    content: '这是一段可以被复制的内容，支持markdown格式。\n\n**粗体文本**\n*斜体文本*\n\n- 列表项1\n- 列表项2',
  },

  methods: {
    handleAction(e) {
      const { name, active, data } = e.detail;

      let message = '';
      switch (name) {
        case 'replay':
          message = '重新生成';
          break;
        case 'copy':
          console.log(data);
          message = '复制成功';
          break;
        case 'good':
          message = active ? '点赞成功' : '取消点赞';
          break;
        case 'bad':
          message = active ? '点踩成功' : '取消点踩';
          break;
        case 'share':
          message = '分享功能';
          break;
        default:
          message = `执行了${name}操作`;
      }

      Toast({
        context: this,
        selector: '#t-toast',
        message,
        theme: 'success',
      });
    },
  },
});
```

```css
.container {
  padding: 32rpx;
  background-color: var(--td-bg-color-container);
}

.layout-btn {
  margin: 16rpx 0;
  padding: 12rpx 24rpx;
  background-color: #0052d9;
  color: #fff;
  border: none;
  border-radius: 8rpx;
  font-size: 28rpx;
}

.demo-text {
  padding: 16rpx 0;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}
```

```json
{
  "component": true,
  "usingComponents": {
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar",
    "t-toast": "tdesign-miniprogram/toast/toast"
  }
}
```