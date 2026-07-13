# Icon 图标

## 引入

```json
{
  "usingComponents": {
    "t-icon": "tdesign-miniprogram/icon/icon"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-icon name="notification" />
<t-icon name="arrow-right" />
<t-icon name="user" />
```

### 图标尺寸

```xml
<t-icon name="notification" size="small" />
<t-icon name="notification" size="medium" />
<t-icon name="notification" size="large" />
<t-icon name="notification" size="48" />
```

### 图标颜色

```xml
<t-icon name="notification" color="#1677ff" />
<t-icon name="notification" color="#ff4d4f" />
<t-icon name="notification" color="#52c41a" />
```

### 自定义图标

```xml
<t-icon prefix-class="my-icon" name="custom-icon" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| name | String | - | 图标名称 |
| size | String / Number | medium | 图标尺寸，可选值：small / medium / large 或数字 |
| color | String | - | 图标颜色 |
| prefix-class | String | t-icon | 图标前缀类名 |
| aria-label | String | - | 无障碍标签 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |