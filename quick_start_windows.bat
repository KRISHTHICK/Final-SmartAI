@echo off
echo 🎨 SmartAI Fashion Platform - Quick Start
echo ==========================================

:: Add Node.js to PATH for this session
set "PATH=%PATH%;C:\Program Files\nodejs"

echo.
echo 🔍 Checking requirements...

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org/
    pause
    exit /b 1
)

:: Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Python: 
python --version
echo ✅ Node.js: 
node --version
echo ✅ npm: 
npm --version

echo.
echo 🚀 Quick Setup and Start...

:: Setup backend if needed
if not exist "backend\venv" (
    echo 📦 Setting up backend...
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    if not exist "static\generated" mkdir static\generated
    cd ..
)

:: Setup frontend if needed
if not exist "frontend\node_modules" (
    echo 📦 Setting up frontend...
    cd frontend
    npm install
    cd ..
)

echo.
echo 🎯 Starting Platform...

:: Start backend
echo 🚀 Starting backend...
start "SmartAI Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python main.py"

:: Wait a bit
timeout /t 3 /nobreak >nul

:: Start frontend
echo 🎨 Starting frontend...
start "SmartAI Frontend" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo 🎉 Platform is starting!
echo.
echo 🌐 URLs:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo.
echo ⏳ Wait for both servers to fully start (30-60 seconds)
echo 🌐 Frontend will open in browser automatically
echo.
pause