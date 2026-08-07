import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

def create_desktop_demo_launchers():
    print("[OASIS Promo Demo] Creating Desktop Demo launchers...")
    
    # 1. Batch File Launcher
    bat_content = """@echo off
title OASIS Ready Player One - Father & Son Desktop Showcase Demo
color 0A
echo =======================================================================
echo    WELCOME TO THE OASIS - READY PLAYER ONE DESKTOP SHOWCASE DEMO
echo    Mode Bureau (Desktop 3D) - Safe for father-son presentation without VR headset!
echo =======================================================================
echo.
echo Launching Godot 4 Client Engine...
cd /d "%~dp0"
start Godot4.exe "res://scenes/hub/oasis_master_rpo_movie.tscn"
echo.
echo Demo started successfully! Enjoy exploring the OASIS together!
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
