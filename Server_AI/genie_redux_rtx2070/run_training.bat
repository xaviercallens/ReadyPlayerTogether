@echo off
REM GenieRedux RTX 2070 - Training Launcher
REM Trains the TinyWorldModel on synthetic data

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   GenieRedux RTX 2070 - Training
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10 or 3.11.
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist "train.py" (
    echo [ERROR] train.py not found. Please run from Server_AI\genie_redux_rtx2070\
    pause
    exit /b 1
)

echo [GenieRedux] Generating dataset if missing...
python dataset.py

echo.
echo [GenieRedux] Starting training...
echo [GenieRedux] Batch size: 64, Epochs: 30
echo [GenieRedux] This should take 5-10 minutes on RTX 2070
echo.

REM Run training
python train.py --batch_size 64 --epochs 30

echo.
echo [GenieRedux] Training finished. Models saved in checkpoints\
pause
