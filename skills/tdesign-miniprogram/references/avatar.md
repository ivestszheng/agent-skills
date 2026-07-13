# Avatar 头像

## 引入

```json
{
  "usingComponents": {
    "t-avatar": "tdesign-miniprogram/avatar/avatar"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-avatar icon="user" />
<t-avatar src="https://example.com/avatar.png" />
```

### 头像尺寸

```xml
<t-avatar icon="user" size="small" />
<t-avatar icon="user" size="medium" />
<t-avatar icon="user" size="large" />
```

### 头像形状

```xml
<t-avatar icon="user" shape="circle" />
<t-avatar icon="user" shape="square" />
```

### 文本头像

```xml
<t-avatar text="张三" />
<t-avatar text="张" />
```

### 头像状态

```xml
<t-avatar icon="user" status="online" />
<t-avatar icon="user" status="offline" />
<t-avatar icon="user" status="busy" />
<t-avatar icon="user" status="leave" />
```

### 头像徽标

```xml
<t-avatar icon="user" badge-props="{{{ count: 9 }}}" />
<t-avatar icon="user" badge-props="{{{ dot: true }}}" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| icon | String | - | 图标名称 |
| src | String | - | 图片地址 |
| text | String | - | 文本内容 |
| size | String | medium | 尺寸，可选值：small / medium / large |
| shape | String | circle | 形状，可选值：circle / square |
| status | String | - | 状态，可选值：online / offline / busy / leave |
| badge-props | Object | - | 徽标配置 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |