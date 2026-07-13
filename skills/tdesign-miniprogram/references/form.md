# Form 表单

## 引入

```json
{
  "usingComponents": {
    "t-form": "tdesign-miniprogram/form/form",
    "t-form-item": "tdesign-miniprogram/form/form-item",
    "t-input": "tdesign-miniprogram/input/input",
    "t-switch": "tdesign-miniprogram/switch/switch"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-form value="{{formData}}" bind:submit="onSubmit">
  <t-form-item label="用户名" name="username" required>
    <t-input value="{{formData.username}}" bind:change="onFieldChange" data-name="username" />
  </t-form-item>
  <t-form-item label="密码" name="password" required>
    <t-input type="password" value="{{formData.password}}" bind:change="onFieldChange" data-name="password" />
  </t-form-item>
  <t-form-item label="记住我" name="remember">
    <t-switch value="{{formData.remember}}" bind:change="onFieldChange" data-name="remember" />
  </t-form-item>
  <t-button type="primary" bind:click="onSubmit">提交</t-button>
</t-form>
```

```javascript
Page({
  data: {
    formData: {
      username: '',
      password: '',
      remember: false
    }
  },
  onFieldChange(e) {
    const { name } = e.currentTarget.dataset;
    this.setData({
      [`formData.${name}`]: e.detail.value
    });
  },
  onSubmit() {
    console.log('表单提交', this.data.formData);
  }
});
```

### 表单验证

```xml
<t-form value="{{formData}}" rules="{{rules}}" bind:submit="onSubmit">
  <t-form-item label="邮箱" name="email" required>
    <t-input value="{{formData.email}}" bind:change="onFieldChange" data-name="email" />
  </t-form-item>
  <t-form-item label="手机号" name="phone" required>
    <t-input value="{{formData.phone}}" bind:change="onFieldChange" data-name="phone" />
  </t-form-item>
</t-form>
```

```javascript
Page({
  data: {
    formData: {},
    rules: {
      email: [
        { required: true, message: '请输入邮箱' },
        { pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, message: '邮箱格式不正确' }
      ],
      phone: [
        { required: true, message: '请输入手机号' },
        { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确' }
      ]
    }
  }
});
```

## API

### Form Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | Object | {} | 表单数据 |
| rules | Object | {} | 验证规则 |

### FormItem Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| label | String | - | 标签文本 |
| name | String | - | 字段名 |
| required | Boolean | false | 是否必填 |
| error | String | - | 错误信息 |

### Events

| 事件名 | 参数 | 说明 |
|--------|------|------|
| submit | - | 提交事件 |
| validate | { errors } | 验证事件 |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |