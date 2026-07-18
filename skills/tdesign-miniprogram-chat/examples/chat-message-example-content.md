<!--
  文件名: chat-message-example-content.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-message#配置消息属性
  场景: 配置消息属性
  描述: 演示 content 插槽自定义，支持附件、图片、文件、思考过程等多种消息内容。
  依赖组件: t-chat-message, t-chat-actionbar, t-avatar
  关键特性: content插槽, 附件消息, 图片消息, 文件消息, 思考过程
-->

# ChatMessage 代码演示-配置消息属性

支持`content`插槽自定义, `content`插槽使用建议：渲染聊天消息统一用`t-chat-content`；仅在需要“单独使用 Markdown 组件”时使用`t-chat-markdown`。也支持别的 `markdown`渲染组件，选择其他`markdown`渲染库由用户自行安装。

```wxml
<view class="chat-example">
  <!-- 附件消息 -->
  <view class="chat-example-block">
    <t-chat-message
      content="{{pic2.content}}"
      role="{{pic2.role}}"
      chatContentProps="{{chatContentProps}}"
    ></t-chat-message>
  </view>
  <view class="chat-example-block">
    <t-chat-message
      content="{{pic3.content}}"
      role="{{pic3.role}}"
      placement="right"
      chatContentProps="{{chatContentProps}}"
    ></t-chat-message>
  </view>
  <view class="chat-example-block">
    <t-chat-message
      content="{{fileMessage.content}}"
      role="{{fileMessage.role}}"
      chatContentProps="{{chatContentProps}}"
    ></t-chat-message>
  </view>
  <view class="chat-example-block">
    <t-chat-message
      content="{{fileMessage.content}}"
      role="{{fileMessage.role}}"
      placement="right"
      chatContentProps="{{chatContentProps}}"
    ></t-chat-message>
  </view>
  <!-- 思考过程消息 -->
  <view class="chat-example-block">
    <t-chat-message
      content="{{aiMessage.content}}"
      role="{{aiMessage.role}}"
      status="{{aiMessage.status}}"
      variant="text"
    >
      <t-chat-actionbar slot="actionbar" />
    </t-chat-message>
  </view>
</view>
```

```js
Component({
  data: {
    aiMessage: {
      role: 'assistant',
      status: 'complete',
      content: [
        {
          type: 'thinking',
          data: {
            title: '已完成思考（耗时3秒）',
            text: '好的，我现在需要回答用户关于对比近3年当代偶像爱情剧并总结创作经验的问题\n查询网络信息中...\n根据网络搜索结果，成功案例包括《春色寄情人》《要久久爱》《你也有今天》等，但缺乏具体播放数据，需要结合行业报告总结共同特征。2022-2024年偶像爱情剧的创作经验主要集中在题材创新、现实元素融入、快节奏叙事等方面。结合行业报告和成功案例，总结出以下创作经验。',
          },
        },
        {
          type: 'text',
          data: '不，牛顿第一定律并不适用于所有参考系。它只适用于惯性参考系。',
        },
      ],
    },
    pic1: {
      role: 'user',
      name: '张三',
      avatar: 'https://tdesign.gtimg.com/site/avatar.jpg',
      content: [
        {
          type: 'attachment',
          data: [
            {
              fileType: 'image',
              name: 'avatar.jpg',
              size: 234234,
              url: 'https://tdesign.gtimg.com/demo/demo-image-1.png',
              width: 1920, // 图片实际宽度
              height: 1080, // 图片实际高度
            },
          ],
        },
        {
          type: 'text',
          data: '分析以下内容，总结一篇广告策划方案',
        },
      ],
    },
    pic3: {
      role: 'user',
      content: [
        {
          type: 'attachment',
          data: [
            {
              fileType: 'image',
              name: 'avatar.jpg',
              size: 234234,
              url: 'https://tdesign.gtimg.com/demo/demo-image-1.png',
              width: 1920, // 图片实际宽度
              height: 1080, // 图片实际高度
            },
          ],
        },
        {
          type: 'text',
          data: '分析以下',
        },
      ],
    },
    pic2: {
      role: 'user',
      content: [
        {
          type: 'attachment',
          data: [
            {
              fileType: 'image',
              name: 'avatar.jpg',
              size: 234234,
              url: 'https://tdesign.gtimg.com/demo/demo-image-1.png',
              width: 1920, // 为了更好的适配不同尺寸图片建议传入宽高，不传也有兜底尺寸
              height: 1080, // 为了更好的适配不同尺寸图片建议传入宽高，不传也有兜底尺寸
            },
            {
              fileType: 'image',
              name: 'avatar2.jpg',
              size: 234234,
              url: 'https://tdesign.gtimg.com/demo/demo-image-1.png',
              width: 1920, // 图片实际宽度
              height: 1080, // 图片实际高度
            },
          ],
        },
        {
          type: 'text',
          data: '分析以下内容，总结一篇广告策划方案',
        },
      ],
    },
    fileMessage: {
      role: 'user',
      content: [
        {
          type: 'attachment',
          data: [
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
        {
          type: 'text',
          data: '不，牛顿第一定律并不适用于所有参考系。它只适用于惯性参考系。',
        },
      ],
    },
  },
});
```

```css
.chat-example {
  display: flex;
  flex-direction: column;
  gap: 32rpx;
}

.chat-example-block {
  background-color: var(--td-bg-color-container);
  padding: 32rpx 32rpx 0 32rpx;
}
```

```json
{
  "component": true,
  "usingComponents": {
    "t-chat-message": "tdesign-miniprogram/chat-message/chat-message",
    "t-chat-actionbar": "tdesign-miniprogram/chat-actionbar/chat-actionbar",
    "t-avatar": "tdesign-miniprogram/avatar/avatar"
  }
}
```