@echo off
REM OASIS - Simple PyTorch Installation on D: Drive

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════
echo   OASIS - PyTorch Installation on D: Drive
echo ════════════════════════════════════════════════════════════
echo.

REM Step 1: Create temp directory on D:
echo [OASIS] Step 1: Creating temporary directory on D:\
if not exist "D:\xdev\Oasis\temp" (
    mkdir "D:\xdev\Oasis\temp"
    echo [OASIS] + Created: D:\xdev\Oasis\temp
) else (
    echo [OASIS] + Already exists: D:\xdev\Oasis\temp
)

REM Step 2: Set environment variables
echo.
echo [OASIS] Step 2: Setting environment variables...
setx TEMP "D:\xdev\Oasis\temp"
setx TMP "D:\xdev\Oasis\temp"
set TEMP=D:\xdev\Oasis\temp
set TMP=D:\xdev\Oasis\temp
echo [OASIS] + TEMP = D:\xdev\Oasis\temp
echo [OASIS] + TMP = D:\xdev\Oasis\temp

REM Step 3: Clean pip cache
echo.
echo [OASIS] Step 3: Cleaning pip cache...
pip cache purge >nul 2>&1
echo [OASIS] + Pip cache cleaned

REM Step 4: Configure pip for D: drive
echo.
echo [OASIS] Step 4: Configuring pip for D: drive...
if not exist "%APPDATA%\pip" mkdir "%APPDATA%\pip"
(
    echo [global]
    echo cache-dir = D:\xdev\Oasis\pip_cache
    echo index-url = https://pypi.org/simple/
) > "%APPDATA%\pip\pip.ini"
echo [OASIS] + Pip configured for D:\xdev\Oasis\pip_cache

REM Step 5: Install PyTorch
echo.
echo [OASIS] Step 5: Installing PyTorch with CUDA 11.8...
echo [OASIS] This may take 5-10 minutes...
echo.

pip install --upgrade torch==2.4.1+cu118 torchvision==0.19.1+cu118 --index-url https://download.pytorch.org/whl/cu118

if errorlevel 1 (
    echo.
    echo [OASIS] - PyTorch installation failed!
    echo [OASIS] Please check disk space and try again
    pause
    exit /b 1
)

echo.
echo [OASIS] + PyTorch installed successfully!

REM Step 6: Test PyTorch
echo.
echo [OASIS] Step 6: Testing PyTorch...
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"

if errorlevel 1 (
    echo [OASIS] - PyTorch test failed
) else (
    echo [OASIS] + PyTorch test passed!
)

echo.
echo ════════════════════════════════════════════════════════════
echo   Installation Complete!
echo ════════════════════════════════════════════════════════════
echo.

echo [OASIS] Next steps:
echo   1. Train model: .\Server_AI\genie_redux_rtx2070\run_training.bat
echo   2. Launch demo: .\Server_AI\genie_redux_rtx2070\launch_demo.bat
echo.

pause
