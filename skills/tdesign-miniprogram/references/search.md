# Search 搜索框

## 引入

```json
{
  "usingComponents": {
    "t-search": "tdesign-miniprogram/search/search"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-search value="{{value}}" bind:change="onChange" placeholder="请输入搜索内容" />
```

```javascript
Page({
  data: {
    value: ''
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 搜索事件

```xml
<t-search 
  value="{{value}}" 
  bind:change="onChange" 
  bind:search="onSearch" 
  placeholder="请输入搜索内容" 
/>
```

```javascript
Page({
  onSearch(e) {
    console.log('搜索', e.detail.value);
  }
});
```

### 禁用状态

```xml
<t-search disabled placeholder="禁用状态" />
```

### 自定义图标

```xml
<t-search 
  value="{{value}}" 
  left-icon="search" 
  right-icon="clear" 
  placeholder="自定义图标" 
/>
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String | - | 输入值 |
| placeholder | String | - | 占位符 |
| disabled | Boolean | false | 是否禁用 |
| left-icon | String | - | 左侧图标 |
| right-icon | String | - | 右侧图标 |
| clearable | Boolean | false | 是否可清除 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |
| search | { value } | 搜索事件 |
| focus | - | 聚焦事件 |
| blur | - | 失焦事件 |
| clear | - | 清除事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |