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
