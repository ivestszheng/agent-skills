<!--
  文件名: chat-markdown-example-streaming-output-cursor.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-markdown#_05-流式输出光标
  场景: 流式输出光标
  描述: 演示 ChatMarkdown 流式输出时的光标动画，支持自定义尾部组件。
  依赖组件: t-chat-markdown, t-segmented
  关键特性: 流式输出光标, streaming属性, generic:tail-component, 自定义尾部
-->

# ChatMarkdown 代码演示-流式输出光标

```wxml
<view class="chat-example-block">
  <!-- 分段组件 -->
  <view style="margin-bottom: 16px">
    <t-segmented options="{{segmentedOptions}}" value="{{selectedSegment}}" bind:change="handleSegmentChange" />
  </view>

  <scroll-view class="chat-example-scroll" scroll-y>
    <!-- 圆点：使用自定义 tail-component -->
    <t-chat-markdown
      wx:if="{{selectedSegment === 1}}"
      content="{{content}}"
      streaming="{{streaming}}"
      generic:tail-component="custom-tail"
      bind:click="handleNodeTap"
    />
    <!-- 省略号：使用 custom-tail2 -->
    <t-chat-markdown
      wx:elif="{{selectedSegment === 2}}"
      content="{{content}}"
      streaming="{{streaming}}"
      generic:tail-component="custom-tail2"
      bind:click="handleNodeTap"
    />
    <!-- 无动画：不传 streaming -->
    <t-chat-markdown wx:elif="{{selectedSegment === 3}}" content="{{content}}" bind:click="handleNodeTap" />
    <!-- 其他（光标）：默认内置 tail 组件 -->
    <t-chat-markdown
      wx:elif="{{selectedSegment === 0}}"
      content="{{content}}"
      streaming="{{streaming}}"
      bind:click="handleNodeTap"
    />
  </scroll-view>
</view>
```

```js
import markdownData from '../base/mock2.js';

const CHUNK_SIZE = 1;
const INTERVAL_MS = 100;

Page({
  data: {
    segmentedOptions: [
      { value: 0, label: '光标' },
      { value: 1, label: '圆点' },
      { value: 2, label: '省略号' },
      { value: 3, label: '无动画' },
    ],
    selectedSegment: -1, // 初始不选中任何分段
    content: '',
    streaming: { hasNextChunk: false, tail: true },
  },

  onLoad() {
    this._timer = null;
  },

  startStreaming(segmentValue) {
    // 停止上一个定时器
    if (this._timer) {
      clearInterval(this._timer);
      this._timer = null;
    }

    // 先将 selectedSegment 设为 -1，强制销毁所有 t-chat-markdown 节点
    this.setData({ content: '', selectedSegment: -1 });

    // 下一帧再挂载新节点并开始播放
    setTimeout(() => {
      let index = 0;

      // 无动画：不传 streaming，仅更新 content
      if (segmentValue === 3) {
        this.setData({ selectedSegment: segmentValue });
        this._timer = setInterval(() => {
          index += CHUNK_SIZE;
          const isDone = index >= markdownData.length;
          this.setData({ content: markdownData.slice(0, index) });
          if (isDone) {
            clearInterval(this._timer);
            this._timer = null;
          }
        }, INTERVAL_MS);
        return;
      }

      this.setData({
        selectedSegment: segmentValue,
        streaming: { hasNextChunk: true, tail: true },
      });

      this._timer = setInterval(() => {
        index += CHUNK_SIZE;
        const isDone = index >= markdownData.length;
        this.setData({
          content: markdownData.slice(0, index),
          streaming: { hasNextChunk: !isDone, tail: true },
        });
        if (isDone) {
          clearInterval(this._timer);
          this._timer = null;
        }
      }, INTERVAL_MS);
    }, 0);
  },

  // 分段切换事件处理
  handleSegmentChange(e) {
    const segmentValue = e.detail.value;
    this.startStreaming(segmentValue);
  },

  handleNodeTap(e) {
    const { node } = e.detail;
    if (node && node.type === 'image') {
      wx.previewImage({ urls: [node.href], current: node.href });
    }
  },
});
```

```css
.chat-example-block {
  background-color: var(--td-bg-color-container);
  padding: 32rpx;
}

.chat-example-scroll {
  height: 800rpx;
  padding: 16rpx;
  width: 95%;
  border: 1rpx solid gray;
}
```

```json
{
  "usingComponents": {
    "t-chat-markdown": "tdesign-miniprogram/chat-markdown/chat-markdown",
    "t-segmented": "tdesign-miniprogram/segmented/segmented",
    "custom-tail": "./custom-tail/custom-tail",
    "custom-tail2": "./custom-tail2/custom-tail2"
  }
}
```