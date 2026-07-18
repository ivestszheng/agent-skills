<!--
  文件名: chat-markdown-example-list.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-markdown#列表
  场景: 列表
  描述: 演示 ChatMarkdown 对无序列表和有序列表的渲染。
  依赖组件: t-chat-markdown
  关键特性: 无序列表, 有序列表, 嵌套列表
-->

# ChatMarkdown 代码演示-列表

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
.chat-example-block {
  background-color: var(--td-bg-color-container);
  padding: 32rpx;
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
- 无序列表
- 无序列表
  - 嵌套列表
  - 嵌套列表

1. 有序列表
2. 有序列表
`;

export default mockMarkdownData;
```