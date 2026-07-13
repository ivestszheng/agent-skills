# Textarea 多行文本框

## 引入

```json
{
  "usingComponents": {
    "t-textarea": "tdesign-miniprogram/textarea/textarea"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-textarea value="{{value}}" bind:change="onChange" placeholder="请输入内容" />
```

```javascript
Page({
  data: {
    value: ''
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 指定行数

```xml
<t-textarea rows="3" placeholder="3行文本框" />
<t-textarea rows="5" placeholder="5行文本框" />
```

### 自动高度

```xml
<t-textarea auto-height placeholder="自动高度" />
```

### 禁用与只读

```xml
<t-textarea disabled placeholder="禁用状态" />
<t-textarea readonly placeholder="只读状态" />
```

### 字数统计

```xml
<t-textarea maxlength="100" show-word-limit placeholder="字数统计" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String | - | 输入值 |
| placeholder | String | - | 占位符 |
| rows | Number | 3 | 行数 |
| maxlength | Number | - | 最大长度 |
| disabled | Boolean | false | 是否禁用 |
| readonly | Boolean | false | 是否只读 |
| auto-height | Boolean | false | 是否自动高度 |
| show-word-limit | Boolean | false | 是否显示字数统计 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |
| focus | - | 聚焦事件 |
| blur | - | 失焦事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |