<!--
  文件名: attachments-example-file.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/attachments#文件类型
  场景: 文件类型
  描述: 演示多种文件类型附件的展示（doc、excel、pdf、ppt、video 等）。
  依赖组件: t-attachments
  关键特性: 文件类型, doc/excel/pdf/ppt/video, 文件图标
-->

# Attachments 代码演示-文件类型

```wxml
<view class="chat-example">
  <!-- 有效的示例，呈现效果为 单行滚动 -->
  <!-- <view class="chat-example-block">
    <t-attachments items="{{items}}" bind:fileClick="onFileClick" bind:remove="onRemove" bind:add="onAdd" />
  </view> -->

  <view class="chat-example-block" wx:for="{{items}}" wx:for-item="item" wx:key="url">
    <t-attachments items="{{[item]}}" bind:fileClick="onFileClick" bind:remove="onRemove" bind:add="onAdd" />
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
        status: 'success',
      },
      {
        fileType: 'excel',
        name: 'excel-file.xlsx',
        url: 'https://example.com/excel-file.xlsx',
        size: 222859,
        status: 'success',
      },
      {
        fileType: 'pdf',
        name: 'pdf-file.pdf',
        url: 'https://example.com/pdf-file.pdf',
        size: 222859,
        status: 'success',
      },
      {
        fileType: 'ppt',
        name: 'ppt-file.pptx',
        url: 'https://example.com/ppt-file.pptx',
        size: 222859,
        status: 'success',
      },
      {
        fileType: 'video',
        name: 'video-file.mp4',
        url: 'https://example.com/video-file.mp4',
        size: 222859,
        status: 'success',
      },
      {
        fileType: 'file',
        name: 'file',
        url: 'https://example.com/audio-file.mp3',
        size: 222859,
        status: 'success',
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
.chat-example {
  padding: 32rpx;
  box-sizing: border-box;
  background-color: var(--td-bg-color-container);
}

.chat-example-block {
  display: inline-flex;
  width: 336rpx;
  margin-bottom: 26rpx;
}
```

```json
{
  "styleIsolation": "isolated",
  "usingComponents": {
    "t-attachments": "tdesign-miniprogram/attachments/attachments"
  }
}
```