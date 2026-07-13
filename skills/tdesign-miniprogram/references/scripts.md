# 脚本工具

## init-project.ps1 - 项目初始化脚本

### 功能

自动完成 TDesign 小程序项目的初始化配置：
1. 检查并初始化 npm
2. 安装 `tdesign-miniprogram` 依赖
3. 移除 `app.json` 中的 `"style": "v2"`
4. 配置 `project.config.json` 的 npm 构建选项
5. 复制脚本工具到项目目录

### 用法

在微信小程序项目根目录执行：

```powershell
pwsh -File scripts/init-project.ps1
```

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| ProjectDir | String | 当前目录 | 项目根目录路径 |

## create-page.js - 页面模板生成器

### 功能

快速生成四种常见页面类型的完整模板文件（wxml/wxss/js/json）：
- **home**: 首页模板（轮播图、宫格导航、推荐卡片）
- **list**: 列表页模板（搜索、筛选、列表数据）
- **form**: 表单页模板（各种输入组件）
- **detail**: 详情页模板（商品信息、规格、评价）

### 用法

```bash
# 生成首页
node scripts/create-page.js home

# 生成列表页
node scripts/create-page.js list

# 生成表单页
node scripts/create-page.js form

# 生成详情页
node scripts/create-page.js detail

# 指定自定义路径
node scripts/create-page.js list pages/product/list
```

### 页面模板包含的组件

**home 首页**：
- `t-navbar` - 导航条
- `t-grid` / `t-grid-item` - 宫格导航
- `t-badge` - 徽章

**list 列表页**：
- `t-navbar` - 导航条
- `t-search` - 搜索框
- `t-cell` / `t-cell-group` - 单元格列表
- `t-badge` - 徽章
- `t-loading` - 加载状态

**form 表单页**：
- `t-navbar` - 导航条
- `t-form` - 表单容器
- `t-cell` / `t-cell-group` - 表单项容器
- `t-input` / `t-textarea` - 输入组件
- `t-radio` / `t-radio-group` - 单选组件
- `t-checkbox` / `t-checkbox-group` - 多选组件
- `t-datetime-picker` - 日期选择器
- `t-switch` - 开关组件
- `t-button` - 按钮

**detail 详情页**：
- `t-navbar` - 导航条
- `t-badge` - 徽章
- `t-cell` / `t-cell-group` - 规格参数
- `t-avatar` - 头像
- `t-rate` - 评分
- `t-button` - 按钮

## mock-server.py - 模拟服务端

### 功能

基于 Flask 提供完整的模拟 API 接口，用于小程序开发测试。

### 安装依赖

```bash
pip install flask
```

### 运行

```bash
python scripts/mock-server.py
```

### 可用接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/products` | GET | 获取商品列表，支持分页和搜索 |
| `/api/products/{id}` | GET | 获取商品详情 |
| `/api/users` | GET | 获取用户列表 |
| `/api/banners` | GET | 获取轮播图数据 |
| `/api/login` | POST | 用户登录 |
| `/api/form/submit` | POST | 提交表单 |

### 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### 使用示例

```javascript
// 小程序中调用
wx.request({
  url: 'http://localhost:5000/api/products',
  method: 'GET',
  data: { page: 1, page_size: 10 },
  success(res) {
    console.log(res.data);
  }
});
```

### 注意事项

1. 确保微信开发者工具已勾选「不校验合法域名」
2. 服务默认运行在 `http://localhost:5000`
3. 接口返回延迟 0.3-0.5 秒模拟真实网络