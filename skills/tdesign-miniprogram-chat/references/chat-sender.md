<!--
  文件名: chat-sender.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-sender
 -->
# ChatSender 对话输入框

聊天输入框组件，支持文字输入、附件上传、内容引用等功能。

## 引入

```json
{
  "usingComponents": {
    "t-chat-sender": "tdesign-miniprogram/chat-sender/chat-sender"
  }
}
```

## 基础用法

```xml
<t-chat-sender
  value="{{value}}"
  loading="{{loading}}"
  disabled="{{disabled}}"
  autoRiseWithKeyboard="{{true}}"
  renderPresets="{{renderPresets}}"
  bind:send="onSend"
  bind:stop="onStop"
  bind:focus="onFocus"
/>
```

## Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `value` | String | `''` | 输入框的值（受控） |
| `loading` | Boolean | `false` | 加载状态，为 true 时显示停止按钮 |
| `disabled` | Boolean | `false` | 禁用状态 |
| `autoRiseWithKeyboard` | Boolean | `false` | 键盘弹起时是否自动上推输入框 |
| `renderPresets` | Array | - | 预设操作按钮配置 |
| `placeholder` | String | - | 输入框占位文本 |
| `textareaProps` | Object | - | 透传给内部 textarea 的属性，如 `{ autosize: { maxHeight, minHeight } }` |
| `fileList` | Array | `[]` | 文件列表（受控） |
| `attachmentsProps` | Object | - | 附件区域配置，如 `{ items, removable, imageViewer }` |
| `visible` | Boolean | `false` | 是否显示上传选择面板 |

## 事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `bind:send` | 发送消息 | `{ value: string }` |
| `bind:stop` | 停止生成 | `{ value: string }` |
| `bind:focus` | 输入框聚焦 | `{ value, context }` |
| `bind:blur` | 输入框失焦 | `{ value, context }` |
| `bind:change` | 输入内容变化 | `{ value: string }` |
| `bind:uploadClick` | 点击上传按钮 | - |
| `bind:fileClick` | 点击文件 | `{ file }` |
| `bind:fileDelete` | 删除文件 | `{ file }` |
| `bind:fileChange` | 文件列表变化 | `{ files }` |
| `bind:fileSelect` | 选择文件 | `{ name, files }` |
| `bind:updateVisible` | 上传面板显隐变化 | `visible: boolean` |
| `bind:keyboardheightchange` | 键盘高度变化 | `e.detail` |

## Slots

| 插槽名 | 说明 |
|--------|------|
| `header` | 输入框顶部区域（用于内容引用展示） |
| `footer-prefix` | 输入框底部左侧区域 |
| `suffix` | 输入框底部操作区域 |

## 上传文件示例

支持选择附件及展示附件列表，受控进行文件数据管理：

```xml
<t-chat-sender
  value="{{value}}"
  loading="{{loading}}"
  bind:send="onSend"
  bind:stop="onStop"
>
  <view slot="header">
    <!-- 顶部引用/附件预览区域 -->
  </view>
  <view slot="footer-prefix">
    <!-- 底部左侧，如附件按钮 -->
  </view>
</t-chat-sender>
```

## 预设按钮配置

```javascript
data: {
  renderPresets: [
    { name: 'send', type: 'icon' },
  ],
}
```

## 在 ChatList 中使用

通常将 ChatSender 放在 ChatList 的 `footer` 插槽中：

```xml
<t-chat id="chatList">
  <block wx:for="{{chatList}}" wx:key="chatId">
    <t-chat-message ... />
  </block>
  <view slot="footer">
    <t-chat-sender
      value="{{value}}"
      loading="{{loading}}"
      bind:send="onSend"
      bind:stop="onStop"
    />
  </view>
</t-chat>
```

## 完整业务示例

实际业务场景的完整页面示例（含 wxml / js / css / json 四件套）已放在 `examples/` 目录，可直接作为页面模板参考：

| 示例 | 场景说明 | 关键特性 |
|------|----------|----------|
| [基础类型](../examples/chat-sender-example-basic.md) | 标准输入框 | `textareaProps` 自动高度、`footer-prefix` 自定义按钮 |
| [上传文件](../examples/chat-sender-example-upload.md) | 附件上传 | `upload` 预设按钮、`attachmentsProps` 文件列表管理 |
| [文件引用](../examples/chat-sender-example-file-citation.md) | 引用文件展示 | `header` 插槽、文件图标引用 |
| [内容引用](../examples/chat-sender-example-content-citation.md) | 引用文本展示 | `header` 插槽、文本内容引用、关闭引用 |
