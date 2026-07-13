# Progress 进度条

## 引入

```json
{
  "usingComponents": {
    "t-progress": "tdesign-miniprogram/progress/progress"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-progress value="{{value}}" />
```

```javascript
Page({
  data: {
    value: 50
  }
});
```

### 设置样式

```xml
<t-progress value="{{value}}" theme="primary" />
<t-progress value="{{value}}" theme="success" />
<t-progress value="{{value}}" theme="warning" />
<t-progress value="{{value}}" theme="danger" />
```

### 显示数值

```xml
<t-progress value="{{value}}" show-value />
<t-progress value="{{value}}" show-value label="自定义标签" />
```

### 设置高度

```xml
<t-progress value="{{value}}" stroke-width="8" />
<t-progress value="{{value}}" stroke-width="16" />
```

### 环形进度条

```xml
<t-progress value="{{value}}" type="circle" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Number | 0 | 当前值 |
| type | String | line | 类型，可选值：line / circle |
| theme | String | primary | 主题，可选值：primary / success / warning / danger |
| stroke-width | Number | 8 | 线条宽度 |
| show-value | Boolean | false | 是否显示数值 |
| label | String | - | 自定义标签 |
| color | String | - | 自定义颜色 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |