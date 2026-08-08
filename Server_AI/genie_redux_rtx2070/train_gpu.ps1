# OASIS - Train TinyWorldModel on RTX 2070 GPU
# Uses PyTorch environment on E: drive

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  OASIS - Train TinyWorldModel on RTX 2070 GPU              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Detect PyTorch environment location
$venvPath = "E:\venv_pytorch"
if (-not (Test-Path $venvPath)) {
    $venvPath = "D:\venv_pytorch"
}

if (-not (Test-Path $venvPath)) {
    Write-Host "[OASIS] - Virtual environment not found!" -ForegroundColor Red
    Write-Host "[OASIS] Please run: install_pytorch_e_drive.bat" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Activate virtual environment
Write-Host "[OASIS] Step 1: Activating PyTorch environment from $venvPath..." -ForegroundColor Yellow
& "$venvPath\Scripts\Activate.ps1"
Write-Host "[OASIS] + Virtual environment activated" -ForegroundColor Green

# Step 2: Set training configuration
Write-Host ""
Write-Host "[OASIS] Step 2: Configuring training parameters..." -ForegroundColor Yellow
$epochs = 50
$batchSize = 32
$learningRate = 0.001
$device = "cuda"
Write-Host "[OASIS] + Epochs: $epochs" -ForegroundColor Cyan
Write-Host "[OASIS] + Batch size: $batchSize" -ForegroundColor Cyan
Write-Host "[OASIS] + Learning rate: $learningRate" -ForegroundColor Cyan
Write-Host "[OASIS] + Device: $device (RTX 2070)" -ForegroundColor Cyan

# Step 3: Generate dataset
Write-Host ""
Write-Host "[OASIS] Step 3: Generating synthetic dataset..." -ForegroundColor Yellow
python dataset.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[OASIS] - Dataset generation failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OASIS] + Dataset generated successfully" -ForegroundColor Green

# Step 4: Train model on GPU
Write-Host ""
Write-Host "[OASIS] Step 4: Training TinyWorldModel on GPU..." -ForegroundColor Yellow
Write-Host "[OASIS] This will take 5-10 minutes on RTX 2070..." -ForegroundColor Yellow
Write-Host ""

python train.py --epochs $epochs --batch_size $batchSize --learning_rate $learningRate --device $device

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[OASIS] - Training failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Training Complete!                                        ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "[OASIS] Model saved to: checkpoints\best_model.pt" -ForegroundColor Green
Write-Host "[OASIS] Next steps:" -ForegroundColor Cyan
Write-Host "  1. Launch demo: python demo_pretrained.py --mode pytorch" -ForegroundColor Cyan
Write-Host "  2. Or run: launch_demo.bat" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
