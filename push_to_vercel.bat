@echo off
title Push NEURONEXUS to GitHub & Vercel
echo ======================================================================
echo           NEURONEXUS - Deploying to GitHub & Vercel
echo ======================================================================
echo.

git status
echo.
echo Pushing latest clean build to origin main...
git push origin main --force

echo.
if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo [SUCCESS] Code pushed to GitHub! Vercel is now building your site.
    echo Check your Vercel dashboard: https://vercel.com/dashboard
    echo ======================================================================
) else (
    echo ======================================================================
    echo [NOTE] If prompted for GitHub login, please sign in above to complete.
    echo ======================================================================
)

echo.
pause
