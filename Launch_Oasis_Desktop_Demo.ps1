# OASIS Ready Player One - Father & Son Desktop Showcase Launcher
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