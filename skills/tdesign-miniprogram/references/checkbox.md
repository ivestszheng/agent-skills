# CheckBox 多选框

## 引入

```json
{
  "usingComponents": {
    "t-checkbox-group": "tdesign-miniprogram/checkbox/checkbox-group",
    "t-checkbox": "tdesign-miniprogram/checkbox/checkbox"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-checkbox-group value="{{value}}" bind:change="onChange">
  <t-checkbox label="选项一" value="1" />
  <t-checkbox label="选项二" value="2" />
  <t-checkbox label="选项三" value="3" />
</t-checkbox-group>
```

```javascript
Page({
  data: {
    value: ['1']
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 全选与反选

```xml
<t-checkbox-group value="{{value}}" bind:change="onChange">
  <t-checkbox label="全选" value="all" indeterminate="{{indeterminate}}" />
  <view class="options">
    <t-checkbox label="选项一" value="1" />
    <t-checkbox label="选项二" value="2" />
    <t-checkbox label="选项三" value="3" />
  </view>
</t-checkbox-group>
```

### 禁用状态

```xml
<t-checkbox-group value="{{value}}">
  <t-checkbox label="选项一" value="1" />
  <t-checkbox label="选项二" value="2" disabled />
  <t-checkbox label="选项三" value="3" />
</t-checkbox-group>
```

### 横向排列

```xml
<t-checkbox-group value="{{value}}" layout="horizontal">
  <t-checkbox label="选项一" value="1" />
  <t-checkbox label="选项二" value="2" />
  <t-checkbox label="选项三" value="3" />
</t-checkbox-group>
```

## API

### CheckBoxGroup Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Array | [] | 当前值 |
| layout | String | vertical | 布局方式，可选值：horizontal / vertical |

### CheckBox Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| label | String | - | 标签文本 |
| value | String / Number | - | 值 |
| disabled | Boolean | false | 是否禁用 |
| indeterminate | Boolean | false | 半选状态 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |