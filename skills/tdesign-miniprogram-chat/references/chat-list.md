# ChatList 对话列表

官方文档: <https://tdesign.tencent.com/miniprogram-chat/components/chat-list>

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

## 核心 API

### 滚动到底部

```javascript
scrollToBottom() {
  const chatListComponent = this.selectComponent('#chatList');
  if (chatListComponent && typeof chatListComponent.scrollToBottom === 'function') {
    chatListComponent.scrollToBottom();
  }
}
```

### 事件

| 事件名 | 说明 |
|--------|------|
| `bindscroll` | 列表滚动时触发 |

### 虚拟列表优化

组件内置虚拟列表优化性能，仅在 `data` 属性中使用时生效：

```xml
<!-- 内置虚拟列表优化（data 属性方式） -->
<t-chat id="chatList" data="{{chatList}}" />
```

> 注意：使用 `data` 属性时，组件会自动使用虚拟列表，不再需要手动 `wx:for`。适合大量消息场景。

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

