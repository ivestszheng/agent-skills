<!--
  文件名: chat-markdown-example-title-and-text.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-markdown#标题与文本
  场景: 标题与文本
  描述: 演示 ChatMarkdown 对标题、加粗、删除线、行内代码等基础文本样式的渲染。
  依赖组件: t-chat-markdown
  关键特性: 标题渲染, 加粗/删除线, 行内代码, 基础文本样式
-->

# ChatMarkdown 代码演示-标题与文本

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
# 一级标题

## 二级标题

### 三级标题

#### 四级标题

##### 五级标题

###### 六级标题

正文

**加粗正文**

~~删除线~~

行内代码: \`console.log('Hello')\`
`;

export default mockMarkdownData;
```