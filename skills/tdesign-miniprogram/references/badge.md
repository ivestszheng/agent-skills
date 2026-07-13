# Badge 徽章

## 引入

```json
{
  "usingComponents": {
    "t-badge": "tdesign-miniprogram/badge/badge"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-badge count="9">消息</t-badge>
```

### 红点徽标

```xml
<t-badge dot>消息</t-badge>
<t-badge dot offset="[1, -1]">
  <t-icon name="notification" size="48rpx" />
</t-badge>
```

### 数字徽标

```xml
<t-badge count="8">消息</t-badge>
<t-badge count="99">消息</t-badge>
<t-badge count="100" max-count="99">消息</t-badge>
```

### 自定义徽标

```xml
<t-badge count="NEW">
  <t-button icon="notification" shape="square" size="large" />
</t-badge>
```

### 徽标形状

```xml
<t-badge count="2">圆形</t-badge>
<t-badge count="2" shape="square">方形</t-badge>
<t-badge count="2" shape="bubble">气泡</t-badge>
```

### 角标

```xml
<t-cell title="标题">
  <t-badge count="NEW" shape="ribbon-left" slot="note" />
</t-cell>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| count | String / Number | 0 | 徽标内容 |
| dot | Boolean | false | 是否红点 |
| max-count | Number | 99 | 封顶数字 |
| offset | Array | - | 位置偏移 |
| shape | String | circle | 形状，可选值：circle / square / bubble / ribbon / ribbon-right / ribbon-left / triangle-right / triangle-left |
| show-zero | Boolean | false | 是否显示零值 |
| size | String | medium | 尺寸，可选值：medium / large |

### Slots

| 名称 | 说明 |
|------|------|
| - | 默认插槽，徽标包裹内容 |
| count | 徽标内容插槽 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |
| t-class-content | 内容样式类 |
| t-class-count | 计数样式类 |