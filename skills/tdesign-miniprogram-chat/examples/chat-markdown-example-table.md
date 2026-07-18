<!--
  文件名: chat-markdown-example-table.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-markdown#表格
  场景: 表格
  描述: 演示 ChatMarkdown 对 Markdown 表格语法的渲染，支持对齐方式。
  依赖组件: t-chat-markdown
  关键特性: 表格渲染, 对齐方式, 左/中/右对齐
-->

# ChatMarkdown 代码演示-表格

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
| 左对齐     | 居中对齐 | 右对齐 | 内容 |
| :--------- | :------: | -----: | ----- |
| 单元格     |  单元格  | 单元格 | 单元格 |
| 长文本示例| 长文本示例长文本示例长文本示例 |   $100 | 文本内容 |
| 文本示例 | 文本内容 | $100 |  文本内容 |
`;

export default mockMarkdownData;
```