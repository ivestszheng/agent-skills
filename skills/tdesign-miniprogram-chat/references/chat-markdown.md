<!--
  文件名: chat-markdown.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-markdown
 -->
# ChatMarkdown Markdown 渲染

在聊天场景中渲染 Markdown 内容的组件，支持标题、列表、代码块、表格、图片、超链接、引用，以及流式输出光标。

## 引入

```json
{
  "usingComponents": {
    "t-chat-markdown": "tdesign-miniprogram/chat-markdown/chat-markdown"
  }
}
```

## Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `content` | String | `''` | Markdown 文本内容 |
| `streaming` | Boolean | `false` | 是否处于流式输出状态（显示光标动画） |

## 事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `bind:click` | 节点点击 | `{ node: { type, href, text } }` |

## Slots

| 插槽名 | 说明 |
|--------|------|
| `tail-component` | 自定义流式输出尾部组件（如圆点、省略号） |

## 基础 Markdown 样式

### 标题与文本

```xml
<t-chat-markdown content="{{markdownContent}}" bind:click="handleNodeTap" />
```

```javascript
import markdownData from './mock.js';

Page({
  data: { markdownContent: markdownData },
  handleNodeTap(e) {
    const { node } = e.detail;
    // 图片节点预览
    if (node && node.type === 'image') {
      wx.previewImage({ urls: [node.href], current: node.href });
    }
  },
});
```

Markdown 数据示例：

```markdown
# 一级标题

## 二级标题

**加粗正文**

~~删除线~~

行内代码：`console.log('Hello')`
```

### 列表

```markdown
- 无序列表
  - 嵌套列表

1. 有序列表
2. 有序列表
```

### 代码块

```markdown
```TDesign-登录表单.jsx
import { Form, Input, Button } from 'tdesign-react';
const LoginForm = () => {
  const [loading, setLoading] = useState(false);
```
```

### 表格

```markdown
| 左对齐 | 居中对齐 | 右对齐 | 内容 |
|:-------|:------:|-------:|------|
| 单元格 | 单元格 | 单元格 | 单元格 |
```

### 图片与超链接

```markdown
![示例](https://tdesign.gtimg.com/demo/demo-image-1.png "示例")
这是一个链接 [Markdown语法](https://markdown.com.cn)。
```

### 引用

```markdown
> TDesign distills Tencent's years of design experience...
```

## 流式输出光标

组件内置了流式输出时的光标动画。通过 `streaming` 属性控制：

```xml
<!-- 默认光标 -->
<t-chat-markdown
  content="{{content}}"
  streaming="{{streaming}}"
  bind:click="handleNodeTap"
/>
```

### 自定义尾部组件

使用 `generic:tail-component` 自定义流式输出尾部样式：

```xml
<!-- 圆点自定义尾部 -->
<t-chat-markdown
  content="{{content}}"
  streaming="{{streaming}}"
  generic:tail-component="custom-tail"
/>

<!-- 省略号自定义尾部 -->
<t-chat-markdown
  content="{{content}}"
  streaming="{{streaming}}"
  generic:tail-component="custom-tail2"
/>
```

### 无动画模式

不传 `streaming` 属性时，不显示任何尾部动画：

```xml
<t-chat-markdown content="{{content}}" bind:click="handleNodeTap" />
```

## FAQ

MarkdownNode 数据结构由 marked 解析器生成，不同节点类型包含不同字段，常见结构如下：


| type 值 | 说明 | 主要字段 |
| :--- | :--- | :--- |
| `heading` | 标题 | `type`, `raw`, `depth` (1-6), `text`, `tokens` (子节点) |
| `paragraph` | 段落 | `type`, `raw`, `text`, `tokens` (子节点) |
| `text` | 文本 | `type`, `raw`, `text`, `tokens` (子节点, 可选) |
| `strong` | 加粗 | `type`, `raw`, `text`, `tokens` (子节点) |
| `em` | 斜体 | `type`, `raw`, `text`, `tokens` (子节点) |
| `del` | 删除线 | `type`, `raw`, `text`, `tokens` (子节点) |
| `link` | 链接 | `type`, `raw`, `text`, `href`, `title`, `tokens` (子节点) |
| `image` | 图片 | `type`, `raw`, `text`, `href`, `title` |
| `list` | 列表 | `type`, `raw`, `ordered` (是否有序), `items` (列表项数组) |
| `blockquote` | 引用块 | `type`, `raw`, `text`, `tokens` (子节点) |
| `code` | 代码块 | `type`, `raw`, `text` (代码内容), `lang` (语言) |
| `codespan` | 行内代码 | `type`, `raw`, `text` |
| `table` | 表格 | `type`, `raw`, `header` (表头数组), `rows` (行数组), `align` (对齐方式) |


> 注：table 和 code 节点点击时，node 为整个节点对象（含完整表格/代码数据）；其余节点点击时，node 为对应的 marked token 对象。

## 完整业务示例

实际业务场景的完整页面示例（含 wxml / js / css / json 四件套）已放在 `examples/` 目录，可直接作为页面模板参考：

| 示例 | 场景说明 | 关键特性 |
|------|----------|----------|
| [标题与文本](../examples/chat-markdown-example-title-and-text.md) | 基础文本样式 | 标题渲染, 加粗/删除线, 行内代码, 基础文本样式 |
| [列表](../examples/chat-markdown-example-list.md) | 有序/无序列表 | 无序列表, 有序列表, 嵌套列表 |
| [代码块](../examples/chat-markdown-example-code.md) | 代码语法高亮 | 代码块渲染, 语法高亮, marked解析 |
| [表格](../examples/chat-markdown-example-table.md) | 表格对齐渲染 | 表格渲染, 对齐方式, 左/中/右对齐 |
| [图片与链接](../examples/chat-markdown-example-img-and-link.md) | 图片与超链接 | 图片渲染, 超链接, 图片预览, click事件 |
| [引用](../examples/chat-markdown-example-quote.md) | 引用块渲染 | 引用块渲染, blockquote样式 |
| [流式输出光标](../examples/chat-markdown-example-streaming-output-cursor.md) | 流式光标动画 | 流式输出光标, streaming属性, generic:tail-component, 自定义尾部 |