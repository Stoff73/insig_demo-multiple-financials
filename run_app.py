#!/usr/bin/env python
"""Start the Insig AI Analysis application.

This module launches both the FastAPI backend server and the React
frontend development server for the Insig Analyst financial analysis
system. It handles process management and cleanup.
"""

import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

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
    env = os.environ.copy()
    backend_process = subprocess.Popen(
        [
            python_executable, "-m", "uvicorn", 
            "backend.main:app",
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "info"
        ],
        cwd=Path(__file__).parent,
        env=env,
        # Don't capture output initially to see what's happening
        stdout=None,
        stderr=None
    )
    
    # Wait for backend to start and check if it's running
    print("Waiting for backend to start...")
    backend_started = False
    for i in range(20):  # Try for 20 seconds
        # Give it a moment to start before checking
        time.sleep(1)
        
        # Check if process died
        if backend_process.poll() is not None:
            print(f"Error: Backend process exited with code {backend_process.poll()}")
            sys.exit(1)
        
        # Check if port is open
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()
            if result == 0:
                backend_started = True
                print("Backend started successfully!")
                break
        except Exception as e:
            pass  # Keep trying
    
    if not backend_started:
        print("Error: Backend failed to start within 20 seconds")
        print("Attempting to check if port is in use...")
        os.system("lsof -i:8000")
        backend_process.terminate()
        sys.exit(1)
    
    # Start frontend
    print("Starting React frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_dir)
    
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        env=env,
        stdout=None,
        stderr=None
    )
    
    print("=" * 40)
    print("Application started successfully!")
    print("Frontend: http://localhost:5173")  # Vite dev server port
    print("Backend API: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("")
    print("Press Ctrl+C to stop all services")
    print("=" * 40)
    
    # Function to handle shutdown
    def shutdown(signum=None, frame=None):
        print("\nStopping services...")
        try:
            backend_process.terminate()
            frontend_process.terminate()
            # Give processes time to terminate gracefully
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if still running
            backend_process.kill()
            frontend_process.kill()
        except Exception:
            pass
        print("Services stopped.")
        sys.exit(0)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    
    try:
        # Monitor processes
        while True:
            # Check if either process has died
            backend_poll = backend_process.poll()
            frontend_poll = frontend_process.poll()
            
            if backend_poll is not None:
                print(f"\nBackend process exited with code {backend_poll}")
                shutdown()
                
            if frontend_poll is not None:
                print(f"\nFrontend process exited with code {frontend_poll}")
                shutdown()
            
            # Small sleep to avoid busy waiting
            time.sleep(1)
            
    except KeyboardInterrupt:
        shutdown()

if __name__ == "__main__":
    main()