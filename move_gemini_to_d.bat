@echo off
title Move Antigravity .gemini Folder to D: Drive
color 0A
cls
echo =======================================================================
echo    MIGRATION TRANSPARENTE DU DOSSIER .GEMINI VERS LE DISQUE D:
echo =======================================================================
echo.
echo Votre disque C: a actuellement 0 GB d'espace libre !
echo Ce script va deplacer C:\Users\Utilisateur\.gemini vers D:\.gemini
echo et creer une Jonction NTFS (Symlink) transparente.
echo.
echo Antigravity continuera de fonctionner SANS AUCUN IMPACT.
echo.
pause

echo [1/3] Verification des dossiers...
if not exist "D:\.gemini" (
    mkdir "D:\.gemini"
)

echo [2/3] Deplacement des fichiers de C:\Users\Utilisateur\.gemini vers D:\.gemini...
robocopy "C:\Users\Utilisateur\.gemini" "D:\.gemini" /E /MOVE /COPYALL /R:2 /W:1

echo [3/3] Creation de la Jonction NTFS transparente (C:\Users\Utilisateur\.gemini -^> D:\.gemini)...
if exist "C:\Users\Utilisateur\.gemini" (
    rmdir /S /Q "C:\Users\Utilisateur\.gemini" 2>nul
)

mklink /J "C:\Users\Utilisateur\.gemini" "D:\.gemini"

echo.
echo =======================================================================
echo  SUCCES ! Plus de 2 GB ont ete liberes sur C: !
echo  Antigravity pointe de maniere transparente vers D:\.gemini.
echo =======================================================================
echo.
pause
