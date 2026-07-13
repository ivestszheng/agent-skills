# Drawer 抽屉

## 引入

```json
{
  "usingComponents": {
    "t-drawer": "tdesign-miniprogram/drawer/drawer"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-drawer visible="{{visible}}" bind:close="onClose">
  <view>抽屉内容</view>
</t-drawer>
```

```javascript
Page({
  data: {
    visible: false
  },
  onOpen() {
    this.setData({ visible: true });
  },
  onClose() {
    this.setData({ visible: false });
  }
});
```

### 抽屉位置

```xml
<t-drawer visible="{{visible}}" placement="left">左侧抽屉</t-drawer>
<t-drawer visible="{{visible}}" placement="right">右侧抽屉</t-drawer>
<t-drawer visible="{{visible}}" placement="top">顶部抽屉</t-drawer>
<t-drawer visible="{{visible}}" placement="bottom">底部抽屉</t-drawer>
```

### 抽屉尺寸

```xml
<t-drawer visible="{{visible}}" size="small">小尺寸</t-drawer>
<t-drawer visible="{{visible}}" size="medium">中尺寸</t-drawer>
<t-drawer visible="{{visible}}" size="large">大尺寸</t-drawer>
<t-drawer visible="{{visible}}" size="50%">自定义尺寸</t-drawer>
```

### 带标题抽屉

```xml
<t-drawer visible="{{visible}}" title="抽屉标题" bind:close="onClose">
  <view>抽屉内容</view>
</t-drawer>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| visible | Boolean | false | 是否显示 |
| title | String | - | 标题 |
| placement | String | right | 位置，可选值：left / right / top / bottom |
| size | String | medium | 尺寸，可选值：small / medium / large 或百分比 |
| mask | Boolean | true | 是否显示遮罩 |
| mask-closable | Boolean | true | 点击遮罩是否关闭 |
| closable | Boolean | true | 是否显示关闭按钮 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| close | - | 关闭事件 |
| open | - | 打开事件 |

### Slots

| 名称 | 说明 |
|------|------|
| - | 默认插槽，抽屉内容 |
| title | 标题自定义内容 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |