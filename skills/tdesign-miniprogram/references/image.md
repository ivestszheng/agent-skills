# Image 图片

## 引入

```json
{
  "usingComponents": {
    "t-image": "tdesign-miniprogram/image/image"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-image src="https://example.com/image.png" />
```

### 图片模式

```xml
<t-image src="https://example.com/image.png" mode="aspectFill" />
<t-image src="https://example.com/image.png" mode="aspectFit" />
<t-image src="https://example.com/image.png" mode="widthFix" />
```

### 懒加载

```xml
<t-image src="https://example.com/image.png" lazy-load />
```

### 加载失败

```xml
<t-image src="https://example.com/image.png" error-icon="error" />
```

### 加载中

```xml
<t-image src="https://example.com/image.png" loading-icon="loading" />
```

### 圆角

```xml
<t-image src="https://example.com/image.png" radius="16" />
<t-image src="https://example.com/image.png" radius="round" />
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| src | String | - | 图片地址 |
| mode | String | aspectFill | 图片模式 |
| lazy-load | Boolean | false | 是否懒加载 |
| error-icon | String | - | 错误图标 |
| loading-icon | String | - | 加载中图标 |
| radius | String / Number | - | 圆角 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| load | - | 加载完成事件 |
| error | - | 加载失败事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |