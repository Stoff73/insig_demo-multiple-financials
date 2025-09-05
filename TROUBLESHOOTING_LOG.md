# Troubleshooting Log - Insig Analyst Demo

## Summary of Issues Resolved

This document details the critical issues encountered with the financial analysis application and their resolutions.

## Issue 1: Python 3.13 Compatibility Breaking CrewAI

### Problem
- Application was broken with Python 3.13.5
- CrewAI failed to initialize properly
- Crew wouldn't start when triggered from UI

### Root Cause
CrewAI and its dependencies are not compatible with Python 3.13+ due to breaking changes in the Python ecosystem.

### Solution
1. **Downgraded Python to 3.12.11**
   ```bash
   # Removed old venv
   rm -rf .venv
   
   # Created new venv with Python 3.12
   python3.12 -m venv .venv
   source .venv/bin/activate
   
   # Reinstalled all dependencies
   pip install -r requirements.txt
   ```

2. **Updated Configuration Files**
   - `pyproject.toml`: Changed `python = ">=3.10,<3.14"` to `python = ">=3.10,<=3.12"`
   - `run_app.py`: Added Python version check to enforce 3.10-3.12
   - `CLAUDE.md`: Added CRITICAL warning about Python version requirement

### Result
Application now runs reliably with Python 3.12.

---

## Issue 2: Virtual Environment in Wrong Location

### Problem
Virtual environment was initially created in parent directory instead of application root.

### Root Cause
Confusion about the correct working directory for the application.

### Solution
Moved `.venv` to the application root directory (`/Users/Chris/Desktop/insig/demo/insig_analyst_demo/`).

### Result
Virtual environment now properly located at application root.

---

## Issue 3: Backend Hanging on Startup

### Problem
Backend would hang indefinitely when starting with uvicorn.

### Root Cause
`backend/main.py` contained an `if __name__ == "__main__":` block that caused recursive import when uvicorn tried to load the module:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)
```

### Solution
Removed the problematic if-main block from `backend/main.py`. The backend should be started via:
```bash
python -m uvicorn backend.main:app
```

### Result
Backend now starts cleanly without hanging.

---

## Issue 4: Crew Output Not Visible in Console

### Problem
- When running the application, crew execution happened in the background
- No agent activities, tool usage, or ratio calculations visible in terminal
- User couldn't see what the crew was doing

### Root Cause
In `run_app.py`, the backend process was created with `stdout=subprocess.PIPE`:
```python
backend_process = subprocess.Popen(
    [...],
    stdout=subprocess.PIPE,  # This captured all output
    stderr=subprocess.PIPE,
    ...
)
```
This captured all stdout output, including crew.kickoff() messages, preventing them from appearing in the terminal.

### Solution
Removed stdout capture from subprocess calls in `run_app.py`:
```python
backend_process = subprocess.Popen(
    [...],
    # Don't capture stdout - let it flow to console
    stderr=subprocess.PIPE,  # Only capture errors
    ...
)
```

Applied same fix to:
- Main backend process startup
- Alternative port fallback
- Frontend process startup

### Result
Now when running `python run_app.py`, all CrewAI output appears directly in the terminal:
- Crew kickoff messages
- Agent activities and thoughts
- Tool executions (file reads, calculations)
- Ratio calculations
- Task progress

---

## Files Modified

### Critical Files Changed
1. **backend/main.py** - Removed if-main block causing recursive import
2. **run_app.py** - Removed stdout capture to show crew output
3. **pyproject.toml** - Enforced Python <=3.12
4. **CLAUDE.md** - Added critical warnings and troubleshooting sections

### Files Created
1. **debug_backend.py** - Debug script for running backend with visible output
2. **TROUBLESHOOTING_LOG.md** - This document

---

## Testing Commands

### Verify Python Version
```bash
python --version  # Should show 3.10.x, 3.11.x, or 3.12.x
```

### Test Import
```bash
python -c "import backend.main; import src.insig_analyst_demo.crew; print('Imports successful')"
```

### Run Application with Visible Output
```bash
.venv/bin/python run_app.py
```

### Debug Backend Only
```bash
.venv/bin/python debug_backend.py
```

---

## Current Status

All issues have been resolved. The application now:
- Runs on Python 3.12.11
- Shows all crew execution output in the console
- Starts without hanging
- Has proper virtual environment location

When you run the application and trigger an analysis, you will see:
1. Backend starting up with uvicorn logs
2. Frontend starting with Vite logs  
3. When analysis is triggered: Full CrewAI execution output including agents, tools, and calculations

---

## Prevention Guidelines

To prevent similar issues in the future:
1. Always use Python 3.10-3.12 (not 3.13+)
2. Never add `if __name__ == "__main__":` blocks to FastAPI apps loaded by uvicorn
3. When debugging crew execution, ensure stdout is not captured by subprocess
4. Keep virtual environment in application root directory
5. Test imports after any major dependency changes