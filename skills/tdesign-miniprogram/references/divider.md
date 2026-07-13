# Divider 分割线

## 引入

```json
{
  "usingComponents": {
    "t-divider": "tdesign-miniprogram/divider/divider"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-divider />
```

### 带文字分割线

```xml
<t-divider>文本分割</t-divider>
```

### 文字位置

```xml
<t-divider content-position="left">左侧文本</t-divider>
<t-divider content-position="center">居中文本</t-divider>
<t-divider content-position="right">右侧文本</t-divider>
```

### 垂直分割线

```xml
<view class="flex-container">
  <text>内容一</text>
  <t-divider layout="vertical" />
  <text>内容二</text>
  <t-divider layout="vertical" />
  <text>内容三</text>
</view>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| layout | String | horizontal | 布局，可选值：horizontal / vertical |
| content-position | String | center | 文本位置，可选值：left / center / right |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |