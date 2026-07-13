# ImageViewer 图片预览

## 引入

```json
{
  "usingComponents": {
    "t-image-viewer": "tdesign-miniprogram/image-viewer/image-viewer"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-image-viewer 
  visible="{{visible}}" 
  images="{{images}}" 
  current="{{current}}" 
  bind:close="onClose" 
/>
```

```javascript
Page({
  data: {
    visible: false,
    current: 0,
    images: [
      'https://example.com/image1.png',
      'https://example.com/image2.png',
      'https://example.com/image3.png'
    ]
  },
  onOpen() {
    this.setData({ visible: true });
  },
  onClose() {
    this.setData({ visible: false });
  }
});
```

### 同步关闭

```xml
<t-image-viewer 
  visible="{{visible}}" 
  images="{{images}}" 
  bind:close="onClose" 
  bind:change="onChange" 
/>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| visible | Boolean | false | 是否显示 |
| images | Array | [] | 图片列表 |
| current | Number | 0 | 当前索引 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| close | - | 关闭事件 |
| change | { current } | 切换事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |