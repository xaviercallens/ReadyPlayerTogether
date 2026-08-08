@echo off
REM GenieRedux RTX 2070 - Demo Launcher
REM Runs the interactive world model demo on Windows

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   GenieRedux RTX 2070 - Demo Launcher
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
if not exist "demo_interactive.py" (
    echo [ERROR] demo_interactive.py not found. Please run from Server_AI\genie_redux_rtx2070\
    pause
    exit /b 1
)

echo [GenieRedux] Starting interactive demo...
echo [GenieRedux] Mode: Automatic (GPU if available, else simulation)
echo.

REM Run demo
python demo_interactive.py --mode auto

echo.
echo [GenieRedux] Demo finished.
pause
