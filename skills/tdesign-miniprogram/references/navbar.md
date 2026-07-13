# Navbar 导航条

## 引入

```json
{
  "usingComponents": {
    "t-navbar": "tdesign-miniprogram/navbar/navbar"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-navbar title="标题" />
```

### 带返回按钮

```xml
<t-navbar title="标题" left-icon="arrow-left" bind:left-click="onBack" />
```

### 带右侧按钮

```xml
<t-navbar 
  title="标题" 
  right-icon="more" 
  bind:right-click="onMore" 
/>
```

### 自定义左右内容

```xml
<t-navbar title="标题">
  <view slot="left">自定义左侧</view>
  <view slot="right">自定义右侧</view>
</t-navbar>
```

### 导航栏类型

```xml
<t-navbar title="浅色背景" />
<t-navbar title="透明背景" transparent />
<t-navbar title="深色背景" dark />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | String | - | 标题 |
| left-icon | String | - | 左侧图标 |
| right-icon | String | - | 右侧图标 |
| left-text | String | - | 左侧文字 |
| right-text | String | - | 右侧文字 |
| transparent | Boolean | false | 是否透明背景 |
| dark | Boolean | false | 是否深色背景 |
| fixed | Boolean | false | 是否固定顶部 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| left-click | event | 左侧点击事件 |
| right-click | event | 右侧点击事件 |

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