# Launch_Oasis.ps1 - Launcher for Projet OASIS VR (Godot 4)
$GodotExe = "C:\Users\Utilisateur\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_win64.exe"
$ProjectPath = "D:\xdev\Oasis"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "🚀 Launching Projet OASIS VR in Godot 4..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

Stop-Process -Name "Godot*" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

Start-Process $GodotExe -ArgumentList "-e --path `"$ProjectPath`""
