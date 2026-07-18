<!--
  文件名: chat-sender-example-content-citation.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-sender#内容引用
  场景: 内容引用
  描述: 演示通过 header 插槽展示引用的文本内容。
  依赖组件: t-chat-sender, t-icon, t-navbar
  关键特性: header插槽, 文本内容引用, 关闭引用
-->

# ChatSender 代码演示-内容引用

```wxml
<view class="demo-content-citation-container">
  <view class="chat-sender-demo-wrapper">
    <view class="chat-sender-height-limit">
      <view class="chat-sender-height-left-limit"> </view>
      <view class="chat-sender-height-right-limit"> </view>
    </view>
    <view class="chat-sender-placeholder"> 高度限制：最大高度为132px </view>
    <view class="chat-sender-wrapper">
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
        <view slot="header" class="demo-header" wx:if="{{headerText}}">
          <view style="padding: 4rpx; height: 40rpx; color: var(--td-text-color-disabled)">
            <t-icon name="enter" size="40rpx" style="transform: scaleX(-1)" />
          </view>
          <view class="header-content"> {{headerText}} </view>
          <view style="padding: 4rpx; height: 40rpx; margin-left: auto; color: var(--td-text-color-placeholder)">
            <t-icon name="close" size="40rpx" bind:tap="handleCLoseCite" />
          </view>
        </view>
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
    <view class="demo-content-citation-footer"> 内容由AI生成，仅供参考 </view>
  </view>
</view>
```

```js
Page({
  data: {
    value: '',
    loading: false,
    disabled: false,
    fileList: [],
    visible: false,
    placeholder: '请输入消息...',
    textareaProps: {
      autosize: {
        maxHeight: 264,
        minHeight: 48, // 设置为0时，用自动计算height的高度
      }, // 默认为false
    },
    attachmentsProps: {
      items: [],
      removable: true,
      imageViewer: true,
    },
    renderPresets: [
      {
        name: 'send',
        type: 'icon',
      },
    ],
    deepThinkActive: false,
    netSearchActive: false,
    headerText:
      '牛顿第一定律并不适用于所有参考系，它只适用于惯性参考系。在质点不受外力作用时，能够判断出质点静止或作匀速直线运动的参考系一定是惯性参考系，因此只有在惯性参考系中牛顿第一定律才适用。',
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
    console.log(e, 'e----');

    const { files } = e.detail;
    console.log('文件列表变化:', files);
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
  onUpdateVisible(e) {
    const visible = e.detail;
    console.log('上传面板显示状态:', visible);
    this.setData({ visible });
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

  handleCLoseCite() {
    this.setData({ headerText: '' });
  },
});
```

```css
.demo-content-citation-container {
  padding: 56rpx 0 0 0;
  background-color: var(--td-bg-color-container);
  height: 568rpx;
  position: relative;
}

.demo-content-citation-footer {
  height: 32rpx;
  width: 100%;
  text-align: center;
  font-size: 20rpx;
  line-height: 32rpx;
  color: var(--td-text-color-placeholder);
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

.demo-header {
  display: flex;
  width: calc(100% - 48rpx);
  margin-left: 24rpx;
  height: 62rpx;
  border-bottom: 2rpx solid var(--td-component-stroke);
}

.header-content {
  padding: 2rpx 24rpx;
  box-sizing: border-box;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: var(--td-font-size-body-medium);
  line-height: 44rpx;
  color: var(--td-text-color-placeholder);
}
```

```json
{
  "component": true,
  "styleIsolation": "shared",
  "usingComponents": {
    "t-icon": "tdesign-miniprogram/icon/icon",
    "t-navbar": "tdesign-miniprogram/navbar/navbar",
    "t-chat-sender": "tdesign-miniprogram/chat-sender/chat-sender"
  }
}
```