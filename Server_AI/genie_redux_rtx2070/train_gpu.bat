@echo off
REM OASIS - Train TinyWorldModel on RTX 2070 GPU
REM Uses PyTorch environment on E: drive

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════
echo   OASIS - Train TinyWorldModel on RTX 2070 GPU
echo ════════════════════════════════════════════════════════════
echo.

REM Detect PyTorch environment location
set VENV_PATH=E:\venv_pytorch
if not exist "%VENV_PATH%" (
    set VENV_PATH=D:\venv_pytorch
)

if not exist "%VENV_PATH%" (
    echo [OASIS] - Virtual environment not found!
    echo [OASIS] Please run: install_pytorch_e_drive.bat
    pause
    exit /b 1
)

REM Step 1: Activate virtual environment
echo [OASIS] Step 1: Activating PyTorch environment from %VENV_PATH%...
call "%VENV_PATH%\Scripts\activate.bat"
echo [OASIS] + Virtual environment activated

REM Step 2: Set training configuration
echo.
echo [OASIS] Step 2: Configuring training parameters...
set EPOCHS=50
set BATCH_SIZE=32
set LR=0.001
set DATA_DIR=data
set OUTPUT_DIR=checkpoints
echo [OASIS] + Epochs: %EPOCHS%
echo [OASIS] + Batch size: %BATCH_SIZE%
echo [OASIS] + Learning rate: %LR%
echo [OASIS] + Device: CUDA (RTX 2070)

REM Step 3: Generate dataset
echo.
echo [OASIS] Step 3: Generating synthetic dataset...
python dataset.py
if errorlevel 1 (
    echo [OASIS] - Dataset generation failed
    pause
    exit /b 1
)
echo [OASIS] + Dataset generated successfully

REM Step 4: Train model on GPU
echo.
echo [OASIS] Step 4: Training TinyWorldModel on GPU...
echo [OASIS] This will take 5-10 minutes on RTX 2070...
echo.

python train.py --epochs %EPOCHS% --batch_size %BATCH_SIZE% --lr %LR% --data_dir %DATA_DIR% --output_dir %OUTPUT_DIR%

if errorlevel 1 (
    echo.
    echo [OASIS] - Training failed
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════
echo   Training Complete!
echo ════════════════════════════════════════════════════════════
echo.

echo [OASIS] Model saved to: checkpoints\best_model.pt
echo [OASIS] Next steps:
echo   1. Launch demo: python demo_pretrained.py --mode pytorch
echo   2. Or run: launch_demo.bat
echo.

pause
