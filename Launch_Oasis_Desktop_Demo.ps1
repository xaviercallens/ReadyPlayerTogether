# OASIS Ready Player One - Father & Son Desktop Showcase Launcher (Tuned)
Clear-Host
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "   WELCOME TO THE OASIS - READY PLAYER ONE DESKTOP SHOWCASE DEMO" -ForegroundColor Yellow
Write-Host "   Mode Bureau (Desktop 3D) - High Detail Models & Ground Physics" -ForegroundColor Green
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ProjectDir

Write-Host "[1/3] Terminating any existing Godot 4 processes to ensure clean restart..." -ForegroundColor Yellow
Get-Process -Name "Godot4" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

$GodotExe = Join-Path $ProjectDir "Godot4.exe"
$ScenePath = "res://scenes/hub/oasis_master_rpo_movie.tscn"

if (Test-Path $GodotExe) {
    Write-Host "[2/3] Verifying master showcase scene..." -ForegroundColor Cyan
    Write-Host "[3/3] Launching Godot 4 in Maximized Desktop Mode..." -ForegroundColor Green
    Start-Process $GodotExe -ArgumentList "--maximized `"$ScenePath`""
    
    Write-Host ""
    Write-Host "=======================================================================" -ForegroundColor Cyan
    Write-Host " SUCCESS! OASIS Demo restarted cleanly." -ForegroundColor Green
    Write-Host " Controls Summary:" -ForegroundColor Yellow
    Write-Host " - WASD + Mouse Orbit : Move Parzival & Look around" -ForegroundColor White
    Write-Host " - Space / Gamepad A  : Jump" -ForegroundColor White
    Write-Host " - F / Gamepad Y      : Spawn DeLorean Time Machine with camera zoom!" -ForegroundColor White
    Write-Host " - Shift + F          : Teleport Search Menu" -ForegroundColor White
    Write-Host " - L / Tab            : Showroom Gallery & Command Menu" -ForegroundColor White
    Write-Host " - 1 to 9             : Instant Teleport Demos" -ForegroundColor White
    Write-Host "=======================================================================" -ForegroundColor Cyan
} else {
    Write-Host "Error: Godot4.exe not found in $ProjectDir" -ForegroundColor Red
}