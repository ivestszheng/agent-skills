# Link 链接

## 引入

```json
{
  "usingComponents": {
    "t-link": "tdesign-miniprogram/link/link"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-link href="/pages/index">普通链接</t-link>
```

### 链接类型

```xml
<t-link href="/pages/index" theme="primary">主要链接</t-link>
<t-link href="/pages/index" theme="success">成功链接</t-link>
<t-link href="/pages/index" theme="warning">警告链接</t-link>
<t-link href="/pages/index" theme="danger">危险链接</t-link>
```

### 链接状态

```xml
<t-link href="/pages/index" disabled>禁用链接</t-link>
<t-link href="/pages/index" underline>带下划线</t-link>
<t-link href="/pages/index" hover>悬停效果</t-link>
```

### 图标链接

```xml
<t-link href="/pages/index" icon="arrow-right">带图标</t-link>
<t-link href="/pages/index" icon="arrow-left" icon-position="right">图标在右</t-link>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| href | String | - | 链接地址 |
| theme | String | default | 主题，可选值：primary / success / warning / danger |
| disabled | Boolean | false | 是否禁用 |
| underline | Boolean | true | 是否显示下划线 |
| hover | Boolean | false | 是否显示悬停效果 |
| icon | String | - | 图标名称 |
| icon-position | String | left | 图标位置，可选值：left / right |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| click | event | 点击事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |