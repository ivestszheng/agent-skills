<!--
  文件名: chat-markdown-example-code.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-markdown#代码块
  场景: 代码块
  描述: 演示 ChatMarkdown 对代码块语法的渲染，支持语法高亮语言标注。
  依赖组件: t-chat-markdown
  关键特性: 代码块渲染, 语法高亮, marked解析
-->

# ChatMarkdown 代码演示-代码块

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
\`\`\`TDesign-登录表单.jsx
import { Form, Input, Button, Message } from 'tdesign-react';
const LoginForm = () => { const [loading, setLoading] = useState(false);
\`\`\`
`;

export default mockMarkdownData;
```