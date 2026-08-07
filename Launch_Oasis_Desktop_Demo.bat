@echo off
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
if not exist "scenes\hub\oasis_master_rpo_movie.tscn" (
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