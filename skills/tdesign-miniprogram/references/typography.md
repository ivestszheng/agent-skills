# Typography 排版

## 引入

```json
{
  "usingComponents": {
    "t-text": "tdesign-miniprogram/typography/text",
    "t-title": "tdesign-miniprogram/typography/title"
  }
}
```

## 代码演示

### 标题

```xml
<t-title level="1">一级标题</t-title>
<t-title level="2">二级标题</t-title>
<t-title level="3">三级标题</t-title>
<t-title level="4">四级标题</t-title>
```

### 文本样式

```xml
<t-text>普通文本</t-text>
<t-text bold>粗体文本</t-text>
<t-text disabled>禁用文本</t-text>
<t-text mark>标记文本</t-text>
<t-text code>代码文本</t-text>
<t-text underline>下划线文本</t-text>
<t-text delete>删除线文本</t-text>
```

### 文本颜色

```xml
<t-text theme="primary">主要颜色</t-text>
<t-text theme="success">成功颜色</t-text>
<t-text theme="warning">警告颜色</t-text>
<t-text theme="danger">危险颜色</t-text>
<t-text theme="disabled">禁用颜色</t-text>
```

### 文本大小

```xml
<t-text size="small">小号文本</t-text>
<t-text size="medium">中号文本</t-text>
<t-text size="large">大号文本</t-text>
```

## API

### Title Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| level | Number | 1 | 标题级别，可选值：1 / 2 / 3 / 4 |
| ellipsis | Boolean | false | 是否省略 |
| max-lines | Number | - | 最大行数 |

### Text Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| bold | Boolean | false | 是否粗体 |
| disabled | Boolean | false | 是否禁用 |
| mark | Boolean | false | 是否标记 |
| code | Boolean | false | 是否代码 |
| underline | Boolean | false | 是否下划线 |
| delete | Boolean | false | 是否删除线 |
| theme | String | default | 主题颜色，可选值：primary / success / warning / danger / disabled |
| size | String | medium | 尺寸，可选值：small / medium / large |
| ellipsis | Boolean | false | 是否省略 |
| max-lines | Number | - | 最大行数 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |