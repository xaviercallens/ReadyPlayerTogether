@echo off
REM OASIS - Fix PyTorch Installation (Clean & Reinstall)

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════
echo   OASIS - Fix PyTorch Installation
echo ════════════════════════════════════════════════════════════
echo.

REM Step 1: Set temp directories to D:
echo [OASIS] Step 1: Configuring temp directories to D:\
set TEMP=D:\xdev\Oasis\temp
set TMP=D:\xdev\Oasis\temp
setx TEMP "D:\xdev\Oasis\temp"
setx TMP "D:\xdev\Oasis\temp"
if not exist "D:\xdev\Oasis\temp" mkdir "D:\xdev\Oasis\temp"
echo [OASIS] + TEMP and TMP set to D:\xdev\Oasis\temp

REM Step 2: Uninstall broken PyTorch
echo.
echo [OASIS] Step 2: Uninstalling broken PyTorch...
pip uninstall torch torchvision -y 2>nul
echo [OASIS] + PyTorch uninstalled

REM Step 3: Clean pip cache
echo.
echo [OASIS] Step 3: Cleaning pip cache...
pip cache purge >nul 2>&1
echo [OASIS] + Pip cache cleaned

REM Step 4: Configure pip to use D: drive
echo.
echo [OASIS] Step 4: Configuring pip for D: drive...
if not exist "%APPDATA%\pip" mkdir "%APPDATA%\pip"
(
    echo [global]
    echo cache-dir = D:\xdev\Oasis\pip_cache
    echo index-url = https://pypi.org/simple/
) > "%APPDATA%\pip\pip.ini"
echo [OASIS] + Pip configured for D:\xdev\Oasis\pip_cache

REM Step 5: Upgrade pip
echo.
echo [OASIS] Step 5: Upgrading pip...
python -m pip install --upgrade pip --no-cache-dir
echo [OASIS] + Pip upgraded

REM Step 6: Install PyTorch (no cache, direct to D:)
echo.
echo [OASIS] Step 6: Installing PyTorch with CUDA 11.8...
echo [OASIS] Using D: drive for all temporary files...
echo [OASIS] This may take 10-15 minutes...
echo.

pip install --no-cache-dir --upgrade torch==2.4.1+cu118 torchvision==0.19.1+cu118 --index-url https://download.pytorch.org/whl/cu118

if errorlevel 1 (
    echo.
    echo [OASIS] - Installation failed!
    echo [OASIS] Checking disk space...
    dir C:\ | find "bytes free"
    pause
    exit /b 1
)

echo.
echo [OASIS] + PyTorch installed successfully!

REM Step 7: Test PyTorch
echo.
echo [OASIS] Step 7: Testing PyTorch...
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"

if errorlevel 1 (
    echo [OASIS] - PyTorch test failed
    pause
    exit /b 1
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
