# TabBar 底部标签栏

## 引入

```json
{
  "usingComponents": {
    "t-tab-bar": "tdesign-miniprogram/tab-bar/tab-bar"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-tab-bar 
  value="{{activeTab}}" 
  options="{{tabOptions}}" 
  bind:change="onTabChange" 
/>
```

```javascript
Page({
  data: {
    activeTab: 'home',
    tabOptions: [
      { label: '首页', value: 'home', icon: 'home' },
      { label: '分类', value: 'category', icon: 'category' },
      { label: '购物车', value: 'cart', icon: 'cart' },
      { label: '我的', value: 'profile', icon: 'user' }
    ]
  },
  onTabChange(e) {
    this.setData({
      activeTab: e.detail.value
    });
  }
});
```

### 带徽标的标签栏

```javascript
Page({
  data: {
    tabOptions: [
      { label: '首页', value: 'home', icon: 'home' },
      { label: '消息', value: 'message', icon: 'notification', badgeProps: { count: 99 } },
      { label: '购物车', value: 'cart', icon: 'cart', badgeProps: { dot: true } },
      { label: '我的', value: 'profile', icon: 'user' }
    ]
  }
});
```

### 自定义颜色

```xml
<t-tab-bar 
  value="{{activeTab}}" 
  options="{{tabOptions}}" 
  active-color="#1677ff"
  inactive-color="#999999"
/>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String / Number | - | 当前激活标签值 |
| options | Array | [] | 标签配置数组 |
| active-color | String | - | 激活态颜色 |
| inactive-color | String | - | 未激活态颜色 |
| safe-area | Boolean | true | 是否适配安全区域 |

### Options 配置

| 属性 | 类型 | 说明 |
|------|------|------|
| label | String | 标签文本 |
| value | String / Number | 标签值 |
| icon | String | 图标名称 |
| badgeProps | Object | 徽标配置 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 标签切换事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |