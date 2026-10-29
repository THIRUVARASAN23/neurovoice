@echo off
title Push NEURONEXUS to GitHub and Vercel
echo ======================================================================
echo           NEURONEXUS - Deploying to GitHub and Vercel
echo ======================================================================
echo.

set PATH=C:\Users\Asus\AppData\Local\GitHubDesktop\app-3.6.10\resources\app\git\cmd;%PATH%

echo Configuring Git Credential Manager...
git config credential.helper manager

echo.
echo Pushing commit 26740f2 to origin main...
echo (If a browser window opens, please click "Authorize" to complete the push)
echo.

git push origin main --force

echo.
if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo [SUCCESS] Pushed to GitHub successfully!
    echo Vercel is now building and deploying your site.
    echo ======================================================================
) else (
    echo ======================================================================
    echo [ERROR] Push did not complete. Please check the error above.
    echo ======================================================================
)

echo.
pause
