# 多媒体依赖安装脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  多媒体摘要工具 - 依赖安装" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查虚拟环境
$venvPath = Join-Path $PSScriptRoot "new_venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "❌ 虚拟环境不存在，请先创建虚拟环境" -ForegroundColor Red
    exit 1
}

# 激活虚拟环境
Write-Host "📦 激活虚拟环境..." -ForegroundColor Yellow
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Host "✅ 虚拟环境已激活" -ForegroundColor Green
} else {
    Write-Host "❌ 激活脚本不存在" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host ""
Write-Host "🔧 开始安装多媒体处理依赖..." -ForegroundColor Yellow
Write-Host "这可能需要一些时间，请耐心等待..." -ForegroundColor Gray
Write-Host ""

$packages = @("moviepy", "openai-whisper", "ffmpeg-python")
$success = $true

foreach ($package in $packages) {
    Write-Host "安装 $package..." -ForegroundColor Yellow
    try {
        & pip install $package
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $package 安装成功！" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $package 安装可能有问题，请检查输出" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $package 安装失败: $_" -ForegroundColor Red
        $success = $false
    }
    Write-Host ""
}

# 验证安装
Write-Host "🔍 验证安装..." -ForegroundColor Yellow
try {
    $testScript = @"
try:
    import moviepy
    import whisper
    print('✅ 所有依赖导入成功！')
except ImportError as e:
    print(f'❌ 导入失败: {e}')
    exit(1)
"@
    $testScript | & python -
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "  🎉 所有依赖安装成功！" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "现在请重启服务器以启用视频/音频处理功能：" -ForegroundColor Cyan
        Write-Host "  1. 停止当前服务器 (Ctrl+C)" -ForegroundColor White
        Write-Host "  2. 重新运行: .\start_server.ps1" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "⚠️  安装验证失败，请检查错误信息" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ 验证失败: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
