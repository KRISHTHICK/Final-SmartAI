@echo off
echo 🎨 SmartAI Fashion Platform - Windows Setup
echo ================================================

echo.
echo 🔍 Checking Node.js installation...

:: Add Node.js to PATH for this session
set "PATH=%PATH%;C:\Program Files\nodejs"

:: Check if Node.js is available
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js from https://nodejs.org/
    echo    Make sure to check "Add to PATH" during installation
    pause
    exit /b 1
)

:: Check npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm not found with Node.js
    pause
    exit /b 1
)

echo ✅ Node.js found: 
node --version
echo ✅ npm found: 
npm --version

echo.
echo 🔧 Setting up Backend...
cd backend

:: Create virtual environment
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

:: Activate virtual environment and install dependencies
echo 📥 Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

:: Create necessary directories
if not exist "static\generated" mkdir static\generated
if not exist "logs" mkdir logs

echo ✅ Backend setup complete!

cd ..

echo.
echo 🎨 Setting up Frontend...
cd frontend

:: Install npm dependencies
echo 📥 Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Frontend setup complete!

cd ..

echo.
echo 🎉 Setup Complete!
echo.
echo 🚀 To start the platform:
echo    1. Run: start_platform.bat
echo    2. Or manually:
echo       Backend: cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo       Frontend: cd frontend ^&^& npm start
echo.
echo 🌐 Access URLs:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
pause