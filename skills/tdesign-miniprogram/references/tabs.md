# Tabs 选项卡

## 引入

```json
{
  "usingComponents": {
    "t-tabs": "tdesign-miniprogram/tabs/tabs",
    "t-tab-panel": "tdesign-miniprogram/tabs/tab-panel"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-tabs value="{{activeTab}}" bind:change="onTabChange">
  <t-tab-panel label="标签一" value="1">内容一</t-tab-panel>
  <t-tab-panel label="标签二" value="2">内容二</t-tab-panel>
  <t-tab-panel label="标签三" value="3">内容三</t-tab-panel>
</t-tabs>
```

```javascript
Page({
  data: {
    activeTab: '1'
  },
  onTabChange(e) {
    this.setData({
      activeTab: e.detail.value
    });
  }
});
```

### 标签位置

```xml
<t-tabs value="{{activeTab}}" placement="top">顶部标签</t-tabs>
<t-tabs value="{{activeTab}}" placement="bottom">底部标签</t-tabs>
<t-tabs value="{{activeTab}}" placement="left">左侧标签</t-tabs>
<t-tabs value="{{activeTab}}" placement="right">右侧标签</t-tabs>
```

### 标签样式

```xml
<t-tabs value="{{activeTab}}" theme="card">卡片样式</t-tabs>
<t-tabs value="{{activeTab}}" theme="line">下划线样式</t-tabs>
```

### 图标标签

```xml
<t-tabs value="{{activeTab}}">
  <t-tab-panel label="首页" value="1" icon="home">首页内容</t-tab-panel>
  <t-tab-panel label="分类" value="2" icon="category">分类内容</t-tab-panel>
  <t-tab-panel label="我的" value="3" icon="user">我的内容</t-tab-panel>
</t-tabs>
```

## API

### Tabs Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String / Number | - | 当前激活标签值 |
| placement | String | top | 标签位置，可选值：top / bottom / left / right |
| theme | String | line | 标签样式，可选值：line / card |
| swipeable | Boolean | false | 是否可滑动切换 |

### TabPanel Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| label | String | - | 标签文本 |
| value | String / Number | - | 标签值 |
| icon | String | - | 图标名称 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 标签切换事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |