<!--
  文件名: chat-sender-example-upload.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-sender#上传文件
  场景: 上传文件
  描述: 演示附件上传功能，包含上传面板、文件列表管理。
  依赖组件: t-chat-sender, t-icon, t-navbar, t-toast
  关键特性: 附件上传, upload预设按钮, 文件列表管理, attachmentsProps
-->

# ChatSender 代码演示-上传文件

```wxml
<view class="demo-attachments-container {{showUploadMenu ? 'show-upload-menu' : ''}}">
  <view class="chat-sender-demo-wrapper">
    <view class="chat-sender-height-limit">
      <view class="chat-sender-height-left-limit"> </view>
      <view class="chat-sender-height-right-limit"> </view>
    </view>
    <view class="chat-sender-placeholder"> 高度限制：最大高度为132px </view>
    <view class="chat-sender-wrapper" style="{{showUploadMenu ? 'bottom:32rpx;' : ''}}">
      <t-chat-sender
        value="{{value}}"
        loading="{{loading}}"
        disabled="{{disabled}}"
        placeholder="{{placeholder}}"
        textareaProps="{{textareaProps}}"
        fileList="{{fileList}}"
        attachmentsProps="{{attachmentsProps}}"
        renderPresets="{{renderPresets}}"
        visible="{{visible}}"
        bind:send="onSend"
        bind:stop="onStop"
        bind:focus="onFocus"
        bind:blur="onBlur"
        bind:change="onChange"
        bind:uploadClick="onUploadClick"
        bind:fileClick="onFileClick"
        bind:fileDelete="onFileDelete"
        bind:fileChange="onFileChange"
        bind:fileSelect="onFileSelect"
        bind:updateVisible="onUpdateVisible"
        bind:keyboardheightchange="onKeyboardHeightChange"
      >
        <view slot="footer-prefix" class="demo-footer-prefix">
          <view class="deep-think-block {{deepThinkActive ? 'active' : ''}}" bind:tap="onDeepThinkTap">
            <t-icon name="system-sum" size="36rpx" />
            <text class="deep-think-text">深度思考</text>
          </view>
          <view class="net-search-block {{ netSearchActive ? 'active' : '' }}" bind:tap="onNetSearchTap">
            <t-icon name="internet" size="36rpx" />
          </view>
        </view>
      </t-chat-sender>
    </view>
    <view wx:if="{{!visible}}" class="demo-attachments-footer"> 内容由AI生成，仅供参考 </view>
  </view>
</view>
<t-toast id="t-toast" />
```

```js
import Toast from 'tdesign-miniprogram/toast';

Page({
  data: {
    value: '',
    loading: false,
    disabled: false,
    fileList: [
      {
        fileType: 'image',
        name: '图片1.png',
        url: 'https://tdesign.gtimg.com/site/square.png',
      },
      {
        fileType: 'pdf',
        name: '文档.pdf',
        url: 'https://example.com/document.pdf',
        size: 3072,
        status: 'pending',
      },
    ],
    visible: true,
    placeholder: '请输入消息...',
    textareaProps: {
      autosize: {
        maxHeight: 264,
        minHeight: 48, // 设置为0时，用自动计算height的高度
      }, // 默认为false
    },
    attachmentsProps: {
      items: [
        {
          fileType: 'image',
          name: '图片1.png',
          url: 'https://tdesign.gtimg.com/site/square.png',
        },
        {
          fileType: 'pdf',
          name: '文档.pdf',
          url: 'https://example.com/document.pdf',
          size: 3072,
          status: 'pending',
        },
      ],
      removable: true,
      imageViewer: true,
    },
    renderPresets: [
      {
        name: 'upload',
        presets: ['uploadCamera', 'uploadImage', 'uploadAttachment'],
        type: 'bottom',
        status: '',
      },
      {
        name: 'send',
        type: 'icon',
      },
    ],
    deepThinkActive: false,
    netSearchActive: false,
    showUploadMenu: true,
  },

  // 发送消息
  onSend(e) {
    const { value } = e.detail;
    console.log('发送消息:', value);

    if (!value.trim()) {
      wx.showToast({
        title: '请输入消息内容',
        icon: 'none',
      });
      return;
    }

    // 模拟发送状态
    this.setData({ loading: true });

    setTimeout(() => {
      if (this.data.loading) {
        this.setData({
          loading: false,
          value: '', // 清空输入框
        });
        wx.showToast({
          title: '发送成功',
          icon: 'success',
        });
      }
    }, 3000);
  },

  // 停止发送
  onStop(e) {
    const { value } = e.detail;
    console.log('停止发送:', value);

    this.setData({ loading: false });
    wx.showToast({
      title: '已停止发送',
      icon: 'none',
    });
  },

  // 输入框聚焦
  onFocus(e) {
    const { value, context } = e.detail;
    console.log('输入框聚焦:', value, context);
  },

  // 输入框失焦
  onBlur(e) {
    const { value, context } = e.detail;
    console.log('输入框失焦:', value, context);
  },

  // 输入内容变化
  onChange(e) {
    const { value } = e.detail;
    console.log('输入内容变化:', value);
    this.setData({ value });
  },

  // 点击上传按钮
  onUploadClick() {
    console.log('点击上传按钮');
  },

  // 点击文件
  onFileClick(e) {
    const { file } = e.detail;
    console.log('点击文件:', file);
    wx.showToast({
      title: `点击了文件: ${file.name}`,
      icon: 'none',
    });
  },

  // 删除文件
  onFileDelete(e) {
    const { file } = e.detail;
    console.log('删除文件:', file);
    wx.showToast({
      title: '文件删除成功',
      icon: 'success',
    });
  },

  // 文件列表变化
  onFileChange(e) {
    const { files } = e.detail;
    console.log('文件列表变化:', files);
    this.setData({ attachmentsProps: { ...this.data.attachmentsProps, items: files } });
    this.setData({ fileList: files });
  },

  // 选择文件
  onFileSelect(e) {
    const { name, files } = e.detail;
    console.log('选择文件:', name, files);

    wx.showToast({
      title: `选择了${files.length}个文件`,
      icon: 'success',
    });
  },

  // 上传面板显示状态变化
  onUpdateVisible() {
    Toast({
      context: this,
      selector: '#t-toast',
      message: '暂不可操作',
    });
  },

  // 键盘高度变化
  onKeyboardHeightChange(e) {
    console.log('键盘高度变化:', e.detail);
  },

  // 切换禁用状态
  toggleDisabled() {
    this.setData({ disabled: !this.data.disabled });
  },

  // 切换加载状态
  toggleLoading() {
    this.setData({ loading: !this.data.loading });
  },

  // 清空输入框
  clearInput() {
    this.setData({ value: '' });
  },

  onDeepThinkTap() {
    this.setData({ deepThinkActive: !this.data.deepThinkActive });
  },

  onNetSearchTap() {
    this.setData({ netSearchActive: !this.data.netSearchActive });
  },
});
```

```css
.demo-attachments-container {
  padding: 56rpx 0 0 0;
  background-color: var(--td-bg-color-container);
  height: 608rpx;
  position: relative;
  transition: all 0.3s;
}

.show-upload-menu {
  height: 780rpx;
}

.demo-attachments-footer {
  height: 32rpx;
  width: 100%;
  text-align: center;
  font-size: 20rpx;
  line-height: 32rpx;
  color: rgba(0, 0, 0, 0.4);
  position: absolute;
  bottom: 32rpx;
}

/* 聊天发送器包装器 */
.chat-sender-wrapper {
  /* border: 2rpx solid #e5e5e5; */
  border-radius: 8rpx;
  overflow: hidden;
  background-color: var(--td-bg-color-container);
}

.demo-footer-prefix {
  display: flex;
  align-items: center;
}

.deep-think-block {
  padding: 0 24rpx;
  height: 60rpx;
  margin-right: 16rpx;
}

.deep-think-text {
  margin-left: 8rpx;
}

.deep-think-block,
.net-search-block {
  color: var(--td-text-color-primary);
  border-radius: 200rpx;
  border: 2rpx solid var(--td-component-border);
  display: flex;
  justify-content: center;
  align-items: center;
}

.net-search-block {
  width: 64rpx;
  height: 60rpx;
}

.active {
  border-color: var(--td-brand-color-light-active);
  color: var(--td-brand-color);
  background-color: var(--td-brand-color-light);
}
```

```json
{
  "component": true,
  "styleIsolation": "shared",
  "usingComponents": {
    "t-icon": "tdesign-miniprogram/icon/icon",
    "t-navbar": "tdesign-miniprogram/navbar/navbar",
    "t-chat-sender": "tdesign-miniprogram/chat-sender/chat-sender",
    "t-toast": "tdesign-miniprogram/toast/toast"
  }
}
```