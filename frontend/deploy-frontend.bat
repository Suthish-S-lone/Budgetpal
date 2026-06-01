@echo off
REM Frontend Deployment Script for BudgetPal (Windows)
REM This script prepares and deploys the frontend to Firebase Hosting

echo.
echo 🚀 BudgetPal Frontend Deployment
echo ================================
echo.

REM Check if config.prod.js exists
if not exist "frontend\config.prod.js" (
    echo ❌ Error: frontend\config.prod.js not found!
    echo Please create it from config.prod.js template
    exit /b 1
)

REM Backup local config if it exists
if exist "frontend\config.js" (
    echo 📦 Backing up local config.js...
    copy /Y "frontend\config.js" "frontend\config.js.backup" >nul
)

REM Copy production config
echo 📝 Using production configuration...
copy /Y "frontend\config.prod.js" "frontend\config.js" >nul

REM Deploy to Firebase Hosting
echo 🚀 Deploying to Firebase Hosting...
call firebase deploy --only hosting

REM Restore local config
if exist "frontend\config.js.backup" (
    echo 🔄 Restoring local config...
    move /Y "frontend\config.js.backup" "frontend\config.js" >nul
) else (
    echo 🧹 Cleaning up production config...
    del "frontend\config.js"
)

echo.
echo ✅ Deployment complete!
echo 🌐 Your app is live at: https://budgetpal-470505.web.app
echo.
pause