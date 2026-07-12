# Attachments 文件附件

聊天消息中的文件附件展示组件，支持图片、文档、视频等多种文件类型。

## 引入

```json
{
  "usingComponents": {
    "t-attachments": "tdesign-miniprogram/attachments/attachments"
  }
}
```

## Props

| 名称 | 类型 | 默认值 | 说明 | 必传 |
|------|------|--------|------|------|
| `items` | Array | `[]` | 附件列表（FileItem[]） | **Y** |
| `image-viewer` | Boolean | `true` | 是否启用图片预览功能 | N |

### FileItem 类型

```typescript
interface FileItem {
  fileType: 'image' | 'video' | 'audio' | 'pdf' | 'doc' | 'ppt' | 'txt';
  name: string;       // 文件名
  url: string;        // 文件 URL
  size: number;       // 文件大小（字节）
  status?: 'success' | 'fail' | 'pending' | 'error';  // 上传状态
  progress?: number;  // 上传进度（0-100）
}
```

## 事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `bind:fileClick` | 点击文件 | `{ item: FileItem }` |
| `bind:remove` | 删除文件 | `{ item: FileItem, index: number }` |
| `bind:add` | 点击添加按钮 | - |

## 图片类型

```xml
<t-attachments
  items="{{items}}"
  bind:fileClick="onFileClick"
  bind:remove="onRemove"
  bind:add="onAdd"
/>
```

```javascript
Page({
  data: {
    items: [
      {
        fileType: 'image',
        name: 'sample-image.jpg',
        url: 'https://tdesign.gtimg.com/site/avatar.jpg',
        size: 1024,
        status: 'success',
      },
    ],
  },
  onFileClick(e) {
    const { item } = e.detail;
    wx.showToast({ title: `点击了${item.name}`, icon: 'none' });
  },
  onRemove(e) {
    const { index } = e.detail;
    const newItems = [...this.data.items];
    newItems.splice(index, 1);
    this.setData({ items: newItems });
  },
  onAdd() {
    wx.chooseImage({
      count: 1,
      success: (res) => {
        const newFile = {
          fileType: 'image',
          name: res.tempFiles[0].path.split('/').pop(),
          url: res.tempFilePaths[0],
          size: res.tempFiles[0].size,
          status: 'success',
        };
        this.setData({ items: [...this.data.items, newFile] });
      },
    });
  },
});
```

## 文件类型

支持 doc、excel、pdf、ppt、video、audio、txt 等类型，自动显示对应图标：

```javascript
data: {
  items: [
    { fileType: 'doc', name: 'word-file.doc', url: '...', size: 222859, status: 'success' },
    { fileType: 'excel', name: 'excel-file.xlsx', url: '...', size: 222859, status: 'success' },
    { fileType: 'pdf', name: 'pdf-file.pdf', url: '...', size: 222859, status: 'success' },
    { fileType: 'ppt', name: 'ppt-file.pptx', url: '...', size: 222859, status: 'success' },
    { fileType: 'video', name: 'video-file.mp4', url: '...', size: 222859, status: 'success' },
  ],
}
```

## 加载状态

通过 `status` 字段控制附件的显示状态：

- `pending`：上传中，显示加载动画
- `success`：上传成功
- `fail` / `error`：上传失败

```javascript
{ fileType: 'image', name: 'uploading.jpg', url: '...', size: 1024, status: 'pending' }
```
