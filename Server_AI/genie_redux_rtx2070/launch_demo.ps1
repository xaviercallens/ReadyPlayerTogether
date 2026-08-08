# GenieRedux - Launch Pretrained Model Demo
# Demonstrates the world model concept with trained or pretrained checkpoint

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  GenieRedux - World Model Demonstration                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Navigate to demo directory
Set-Location "D:\xdev\Oasis\Server_AI\genie_redux_rtx2070"

# Check if checkpoint exists
$checkpointPath = "checkpoints\best_model.pt"
if (Test-Path $checkpointPath) {
    Write-Host "[GenieRedux] ✓ Found trained model: $checkpointPath" -ForegroundColor Green
    Write-Host "[GenieRedux] Launching demo with trained TinyWorldModel..." -ForegroundColor Yellow
} else {
    Write-Host "[GenieRedux] ⚠ Trained model not found at: $checkpointPath" -ForegroundColor Yellow
    Write-Host "[GenieRedux] Will use simulation mode (no GPU required)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[GenieRedux] Demo Configuration:" -ForegroundColor Cyan
Write-Host "  - Frames: 300" -ForegroundColor Cyan
Write-Host "  - FPS: 25" -ForegroundColor Cyan
Write-Host "  - Mode: Auto (GPU if available, else simulation)" -ForegroundColor Cyan
Write-Host ""

Write-Host "[GenieRedux] Starting demo..." -ForegroundColor Yellow
Write-Host ""

# Run demo
python demo_pretrained.py --frames 300 --fps 25 --mode auto

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  Demo Complete!                                            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "[GenieRedux] Concept demonstrated:" -ForegroundColor Cyan
Write-Host "  ✓ Interactive world model (action → prediction → frame)" -ForegroundColor Green
Write-Host "  ✓ Real-time frame generation" -ForegroundColor Green
Write-Host "  ✓ Keyboard-driven gameplay simulation" -ForegroundColor Green
Write-Host ""

Write-Host "[GenieRedux] Next steps:" -ForegroundColor Cyan
Write-Host "  1. Train model longer: .\run_training.ps1" -ForegroundColor Cyan
Write-Host "  2. Integrate with Godot 2D frontend" -ForegroundColor Cyan
Write-Host "  3. Connect to WebSocket backend" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
