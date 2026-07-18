<!--
  文件名: chat-markdown-example-img-and-link.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-markdown#_03-图片与链接
  场景: 图片与链接
  描述: 演示 ChatMarkdown 对图片和超链接的渲染，支持图片点击预览。
  依赖组件: t-chat-markdown
  关键特性: 图片渲染, 超链接, 图片预览, click事件
-->

# ChatMarkdown 代码演示-图片与链接

```wxml
<view class="chat-example-block">
  <t-chat-markdown content="{{markdownContent}}" bind:click="handleNodeTap" />
</view>
```

```js
import markdownData from './mock.js';
// 内置marked处理
Page({
  data: {
    markdownContent: markdownData,
  },
  handleNodeTap(e) {
    const { node } = e.detail;
    // 打印节点信息
    console.log('点击节点', node);
    // 图片节点预览
    if (node && node.type === 'image') {
      wx.previewImage({
        urls: [node.href],
        current: node.href,
      });
    }
  },
});
```

```css
.demo-container {
  padding: 32rpx;
  background-color: #fff;
}

.text {
  margin-left: 10rpx;
  margin-bottom: 32rpx;
}
```

```json
{
  "usingComponents": {
    "t-chat-markdown": "tdesign-miniprogram/chat-markdown/chat-markdown"
  }
}
```

```js
const mockMarkdownData = `
![示例](https://tdesign.gtimg.com/demo/demo-image-1.png "示例")
这是一个链接 [Markdown语法](https://markdown.com.cn)。
`;

export default mockMarkdownData;
```