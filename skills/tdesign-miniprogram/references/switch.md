# Switch 开关

## 引入

```json
{
  "usingComponents": {
    "t-switch": "tdesign-miniprogram/switch/switch"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-switch value="{{value}}" bind:change="onChange" />
```

```javascript
Page({
  data: {
    value: false
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 禁用状态

```xml
<t-switch value="{{value}}" disabled />
```

### 自定义颜色

```xml
<t-switch value="{{value}}" active-color="#52c41a" inactive-color="#d9d9d9" />
```

### 加载状态

```xml
<t-switch value="{{value}}" loading />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Boolean | false | 当前值 |
| disabled | Boolean | false | 是否禁用 |
| loading | Boolean | false | 是否加载中 |
| active-color | String | - | 激活态颜色 |
| inactive-color | String | - | 未激活态颜色 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |