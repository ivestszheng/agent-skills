<!--
  文件名: chat-list.md
  官方文档：https://tdesign.tencent.com/miniprogram-chat/components/chat-list
 -->
# ChatList 对话列表

对话消息列表容器组件，负责管理消息的渲染和滚动行为。

## 引入

```json
{
  "usingComponents": {
    "t-chat": "tdesign-miniprogram/chat-list/chat-list"
  }
}
```

## 核心用法

```xml
<view class="chat-box" style="height: {{contentHeight}};">
  <t-chat id="chatList" bindscroll="onScroll">
    <block wx:for="{{chatList}}" wx:key="chatId">
      <t-chat-message
        chat-id="{{item.chatId}}"
        avatar="{{item.avatar || ''}}"
        name="{{item.name || ''}}"
        datetime="{{item.datetime || ''}}"
        content="{{item.content}}"
        role="{{item.role}}"
        placement="{{item.role === 'user' ? 'right' : 'left'}}"
        status="{{item.status || ''}}"
        bind:message-longpress="showPopover"
        bind:click="onClick"
      >
        <t-chat-actionbar
          wx:if="{{index !== chatList.length - 1 && item.status === 'complete' && item.role === 'assistant'}}"
          id="{{'actionbar-'+item.chatId}}"
          chat-id="{{item.chatId}}"
          comment="{{item.comment}}"
          slot="actionbar"
          placement="end"
          bind:actions="handleAction"
        />
      </t-chat-message>
    </block>
    <view slot="footer">
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
    </view>
  </t-chat>
</view>
```

## Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `data` | Array | - | 列表数据。传入后组件自动渲染 `t-chat-message`，无需手动 `wx:for`；配合 `virtualList` 可启用虚拟列表 |
| `layout` | String | `'both'` | 布局方式：`'both'`（用户靠右、助手靠左）/ `'single'`（全部靠左） |
| `reverse` | Boolean | `true` | 是否反转列表（最新消息在顶部）。默认 `true`，适合"新消息插入数组头部"的场景 |
| `animation` | String | `'skeleton'` | 消息加载动画类型：`'skeleton'` / `'moving'` / `'gradient'` / `'dot'`，透传给内部 `chat-message` |
| `virtualList` | Boolean | `false` | 是否开启虚拟列表。开启后仅渲染可视范围内的消息，优化大量消息性能 |
| `fragmentLen` | Number | `8` | 虚拟列表初始渲染片段长度，滚动到边缘时按步长递增 |

## Methods

通过 `this.selectComponent('#chatList')` 获取实例后调用：

| 方法名 | 说明 | 参数 |
|--------|------|------|
| `scrollToBottom()` | 滚动到底部（`reverse` 为 `true` 时滚动到顶部） | 无 |
| `setScrollTop(scrollTop)` | 设置滚动条位置 | `scrollTop`: Number，默认 `0` |

```javascript
scrollToBottom() {
  const chatListComponent = this.selectComponent('#chatList');
  if (chatListComponent && typeof chatListComponent.scrollToBottom === 'function') {
    chatListComponent.scrollToBottom();
  }
}
```

## Events

| 事件名 | 说明 | 回调参数 |
|--------|------|----------|
| `bindscroll` | 列表滚动时触发 | `e.detail`：scroll-view 原生 scroll 事件对象，含 `scrollTop`、`scrollHeight`、`deltaY` 等 |

## Slots

| 插槽名 | 说明 |
|--------|------|
| `default` | 默认插槽。当 `data` 属性为空或未传入时渲染，通常用于手动 `wx:for` 遍历 `t-chat-message` |
| `footer` | 底部插槽，始终渲染。通常用于放置 `t-chat-sender` 输入框 |

## 虚拟列表优化

当消息量较大时，传入 `data` 属性并开启 `virtualList` 即可启用虚拟列表，无需手动 `wx:for`：

```xml
<!-- 虚拟列表模式：组件自动渲染 data 中的消息 -->
<t-chat id="chatList" data="{{chatList}}" virtualList="{{true}}" />
```

> 注意：使用 `data` 属性时，组件自动遍历渲染 `chat-message`，不再需要手动 `wx:for`。`virtualList` 控制是否仅渲染可视范围。

## 完整业务示例

实际业务场景的完整页面示例（含 wxml / js / wxss / json 四件套）已拆分到 `examples/` 目录，可直接作为页面模板参考：

| 示例 | 场景说明 | 关键特性 |
|------|----------|----------|
| [基础使用](../examples/chat-list-example-basic.md) | 标准对话流程 | 文本消息、流式输出、操作栏、长按弹出 |
| [组合式用法](../examples/chat-list-example-composition.md) | 思考过程 + 正文 | `chatContentProps.thinking`、分阶段流式 |
| [自定义](../examples/chat-list-example-custom.md) | 图表消息渲染 | `slot="content"` 自定义内容、`chart-component` |
| [文案助手](../examples/chat-list-example-copywriting.md) | 附件上传 + 文案生成 | `t-chat-sender` 附件、`markdownProps` 流式尾标 |
| [图像生成](../examples/chat-list-example-image.md) | 多图结果展示 | `imageview` 内容类型、`t-attachments` |
| [任务规划](../examples/chat-list-example-task.md) | Agent 多步骤任务 | `agent` 内容类型、`t-steps` 步骤条 |

