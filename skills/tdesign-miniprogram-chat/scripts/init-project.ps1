# TDesign Miniprogram Chat - 项目初始化脚本
# 用法: 在小程序项目根目录执行 pwsh -File scripts/init-project.ps1
#
# 功能:
#   1. 初始化 npm (如未初始化)
#   2. 安装 tdesign-miniprogram
#   3. 检查并移除 app.json 中的 "style": "v2"
#   4. 提示后续操作

param(
    [string]$ProjectDir = (Get-Location)
)

$ErrorActionPreference = "Stop"

Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "TDesign Miniprogram Chat - 项目初始化" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# 检查是否在微信小程序项目目录中
$appJsonPath = Join-Path $ProjectDir "app.json"
if (-not (Test-Path $appJsonPath)) {
    Write-Host "[错误] 未找到 app.json，请确保在微信小程序项目根目录中执行此脚本。" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[1/4] 检查 package.json..." -ForegroundColor Yellow

if (-not (Test-Path (Join-Path $ProjectDir "package.json"))) {
    Write-Host "    未找到 package.json，正在初始化 npm..." -ForegroundColor Gray
    npm init -y
    Write-Host "    已初始化 npm" -ForegroundColor Green
} else {
    Write-Host "    package.json 已存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/4] 安装 tdesign-miniprogram..." -ForegroundColor Yellow
npm install tdesign-miniprogram -S --production
Write-Host "    安装完成" -ForegroundColor Green

Write-Host ""
Write-Host "[3/4] 检查 app.json..." -ForegroundColor Yellow

$appJson = Get-Content $appJsonPath -Raw | ConvertFrom-Json
$modified = $false

if ($appJson.PSObject.Properties.Name -contains "style" -and $appJson.style -eq "v2") {
    Write-Host "    检测到 `"style`": `"v2`"，正在移除..." -ForegroundColor Gray
    $appJson.PSObject.Properties.Remove("style")
    $modified = $true
} else {
    Write-Host "    app.json 配置正确（无需修改 style）" -ForegroundColor Green
}

if ($modified) {
    $appJsonContent = $appJson | ConvertTo-Json -Depth 10
    Set-Content -Path $appJsonPath -Value $appJsonContent -Encoding UTF8
    Write-Host "    已更新 app.json" -ForegroundColor Green
}

Write-Host ""
Write-Host "[4/4] 生成聊天页面模板..." -ForegroundColor Yellow

$scriptsDir = Join-Path $ProjectDir "scripts"
if (-not (Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Force -Path $scriptsDir | Out-Null
    Write-Host "    已创建 scripts/ 目录" -ForegroundColor Gray
}

# 复制 sse-client.js 到 scripts 目录
$sseClientSource = Join-Path $PSScriptRoot "sse-client.js"
$sseClientTarget = Join-Path $scriptsDir "sse-client.js"
if (Test-Path $sseClientSource) {
    Copy-Item -Path $sseClientSource -Destination $sseClientTarget -Force
    Write-Host "    已复制 sse-client.js" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "初始化完成！" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host ""
Write-Host "后续步骤:" -ForegroundColor Yellow
Write-Host "  1. 打开微信开发者工具" -ForegroundColor White
Write-Host "  2. 在工具栏中执行: 工具 -> 构建 npm" -ForegroundColor White
Write-Host "  3. 勾选: 将 JS 编译成 ES5" -ForegroundColor White
Write-Host "  4. 运行以下命令生成聊天页面:" -ForegroundColor White
Write-Host "     node scripts/create-chat-page.js pages/chat/chat" -ForegroundColor Cyan
Write-Host "  5. 将页面路径注册到 app.json 的 pages 数组中" -ForegroundColor White
Write-Host ""
