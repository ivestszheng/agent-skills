# Cell 单元格

## 引入

```json
{
  "usingComponents": {
    "t-cell": "tdesign-miniprogram/cell/cell",
    "t-cell-group": "tdesign-miniprogram/cell-group/cell-group"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-cell-group>
  <t-cell title="标题" />
  <t-cell title="标题" sub-title="副标题" />
  <t-cell title="标题" right-icon="arrow-right" />
</t-cell-group>
```

### 带左侧图标

```xml
<t-cell-group>
  <t-cell title="标题" left-icon="user" />
  <t-cell title="标题" left-icon="phone" />
  <t-cell title="标题" left-icon="email" />
</t-cell-group>
```

### 带右侧内容

```xml
<t-cell-group>
  <t-cell title="姓名" value="张三" />
  <t-cell title="手机号" value="13800138000" />
  <t-cell title="邮箱" value="zhangsan@example.com" />
</t-cell-group>
```

### 自定义内容

```xml
<t-cell-group>
  <t-cell title="自定义右侧">
    <view slot="right">自定义内容</view>
  </t-cell>
</t-cell-group>
```

### 禁用状态

```xml
<t-cell-group>
  <t-cell title="禁用单元格" disabled />
</t-cell-group>
```

## API

### CellGroup Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| bordered | Boolean | true | 是否显示边框 |

### Cell Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | String | - | 标题 |
| sub-title | String | - | 副标题 |
| value | String | - | 右侧值 |
| left-icon | String | - | 左侧图标 |
| right-icon | String | - | 右侧图标 |
| disabled | Boolean | false | 是否禁用 |
| arrow | Boolean | false | 是否显示箭头 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| click | - | 点击事件 |

### Slots

| 名称 | 说明 |
|------|------|
| left | 左侧自定义内容 |
| right | 右侧自定义内容 |
| title | 标题自定义内容 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |