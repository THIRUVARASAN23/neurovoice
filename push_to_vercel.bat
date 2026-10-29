@echo off
title Deploy NEURONEXUS FastAPI to GitHub & Vercel
echo ======================================================================
echo           NEURONEXUS - Deploying FastAPI Backend to Vercel
echo ======================================================================
echo.

set PATH=C:\Users\Asus\AppData\Local\GitHubDesktop\app-3.6.10\resources\app\git\cmd;%PATH%

echo Latest commit:
git log -1 --oneline
echo.

echo Pushing to GitHub (origin main)...
git push origin main --force

echo.
if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo [SUCCESS] Code pushed to GitHub!
    echo Vercel is now deploying your FastAPI backend and static frontend.
    echo.
    echo Your endpoints will be available at:
    echo   - Web App:      https://neuroonexus.vercel.app/
    echo   - FastAPI Docs: https://neuroonexus.vercel.app/docs
    echo   - API Health:   https://neuroonexus.vercel.app/api/health
    echo ======================================================================
) else (
    echo ======================================================================
    echo [NOTE] If a browser window opened, click Authorize to complete push.
    echo ======================================================================
)

echo.
pause
