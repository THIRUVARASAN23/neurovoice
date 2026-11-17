@echo off
title Deploy NEURONEXUS to GitHub & Vercel
echo ======================================================================
echo           NEURONEXUS - Deploying to GitHub & Vercel
echo ======================================================================
echo.

set PATH=C:\Users\Asus\AppData\Local\GitHubDesktop\app-3.6.10\resources\app\git\cmd;%PATH%

if not exist ".git" (
    echo Initializing Git repository...
    git init
    git branch -M main
    git remote add origin https://github.com/TanushreeProgrammer/neuronexus-extended.git
)

echo Staging all changes...
git add .

echo Committing changes...
git commit -m "Fix text encoding, character rendering, Vercel configuration, and server paths"

echo.
echo Pushing to GitHub (origin main)...
git push origin main --force

echo.
if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo [SUCCESS] Code pushed to GitHub!
    echo Vercel is now deploying your latest changes.
    echo.
    echo Your endpoints will be available at:
    echo   - Web App:      https://neuronexusx.vercel.app/
    echo   - FastAPI Docs: https://neuronexusx.vercel.app/docs
    echo   - API Health:   https://neuronexusx.vercel.app/api/health
    echo ======================================================================
) else (
    echo ======================================================================
    echo [NOTE] If a browser window opened, click Authorize to complete push.
    echo ======================================================================
)

echo.
pause

