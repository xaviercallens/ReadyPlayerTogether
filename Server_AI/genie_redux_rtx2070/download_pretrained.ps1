# GenieRedux RTX 2070 - Download Pretrained Models (PowerShell)
# Downloads lightweight pretrained models from Hugging Face

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GenieRedux - Download Pretrained Models" -ForegroundColor Cyan
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

Write-Host "[GenieRedux] Installing huggingface_hub if needed..." -ForegroundColor Yellow
pip install huggingface_hub --quiet

Write-Host ""
Write-Host "[GenieRedux] Starting download..." -ForegroundColor Yellow
Write-Host "[GenieRedux] Note: Full GenieRedux models require 24-80GB VRAM." -ForegroundColor Yellow
Write-Host "[GenieRedux] For RTX 2070 demo, we'll use lightweight distilled versions." -ForegroundColor Yellow
Write-Host ""

# Run download script
python download_pretrained.py

Write-Host ""
Write-Host "[GenieRedux] Download complete!" -ForegroundColor Green
Write-Host "[GenieRedux] Models saved in: checkpoints\" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
