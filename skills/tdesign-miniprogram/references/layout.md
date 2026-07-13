# Layout 布局

## 引入

```json
{
  "usingComponents": {
    "t-row": "tdesign-miniprogram/layout/row",
    "t-col": "tdesign-miniprogram/layout/col"
  }
}
```

## 代码演示

### 基础布局

```xml
<t-row>
  <t-col span="8">1/3</t-col>
  <t-col span="8">1/3</t-col>
  <t-col span="8">1/3</t-col>
</t-row>
```

### 间距

```xml
<t-row gutter="16">
  <t-col span="8">间距 16</t-col>
  <t-col span="8">间距 16</t-col>
  <t-col span="8">间距 16</t-col>
</t-row>
```

### 对齐方式

```xml
<t-row justify="center">
  <t-col span="6">居中</t-col>
  <t-col span="6">居中</t-col>
</t-row>

<t-row justify="space-between">
  <t-col span="6">两端对齐</t-col>
  <t-col span="6">两端对齐</t-col>
</t-row>

<t-row align="middle">
  <t-col span="6">垂直居中</t-col>
  <t-col span="12">垂直居中</t-col>
</t-row>
```

### 响应式布局

```xml
<t-row>
  <t-col span="24" sm="12" md="8" lg="6">响应式</t-col>
  <t-col span="24" sm="12" md="8" lg="6">响应式</t-col>
  <t-col span="24" sm="12" md="8" lg="6">响应式</t-col>
</t-row>
```

## API

### Row Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| gutter | Number | 0 | 列间距 |
| justify | String | left | 水平对齐方式，可选值：left / right / center / space-around / space-between |
| align | String | top | 垂直对齐方式，可选值：top / middle / bottom |

### Col Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| span | Number | 24 | 列宽度 |
| offset | Number | 0 | 偏移量 |
| sm | Number | - | 小屏幕宽度 |
| md | Number | - | 中屏幕宽度 |
| lg | Number | - | 大屏幕宽度 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |