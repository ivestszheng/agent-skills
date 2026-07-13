# Steps 步骤条

## 引入

```json
{
  "usingComponents": {
    "t-steps": "tdesign-miniprogram/steps/steps",
    "t-step": "tdesign-miniprogram/steps/step"
  }
}
```

## 代码演示

### 基础用法

```xml
<t-steps current="2">
  <t-step title="步骤一" />
  <t-step title="步骤二" />
  <t-step title="步骤三" />
</t-steps>
```

### 带描述步骤条

```xml
<t-steps current="2">
  <t-step title="步骤一" description="描述内容" />
  <t-step title="步骤二" description="描述内容" />
  <t-step title="步骤三" description="描述内容" />
</t-steps>
```

### 步骤条方向

```xml
<t-steps current="2" layout="horizontal">水平步骤条</t-steps>
<t-steps current="2" layout="vertical">垂直步骤条</t-steps>
```

### 自定义状态

```xml
<t-steps current="2" active-icon="success" inactive-icon="circle">
  <t-step title="步骤一" status="finish" />
  <t-step title="步骤二" status="process" />
  <t-step title="步骤三" status="wait" />
</t-steps>
```

## API

### Steps Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| current | Number | 0 | 当前步骤索引 |
| layout | String | horizontal | 方向，可选值：horizontal / vertical |
| active-icon | String | - | 激活态图标 |
| inactive-icon | String | - | 未激活态图标 |

### Step Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| title | String | - | 标题 |
| description | String | - | 描述 |
| status | String | - | 状态，可选值：wait / process / finish / error |

### External Classes

| 类名 | 说明 |
|------|------|
| t-class | 根节点样式类 |