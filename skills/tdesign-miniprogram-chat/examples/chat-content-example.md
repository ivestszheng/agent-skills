<!--
  文件名: chat-content-example.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-content#_01-组件类型
  场景: 组件类型
  描述: 演示 ChatContent 根据 role 自动切换渲染：user 纯文本、assistant Markdown。
  依赖组件: t-chat-content
  关键特性: 文本渲染, Markdown渲染, role自动切换, HTML转义
-->

# ChatContent 代码演示-组件类型

```wxml
<view class="chat-example">
  <view class="title">用户内容纯文本支持HTML转义</view>
  <view class="chat-example-block">
    <t-chat-content content="{{userContent}}" role="user"></t-chat-content>
  </view>
</view>

<view class="chat-example">
  <view class="title">助手内容（Markdown）</view>
  <view class="chat-example-block">
    <t-chat-content content="{{assistantContent}}" role="assistant" bindclick="onClick"></t-chat-content>
  </view>
</view>
```

```js
// import { Lexer } from 'marked';
import markdownData from './mock.js';

// 创建Lexer实例时添加配置，禁用gfm规范中的缩进代码块
// const lexer = new Lexer({});

// const tokens = lexer.lex(markdownData);

Component({
  data: {
    userContent: {
      type: 'text',
      data: '这是用户发送的普通文本内容',
    },
    assistantContent: {
      type: 'markdown',
      data: markdownData,
    },
  },
  methods: {
    onClick(e) {
      const { node } = e.detail;
      console.log('点击节点', node);
    },
  },
});
```

```css
.chat-example {
  margin-bottom: 32rpx;
}

.chat-example-block {
  padding: 32rpx;
  background-color: var(--td-bg-color-container);
}

.title {
  padding: 0 32rpx 32rpx;
  font-size: 28rpx;
  line-height: 44rpx;
  color: var(--bg-color-demo-desc);
}
```

```json
{
  "component": true,
  "styleIsolation": "shared",
  "usingComponents": {
    "t-chat-content": "tdesign-miniprogram/chat-content/chat-content"
  }
}
```

```js
const mockMarkdownData = `# Markdown功能测试 (H1标题)

## 基础语法测试 (H2标题)

### 列表测试

- 无序列表项1
- 无序列表项2
    - 缩进列表项1（4个空格缩进）
    - 缩进列表项2（4个空格缩进）

1. 有序列表项1
2. 有序列表项2
    1. 缩进有序列表项1（4个空格缩进）
    2. 缩进有序列表项2（4个空格缩进）

### 代码块测试

\`\`\`javascript
// JavaScript 代码块
function greet(name) {
  console.log(\`Hello, \${name}!\`);
}
greet('Markdown');
\`\`\`

### 其他元素

> 引用文本块
> 多行引用内容

**加粗文字** _斜体文字_ ~~删除线~~

这是一个链接 [TDesign](https://tdesign.tencent.com)。
`;

export default mockMarkdownData;
```