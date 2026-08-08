# GenieRedux RTX 2070 - Training Launcher (PowerShell)
# Trains the TinyWorldModel on synthetic data

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GenieRedux RTX 2070 - Training" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[GenieRedux] Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Please install Python 3.10 or 3.11." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if in correct directory
if (-not (Test-Path "train.py")) {
    Write-Host "[ERROR] train.py not found." -ForegroundColor Red
    Write-Host "Please run from: Server_AI\genie_redux_rtx2070\" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[GenieRedux] Generating dataset if missing..." -ForegroundColor Yellow
python dataset.py

Write-Host ""
Write-Host "[GenieRedux] Starting training..." -ForegroundColor Yellow
Write-Host "[GenieRedux] Batch size: 64, Epochs: 30" -ForegroundColor Yellow
Write-Host "[GenieRedux] This should take 5-10 minutes on RTX 2070" -ForegroundColor Yellow
Write-Host ""

# Run training
python train.py --batch_size 64 --epochs 30

Write-Host ""
Write-Host "[GenieRedux] Training finished. Models saved in checkpoints\" -ForegroundColor Green
Read-Host "Press Enter to exit"
