# Grid 宫格

## 引入

```json
{
  "usingComponents": {
    "t-grid": "tdesign-miniprogram/grid/grid",
    "t-grid-item": "tdesign-miniprogram/grid/grid-item"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-grid>
  <t-grid-item icon="home" label="首页" />
  <t-grid-item icon="category" label="分类" />
  <t-grid-item icon="cart" label="购物车" />
  <t-grid-item icon="user" label="我的" />
</t-grid>
```

### 列数

```xml
<t-grid column-num="3">
  <t-grid-item icon="home" label="首页" />
  <t-grid-item icon="category" label="分类" />
  <t-grid-item icon="cart" label="购物车" />
  <t-grid-item icon="user" label="我的" />
  <t-grid-item icon="message" label="消息" />
  <t-grid-item icon="settings" label="设置" />
</t-grid>
```

### 间距

```xml
<t-grid column-num="4" gutter="16">
  <t-grid-item icon="home" label="首页" />
  <t-grid-item icon="category" label="分类" />
  <t-grid-item icon="cart" label="购物车" />
  <t-grid-item icon="user" label="我的" />
</t-grid>
```

### 边框

```xml
<t-grid column-num="4" bordered>
  <t-grid-item icon="home" label="首页" />
  <t-grid-item icon="category" label="分类" />
  <t-grid-item icon="cart" label="购物车" />
  <t-grid-item icon="user" label="我的" />
</t-grid>
```

### 自定义内容

```xml
<t-grid column-num="4">
  <t-grid-item>
    <view class="custom-content">自定义</view>
  </t-grid-item>
  <t-grid-item>
    <view class="custom-content">内容</view>
  </t-grid-item>
</t-grid>
```

## API

### Grid Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| column-num | Number | 4 | 列数 |
| gutter | Number | 0 | 间距 |
| bordered | Boolean | false | 是否显示边框 |

### GridItem Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| icon | String | - | 图标名称 |
| label | String | - | 标签文本 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| click | - | 点击事件 |

### Slots

| 名称 | 说明 |
|------|------|
| - | 默认插槽，自定义内容 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |