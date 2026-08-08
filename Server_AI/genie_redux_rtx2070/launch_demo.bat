@echo off
REM GenieRedux - Launch Pretrained Model Demo
REM Demonstrates the world model concept with trained or pretrained checkpoint

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════
echo   GenieRedux - World Model Demonstration
echo ════════════════════════════════════════════════════════════
echo.

REM Navigate to demo directory
cd /d "D:\xdev\Oasis\Server_AI\genie_redux_rtx2070"

REM Check if checkpoint exists
if exist "checkpoints\best_model.pt" (
    echo [GenieRedux] Found trained model: checkpoints\best_model.pt
    echo [GenieRedux] Launching demo with trained TinyWorldModel...
) else (
    echo [GenieRedux] Trained model not found at: checkpoints\best_model.pt
    echo [GenieRedux] Will use simulation mode (no GPU required)
)

echo.
echo [GenieRedux] Demo Configuration:
echo   - Frames: 300
echo   - FPS: 25
echo   - Mode: Auto (GPU if available, else simulation)
echo.

echo [GenieRedux] Starting demo...
echo.

REM Run demo
python demo_pretrained.py --frames 300 --fps 25 --mode auto

echo.
echo ════════════════════════════════════════════════════════════
echo   Demo Complete!
echo ════════════════════════════════════════════════════════════
echo.

echo [GenieRedux] Concept demonstrated:
echo   + Interactive world model (action ^→ prediction ^→ frame)
echo   + Real-time frame generation
echo   + Keyboard-driven gameplay simulation
echo.

echo [GenieRedux] Next steps:
echo   1. Train model longer: .\run_training.bat
echo   2. Integrate with Godot 2D frontend
echo   3. Connect to WebSocket backend
echo.

pause
