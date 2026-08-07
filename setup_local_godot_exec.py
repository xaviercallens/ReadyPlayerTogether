import os
import shutil

BASE_DIR = r"D:\xdev\Oasis"
GODOT_SRC = r"C:\Users\Utilisateur\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_win64.exe"
GODOT_DEST = os.path.join(BASE_DIR, "Godot4.exe")

if os.path.exists(GODOT_SRC):
    shutil.copy2(GODOT_SRC, GODOT_DEST)
    print(f"Copied Godot 4 executable directly to: {GODOT_DEST}")
else:
    print(f"Godot source executable not found at: {GODOT_SRC}")

# Update Launch_Oasis.bat to use the local Godot4.exe
BAT_CONTENT = """@echo off
echo ===================================================
echo  Lancement du Projet OASIS (Mode Bureau Godot 4)
echo ===================================================
cd /d "%~dp0"
start Godot4.exe --path "%~dp0"
"""

with open(os.path.join(BASE_DIR, "Launch_Oasis.bat"), "w", encoding="utf-8") as f:
    f.write(BAT_CONTENT)

print("Launch_Oasis.bat updated with direct local Godot4.exe!")
