# ChatLoading 对话加载

对话场景专用的加载动画组件，支持多种动效类型和文案描述。

## 引入

```json
{
  "usingComponents": {
    "t-chat-loading": "tdesign-miniprogram/chat-loading/chat-loading"
  }
}
```

## Props

| 名称 | 类型 | 默认值 | 说明 | 必传 |
|------|------|--------|------|------|
| `style` | Object | - | 样式 | N |
| `custom-style` | Object | - | 样式（虚拟化组件节点场景） | N |
| `animation` | String | `'moving'` | 加载动效类型 | N |
| `text` | String | - | 加载过程展示的文字内容 | N |

## 动效类型

| 值 | 说明 |
|----|------|
| `moving` | 移动波浪（默认） |
| `gradient` | 渐变呼吸效果 |
| `dots` | 圆点跳动 |
| `skeleton` | 骨架屏 |

## 基础用法

```xml
<!-- 渐变动效 -->
<t-chat-loading animation="gradient" />

<!-- 移动波浪 -->
<t-chat-loading animation="moving" />

<!-- 圆点跳动 -->
<t-chat-loading animation="dots" />
```

## 带文案描述

```xml
<t-chat-loading animation="dots" text="加载中..." />
<t-chat-loading animation="gradient" text="深度思考中..." />
<t-chat-loading animation="moving" text="正在理解中..." />
```

## 在 ChatMessage 中使用

通常在消息 `status` 为 `pending` 时展示加载动画：

```xml
<t-chat-message
  content="{{item.content}}"
  role="{{item.role}}"
  status="{{item.status}}"
>
  <t-chat-loading
    wx:if="{{item.status === 'pending' && !item.content[0].data}}"
    animation="dots"
    text="思考中..."
  />
</t-chat-message>
```

## 切换动效

```javascript
Component({
  data: {
    currentAnimation: 'moving',
  },
  methods: {
    switchAnimation(e) {
      const { animation } = e.currentTarget.dataset;
      this.setData({ currentAnimation: animation });
    },
  },
});
```

## 完整业务示例

实际业务场景的完整页面示例（含 wxml / js / css / json 四件套）已放在 `examples/` 目录，可直接作为页面模板参考：

| 示例 | 场景说明 | 关键特性 |
|------|----------|----------|
| [动画样式](../examples/chat-loading-example-animation.md) | 多种动效切换 | 动画样式, gradient/moving/dots, 动效切换 |
| [带文案描述的加载组件](../examples/chat-loading-example-text.md) | 加载文案展示 | 加载文案, text属性, dots动画 |
