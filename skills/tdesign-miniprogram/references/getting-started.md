# 快速上手

## 前置条件

- 已学习微信官方 [小程序简易教程](https://developers.weixin.qq.com/miniprogram/dev/framework/) 和 [自定义组件介绍](https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/)
- 最低基础库版本 `^2.12.0`

## 安装

```bash
npm i tdesign-miniprogram -S --production
```

安装完成后，在微信开发者工具中执行 **工具 → 构建 npm**。

> 如果构建时出现 `NPM packages not found`，需在 `project.config.json` 中补充 `packNpmManually` 和 `packNpmRelationList` 配置。

构建成功后勾选 **将 JS 编译成 ES5**。

## 修改 app.json

将 `app.json` 中的 `"style": "v2"` **移除**。该配置会启用新版组件样式，导致 TDesign 组件样式错乱。

```json
{
  "pages": ["pages/index/index"],
  "style": "v2",
  "usingComponents": {}
}
```

修改为：

```json
{
  "pages": ["pages/index/index"],
  "usingComponents": {}
}
```

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
    "t-button": "tdesign-miniprogram/button/button"
  }
}
```

## 最小示例

### WXML

```xml
<view class="container">
  <t-button theme="primary">主要按钮</t-button>
  <t-button theme="default">默认按钮</t-button>
  <t-button theme="danger">危险按钮</t-button>
</view>
```

### WXSS

```css
.container {
  padding: 32rpx;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}
```

### JS

```javascript
Page({
  onLoad() {
    console.log('页面加载完成');
  },
  onClick(e) {
    console.log('按钮点击', e);
  }
});
```

## 在开发者工具中预览

```bash
npm install
npm run dev
```

打开微信开发者工具，将 `_example` 目录添加进去即可预览示例。

## 基础库版本

最低基础库版本 `^2.12.0`

### 组件与基础库版本对应关系

| 组件 | API | 最低基础库 |
|---|---|---|
| Upload | wx.previewMedia | 2.12.0 |
| Upload | wx.chooseMedia | 2.10.0 |
| Upload | wx.chooseMessageFile | 2.5.0 |
| Navbar | wx.getMenuButtonBoundingClientRect | 2.1.0 |