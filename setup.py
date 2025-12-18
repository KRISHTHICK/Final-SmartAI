"""
SmartAI Fashion Platform Setup Script
Automated setup for the complete AI-driven fashion ecosystem
"""

import os
import subprocess
import sys
import platform
from pathlib import Path

def run_command(command, cwd=None, shell=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Need Python 3.8+")
        return False

def check_node_version():
    """Check if Node.js is installed"""
    success, output = run_command("node --version")
    if success:
        version = output.strip()
        print(f"✅ Node.js {version} found")
        return True
    else:
        print("❌ Node.js not found. Please install Node.js 16+ from https://nodejs.org/")
        return False

def setup_backend():
    """Set up the backend environment"""
    print("\n🔧 Setting up backend...")
    
    # Create virtual environment
    print("📦 Creating Python virtual environment...")
    success, output = run_command("python -m venv venv", cwd="backend")
    if not success:
        print(f"❌ Failed to create virtual environment: {output}")
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        pip_path = "backend/venv/Scripts/pip"
        python_path = "backend/venv/Scripts/python"
    else:
        pip_path = "backend/venv/bin/pip"
        python_path = "backend/venv/bin/python"
    
    print("📥 Installing Python dependencies...")
    success, output = run_command(f"{pip_path} install -r backend/requirements.txt")
    if not success:
        print(f"❌ Failed to install Python dependencies: {output}")
        return False
    
    # Create necessary directories
    os.makedirs("backend/static/generated", exist_ok=True)
    os.makedirs("backend/logs", exist_ok=True)
    
    print("✅ Backend setup completed")
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("\n🎨 Setting up frontend...")
    
    # Install npm dependencies
    print("📥 Installing Node.js dependencies...")
    success, output = run_command("npm install", cwd="frontend")
    if not success:
        print(f"❌ Failed to install Node.js dependencies: {output}")
        return False
    
    print("✅ Frontend setup completed")
    return True

def create_env_file():
    """Create environment configuration file"""
    print("\n⚙️ Creating environment configuration...")
    
    env_content = """# SmartAI Fashion Platform Environment Configuration

# API Keys (Optional - for enhanced features)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
REPLICATE_API_TOKEN=your_replicate_token_here

# Database Configuration
DATABASE_URL=sqlite:///smartai_fashion.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/smartai.log

# AI Model Configuration
USE_GPU=False
MODEL_CACHE_DIR=./model_cache
MAX_IMAGE_SIZE=2048

# WebSocket Configuration
WS_MAX_CONNECTIONS=100
WS_HEARTBEAT_INTERVAL=30

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_BURST=10

# File Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=["jpg", "jpeg", "png", "webp"]

# Sustainability Scoring
SUSTAINABILITY_WEIGHTS_MATERIALS=0.30
SUSTAINABILITY_WEIGHTS_PRODUCTION=0.25
SUSTAINABILITY_WEIGHTS_CERTIFICATIONS=0.20
SUSTAINABILITY_WEIGHTS_DURABILITY=0.15
SUSTAINABILITY_WEIGHTS_PACKAGING=0.10
"""
    
    with open("backend/.env", "w") as f:
        f.write(env_content)
    
    print("✅ Environment file created at backend/.env")
    print("📝 Please update the API keys in backend/.env for full functionality")

def create_startup_scripts():
    """Create startup scripts for easy development"""
    print("\n📜 Creating startup scripts...")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting SmartAI Fashion Platform...

echo.
echo 🚀 Starting Backend Server...
start "Backend" cmd /k "cd backend && venv\\Scripts\\activate && python main.py"

timeout /t 3 /nobreak > nul

echo.
echo 🎨 Starting Frontend Server...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo ✅ SmartAI Fashion Platform is starting up!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
pause
"""
    
    with open("start_windows.bat", "w") as f:
        f.write(windows_script)
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "Starting SmartAI Fashion Platform..."

echo ""
echo "🚀 Starting Backend Server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

sleep 3

echo ""
echo "🎨 Starting Frontend Server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ SmartAI Fashion Platform is running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
"""
    
    with open("start_unix.sh", "w") as f:
        f.write(unix_script)
    
    # Make Unix script executable
    if platform.system() != "Windows":
        os.chmod("start_unix.sh", 0o755)
    
    print("✅ Startup scripts created")

def main():
    """Main setup function"""
    print("🎨 SmartAI Fashion Platform Setup")
    print("=" * 50)
    
    # Check system requirements
    print("\n🔍 Checking system requirements...")
    
    if not check_python_version():
        return False
    
    if not check_node_version():
        return False
    
    # Setup backend
    if not setup_backend():
        return False
    
    # Setup frontend
    if not setup_frontend():
        return False
    
    # Create configuration files
    create_env_file()
    create_startup_scripts()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update API keys in backend/.env (optional)")
    print("2. Run the platform:")
    
    if platform.system() == "Windows":
        print("   - Windows: Double-click start_windows.bat")
    else:
        print("   - Unix/Mac: ./start_unix.sh")
    
    print("   - Or manually:")
    print("     Backend: cd backend && venv/Scripts/activate && python main.py")
    print("     Frontend: cd frontend && npm start")
    
    print("\n🌐 Access URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000")
    print("   API Documentation: http://localhost:8000/docs")
    
    print("\n💡 Features available:")
    print("   ✅ Real-time AI styling")
    print("   ✅ Cultural fusion creation")
    print("   ✅ Sustainable marketplace")
    print("   ✅ WebSocket real-time updates")
    print("   ✅ User management & history")
    print("   ✅ Analytics dashboard")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        sys.exit(1)