# SideBar 侧边导航栏

## 引入

```json
{
  "usingComponents": {
    "t-side-bar": "tdesign-miniprogram/side-bar/side-bar",
    "t-side-bar-item": "tdesign-miniprogram/side-bar/side-bar-item"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-side-bar value="{{active}}" bind:change="onChange">
  <t-side-bar-item label="菜单一" value="1" />
  <t-side-bar-item label="菜单二" value="2" />
  <t-side-bar-item label="菜单三" value="3" />
</t-side-bar>
```

```javascript
Page({
  data: {
    active: '1'
  },
  onChange(e) {
    this.setData({ active: e.detail.value });
  }
});
```

### 带图标侧边栏

```xml
<t-side-bar value="{{active}}">
  <t-side-bar-item label="首页" value="1" icon="home" />
  <t-side-bar-item label="分类" value="2" icon="category" />
  <t-side-bar-item label="购物车" value="3" icon="cart" />
  <t-side-bar-item label="我的" value="4" icon="user" />
</t-side-bar>
```

### 禁用状态

```xml
<t-side-bar value="{{active}}">
  <t-side-bar-item label="菜单一" value="1" />
  <t-side-bar-item label="菜单二" value="2" disabled />
  <t-side-bar-item label="菜单三" value="3" />
</t-side-bar>
```

## API

### SideBar Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String / Number | - | 当前激活值 |

### SideBarItem Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| label | String | - | 标签文本 |
| value | String / Number | - | 标签值 |
| icon | String | - | 图标名称 |
| disabled | Boolean | false | 是否禁用 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 切换事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |