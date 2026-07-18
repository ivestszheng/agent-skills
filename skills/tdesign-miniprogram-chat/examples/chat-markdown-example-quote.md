<!--
  文件名: chat-markdown-example-quote.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-markdown#_04-引用
  场景: 引用
  描述: 演示 ChatMarkdown 对引用块语法的渲染。
  依赖组件: t-chat-markdown
  关键特性: 引用块渲染, blockquote样式
-->

# ChatMarkdown 代码演示-引用

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
下面是引用示例

> TDesign distills Tencent's years of design experience into professional design guideline, providing universal design solutions that assist product managers, designers, developers, and other roles in efficiently completing the design and development of enterprise-level products, while maintaining consistent design language and style to meet user experience requirements.
`;

export default mockMarkdownData;
```