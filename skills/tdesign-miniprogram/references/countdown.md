# CountDown 倒计时

## 引入

```json
{
  "usingComponents": {
    "t-count-down": "tdesign-miniprogram/count-down/count-down"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-count-down value="{{endTime}}" />
```

```javascript
Page({
  data: {
    endTime: Date.now() + 60 * 60 * 1000
  }
});
```

### 显示天数

```xml
<t-count-down value="{{endTime}}" show-days />
```

### 自定义格式

```xml
<t-count-down value="{{endTime}}" format="HH:mm:ss" />
```

### 毫秒级显示

```xml
<t-count-down value="{{endTime}}" millisecond />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Number | - | 结束时间戳 |
| format | String | HH:mm:ss | 时间格式 |
| show-days | Boolean | false | 是否显示天数 |
| millisecond | Boolean | false | 是否毫秒级显示 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| finish | - | 倒计时结束事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |