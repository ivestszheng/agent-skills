# Calendar 日历

## 引入

```json
{
  "usingComponents": {
    "t-calendar": "tdesign-miniprogram/calendar/calendar"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-calendar value="{{value}}" bind:change="onChange" />
```

```javascript
Page({
  data: {
    value: new Date()
  },
  onChange(e) {
    console.log('选择日期', e.detail.value);
  }
});
```

### 选择范围

```xml
<t-calendar type="range" value="{{value}}" bind:change="onChange" />
```

```javascript
Page({
  data: {
    value: [new Date('2024-01-01'), new Date('2024-01-10')]
  }
});
```

### 禁用日期

```xml
<t-calendar 
  value="{{value}}" 
  disabled-date="{{disabledDate}}" 
  bind:change="onChange" 
/>
```

```javascript
Page({
  data: {
    disabledDate(date) {
      return date < new Date();
    }
  }
});
```

### 设置可选范围

```xml
<t-calendar 
  value="{{value}}" 
  min-date="{{minDate}}" 
  max-date="{{maxDate}}" 
  bind:change="onChange" 
/>
```

```javascript
Page({
  data: {
    minDate: new Date('2024-01-01'),
    maxDate: new Date('2024-12-31')
  }
});
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Date / Array | - | 当前值 |
| type | String | single | 选择类型，可选值：single / range |
| disabled-date | Function | - | 禁用日期函数 |
| min-date | Date | - | 最小可选日期 |
| max-date | Date | - | 最大可选日期 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |