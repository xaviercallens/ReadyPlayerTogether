@echo off
REM Setup GenieRedux RTX 2070 environment on Windows
REM Reinstalls PyTorch with CUDA 11.8 which is compatible with RTX 2070 drivers.

echo [OASIS] Setting up GenieRedux RTX 2070 environment...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10 or 3.11.
    exit /b 1
)

REM Install PyTorch with CUDA 11.8 for RTX 2070 compatibility
echo [OASIS] Installing PyTorch with CUDA 11.8...
pip install --upgrade torch==2.4.1+cu118 torchvision==0.19.1+cu118 --index-url https://download.pytorch.org/whl/cu118

REM Install common dependencies
echo [OASIS] Installing common dependencies...
pip install numpy pillow opencv-python

echo [OASIS] Setup complete. Test with: python -c "import torch; print(torch.cuda.is_available())"
pause
