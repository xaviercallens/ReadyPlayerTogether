@echo off
title OASIS Ready Player One - Father and Son Desktop Showcase Demo
color 0A
echo =======================================================================
echo    WELCOME TO THE OASIS - READY PLAYER ONE DESKTOP SHOWCASE DEMO
echo    Mode Bureau (Desktop 3D) - Safe for presentation without VR headset!
echo =======================================================================
echo.
echo Launching Godot 4 Client Engine...
cd /d "%~dp0"
start Godot4.exe "res://scenes/hub/oasis_master_rpo_movie.tscn"
echo.
echo Demo started successfully! Enjoy exploring the OASIS together!