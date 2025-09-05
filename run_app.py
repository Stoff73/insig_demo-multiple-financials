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

def cleanup_stale_processes():
    """Clean up any stale processes from previous runs.
    
    This function ensures ports are free and no zombie processes remain.
    """
    ports_to_clean = [8000, 8001, 3000, 5173]
    
    for port in ports_to_clean:
        try:
            result = subprocess.run(
                ['lsof', f'-ti:{port}'], 
                capture_output=True, 
                text=True,
                timeout=2
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        subprocess.run(
                            ['kill', '-9', pid], 
                            capture_output=True,
                            timeout=1
                        )
                        print(f"  Killed process {pid} on port {port}")
                    except subprocess.SubprocessError:
                        pass
        except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
    
    # Also clean up any lingering uvicorn or node processes
    try:
        subprocess.run(
            ['pkill', '-f', 'uvicorn.*backend.main:app'],
            capture_output=True,
            timeout=2
        )
    except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    try:
        subprocess.run(
            ['pkill', '-f', 'npm.*run.*dev'],
            capture_output=True,
            timeout=2
        )
    except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Give system time to release ports
    time.sleep(1)

def verify_environment():
    """Verify the environment is properly set up.
    
    Returns:
        bool: True if environment is valid, False otherwise.
    """
    # Check Python version - CRITICAL: Must use Python 3.12 or below
    if sys.version_info < (3, 10) or sys.version_info >= (3, 13):
        print(f"Error: Python version {sys.version_info.major}.{sys.version_info.minor} is not supported.")
        print("CRITICAL: Please use Python 3.10, 3.11, or 3.12 (3.12 recommended for stability)")
        print("Python 3.13+ causes compatibility issues with CrewAI")
        return False
    
    # Check if .env file exists and has required variables
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        print("Warning: .env file not found. Make sure OPENAI_API_KEY is set.")
    
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set it in your .env file or environment.")
        return False
    
    return True

def main():
    print("Starting Insig AI Analysis System...")
    print("=" * 40)
    
    # Verify environment first
    if not verify_environment():
        sys.exit(1)
    
    # Clean up any stale processes
    print("Cleaning up existing processes...")
    cleanup_stale_processes()
    
    # Use venv Python if available (check current directory first, then parent)
    venv_python = Path(__file__).parent / ".venv" / "bin" / "python"
    if not venv_python.exists():
        venv_python = Path(__file__).parent.parent / ".venv" / "bin" / "python"
    
    if venv_python.exists():
        python_executable = str(venv_python)
        print(f"  Using virtual environment Python: {python_executable}")
    else:
        python_executable = sys.executable
        print(f"  Warning: No virtual environment found, using system Python: {python_executable}")
    
    # Create backend directory if it doesn't exist
    backend_dir = Path(__file__).parent / "backend"
    backend_dir.mkdir(exist_ok=True)
    
    # Ensure tasks.json exists and is writable
    tasks_file = backend_dir / "tasks.json"
    if not tasks_file.exists():
        tasks_file.write_text("{}")
        print("  Created empty tasks.json file")
    # Fix corrupted tasks.json
    try:
        import json
        with open(tasks_file, 'r') as f:
            json.load(f)
    except (json.JSONDecodeError, Exception):
        print("  Fixed corrupted tasks.json")
        tasks_file.write_text("{}")
    
    # Start backend
    print("Starting FastAPI backend...")
    env = os.environ.copy()
    
    # Let stdout through so crew output is visible in console
    backend_process = subprocess.Popen(
        [
            python_executable, "-m", "uvicorn", 
            "backend.main:app",
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "info",
            "--timeout-keep-alive", "75"
        ],
        cwd=Path(__file__).parent,
        env=env,
        # Don't capture stdout - let it flow to console
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Monitor backend startup with better error reporting
    print("Waiting for backend to start...")
    backend_started = False
    error_output = []
    
    for i in range(30):  # Try for 30 seconds
        time.sleep(1)
        
        # Check if process died
        if backend_process.poll() is not None:
            print(f"\nError: Backend process exited with code {backend_process.poll()}")
            
            # Capture any error output
            if backend_process.stderr:
                stderr_output = backend_process.stderr.read()
                if stderr_output:
                    print("\nBackend error output:")
                    print(stderr_output)
            
            # Try alternative port if 8000 is blocked
            print("\nAttempting to start on alternative port 8001...")
            backend_process = subprocess.Popen(
                [
                    python_executable, "-m", "uvicorn", 
                    "backend.main:app",
                    "--host", "0.0.0.0", 
                    "--port", "8001",
                    "--log-level", "info"
                ],
                cwd=Path(__file__).parent,
                env=env,
                # Don't capture stdout - let it flow to console
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(2)
            
            # Check alternative port
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', 8001))
                sock.close()
                if result == 0:
                    backend_started = True
                    print("Backend started successfully on port 8001!")
                    print("Note: API will be available at http://localhost:8001")
                    break
            except Exception:
                pass
            
            if not backend_started:
                print("Failed to start on alternative port as well.")
                backend_process.terminate()
                sys.exit(1)
        
        # Check if port 8000 is open
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', 8000))
            sock.close()
            if result == 0:
                backend_started = True
                print("Backend started successfully!")
                break
        except Exception:
            pass
        
        # Show progress
        if i % 5 == 0 and i > 0:
            print(f"  Still waiting... ({i} seconds)")
    
    if not backend_started:
        print("\nError: Backend failed to start within 30 seconds")
        
        # Show any captured errors
        if backend_process.stderr:
            stderr_output = backend_process.stderr.read()
            if stderr_output:
                print("\nBackend error output:")
                print(stderr_output)
        
        backend_process.terminate()
        sys.exit(1)
    
    # Start frontend
    print("Starting React frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Verify frontend directory exists
    if not frontend_dir.exists():
        print(f"Error: Frontend directory not found at {frontend_dir}")
        backend_process.terminate()
        sys.exit(1)
    
    # Check if package.json exists
    if not (frontend_dir / "package.json").exists():
        print(f"Error: package.json not found in {frontend_dir}")
        backend_process.terminate()
        sys.exit(1)
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("  Installing frontend dependencies...")
        result = subprocess.run(
            ["npm", "install"], 
            cwd=frontend_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("Error installing frontend dependencies:")
            print(result.stderr)
            backend_process.terminate()
            sys.exit(1)
    
    # Kill any process on port 5173 first
    try:
        subprocess.run(
            ['lsof', '-ti:5173'], 
            capture_output=True,
            timeout=1
        )
    except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        env=env,
        # Don't capture output - let it flow to console
        text=True,
        bufsize=1
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
        # Simple monitoring - just check if processes are still running
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
            time.sleep(2)
            
    except KeyboardInterrupt:
        shutdown()
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        shutdown()

if __name__ == "__main__":
    main()