# Upload 上传

## 引入

```json
{
  "usingComponents": {
    "t-upload": "tdesign-miniprogram/upload/upload"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-upload 
  file-list="{{fileList}}" 
  bind:change="onChange" 
/>
```

```javascript
Page({
  data: {
    fileList: []
  },
  onChange(e) {
    this.setData({ fileList: e.detail.fileList });
  }
});
```

### 限制数量

```xml
<t-upload 
  file-list="{{fileList}}" 
  max-count="3" 
  bind:change="onChange" 
/>
```

### 限制类型

```xml
<t-upload 
  file-list="{{fileList}}" 
  accept="image" 
  bind:change="onChange" 
/>
```

### 预览功能

```xml
<t-upload 
  file-list="{{fileList}}" 
  preview 
  bind:change="onChange" 
/>
```

### 删除功能

```xml
<t-upload 
  file-list="{{fileList}}" 
  deletable 
  bind:change="onChange" 
/>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| file-list | Array | [] | 文件列表 |
| accept | String | all | 接受类型，可选值：image / video / all |
| max-count | Number | 9 | 最大数量 |
| max-size | Number | 10 | 最大大小(MB) |
| preview | Boolean | false | 是否可预览 |
| deletable | Boolean | false | 是否可删除 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { fileList } | 文件变化事件 |
| upload | { file } | 上传事件 |
| delete | { file } | 删除事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |