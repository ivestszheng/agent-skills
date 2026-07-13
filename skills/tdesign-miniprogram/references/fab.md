# Fab 悬浮按钮

## 引入

```json
{
  "usingComponents": {
    "t-fab": "tdesign-miniprogram/fab/fab"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-fab icon="plus" />
```

### 悬浮按钮类型

```xml
<t-fab icon="plus" theme="primary" />
<t-fab icon="plus" theme="default" />
<t-fab icon="plus" theme="danger" />
```

### 悬浮按钮状态

```xml
<t-fab icon="plus" disabled />
<t-fab icon="plus" loading />
```

### 带文字悬浮按钮

```xml
<t-fab icon="plus">新建</t-fab>
```

### 悬浮按钮位置

```xml
<t-fab icon="plus" placement="top-right" />
<t-fab icon="plus" placement="bottom-right" />
<t-fab icon="plus" placement="bottom-left" />
<t-fab icon="plus" placement="top-left" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| icon | String | - | 图标名称 |
| theme | String | primary | 主题，可选值：primary / default / danger |
| disabled | Boolean | false | 是否禁用 |
| loading | Boolean | false | 是否加载中 |
| placement | String | bottom-right | 位置，可选值：top-right / bottom-right / bottom-left / top-left |
| visible | Boolean | true | 是否显示 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| click | event | 点击事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |