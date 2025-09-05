#!/usr/bin/env python
"""Debug script for running backend with visible crew output.

This script demonstrates how to run the backend with full console output
visibility for debugging CrewAI execution.

ISSUE FIXED: Crew output not visible in console when running the application.
SOLUTION: Remove stdout capture from subprocess calls to allow crew.kickoff()
          output to flow directly to the terminal.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run backend with visible crew output for debugging."""
    print("=" * 60)
    print("RUNNING BACKEND WITH VISIBLE CREW OUTPUT")
    print("=" * 60)
    print()
    print("This script runs the backend without capturing stdout,")
    print("allowing all CrewAI output to be visible in the console.")
    print()
    print("Starting backend on http://localhost:8000")
    print("API docs available at http://localhost:8000/docs")
    print()
    print("When you trigger an analysis from the web UI,")
    print("you'll see all crew execution output here.")
    print("=" * 60)
    print()
    
    # Use venv Python if available
    venv_python = Path(__file__).parent / ".venv" / "bin" / "python"
    if venv_python.exists():
        python_executable = str(venv_python)
    else:
        python_executable = sys.executable
    
    # Run backend WITHOUT capturing stdout
    # This is the key difference - no stdout=subprocess.PIPE
    subprocess.run([
        python_executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--log-level", "info"
    ])

if __name__ == "__main__":
    main()