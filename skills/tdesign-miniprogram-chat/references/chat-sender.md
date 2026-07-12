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

## 事件

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `bind:send` | 发送消息 | `{ value: string }` |
| `bind:stop` | 停止生成 | - |
| `bind:focus` | 输入框聚焦 | - |

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
