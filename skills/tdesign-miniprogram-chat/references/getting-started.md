# 快速上手

## 前置条件

- 已学习微信官方 [小程序简易教程](https://developers.weixin.qq.com/miniprogram/dev/framework/) 和 [自定义组件介绍](https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/)
- 最低基础库版本 `^2.6.5`

## 安装

```bash
npm i tdesign-miniprogram -S --production
```

安装完成后，在微信开发者工具中执行 **工具 → 构建 npm**。

> 如果构建时出现 `NPM packages not found`，需在 `project.config.json` 中补充 `packNpmManually` 和 `packNpmRelationList` 配置，详见 [NPM 支持](https://developers.weixin.qq.com/miniprogram/dev/devtools/npm.html?search-key=npm)。

构建成功后勾选 **将 JS 编译成 ES5**。

## 修改 app.json

将 `app.json` 中的 `"style": "v2"` **移除**。该配置会启用新版组件样式，导致 TDesign 组件样式错乱。

## 修改 tsconfig.json（TypeScript 项目）

```json
{
  "paths": {
    "tdesign-miniprogram/*": ["./miniprogram/miniprogram_npm/tdesign-miniprogram/*"]
  }
}
```

## 引入组件

在页面或组件的 `index.json` 中配置：

```json
{
  "usingComponents": {
    "t-chat": "tdesign-miniprogram/chat-list/chat-list",
    "t-chat-message": "tdesign-miniprogram/chat-message/chat-message",
    "t-chat-sender": "tdesign-miniprogram/chat-sender/chat-sender"
  }
}
```

## 最小示例

### WXML

```xml
<t-chat layout="single">
  <t-chat-message
    avatar="{{item.avatar}}"
    name="{{item.name}}"
    content="{{item.content}}"
    role="{{item.role}}"
  />
  <view slot="footer">
    <t-chat-sender bind:send="onSend" />
  </view>
</t-chat>
```

### JS

```javascript
Component({
  data: {
    chatList: [
      {
        avatar: 'https://tdesign.gtimg.com/site/chat-avatar.png',
        role: 'assistant',
        status: 'complete',
        content: [
          { type: 'text', data: '你好，有什么可以帮你的？' }
        ],
        chatId: 'msg-1',
      },
    ],
    value: '',
    loading: false,
  },
  methods: {
    onSend(e) {
      const { value } = e.detail;
      if (!value || value.trim() === '') return;

      const userMessage = {
        role: 'user',
        content: [{ type: 'text', data: value.trim() }],
        chatId: 'msg-' + Date.now(),
      };

      this.setData({
        chatList: [userMessage, ...this.data.chatList],
        value: '',
      });
    },
  },
});
```

## 在开发者工具中预览

```bash
# 克隆仓库后
npm install
npm run dev
```

打开微信开发者工具，将 `_example` 目录添加进去即可预览。
