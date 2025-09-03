#!/usr/bin/env python
"""
Start the Insig AI Analysis application
"""
import subprocess
import sys
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file before anything else
load_dotenv()

def main():
    print("Starting Insig AI Analysis System...")
    print("=" * 40)
    
    # Kill any existing processes on our ports
    print("Cleaning up existing processes...")
    # Use subprocess without shell=True to avoid command injection
    try:
        # Get PIDs on port 8000
        result = subprocess.run(['lsof', '-ti:8000'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        pass  # lsof might not be available on all systems
    
    try:
        # Get PIDs on port 3000
        result = subprocess.run(['lsof', '-ti:3000'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        pass  # lsof might not be available on all systems
    
    # Use venv Python if available, otherwise system Python
    venv_python = Path(__file__).parent / ".venv" / "bin" / "python"
    python_executable = str(venv_python) if venv_python.exists() else sys.executable
    
    # Start backend
    print("Starting FastAPI backend...")
    backend_process = subprocess.Popen(
        [python_executable, "-m", "uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=Path(__file__).parent
    )
    
    # Wait for backend to start
    print("Waiting for backend to start...")
    time.sleep(3)
    
    # Start frontend
    print("Starting React frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_dir)
    
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir
    )
    
    print("=" * 40)
    print("Application started successfully!")
    print("Frontend: http://localhost:3000")
    print("Backend API: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("")
    print("Press Ctrl+C to stop all services")
    print("=" * 40)
    
    try:
        # Wait for processes
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("Services stopped.")

if __name__ == "__main__":
    main()