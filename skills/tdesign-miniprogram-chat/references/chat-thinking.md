# ChatThinking 思考过程

展示 AI 思考/推理过程的折叠面板组件，支持多种加载动效和布局方式。

## 引入

```json
{
  "usingComponents": {
    "t-chat-thinking": "tdesign-miniprogram/chat-thinking/chat-thinking"
  }
}
```

## 基础用法

```xml
<t-chat-thinking
  content="{{thinkingContent}}"
  collapsed="{{collapsed}}"
  animation="{{animation}}"
  layout="{{layout}}"
/>
```

## Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `content` | String | - | 思考过程文本内容 |
| `collapsed` | Boolean | `false` | 是否折叠面板 |
| `animation` | String | - | 加载动效类型：`gradient` / `moving` / `dots` |
| `layout` | String | - | 布局方式 |

## Slots

| 插槽名 | 说明 |
|--------|------|
| `content` | 自定义思考过程显示内容 |

## 组件状态

### 思考中

显示加载动效，表示 AI 正在思考：

```xml
<t-chat-thinking
  content="正在分析问题..."
  collapsed="{{false}}"
  animation="dots"
/>
```

### 思考完成

思考完成后自动收起面板：

```xml
<t-chat-thinking
  content="经过分析，我认为..."
  collapsed="{{true}}"
/>
```

## 在 ChatMessage 中使用

通常放在 `t-chat-message` 的 content 数组中，或通过插槽嵌入：

```xml
<t-chat-message
  content="{{item.content}}"
  role="{{item.role}}"
  status="{{item.status}}"
>
  <!-- 思考过程可作为消息内容的一部分展示 -->
  <t-chat-thinking
    wx:if="{{item.thinking}}"
    content="{{item.thinking}}"
    collapsed="{{item.status === 'complete'}}"
    animation="dots"
  />
</t-chat-message>
```

## 布局方式

通过 `layout` 属性设置思考过程的展示布局，支持不同的视觉风格。

## 完整业务示例

实际业务场景的完整页面示例（含 wxml / js / css / json 四件套）已放在 `examples/` 目录，可直接作为页面模板参考：

| 示例 | 场景说明 | 关键特性 |
|------|----------|----------|
| [组件类型](../examples/chat-thinking-example-type.md) | 打字机效果 + 动效 | 组件类型, 打字机效果, 动效类型, collapsed控制 |
| [思考中](../examples/chat-thinking-example-status-pending.md) | 思考中状态 | 思考中状态, status:pending, 加载动效 |
| [思考完成](../examples/chat-thinking-example-status-complete.md) | 思考完成状态 | 思考完成状态, status:complete, 面板收起 |
| [组件样式](../examples/chat-thinking-example-layout-and-content.md) | 布局与插槽 | layout布局, block/border样式, content插槽自定义 |
