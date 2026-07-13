---
name: "tdesign-miniprogram"
description: >
  TDesign 微信小程序基础组件库（tdesign-miniprogram）完整开发指南。
  当用户在微信小程序中开发界面、使用 TDesign 基础组件、配置项目依赖、
  或提及 button / icon / layout / navbar / tabs / input / cell / badge / avatar / form / picker / drawer / dialog / toast / loading 等基础组件时使用。
---

# TDesign 微信小程序基础组件

TDesign Miniprogram 是腾讯 TDesign 团队为微信小程序打造的专业基础组件库，基于 `tdesign-miniprogram` 包，提供从基础布局、导航、输入到数据展示等完整组件体系。

## 快速导航

| 场景 | 参考文档 |
|------|----------|
| 安装配置与快速上手 | [$getting-started](references/getting-started.md) |
| 项目配置与问题排查 | [$configuration](references/configuration.md) |

### 基础组件

| 组件 | 参考文档 |
|------|----------|
| Button 按钮 | [$button](references/button.md) |
| Icon 图标 | [$icon](references/icon.md) |
| Layout 布局 | [$layout](references/layout.md) |
| Link 链接 | [$link](references/link.md) |
| Typography 排版 | [$typography](references/typography.md) |
| Divider 分割线 | [$divider](references/divider.md) |
| Fab 悬浮按钮 | [$fab](references/fab.md) |

### 导航组件

| 组件 | 参考文档 |
|------|----------|
| Navbar 导航条 | [$navbar](references/navbar.md) |
| Tabs 选项卡 | [$tabs](references/tabs.md) |
| TabBar 底部标签栏 | [$tabbar](references/tabbar.md) |
| Drawer 抽屉 | [$drawer](references/drawer.md) |
| SideBar 侧边导航栏 | [$sidebar](references/sidebar.md) |
| Steps 步骤条 | [$steps](references/steps.md) |
| BackTop 返回顶部 | [$backtop](references/backtop.md) |

### 输入组件

| 组件 | 参考文档 |
|------|----------|
| Input 输入框 | [$input](references/input.md) |
| Textarea 多行文本框 | [$textarea](references/textarea.md) |
| Picker 选择器 | [$picker](references/picker.md) |
| Radio 单选框 | [$radio](references/radio.md) |
| CheckBox 多选框 | [$checkbox](references/checkbox.md) |
| Switch 开关 | [$switch](references/switch.md) |
| Form 表单 | [$form](references/form.md) |
| Search 搜索框 | [$search](references/search.md) |
| Stepper 步进器 | [$stepper](references/stepper.md) |
| Slider 滑动选择器 | [$slider](references/slider.md) |
| Rate 评分 | [$rate](references/rate.md) |
| Calendar 日历 | [$calendar](references/calendar.md) |
| DateTimePicker 日期选择器 | [$datetimepicker](references/datetimepicker.md) |
| Upload 上传 | [$upload](references/upload.md) |

### 数据展示组件

| 组件 | 参考文档 |
|------|----------|
| Cell 单元格 | [$cell](references/cell.md) |
| Badge 徽章 | [$badge](references/badge.md) |
| Avatar 头像 | [$avatar](references/avatar.md) |
| Progress 进度条 | [$progress](references/progress.md) |
| Empty 空状态 | [$empty](references/empty.md) |
| Grid 宫格 | [$grid](references/grid.md) |
| Collapse 折叠面板 | [$collapse](references/collapse.md) |
| CountDown 倒计时 | [$countdown](references/countdown.md) |
| Image 图片 | [$image](references/image.md) |
| ImageViewer 图片预览 | [$imageviewer](references/imageviewer.md) |

### 反馈组件

| 组件 | 参考文档 |
|------|----------|
| Toast 轻提示 | [$toast](references/toast.md) |
| Dialog 对话框 | [$dialog](references/dialog.md) |
| Loading 加载 | [$loading](references/loading.md) |

### 脚本工具

| 工具 | 参考文档 |
|------|----------|
| 项目初始化与脚本工具 | [$scripts](references/scripts.md) |

## 核心概念

### 组件引入方式

TDesign 组件支持全局引入和局部引入两种方式：

**全局引入**（在 `app.json` 中配置）：
```json
{
  "usingComponents": {
    "t-button": "tdesign-miniprogram/button/button",
    "t-icon": "tdesign-miniprogram/icon/icon"
  }
}
```

**局部引入**（在页面或组件的 `index.json` 中配置）：
```json
{
  "usingComponents": {
    "t-button": "tdesign-miniprogram/button/button"
  }
}
```

### 通用属性

大部分 TDesign 组件支持以下通用属性：

| 属性 | 类型 | 说明 |
|------|------|------|
| style | Object | 内联样式 |
| class | String | 外部样式类 |
| t-class | String | 组件根节点样式类 |
| data-\* | String | 自定义数据属性 |

### 事件处理

组件事件通过 `bind:` 或 `bind` 前缀绑定：
```xml
<t-button bind:click="onClick">点击</t-button>
<t-input bind:change="onInputChange" />
```

## 路由规则

### 安装/配置问题
- **安装 tdesign-miniprogram** → 加载 [$getting-started](references/getting-started.md)
- **项目配置错误排查** → 加载 [$configuration](references/configuration.md)

### 基础组件
- **Button / 按钮** → 加载 [$button](references/button.md)
- **Icon / 图标** → 加载 [$icon](references/icon.md)
- **Layout / 布局** → 加载 [$layout](references/layout.md)
- **Link / 链接** → 加载 [$link](references/link.md)
- **Typography / 排版** → 加载 [$typography](references/typography.md)
- **Divider / 分割线** → 加载 [$divider](references/divider.md)
- **Fab / 悬浮按钮** → 加载 [$fab](references/fab.md)

### 导航组件
- **Navbar / 导航条** → 加载 [$navbar](references/navbar.md)
- **Tabs / 选项卡** → 加载 [$tabs](references/tabs.md)
- **TabBar / 底部标签栏** → 加载 [$tabbar](references/tabbar.md)
- **Drawer / 抽屉** → 加载 [$drawer](references/drawer.md)
- **SideBar / 侧边栏** → 加载 [$sidebar](references/sidebar.md)
- **Steps / 步骤条** → 加载 [$steps](references/steps.md)
- **BackTop / 返回顶部** → 加载 [$backtop](references/backtop.md)

### 输入组件
- **Input / 输入框** → 加载 [$input](references/input.md)
- **Textarea / 多行文本** → 加载 [$textarea](references/textarea.md)
- **Picker / 选择器** → 加载 [$picker](references/picker.md)
- **Radio / 单选框** → 加载 [$radio](references/radio.md)
- **CheckBox / 多选框** → 加载 [$checkbox](references/checkbox.md)
- **Switch / 开关** → 加载 [$switch](references/switch.md)
- **Form / 表单** → 加载 [$form](references/form.md)
- **Search / 搜索** → 加载 [$search](references/search.md)
- **Stepper / 步进器** → 加载 [$stepper](references/stepper.md)
- **Slider / 滑动选择器** → 加载 [$slider](references/slider.md)
- **Rate / 评分** → 加载 [$rate](references/rate.md)
- **Calendar / 日历** → 加载 [$calendar](references/calendar.md)
- **DateTimePicker / 日期选择器** → 加载 [$datetimepicker](references/datetimepicker.md)
- **Upload / 上传** → 加载 [$upload](references/upload.md)

### 数据展示组件
- **Cell / 单元格** → 加载 [$cell](references/cell.md)
- **Badge / 徽章** → 加载 [$badge](references/badge.md)
- **Avatar / 头像** → 加载 [$avatar](references/avatar.md)
- **Progress / 进度条** → 加载 [$progress](references/progress.md)
- **Empty / 空状态** → 加载 [$empty](references/empty.md)
- **Grid / 宫格** → 加载 [$grid](references/grid.md)
- **Collapse / 折叠面板** → 加载 [$collapse](references/collapse.md)
- **CountDown / 倒计时** → 加载 [$countdown](references/countdown.md)
- **Image / 图片** → 加载 [$image](references/image.md)
- **ImageViewer / 图片预览** → 加载 [$imageviewer](references/imageviewer.md)

### 反馈组件
- **Toast / 轻提示** → 加载 [$toast](references/toast.md)
- **Dialog / 对话框** → 加载 [$dialog](references/dialog.md)
- **Loading / 加载** → 加载 [$loading](references/loading.md)

### 脚本工具
- **脚本工具 / 初始化 / 页面生成 / 模拟数据** → 加载 [$scripts](references/scripts.md)

## 官方资源

- 官方文档：https://tdesign.tencent.com/miniprogram/overview
- GitHub：https://github.com/Tencent/tdesign-miniprogram
- NPM：https://www.npmjs.com/package/tdesign-miniprogram