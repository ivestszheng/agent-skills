# Empty 空状态

## 引入

```json
{
  "usingComponents": {
    "t-empty": "tdesign-miniprogram/empty/empty"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-empty />
```

### 自定义文案

```xml
<t-empty text="暂无数据" />
<t-empty text="暂无数据" sub-text="点击添加" />
```

### 自定义图标

```xml
<t-empty icon="search" text="未找到结果" />
```

### 自定义内容

```xml
<t-empty>
  <view>自定义空状态内容</view>
  <t-button theme="primary" size="small">去添加</t-button>
</t-empty>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| icon | String | empty | 图标名称 |
| text | String | 暂无数据 | 主文案 |
| sub-text | String | - | 副文案 |

### Slots

| 名称 | 说明 |
|------|------|
| - | 默认插槽，自定义内容 |
| icon | 图标自定义 |
| text | 文案自定义 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |