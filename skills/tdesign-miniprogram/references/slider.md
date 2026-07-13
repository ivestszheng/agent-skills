# Slider 滑动选择器

## 引入

```json
{
  "usingComponents": {
    "t-slider": "tdesign-miniprogram/slider/slider"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-slider value="{{value}}" bind:change="onChange" />
```

```javascript
Page({
  data: {
    value: 50
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 设置范围

```xml
<t-slider value="{{value}}" min="0" max="100" bind:change="onChange" />
```

### 设置步长

```xml
<t-slider value="{{value}}" step="5" bind:change="onChange" />
```

### 禁用状态

```xml
<t-slider value="{{value}}" disabled />
```

### 显示数值

```xml
<t-slider value="{{value}}" show-value bind:change="onChange" />
```

### 自定义颜色

```xml
<t-slider value="{{value}}" active-color="#1677ff" inactive-color="#e5e5e5" bind:change="onChange" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Number | 0 | 当前值 |
| min | Number | 0 | 最小值 |
| max | Number | 100 | 最大值 |
| step | Number | 1 | 步长 |
| disabled | Boolean | false | 是否禁用 |
| show-value | Boolean | false | 是否显示数值 |
| active-color | String | - | 激活态颜色 |
| inactive-color | String | - | 未激活态颜色 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |
| changing | { value } | 拖动中事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |