# Dialog 对话框

## 引入

```json
{
  "usingComponents": {
    "t-dialog": "tdesign-miniprogram/dialog/dialog"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-dialog 
  visible="{{visible}}" 
  title="标题" 
  content="内容" 
  bind:close="onClose" 
  bind:confirm="onConfirm" 
/>
```

```javascript
Page({
  data: {
    visible: false
  },
  showDialog() {
    this.setData({ visible: true });
  },
  onClose() {
    this.setData({ visible: false });
  },
  onConfirm() {
    this.setData({ visible: false });
  }
});
```

### 确认对话框

```xml
<t-dialog 
  visible="{{visible}}" 
  type="confirm" 
  title="确认操作" 
  content="确定要执行此操作吗？" 
  bind:close="onClose" 
  bind:confirm="onConfirm" 
/>
```

### 自定义按钮

```xml
<t-dialog 
  visible="{{visible}}" 
  title="标题" 
  content="内容" 
  confirm-btn="{{{ text: '自定义确定', theme: 'primary' }}}" 
  cancel-btn="{{{ text: '自定义取消', theme: 'default' }}}" 
  bind:close="onClose" 
  bind:confirm="onConfirm" 
/>
```

### 无标题对话框

```xml
<t-dialog 
  visible="{{visible}}" 
  content="内容" 
  bind:close="onClose" 
/>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| visible | Boolean | false | 是否显示 |
| title | String | - | 标题 |
| content | String | - | 内容 |
| type | String | alert | 类型，可选值：alert / confirm |
| confirm-btn | Object | - | 确认按钮配置 |
| cancel-btn | Object | - | 取消按钮配置 |
| mask | Boolean | true | 是否显示遮罩 |
| mask-closable | Boolean | true | 点击遮罩是否关闭 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| close | - | 关闭事件 |
| confirm | - | 确认事件 |
| cancel | - | 取消事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |