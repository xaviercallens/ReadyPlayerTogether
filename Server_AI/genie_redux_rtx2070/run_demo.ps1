# GenieRedux RTX 2070 - Demo Launcher (PowerShell)
# Runs the interactive world model demo on Windows

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GenieRedux RTX 2070 - Demo Launcher" -ForegroundColor Cyan
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
if (-not (Test-Path "demo_interactive.py")) {
    Write-Host "[ERROR] demo_interactive.py not found." -ForegroundColor Red
    Write-Host "Please run from: Server_AI\genie_redux_rtx2070\" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[GenieRedux] Starting interactive demo..." -ForegroundColor Yellow
Write-Host "[GenieRedux] Mode: Automatic (GPU if available, else simulation)" -ForegroundColor Yellow
Write-Host ""

# Run demo
python demo_interactive.py --mode auto

Write-Host ""
Write-Host "[GenieRedux] Demo finished." -ForegroundColor Green
Read-Host "Press Enter to exit"
