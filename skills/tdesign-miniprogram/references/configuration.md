# 项目配置与问题排查

## project.config.json 配置

当构建 npm 时出现 `NPM packages not found` 错误，需要在 `project.config.json` 中配置 `packNpmManually` 和 `packNpmRelationList`。

```json
{
  "setting": {
    "packNpmManually": true,
    "packNpmRelationList": [
      {
        "packageJsonPath": "./package.json",
        "miniprogramNpmDistDir": "./miniprogram/"
      }
    ]
  }
}
```

## app.json 配置注意事项

### 移除 style: v2

```json
{
  "pages": ["pages/index/index"],
  "usingComponents": {}
}
```

### 全局注册组件

```json
{
  "pages": ["pages/index/index"],
  "usingComponents": {
    "t-button": "tdesign-miniprogram/button/button",
    "t-icon": "tdesign-miniprogram/icon/icon",
    "t-cell": "tdesign-miniprogram/cell/cell",
    "t-cell-group": "tdesign-miniprogram/cell-group/cell-group"
  }
}
```

## tsconfig.json 配置

### 路径别名配置

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "tdesign-miniprogram/*": ["./miniprogram/miniprogram_npm/tdesign-miniprogram/*"]
    }
  }
}
```

## 常见问题

### Q1: 构建 npm 报错 `NPM packages not found`

**原因**：项目未正确配置 npm 构建路径。

**解决方案**：在 `project.config.json` 中添加：

```json
{
  "setting": {
    "packNpmManually": true,
    "packNpmRelationList": [
      {
        "packageJsonPath": "./package.json",
        "miniprogramNpmDistDir": "./miniprogram/"
      }
    ]
  }
}
```

### Q2: 组件样式错乱

**原因**：`app.json` 中启用了 `"style": "v2"`。

**解决方案**：移除 `"style": "v2"` 配置。

### Q3: 组件找不到或路径错误

**原因**：组件路径配置错误或 npm 未构建。

**解决方案**：
1. 确保执行了 **工具 → 构建 npm**
2. 检查组件路径是否正确：`tdesign-miniprogram/组件名/组件名`
3. 检查 `miniprogram_npm` 目录是否存在

### Q4: TypeScript 项目找不到类型定义

**原因**：未配置路径别名或未安装类型定义。

**解决方案**：
1. 在 `tsconfig.json` 中配置 `paths`
2. 安装 `@types/wechat-miniprogram`

### Q5: 自定义 tabBar 组件路径问题

**原因**：自定义 tabBar 页面路径与 `app.json` 中的配置不一致。

**解决方案**：确保 `custom-tab-bar` 的数据源与 `app.json` 的 `tabBar.list.pagePath` 使用同一套路径规范。

### Q6: husky 安装失败（非 git 仓库）

**原因**：项目不是 git 仓库，导致 husky 的 prepare 脚本失败。

**解决方案**：使用 `--ignore-scripts` 跳过脚本安装：

```bash
npm i --ignore-scripts
```

## 构建流程

1. 安装依赖：`npm install`
2. 构建 npm：在微信开发者工具中执行 **工具 → 构建 npm**
3. 勾选 **将 JS 编译成 ES5**
4. 预览项目