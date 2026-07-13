# Loading 加载

## 引入

```json
{
  "usingComponents": {
    "t-loading": "tdesign-miniprogram/loading/loading"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-loading />
```

### 加载中文字

```xml
<t-loading text="加载中..." />
```

### 加载类型

```xml
<t-loading type="spinner" />
<t-loading type="circular" />
```

### 加载尺寸

```xml
<t-loading size="small" />
<t-loading size="medium" />
<t-loading size="large" />
```

### 全屏加载

```xml
<t-loading fullscreen visible="{{visible}}" />
```

```javascript
Page({
  data: {
    visible: true
  },
  onLoadComplete() {
    this.setData({ visible: false });
  }
});
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| visible | Boolean | true | 是否显示 |
| text | String | - | 加载文本 |
| type | String | spinner | 类型，可选值：spinner / circular |
| size | String | medium | 尺寸，可选值：small / medium / large |
| fullscreen | Boolean | false | 是否全屏 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |