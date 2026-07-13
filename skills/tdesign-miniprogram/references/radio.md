# Radio 单选框

## 引入

```json
{
  "usingComponents": {
    "t-radio-group": "tdesign-miniprogram/radio/radio-group",
    "t-radio": "tdesign-miniprogram/radio/radio"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-radio-group value="{{value}}" bind:change="onChange">
  <t-radio label="选项一" value="1" />
  <t-radio label="选项二" value="2" />
  <t-radio label="选项三" value="3" />
</t-radio-group>
```

```javascript
Page({
  data: {
    value: '1'
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 禁用状态

```xml
<t-radio-group value="{{value}}">
  <t-radio label="选项一" value="1" />
  <t-radio label="选项二" value="2" disabled />
  <t-radio label="选项三" value="3" />
</t-radio-group>
```

### 横向排列

```xml
<t-radio-group value="{{value}}" layout="horizontal">
  <t-radio label="选项一" value="1" />
  <t-radio label="选项二" value="2" />
  <t-radio label="选项三" value="3" />
</t-radio-group>
```

## API

### RadioGroup Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String / Number | - | 当前值 |
| layout | String | vertical | 布局方式，可选值：horizontal / vertical |

### Radio Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| label | String | - | 标签文本 |
| value | String / Number | - | 值 |
| disabled | Boolean | false | 是否禁用 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |