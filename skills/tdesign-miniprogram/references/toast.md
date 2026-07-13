# Toast 轻提示

## 引入

```json
{
  "usingComponents": {
    "t-toast": "tdesign-miniprogram/toast/toast"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-toast visible="{{visible}}" text="提示信息" />
```

```javascript
Page({
  data: {
    visible: false
  },
  showToast() {
    this.setData({ visible: true });
    setTimeout(() => {
      this.setData({ visible: false });
    }, 2000);
  }
});
```

### 提示类型

```xml
<t-toast visible="{{visible}}" type="success" text="操作成功" />
<t-toast visible="{{visible}}" type="error" text="操作失败" />
<t-toast visible="{{visible}}" type="warning" text="警告信息" />
<t-toast visible="{{visible}}" type="info" text="提示信息" />
```

### 自定义时长

```xml
<t-toast visible="{{visible}}" text="提示信息" duration="3000" />
```

### 加载中

```xml
<t-toast visible="{{visible}}" type="loading" text="加载中..." />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| visible | Boolean | false | 是否显示 |
| text | String | - | 提示文本 |
| type | String | info | 类型，可选值：success / error / warning / info / loading |
| duration | Number | 2000 | 显示时长(ms) |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| close | - | 关闭事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |