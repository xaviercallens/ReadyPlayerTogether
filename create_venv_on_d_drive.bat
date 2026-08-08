@echo off
REM OASIS - Create Python Virtual Environment on D: Drive
REM This avoids installing PyTorch on the full C: drive

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════
echo   OASIS - Create Python Virtual Environment on D: Drive
echo ════════════════════════════════════════════════════════════
echo.

REM Step 1: Create venv directory on D:
echo [OASIS] Step 1: Creating Python virtual environment on D:\...
set VENV_PATH=D:\xdev\Oasis\venv_pytorch
if exist "%VENV_PATH%" (
    echo [OASIS] + Virtual environment already exists at %VENV_PATH%
    echo [OASIS] + Skipping creation
) else (
    python -m venv "%VENV_PATH%"
    if errorlevel 1 (
        echo [OASIS] - Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OASIS] + Created virtual environment at %VENV_PATH%
)

REM Step 2: Activate venv
echo.
echo [OASIS] Step 2: Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"
echo [OASIS] + Virtual environment activated

REM Step 3: Upgrade pip in venv
echo.
echo [OASIS] Step 3: Upgrading pip in virtual environment...
python -m pip install --upgrade pip --no-cache-dir
echo [OASIS] + Pip upgraded

REM Step 4: Install PyTorch in venv
echo.
echo [OASIS] Step 4: Installing PyTorch in virtual environment...
echo [OASIS] This may take 10-15 minutes...
echo.

pip install --no-cache-dir torch==2.4.1+cu118 torchvision==0.19.1+cu118 --index-url https://download.pytorch.org/whl/cu118

if errorlevel 1 (
    echo.
    echo [OASIS] - PyTorch installation failed
    pause
    exit /b 1
)

echo.
echo [OASIS] + PyTorch installed successfully in virtual environment!

REM Step 5: Test PyTorch
echo.
echo [OASIS] Step 5: Testing PyTorch...
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
echo   Virtual Environment Ready!
echo ════════════════════════════════════════════════════════════
echo.

echo [OASIS] Virtual environment location: %VENV_PATH%
echo [OASIS] Activation command: %VENV_PATH%\Scripts\activate.bat
echo.

echo [OASIS] Next steps:
echo   1. Activate venv: %VENV_PATH%\Scripts\activate.bat
echo   2. Train model: python Server_AI\genie_redux_rtx2070\train.py
echo   3. Launch demo: python Server_AI\genie_redux_rtx2070\demo_pretrained.py
echo.

pause
