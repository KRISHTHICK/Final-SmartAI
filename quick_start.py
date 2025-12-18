#!/usr/bin/env python3
"""
Quick Start - Get Best in Me Agent Working Like Yesterday
"""

import subprocess
import sys
import time
import os

def start_backend():
    """Start the Best in Me Agent backend"""
    print("🚀 Starting Best in Me Agent Backend...")
    
    # Change to backend directory and start the simple backend
    os.chdir('demo1/backend')
    
    try:
        # Start the backend process
        process = subprocess.Popen([sys.executable, 'simple_best_in_me.py'])
        print(f"✅ Backend started with PID: {process.pid}")
        print("   Backend running on: http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the React frontend"""
    print("\n🎨 Starting React Frontend...")
    
    # Change to frontend directory
    os.chdir('../frontend')
    
    try:
        # Start the frontend process
        env = os.environ.copy()
        env['PATH'] += ';C:\\Program Files\\nodejs'
        
        process = subprocess.Popen(['npm', 'start'], env=env)
        print(f"✅ Frontend started with PID: {process.pid}")
        print("   Frontend will be on: http://localhost:3000")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    """Main function to start everything"""
    print("🎨 SmartAI Fashion Platform - Quick Start")
    print("=" * 50)
    print("Getting Best in Me Agent working like yesterday...")
    print()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend")
        return
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend")
        backend_process.terminate()
        return
    
    print("\n" + "=" * 50)
    print("🎉 SmartAI Fashion Platform is starting!")
    print()
    print("🌐 Access URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:8000")
    print()
    print("📱 To test Best in Me Agent:")
    print("   1. Go to http://localhost:3000")
    print("   2. Click 'Style Studio' in navigation")
    print("   3. Upload pose image + outfit image")
    print("   4. Enter event details (e.g., 'wedding at hotel')")
    print("   5. Click 'Analyze Inputs' → 'Get AI Suggestions' → 'Generate Image'")
    print()
    print("⏳ Wait 30-60 seconds for both servers to fully start...")
    print("🌐 Frontend will open automatically when ready")
    print()
    print("Press Ctrl+C to stop both servers")
    
    try:
        # Keep both processes running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Stopping SmartAI Fashion Platform...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ All processes stopped")

if __name__ == "__main__":
    main()