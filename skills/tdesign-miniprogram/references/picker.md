# Picker 选择器

## 引入

```json
{
  "usingComponents": {
    "t-picker": "tdesign-miniprogram/picker/picker"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-picker 
  value="{{value}}" 
  options="{{options}}" 
  bind:change="onChange" 
  placeholder="请选择" 
/>
```

```javascript
Page({
  data: {
    value: '',
    options: [
      { label: '选项一', value: '1' },
      { label: '选项二', value: '2' },
      { label: '选项三', value: '3' }
    ]
  },
  onChange(e) {
    this.setData({ value: e.detail.value });
  }
});
```

### 级联选择

```xml
<t-picker 
  value="{{value}}" 
  options="{{options}}" 
  cascade 
  bind:change="onChange" 
/>
```

```javascript
Page({
  data: {
    options: [
      {
        label: '一级',
        value: '1',
        children: [
          { label: '二级1', value: '1-1' },
          { label: '二级2', value: '1-2' }
        ]
      }
    ]
  }
});
```

### 多列选择

```xml
<t-picker 
  value="{{value}}" 
  columns="{{columns}}" 
  bind:change="onChange" 
/>
```

```javascript
Page({
  data: {
    columns: [
      {
        options: [
          { label: '周一', value: '1' },
          { label: '周二', value: '2' }
        ]
      },
      {
        options: [
          { label: '上午', value: 'AM' },
          { label: '下午', value: 'PM' }
        ]
      }
    ]
  }
});
```

## API

### Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | String / Array | - | 当前值 |
| options | Array | [] | 选项列表 |
| columns | Array | [] | 多列配置 |
| placeholder | String | - | 占位符 |
| cascade | Boolean | false | 是否级联 |
| disabled | Boolean | false | 是否禁用 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| change | { value } | 值变化事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |