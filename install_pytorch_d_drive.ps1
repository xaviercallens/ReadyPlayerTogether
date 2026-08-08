# OASIS - Install PyTorch on D: Drive
# Configures temp directories and installs PyTorch with CUDA 11.8

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  OASIS - PyTorch Installation on D: Drive                  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create temp directory on D:
Write-Host "[OASIS] Step 1: Creating temporary directory on D:\" -ForegroundColor Yellow
$tempDir = "D:\xdev\Oasis\temp"
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    Write-Host "[OASIS] + Created: $tempDir" -ForegroundColor Green
} else {
    Write-Host "[OASIS] + Already exists: $tempDir" -ForegroundColor Green
}

# Step 2: Set environment variables
Write-Host ""
Write-Host "[OASIS] Step 2: Setting environment variables..." -ForegroundColor Yellow
$env:TEMP = $tempDir
$env:TMP = $tempDir
[Environment]::SetEnvironmentVariable("TEMP", $tempDir, "User")
[Environment]::SetEnvironmentVariable("TMP", $tempDir, "User")
Write-Host "[OASIS] + TEMP = $tempDir" -ForegroundColor Green
Write-Host "[OASIS] + TMP = $tempDir" -ForegroundColor Green

# Step 3: Clean pip cache
Write-Host ""
Write-Host "[OASIS] Step 3: Cleaning pip cache..." -ForegroundColor Yellow
pip cache purge 2>&1 | Out-Null
Write-Host "[OASIS] + Pip cache cleaned" -ForegroundColor Green

# Step 4: Configure pip for D: drive
Write-Host ""
Write-Host "[OASIS] Step 4: Configuring pip for D: drive..." -ForegroundColor Yellow
$pipConfigDir = "$env:APPDATA\pip"
if (-not (Test-Path $pipConfigDir)) {
    New-Item -ItemType Directory -Path $pipConfigDir -Force | Out-Null
}
$pipConfig = "[global]`ncache-dir = D:\xdev\Oasis\pip_cache`nindex-url = https://pypi.org/simple/"
$pipConfig | Out-File -FilePath "$pipConfigDir\pip.ini" -Encoding UTF8 -Force
Write-Host "[OASIS] + Pip configured for D:\xdev\Oasis\pip_cache" -ForegroundColor Green

# Step 5: Check disk space
Write-Host ""
Write-Host "[OASIS] Step 5: Checking disk space..." -ForegroundColor Yellow
$driveC = Get-Volume -DriveLetter C
$driveD = Get-Volume -DriveLetter D
$cFree = [math]::Round($driveC.SizeRemaining / 1GB, 2)
$dFree = [math]::Round($driveD.SizeRemaining / 1GB, 2)
Write-Host "[OASIS] + C: $cFree GB free" -ForegroundColor Cyan
Write-Host "[OASIS] + D: $dFree GB free" -ForegroundColor Cyan

# Step 6: Install PyTorch
Write-Host ""
Write-Host "[OASIS] Step 6: Installing PyTorch with CUDA 11.8..." -ForegroundColor Yellow
Write-Host "[OASIS] This may take 5-10 minutes..." -ForegroundColor Yellow
Write-Host ""

pip install --upgrade torch==2.4.1+cu118 torchvision==0.19.1+cu118 --index-url https://download.pytorch.org/whl/cu118

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OASIS] + PyTorch installed successfully!" -ForegroundColor Green
    
    # Test PyTorch
    Write-Host ""
    Write-Host "[OASIS] Step 7: Testing PyTorch..." -ForegroundColor Yellow
    $pythonTest = @"
import torch
print('PyTorch version:', torch.__version__)
print('CUDA available:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('Device:', torch.cuda.get_device_name(0))
else:
    print('Device: CPU')
"@
    $pythonTest | python
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OASIS] + PyTorch test passed!" -ForegroundColor Green
    } else {
        Write-Host "[OASIS] - PyTorch test failed" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "[OASIS] - PyTorch installation failed!" -ForegroundColor Red
    Write-Host "[OASIS] Please check disk space and try again" -ForegroundColor Red
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Installation Complete!                                    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "[OASIS] Next steps:" -ForegroundColor Cyan
Write-Host "  1. Train model: .\Server_AI\genie_redux_rtx2070\run_training.ps1" -ForegroundColor Cyan
Write-Host "  2. Launch demo: .\Server_AI\genie_redux_rtx2070\launch_demo.ps1" -ForegroundColor Cyan
Write-Host ""
