# DateTimePicker 日期选择器

## 引入

```json
{
  "usingComponents": {
    "t-date-time-picker": "tdesign-miniprogram/date-time-picker/date-time-picker"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-date-time-picker 
  value="{{value}}" 
  bind:change="onChange" 
  placeholder="请选择日期时间" 
/>
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

### 日期选择器

```xml
<t-date-time-picker 
  value="{{value}}" 
  type="date" 
  bind:change="onChange" 
/>
```

### 时间选择器

```xml
<t-date-time-picker 
  value="{{value}}" 
  type="time" 
  bind:change="onChange" 
/>
```

### 日期时间选择器

```xml
<t-date-time-picker 
  value="{{value}}" 
  type="datetime" 
  bind:change="onChange" 
/>
```

### 禁用状态

```xml
<t-date-time-picker disabled placeholder="禁用状态" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String | - | 当前值 |
| type | String | date | 类型，可选值：date / time / datetime |
| placeholder | String | - | 占位符 |
| disabled | Boolean | false | 是否禁用 |
| min-date | String | - | 最小日期 |
| max-date | String | - | 最大日期 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |