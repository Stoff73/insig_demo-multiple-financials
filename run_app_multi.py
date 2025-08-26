#!/usr/bin/env python3
"""
Multi-Company XP Power Analysis Application Runner

This script starts both the backend API server and the frontend development server
for the multi-company analysis system.
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def print_banner():
    """Print application startup banner"""
    print("=" * 60)
    print("XP POWER MULTI-COMPANY ANALYSIS SYSTEM")
    print("=" * 60)
    print()

def check_environment():
    """Check if the environment is properly set up"""
    # Check for .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found. Please create one with OPENAI_API_KEY")
        print("Example: OPENAI_API_KEY=your-api-key-here")
        return False
    
    # Check for required directories
    required_dirs = [
        "data/companies",
        "output/companies",
        "archive/companies",
        "frontend",
        "backend",
        "src/xp_power_demo"
    ]
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting Backend API Server (Multi-Company)...")
    print("-" * 40)
    
    # Use the multi-company backend
    backend_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main_multi:app",
        "--reload",
        "--port",
        "8000",
        "--host",
        "0.0.0.0"
    ]
    
    backend_process = subprocess.Popen(
        backend_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    return backend_process

def start_frontend():
    """Start the React frontend development server"""
    print("\n🎨 Starting Frontend Development Server...")
    print("-" * 40)
    
    frontend_dir = Path("frontend")
    
    # Install dependencies if node_modules doesn't exist
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        install_cmd = ["npm", "install"]
        subprocess.run(install_cmd, cwd=frontend_dir, check=True)
    
    # Start the frontend
    frontend_cmd = ["npm", "run", "dev"]
    
    frontend_process = subprocess.Popen(
        frontend_cmd,
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    return frontend_process

def monitor_processes(backend_proc, frontend_proc):
    """Monitor both processes and handle output"""
    print("\n" + "=" * 60)
    print("✅ Multi-Company Analysis System is running!")
    print("=" * 60)
    print("\n📍 Access the application at:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("\n🔹 Multi-Company Features:")
    print("   - Analyze up to 10 companies simultaneously")
    print("   - Company-specific data folders")
    print("   - Parallel or sequential processing")
    print("   - Individual company reports and archives")
    print("\nPress Ctrl+C to stop the servers\n")
    print("-" * 60)
    
    try:
        # Monitor both processes
        while True:
            # Check if processes are still running
            if backend_proc.poll() is not None:
                print("\n⚠️  Backend process stopped unexpectedly!")
                break
            if frontend_proc.poll() is not None:
                print("\n⚠️  Frontend process stopped unexpectedly!")
                break
            
            # Read and display output from backend
            backend_line = backend_proc.stdout.readline()
            if backend_line:
                print(f"[Backend] {backend_line.strip()}")
            
            # Read and display output from frontend
            frontend_line = frontend_proc.stdout.readline()
            if frontend_line:
                print(f"[Frontend] {frontend_line.strip()}")
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        
        # Terminate processes gracefully
        backend_proc.terminate()
        frontend_proc.terminate()
        
        # Wait for processes to end
        backend_proc.wait(timeout=5)
        frontend_proc.wait(timeout=5)
        
        print("✅ Servers stopped successfully")

def main():
    """Main entry point"""
    print_banner()
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    try:
        # Start servers
        backend_process = start_backend()
        frontend_process = start_frontend()
        
        # Monitor processes
        monitor_processes(backend_process, frontend_process)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()