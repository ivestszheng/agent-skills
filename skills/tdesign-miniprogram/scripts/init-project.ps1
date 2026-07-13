# TDesign Miniprogram - 项目初始化脚本
# 用法: 在小程序项目根目录执行 pwsh -File scripts/init-project.ps1

param(
    [string]$ProjectDir = (Get-Location)
)

$ErrorActionPreference = "Stop"

Write-Host "=" * 50 -ForegroundColor Cyan
Write-Host "TDesign Miniprogram - 项目初始化" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

$appJsonPath = Join-Path $ProjectDir "app.json"
if (-not (Test-Path $appJsonPath)) {
    Write-Host "[错误] 未找到 app.json，请确保在微信小程序项目根目录中执行此脚本。" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[1/5] 检查 package.json..." -ForegroundColor Yellow

if (-not (Test-Path (Join-Path $ProjectDir "package.json"))) {
    Write-Host "    未找到 package.json，正在初始化 npm..." -ForegroundColor Gray
    npm init -y
    Write-Host "    已初始化 npm" -ForegroundColor Green
} else {
    Write-Host "    package.json 已存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/5] 安装 tdesign-miniprogram..." -ForegroundColor Yellow
npm install tdesign-miniprogram -S --production
Write-Host "    安装完成" -ForegroundColor Green

Write-Host ""
Write-Host "[3/5] 检查 app.json..." -ForegroundColor Yellow

$appJson = Get-Content $appJsonPath -Raw | ConvertFrom-Json
$modified = $false

if ($appJson.PSObject.Properties.Name -contains "style" -and $appJson.style -eq "v2") {
    Write-Host "    检测到 `"style`": `"v2`"，正在移除..." -ForegroundColor Gray
    $appJson.PSObject.Properties.Remove("style")
    $modified = $true
} else {
    Write-Host "    app.json 配置正确（无需修改 style）" -ForegroundColor Green
}

if (-not $appJson.PSObject.Properties.Name -contains "usingComponents") {
    Write-Host "    添加 usingComponents 配置..." -ForegroundColor Gray
    $appJson | Add-Member -MemberType NoteProperty -Name "usingComponents" -Value @{}
    $modified = $true
} else {
    Write-Host "    usingComponents 已配置" -ForegroundColor Green
}

if ($modified) {
    $appJsonContent = $appJson | ConvertTo-Json -Depth 10
    Set-Content -Path $appJsonPath -Value $appJsonContent -Encoding UTF8
    Write-Host "    已更新 app.json" -ForegroundColor Green
}

Write-Host ""
Write-Host "[4/5] 配置 project.config.json..." -ForegroundColor Yellow

$projectConfigPath = Join-Path $ProjectDir "project.config.json"
if (Test-Path $projectConfigPath) {
    $projectConfig = Get-Content $projectConfigPath -Raw | ConvertFrom-Json
    $pcModified = $false

    if (-not $projectConfig.PSObject.Properties.Name -contains "setting") {
        $projectConfig | Add-Member -MemberType NoteProperty -Name "setting" -Value @{}
        $pcModified = $true
    }

    if (-not $projectConfig.setting.PSObject.Properties.Name -contains "packNpmManually") {
        $projectConfig.setting | Add-Member -MemberType NoteProperty -Name "packNpmManually" -Value $true
        $pcModified = $true
    }

    if (-not $projectConfig.setting.PSObject.Properties.Name -contains "packNpmRelationList") {
        $projectConfig.setting | Add-Member -MemberType NoteProperty -Name "packNpmRelationList" -Value @(@{
            "packageJsonPath" = "./package.json"
            "miniprogramNpmDistDir" = "./"
        })
        $pcModified = $true
    }

    if ($pcModified) {
        $projectConfigContent = $projectConfig | ConvertTo-Json -Depth 10
        Set-Content -Path $projectConfigPath -Value $projectConfigContent -Encoding UTF8
        Write-Host "    已更新 project.config.json" -ForegroundColor Green
    } else {
        Write-Host "    project.config.json 配置正确" -ForegroundColor Green
    }
} else {
    Write-Host "    未找到 project.config.json，跳过此步骤" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[5/5] 复制脚本工具..." -ForegroundColor Yellow

$scriptsDir = Join-Path $ProjectDir "scripts"
if (-not (Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Force -Path $scriptsDir | Out-Null
    Write-Host "    已创建 scripts/ 目录" -ForegroundColor Gray
}

$sourceDir = $PSScriptRoot
$scriptFiles = @("create-page.js", "mock-server.py")
foreach ($file in $scriptFiles) {
    $sourcePath = Join-Path $sourceDir $file
    $targetPath = Join-Path $scriptsDir $file
    if (Test-Path $sourcePath) {
        Copy-Item -Path $sourcePath -Destination $targetPath -Force
        Write-Host "    已复制 $file" -ForegroundColor Gray
    }
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
Write-Host "  4. 运行以下命令生成页面模板:" -ForegroundColor White
Write-Host "     node scripts/create-page.js home" -ForegroundColor Cyan
Write-Host "     node scripts/create-page.js list" -ForegroundColor Cyan
Write-Host "     node scripts/create-page.js form" -ForegroundColor Cyan
Write-Host "     node scripts/create-page.js detail" -ForegroundColor Cyan
Write-Host ""