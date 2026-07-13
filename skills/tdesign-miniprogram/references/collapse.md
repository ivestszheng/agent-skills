# Collapse 折叠面板

## 引入

```json
{
  "usingComponents": {
    "t-collapse": "tdesign-miniprogram/collapse/collapse",
    "t-collapse-panel": "tdesign-miniprogram/collapse/collapse-panel"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-collapse value="{{value}}" bind:change="onChange">
  <t-collapse-panel title="面板一" value="1">
    面板一内容
  </t-collapse-panel>
  <t-collapse-panel title="面板二" value="2">
    面板二内容
  </t-collapse-panel>
  <t-collapse-panel title="面板三" value="3">
    面板三内容
  </t-collapse-panel>
</t-collapse>
```

```javascript
Page({
  data: {
    value: ['1']
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 手风琴模式

```xml
<t-collapse value="{{value}}" accordion bind:change="onChange">
  <t-collapse-panel title="面板一" value="1">面板一内容</t-collapse-panel>
  <t-collapse-panel title="面板二" value="2">面板二内容</t-collapse-panel>
  <t-collapse-panel title="面板三" value="3">面板三内容</t-collapse-panel>
</t-collapse>
```

### 默认展开

```xml
<t-collapse value="{{['1', '2']}}">
  <t-collapse-panel title="面板一" value="1">面板一内容</t-collapse-panel>
  <t-collapse-panel title="面板二" value="2">面板二内容</t-collapse-panel>
  <t-collapse-panel title="面板三" value="3">面板三内容</t-collapse-panel>
</t-collapse>
```

### 禁用状态

```xml
<t-collapse value="{{value}}">
  <t-collapse-panel title="面板一" value="1">面板一内容</t-collapse-panel>
  <t-collapse-panel title="面板二" value="2" disabled>面板二内容</t-collapse-panel>
  <t-collapse-panel title="面板三" value="3">面板三内容</t-collapse-panel>
</t-collapse>
```

## API

### Collapse Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Array | [] | 当前展开值 |
| accordion | Boolean | false | 是否手风琴模式 |

### CollapsePanel Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | String | - | 标题 |
| value | String / Number | - | 值 |
| disabled | Boolean | false | 是否禁用 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |