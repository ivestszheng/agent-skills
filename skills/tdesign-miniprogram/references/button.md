# Button 按钮

## 引入

```json
{
  "usingComponents": {
    "t-button": "tdesign-miniprogram/button/button"
  }
}
```

## 代码演示

### 按钮类型

```xml
<t-button theme="primary">主要按钮</t-button>
<t-button theme="default">默认按钮</t-button>
<t-button theme="danger">危险按钮</t-button>
<t-button theme="light">浅色按钮</t-button>
```

### 按钮尺寸

```xml
<t-button size="large">大尺寸</t-button>
<t-button size="medium">中尺寸</t-button>
<t-button size="small">小尺寸</t-button>
```

### 按钮状态

```xml
<t-button disabled>禁用状态</t-button>
<t-button loading>加载状态</t-button>
<t-button ghost>幽灵按钮</t-button>
```

### 图标按钮

```xml
<t-button icon="arrow-right">带图标</t-button>
<t-button icon="arrow-right" icon-position="right">图标在右</t-button>
<t-button icon="notification" shape="circle">圆形图标</t-button>
<t-button icon="notification" shape="square">方形图标</t-button>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| theme | String | default | 主题，可选值：primary / default / danger / light |
| size | String | medium | 尺寸，可选值：large / medium / small |
| shape | String | - | 形状，可选值：circle / square |
| icon | String | - | 图标名称 |
| icon-position | String | left | 图标位置，可选值：left / right |
| loading | Boolean | false | 是否加载中 |
| disabled | Boolean | false | 是否禁用 |
| ghost | Boolean | false | 是否幽灵按钮 |
| block | Boolean | false | 是否块级显示 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| click | event | 点击事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |
| t-class-content | 内容样式类 |