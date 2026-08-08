@echo off
REM OASIS - Install PyTorch on E: or D: Drive (Avoid C: completely)
REM Creates venv and installs PyTorch with all temp files on E: or D:

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════
echo   OASIS - PyTorch Installation on E: or D: Drive
echo ════════════════════════════════════════════════════════════
echo.

REM Detect available drive (E: preferred, fallback to D:)
set INSTALL_DRIVE=D:
if exist E:\ (
    set INSTALL_DRIVE=E:
    echo [OASIS] + Detected E: drive, using it for installation
) else (
    echo [OASIS] + E: drive not found, using D: drive
)

REM Step 1: Create directories on target drive
echo.
echo [OASIS] Step 1: Creating directories on %INSTALL_DRIVE%\...
set VENV_PATH=%INSTALL_DRIVE%\venv_pytorch
set TEMP_PATH=%INSTALL_DRIVE%\pytorch_temp
set PIP_CACHE=%INSTALL_DRIVE%\pip_cache

if not exist "%TEMP_PATH%" mkdir "%TEMP_PATH%"
if not exist "%PIP_CACHE%" mkdir "%PIP_CACHE%"
echo [OASIS] + Created directories on %INSTALL_DRIVE%\

REM Step 2: Set environment variables to use target drive
echo.
echo [OASIS] Step 2: Configuring environment variables...
set TEMP=%TEMP_PATH%
set TMP=%TEMP_PATH%
set PIP_CACHE_DIR=%PIP_CACHE%
setx TEMP "%TEMP_PATH%"
setx TMP "%TEMP_PATH%"
echo [OASIS] + TEMP = %TEMP_PATH%
echo [OASIS] + TMP = %TEMP_PATH%
echo [OASIS] + PIP_CACHE_DIR = %PIP_CACHE%

REM Step 3: Create virtual environment on target drive
echo.
echo [OASIS] Step 3: Creating Python virtual environment on %INSTALL_DRIVE%\...
if exist "%VENV_PATH%" (
    echo [OASIS] + Virtual environment already exists
) else (
    python -m venv "%VENV_PATH%"
    if errorlevel 1 (
        echo [OASIS] - Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OASIS] + Created virtual environment at %VENV_PATH%
)

REM Step 4: Activate virtual environment
echo.
echo [OASIS] Step 4: Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"
echo [OASIS] + Virtual environment activated

REM Step 5: Upgrade pip with no-cache
echo.
echo [OASIS] Step 5: Upgrading pip...
python -m pip install --upgrade pip --no-cache-dir
echo [OASIS] + Pip upgraded

REM Step 6: Install PyTorch with explicit cache directory
echo.
echo [OASIS] Step 6: Installing PyTorch with CUDA 11.8...
echo [OASIS] Using %INSTALL_DRIVE%\ for all temporary files...
echo [OASIS] This may take 10-15 minutes...
echo.

pip install --no-cache-dir --cache-dir "%PIP_CACHE%" torch==2.4.1+cu118 torchvision==0.19.1+cu118 --index-url https://download.pytorch.org/whl/cu118

if errorlevel 1 (
    echo.
    echo [OASIS] - PyTorch installation failed
    echo [OASIS] Checking disk space...
    dir %INSTALL_DRIVE%\ | find "bytes free"
    pause
    exit /b 1
)

echo.
echo [OASIS] + PyTorch installed successfully!

REM Step 7: Test PyTorch
echo.
echo [OASIS] Step 7: Testing PyTorch...
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"

if errorlevel 1 (
    echo [OASIS] - PyTorch test failed
    pause
    exit /b 1
) else (
    echo [OASIS] + PyTorch test passed!
)

echo.
echo ════════════════════════════════════════════════════════════
echo   PyTorch Installation Complete!
echo ════════════════════════════════════════════════════════════
echo.

echo [OASIS] Installation location: %VENV_PATH%
echo [OASIS] Temp location: %TEMP_PATH%
echo [OASIS] Pip cache: %PIP_CACHE%
echo.

echo [OASIS] Next steps:
echo   1. Activate venv: %VENV_PATH%\Scripts\activate.bat
echo   2. Train model: python Server_AI\genie_redux_rtx2070\train.py
echo   3. Launch demo: python Server_AI\genie_redux_rtx2070\demo_pretrained.py
echo.

pause
