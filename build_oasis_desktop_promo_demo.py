import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

def create_desktop_demo_launchers():
    print("[OASIS Promo Demo] Creating Tuned Desktop Demo launchers...")
    
    # 1. Batch File Launcher
    bat_content = """@echo off
title OASIS Ready Player One - Father and Son Desktop Showcase Demo
color 0A
cls
echo =======================================================================
echo    WELCOME TO THE OASIS - READY PLAYER ONE DESKTOP SHOWCASE DEMO
echo    Mode Bureau (Desktop 3D) - High Detail Models & Ground Physics
echo =======================================================================
echo.

:: Ensure working directory is set correctly
cd /d "%~dp0"

echo [1/3] Closing any previously running Godot 4 instances...
taskkill /F /IM Godot4.exe /T 2>nul
timeout /t 1 /nobreak >nul

echo [2/3] Verifying master showcase scene configuration...
if not exist "scenes\\hub\\oasis_master_rpo_movie.tscn" (
    echo Building Master RPO Movie Showcase Scene...
    python build_master_rpo_movie_oasis.py
)

echo [3/3] Launching Godot 4 Client Engine in Maximized Desktop Mode...
start "" Godot4.exe --maximized "res://scenes/hub/oasis_master_rpo_movie.tscn"

echo.
echo =======================================================================
echo  SUCCESS! OASIS Demo restarted cleanly.
echo.
echo  Controls Summary:
echo  - WASD + Mouse Orbit : Move Parzival & Look around
echo  - Space / Gamepad A  : Jump
echo  - F / Gamepad Y      : Spawn DeLorean Time Machine with camera zoom!
echo  - Shift + F          : Teleport Search Menu
echo  - L / Tab            : Showroom Gallery & Command Menu
echo  - 1 to 9             : Instant Teleport Demos
echo =======================================================================
echo.
pause
"""
    write_file(os.path.join(BASE_DIR, "Launch_Oasis_Desktop_Demo.bat"), bat_content)

    # 2. PowerShell Launcher
    ps1_content = """# OASIS Ready Player One - Father & Son Desktop Showcase Launcher
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "   WELCOME TO THE OASIS - READY PLAYER ONE DESKTOP SHOWCASE DEMO" -ForegroundColor Yellow
Write-Host "   Mode Bureau (Desktop 3D) - Safe for father-son presentation without VR headset!" -ForegroundColor Green
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ProjectDir

$GodotExe = Join-Path $ProjectDir "Godot4.exe"
if (Test-Path $GodotExe) {
    Write-Host "Launching Godot 4 with Master RPO Movie Showcase Scene..." -ForegroundColor Cyan
    Start-Process $GodotExe -ArgumentList "`"res://scenes/hub/oasis_master_rpo_movie.tscn`""
    Write-Host "OASIS Demo launched! Have fun exploring together!" -ForegroundColor Green
} else {
    Write-Host "Error: Godot4.exe not found in $ProjectDir" -ForegroundColor Red
}
"""
    write_file(os.path.join(BASE_DIR, "Launch_Oasis_Desktop_Demo.ps1"), ps1_content)

    print("[OASIS Promo Demo] Created Launch_Oasis_Desktop_Demo.bat and Launch_Oasis_Desktop_Demo.ps1!")

if __name__ == "__main__":
    create_desktop_demo_launchers()
