# BackTop 返回顶部

## 引入

```json
{
  "usingComponents": {
    "t-back-top": "tdesign-miniprogram/back-top/back-top"
  }
}
```

## 代码演示

### 基础用法

```xml
<scroll-view scroll-y bind:scroll="onScroll">
  <view class="content">
    滚动内容...
  </view>
  <t-back-top scroll-top="{{scrollTop}}" />
</scroll-view>
```

```javascript
Page({
  data: {
    scrollTop: 0
  },
  onScroll(e) {
    this.setData({
      scrollTop: e.detail.scrollTop
    });
  }
});
```

### 自定义位置

```xml
<t-back-top 
  scroll-top="{{scrollTop}}" 
  right="40rpx" 
  bottom="200rpx" 
/>
```

### 自定义图标

```xml
<t-back-top scroll-top="{{scrollTop}}">
  <t-icon name="arrow-up" />
</t-back-top>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| scroll-top | Number | 0 | 滚动距离 |
| visibility-height | Number | 400 | 显示阈值 |
| right | String | 40rpx | 右侧距离 |
| bottom | String | 40rpx | 底部距离 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| click | - | 点击事件 |

### Slots

| 名称 | 说明 |
|------|------|
| - | 默认插槽，自定义内容 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |