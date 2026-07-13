# Rate 评分

## 引入

```json
{
  "usingComponents": {
    "t-rate": "tdesign-miniprogram/rate/rate"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-rate value="{{value}}" bind:change="onChange" />
```

```javascript
Page({
  data: {
    value: 3
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 设置数量

```xml
<t-rate value="{{value}}" count="5" bind:change="onChange" />
<t-rate value="{{value}}" count="10" bind:change="onChange" />
```

### 禁用状态

```xml
<t-rate value="{{value}}" disabled />
```

### 只读状态

```xml
<t-rate value="{{value}}" readonly />
```

### 半星评分

```xml
<t-rate value="{{value}}" allow-half bind:change="onChange" />
```

### 自定义颜色

```xml
<t-rate value="{{value}}" active-color="#ffd700" inactive-color="#e5e5e5" bind:change="onChange" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Number | 0 | 当前值 |
| count | Number | 5 | 星星数量 |
| disabled | Boolean | false | 是否禁用 |
| readonly | Boolean | false | 是否只读 |
| allow-half | Boolean | false | 是否允许半星 |
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