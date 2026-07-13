# Stepper 步进器

## 引入

```json
{
  "usingComponents": {
    "t-stepper": "tdesign-miniprogram/stepper/stepper"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-stepper value="{{value}}" bind:change="onChange" />
```

```javascript
Page({
  data: {
    value: 1
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 设置范围

```xml
<t-stepper value="{{value}}" min="1" max="10" bind:change="onChange" />
```

### 设置步长

```xml
<t-stepper value="{{value}}" step="2" bind:change="onChange" />
```

### 禁用状态

```xml
<t-stepper value="{{value}}" disabled />
```

### 只读状态

```xml
<t-stepper value="{{value}}" readonly />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Number | 1 | 当前值 |
| min | Number | 0 | 最小值 |
| max | Number | 9999 | 最大值 |
| step | Number | 1 | 步长 |
| disabled | Boolean | false | 是否禁用 |
| readonly | Boolean | false | 是否只读 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |