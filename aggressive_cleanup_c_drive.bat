@echo off
REM OASIS - Aggressive Cleanup of C: Drive
REM Safely removes temporary files and caches to free up space for PyTorch

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════
echo   OASIS - Aggressive C: Drive Cleanup
echo ════════════════════════════════════════════════════════════
echo.

echo [OASIS] WARNING: This script will delete temporary files.
echo [OASIS] These are safe to delete, but please review before proceeding.
echo.

REM Step 1: Clean Windows Temp
echo [OASIS] Step 1: Cleaning C:\Windows\Temp...
for /d %%x in (C:\Windows\Temp\*) do @rd /s /q "%%x" 2>nul
for %%x in (C:\Windows\Temp\*) do @del /q "%%x" 2>nul
echo [OASIS] + Cleaned C:\Windows\Temp

REM Step 2: Clean User Temp
echo [OASIS] Step 2: Cleaning user Temp...
for /d %%x in ("%USERPROFILE%\AppData\Local\Temp\*") do @rd /s /q "%%x" 2>nul
for %%x in ("%USERPROFILE%\AppData\Local\Temp\*") do @del /q "%%x" 2>nul
echo [OASIS] + Cleaned user Temp

REM Step 3: Clean pip cache
echo [OASIS] Step 3: Cleaning pip cache...
if exist "%APPDATA%\pip" (
    rd /s /q "%APPDATA%\pip" 2>nul
    echo [OASIS] + Cleaned pip cache
)

REM Step 4: Clean Python cache directories
echo [OASIS] Step 4: Cleaning Python __pycache__...
for /d /r C:\Users %%x in (__pycache__) do @rd /s /q "%%x" 2>nul
echo [OASIS] + Cleaned Python cache

REM Step 5: Clean Windows Update cache
echo [OASIS] Step 5: Cleaning Windows Update cache...
if exist "C:\Windows\SoftwareDistribution\Download" (
    for /d %%x in ("C:\Windows\SoftwareDistribution\Download\*") do @rd /s /q "%%x" 2>nul
    for %%x in ("C:\Windows\SoftwareDistribution\Download\*") do @del /q "%%x" 2>nul
    echo [OASIS] + Cleaned Windows Update cache
)

REM Step 6: Empty Recycle Bin
echo [OASIS] Step 6: Emptying Recycle Bin...
rd /s /q "%SystemRoot%\$Recycle.bin" 2>nul
echo [OASIS] + Emptied Recycle Bin

echo.
echo ════════════════════════════════════════════════════════════
echo   Cleanup Complete!
echo ════════════════════════════════════════════════════════════
echo.

echo [OASIS] Next: Run fix_pytorch_install.bat
echo.

pause
