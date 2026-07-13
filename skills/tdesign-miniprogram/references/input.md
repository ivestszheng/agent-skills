# Input 输入框

## 引入

```json
{
  "usingComponents": {
    "t-input": "tdesign-miniprogram/input/input"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-input value="{{value}}" bind:change="onChange" placeholder="请输入内容" />
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

### 输入框类型

```xml
<t-input type="text" placeholder="文本输入" />
<t-input type="number" placeholder="数字输入" />
<t-input type="idcard" placeholder="身份证输入" />
<t-input type="digit" placeholder="带小数点数字" />
```

### 前缀后缀

```xml
<t-input placeholder="带前缀" prefix-icon="search" />
<t-input placeholder="带后缀" suffix-icon="clear" />
<t-input placeholder="带前后缀" prefix-icon="search" suffix-icon="clear" />
```

### 禁用与只读

```xml
<t-input disabled placeholder="禁用状态" />
<t-input readonly placeholder="只读状态" />
```

### 密码输入

```xml
<t-input type="password" placeholder="密码输入" />
<t-input type="password" visible-on-click placeholder="点击显示密码" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String | - | 输入值 |
| type | String | text | 类型，可选值：text / number / idcard / digit / password |
| placeholder | String | - | 占位符 |
| disabled | Boolean | false | 是否禁用 |
| readonly | Boolean | false | 是否只读 |
| prefix-icon | String | - | 前缀图标 |
| suffix-icon | String | - | 后缀图标 |
| clearable | Boolean | false | 是否可清除 |
| visible-on-click | Boolean | false | 密码框点击显示 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |
| focus | - | 聚焦事件 |
| blur | - | 失焦事件 |
| clear | - | 清除事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |