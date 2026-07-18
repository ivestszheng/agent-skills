<!--
  文件名: attachments-example-file-loading.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/attachments#文件类型加载状态
  场景: 文件类型加载状态
  描述: 演示文件类型附件上传中的加载状态（status: pending）。
  依赖组件: t-attachments
  关键特性: 文件加载状态, status:pending, 文件类型附件
-->

# Attachments 代码演示-文件类型加载状态

```wxml
<view class="chat-example">
  <view class="chat-example-block">
    <t-attachments items="{{items}}" bind:fileClick="onFileClick" bind:remove="onRemove" bind:add="onAdd" />
  </view>
</view>
```

```js
Page({
  data: {
    items: [
      {
        fileType: 'doc',
        name: 'word-file.doc',
        url: 'https://example.com/word-file.doc',
        size: 222859,
        status: 'pending',
      },
    ],
  },

  onFileClick(e) {
    const { item } = e.detail;
    console.log('点击文件:', item);
    wx.showToast({
      title: `点击了${item.name}`,
      icon: 'none',
    });
  },

  onRemove(e) {
    const { item, index } = e.detail;
    console.log('删除文件:', e, item, '索引:', index);

    // 从列表中移除文件
    const newItems = [...this.data.items];
    newItems.splice(index, 1);

    this.setData({
      items: newItems,
    });

    wx.showToast({
      title: '删除成功',
      icon: 'success',
    });
  },

  onAdd() {
    console.log('点击添加按钮');
    wx.showToast({
      title: '点击了添加按钮',
      icon: 'none',
    });

    // 模拟添加新文件
    const newFile = {
      fileType: 'txt',
      name: `新文件${this.data.items.length + 1}.txt`,
      url: 'https://example.com/newfile.txt',
      size: 256,
      status: 'success',
    };

    this.setData({
      items: [...this.data.items, newFile],
    });
  },
});
```

```css
.chat-example-block {
  padding: 32rpx;
  background-color: var(--td-bg-color-container);
}
```

```json
{
  "usingComponents": {
    "t-attachments": "tdesign-miniprogram/attachments/attachments"
  }
}
```