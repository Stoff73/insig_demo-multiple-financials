"""FastAPI backend server for Insig Analyst financial analysis system.

This module provides REST API endpoints for:
- Running financial analysis using CrewAI
- Managing analysis tasks and their status
- File upload/conversion for company data
- Configuration management for agents and tasks
- Rules and ratio configuration management
- Archive management for historical analyses
"""

# Standard library imports
import asyncio
import json
import os
import shutil
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Third-party imports
import yaml
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Add src to path for crew imports
sys.path.append(str(Path(__file__).parent.parent / "src"))
from src.insig_analyst_demo.crew import InsigAnalystDemo

# Add backend to path for modules
sys.path.append(str(Path(__file__).parent))

# Local imports
try:
    from core.archive import archive_existing_outputs as core_archive_outputs
    from core.config import (
        ALLOWED_DOCUMENT_EXTENSIONS,
        BACKEND_HOST,
        BACKEND_PORT,
        CORS_ORIGINS,
        MAX_FILE_SIZE,
        MAX_TASKS,
        TASK_RETENTION_HOURS,
        TASK_TIMEOUT_MINUTES,
    )
    from core.file_utils import list_files_in_directory, save_file_with_timestamp
    from core.pdf_converter import (
        PDFToMarkdownConverter as BestPDFToMarkdownConverter,
    )
    USE_CORE_MODULES = True
except ImportError:
    # Fallback to original imports if core modules not available
    from pdf_converter_best import BestPDFToMarkdownConverter
    USE_CORE_MODULES = False
    # Default values if core config not available
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]
    MAX_TASKS = 100
    TASK_RETENTION_HOURS = 24
    TASK_TIMEOUT_MINUTES = 30
    BACKEND_HOST = "0.0.0.0"
    BACKEND_PORT = 8000
    ALLOWED_DOCUMENT_EXTENSIONS = [
        '.md', '.pdf', '.txt', '.csv', '.xlsx', '.docx'
    ]
    MAX_FILE_SIZE = 100 * 1024 * 1024

from ratio_config_manager import RatioConfigManager
from rules_manager import RulesManager

# Initialize FastAPI application
app = FastAPI(title="Insig Analyst API", version="1.0.0")

# Initialize managers
rules_manager: RulesManager = RulesManager()
ratio_config_manager: Optional[RatioConfigManager] = None

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for task management
running_tasks: Dict[str, Dict[str, Any]] = {}

# Configuration constants
TASKS_FILE: Path = Path(__file__).parent / "tasks.json"
file_cache: Dict[str, Tuple[Any, datetime]] = {}
CACHE_TTL: int = 60  # Cache TTL in seconds

def get_cached_or_compute(
    cache_key: str, compute_func: Any, ttl: int = CACHE_TTL
) -> Any:
    """Simple caching mechanism with TTL.
    
    Args:
        cache_key: Key to store/retrieve cached data.
        compute_func: Function to compute data if not cached.
        ttl: Time to live in seconds.
    
    Returns:
        Cached data or newly computed data.
    """
    current_time = datetime.now()
    
    if cache_key in file_cache:
        cached_data, cached_time = file_cache[cache_key]
        if (current_time - cached_time).total_seconds() < ttl:
            return cached_data
    
    # Compute new data
    data = compute_func()
    file_cache[cache_key] = (data, current_time)
    
    # Clean old cache entries
    keys_to_remove = []
    for key, (_, cached_time) in file_cache.items():
        if (current_time - cached_time).total_seconds() > ttl * 2:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del file_cache[key]
    
    return data

def cleanup_old_tasks() -> int:
    """Remove tasks older than TASK_RETENTION_HOURS.
    
    Returns:
        Number of tasks removed.
    """
    global running_tasks
    current_time = datetime.now()
    tasks_to_remove = []
    
    for task_id, task in running_tasks.items():
        created_at_str = task.get("created_at", "")
        if created_at_str:
            try:
                created_time = datetime.fromisoformat(
                    created_at_str.replace('Z', '+00:00')
                )
                hours_old = (
                    (current_time - created_time).total_seconds()
                    / 3600
                )
                if hours_old > TASK_RETENTION_HOURS:
                    tasks_to_remove.append(task_id)
            except (ValueError, TypeError):
                pass
    
    for task_id in tasks_to_remove:
        del running_tasks[task_id]
    
    # If still too many tasks, remove oldest completed/error tasks
    if len(running_tasks) > MAX_TASKS:
        sorted_tasks = sorted(
            running_tasks.items(),
            key=lambda x: x[1].get("created_at", ""),
            reverse=True
        )
        # Keep only the most recent MAX_TASKS
        running_tasks = dict(sorted_tasks[:MAX_TASKS])
    
    return len(tasks_to_remove)

def save_tasks() -> None:
    """Save tasks to file for persistence."""
    # Clean up old tasks before saving
    cleanup_old_tasks()
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(running_tasks, f, indent=2, default=str)


def load_tasks() -> None:
    """Load tasks from file if exists."""
    global running_tasks
    if TASKS_FILE.exists():
        try:
            with open(TASKS_FILE, 'r') as f:
                running_tasks = json.load(f)
            # Clean up old tasks after loading
            cleanup_old_tasks()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading tasks: {e}")
            running_tasks = {}

# Load tasks on startup
load_tasks()

class AnalysisRequest(BaseModel):
    """Request model for starting analysis."""
    company: str
    ticker: str


class TaskStatus(BaseModel):
    """Task status response model."""
    task_id: str
    status: str
    progress: int
    logs: List[str]
    result: Optional[str] = None
    error: Optional[str] = None

def check_company_data_exists(ticker: str) -> Tuple[bool, List[str]]:
    """Check if required data files exist for a company.
    
    Args:
        ticker: Company ticker symbol.
    
    Returns:
        Tuple of (data exists, list of missing files).
    """
    # Try multiple ticker formats
    ticker_variants = [
        ticker.upper(),  # Original format (e.g., XPP.L)
        ticker.upper().replace('.L', ''),  # Without .L suffix
        ticker.upper().replace('.', '_'),  # With underscore
    ]
    
    data_dir = None
    for variant in ticker_variants:
        test_dir = Path(__file__).parent.parent / "data" / variant
        if test_dir.exists():
            data_dir = test_dir
            break
    
    missing_files = []
    
    # Check if directory exists
    if not data_dir:
        return False, ["Company data folder does not exist"]
    
    # Check if there are any markdown files in the directory
    # We just need at least one data file to proceed
    has_data_files = False
    
    for file in data_dir.iterdir():
        if file.is_file() and file.suffix == '.md':
            has_data_files = True
            break
    
    if not has_data_files:
        missing_files.append("No data files found. Please upload financial data.")
    
    return len(missing_files) == 0, missing_files

def archive_existing_outputs(ticker: str):
    """Archive existing output files for a specific company before new analysis"""
    # Use core module if available, otherwise use custom implementation
    if USE_CORE_MODULES:
        from backend.core.archive import archive_company_outputs as core_archive_outputs
        return core_archive_outputs(ticker)
    
    # Fallback implementation if core module not available
    # Try multiple ticker formats for output directory
    ticker_variants = [
        ticker.upper(),  # Original format (e.g., XPP.L)
        ticker.upper().replace('.L', ''),  # Without .L suffix (e.g., XPP)
        ticker.upper().replace('.', '_'),  # With underscore (e.g., XPP_L)
    ]
    
    output_dir = None
    for variant in ticker_variants:
        test_dir = Path(__file__).parent.parent / "output" / variant
        if test_dir.exists():
            output_dir = test_dir
            ticker = variant  # Use the found variant for archive folder
            break
    
    archive_dir = Path(__file__).parent.parent / "archive" / ticker
    
    if not output_dir:
        return None
    
    # Create archive directory if it doesn't exist
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Create timestamped subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_subdir = archive_dir / timestamp
    archive_subdir.mkdir(exist_ok=True)
    
    # Move all files from output to archive
    for file in output_dir.iterdir():
        if file.is_file() and file.suffix in ['.md', '.pdf', '.json']:
            shutil.move(str(file), str(archive_subdir / file.name))
    
    # Also move any subdirectories
    for subdir in output_dir.iterdir():
        if subdir.is_dir() and subdir.name != '__pycache__':
            shutil.move(str(subdir), str(archive_subdir / subdir.name))
    
    return timestamp

def validate_ratios_completeness(ticker: str) -> tuple[bool, str]:
    """Validate that we have sufficient data in ratios (>80% populated)"""
    ticker_base = ticker.split('.')[0].upper()
    ticker_lower = ticker_base.lower()
    all_ratios_file = Path(__file__).parent.parent / "data" / ticker_base / f"{ticker_lower}_all_ratios.md"
    
    if not all_ratios_file.exists():
        return True, "Ratios file will be generated during analysis"
    
    with open(all_ratios_file, 'r') as f:
        content = f.read()
    
    # Count ratios with values - look for table rows with ratio data
    import re
    # Match lines like: | P/E Ratio | 5.23 | ... or | ROE | N/A | ...
    # Skip header rows and separator rows
    lines = content.split('\n')
    ratio_values = []
    in_table = False
    
    for line in lines:
        if '|' in line:
            # Check if this is a data row (not header or separator)
            if not any(x in line for x in ['---', 'Ratio', 'Metric', 'Value', '===']) and line.strip():
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 3:  # At least | name | value | ...
                    # Get the second column (value)
                    value = parts[2] if len(parts) > 2 else ''
                    # Check if it looks like a numeric value or N/A
                    if re.match(r'^[-\d.]+$|^N/A$|^-$|^$', value):
                        ratio_values.append(value)
    
    total_ratios = len(ratio_values)
    
    if total_ratios == 0:
        return True, "No ratios table found - will be generated during analysis"
    
    # Count ratios that are 0, N/A, or missing
    empty_ratios = sum(1 for val in ratio_values if val in ['0', '0.0', '0.00', 'N/A', '-', ''])
    
    # Calculate percentage of populated ratios
    populated_percentage = ((total_ratios - empty_ratios) / total_ratios) * 100 if total_ratios > 0 else 0
    
    # According to appflow.md: if more than 20% of ratios are 0 or not present, show warning
    # This means we need at least 80% populated
    if populated_percentage < 80:
        return False, f"Warning: Only {populated_percentage:.1f}% of ratios have values (more than 20% are missing or zero)"
    
    return True, f"{populated_percentage:.1f}% of ratios populated"

def check_required_data_files(ticker: str) -> tuple[bool, list]:
    """Check for required financial data files in ticker folder"""
    ticker_base = ticker.split('.')[0].upper()
    data_dir = Path(__file__).parent.parent / "data" / ticker_base
    
    if not data_dir.exists():
        return False, ["Data folder does not exist"]
    
    # Patterns to look for in financial data files
    required_patterns = [
        ['results', 'financial', 'annual'],  # Financial results
        ['balance', 'sheet'],  # Balance sheet
        ['cash', 'flow'],  # Cash flow
        ['income', 'statement'],  # Income statement
        ['report']  # Annual report
    ]
    
    found_files = []
    missing_patterns = []
    
    # Check each file in the directory
    for file in data_dir.iterdir():
        if file.is_file() and file.suffix == '.md':
            file_lower = file.name.lower()
            # Skip ratio files
            if 'ratio' in file_lower or 'agent' in file_lower:
                continue
            
            # Check which patterns this file matches
            for pattern_group in required_patterns:
                if any(pattern in file_lower for pattern in pattern_group):
                    found_files.append(file.name)
                    break
    
    # If we have at least one financial data file, consider it sufficient
    if len(found_files) > 0:
        return True, []
    else:
        return False, ["No financial data files found (need files with: results, financial, balance, cash, income, or report in filename)"]

def run_crew_analysis(task_id: str, company: str, ticker: str):
    """Run crew analysis in background"""
    try:
        print(f"Starting crew analysis for {company} ({ticker})")
        
        # Check for required data files first
        has_files, missing = check_required_data_files(ticker)
        if not has_files:
            running_tasks[task_id]["status"] = "error"
            missing_msg = f"Missing required data files: {', '.join(missing)}"
            running_tasks[task_id]["error"] = missing_msg
            running_tasks[task_id]["logs"].append(f"Error: {missing[0]}")
            save_tasks()
            return
        
        # Archive existing outputs for this company
        archive_timestamp = archive_existing_outputs(ticker)
        if archive_timestamp:
            msg = (
                f"Archived previous outputs to: "
                f"archive/{ticker}/{archive_timestamp}"
            )
            running_tasks[task_id]["logs"].append(msg)
        save_tasks()  # Save after update
        
        # Update status
        running_tasks[task_id]["status"] = "running"
        running_tasks[task_id]["logs"].append(
            f"Starting analysis for {company} ({ticker})"
        )
        running_tasks[task_id]["progress"] = 10
        save_tasks()  # Save after update
        
        print("Initializing crew...")
        # Initialize crew with company-specific parameters
        crew_instance = InsigAnalystDemo()
        crew_instance.company_ticker = ticker  # Set the ticker for the crew
        crew = crew_instance.crew()
        
        running_tasks[task_id]["logs"].append(
            "Crew initialized, starting analysis..."
        )
        running_tasks[task_id]["progress"] = 20
        save_tasks()
        
        # Run the crew with company, ticker, and current date/time
        from datetime import datetime
        current_datetime = datetime.now()
        inputs = {
            'company': company,
            'ticker': ticker,
            'current_date': current_datetime.strftime('%Y-%m-%d'),
            'current_time': current_datetime.strftime('%H:%M:%S')
        }
        
        print(f"Running crew.kickoff with inputs: {inputs}")
        # The crew will process data from {ticker}.json in @before_kickoff
        # JSON file must be provided - no external data fetching
        result = crew.kickoff(inputs=inputs)
        print(f"Crew completed with result: {result}")
        
        # Validate ratio completeness after crew generates them from JSON data
        ratios_valid, ratio_msg = validate_ratios_completeness(ticker)
        if not ratios_valid:
            # Add warning to logs but don't fail the analysis
            running_tasks[task_id]["logs"].append(f"Warning: {ratio_msg}")
            running_tasks[task_id]["logs"].append("Analysis continued despite incomplete ratios")
        else:
            running_tasks[task_id]["logs"].append(f"Ratios validation: {ratio_msg}")
        
        # Update completion
        running_tasks[task_id]["status"] = "completed"
        running_tasks[task_id]["progress"] = 100
        running_tasks[task_id]["result"] = str(result) if result else "Analysis completed"
        running_tasks[task_id]["logs"].append("Analysis completed successfully")
        running_tasks[task_id]["archive_timestamp"] = archive_timestamp
        save_tasks()  # Save final state
        
    except Exception as e:
        print(f"Error in run_crew_analysis: {e}")
        import traceback
        traceback.print_exc()
        running_tasks[task_id]["status"] = "error"
        running_tasks[task_id]["error"] = str(e)
        running_tasks[task_id]["logs"].append(f"Error: {str(e)}")
        save_tasks()  # Save error state

@app.get("/")
async def root():
    return {"message": "XP Power Analysis API", "status": "running"}

@app.post("/api/analysis/start")
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Start a new analysis"""
    task_id = str(uuid.uuid4())
    
    # Extract base ticker without exchange suffix for folder names
    ticker_base = request.ticker.split('.')[0].upper()
    ticker_lower = ticker_base.lower()
    data_dir = Path(__file__).parent.parent / "data" / ticker_base
    
    # Create data folder if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if ratio_rules.md exists, create default if not
    ratio_rules_file = data_dir / f"{ticker_lower}_ratio_rules.md"
    ratio_rules_created = False
    if not ratio_rules_file.exists():
        # Create default ratio_rules.md
        from ratio_config_manager import RatioConfigManager
        manager = RatioConfigManager(ticker=request.ticker)
        ratio_rules_created = True
    
    # Check if company data exists
    data_exists, missing_files = check_company_data_exists(request.ticker)
    
    if not data_exists:
        return {
            "task_id": None,
            "status": "error",
            "message": f"Data folder created for {request.ticker}. {'Default ratio_rules.md file created. ' if ratio_rules_created else ''}Please upload required files.",
            "missing_files": missing_files,
            "ratio_rules_created": ratio_rules_created
        }
    
    # Initialize task tracking
    running_tasks[task_id] = {
        "task_id": task_id,
        "status": "initializing",
        "progress": 0,
        "logs": [f"Task {task_id} created at {datetime.now().isoformat()}"],
        "result": None,
        "error": None,
        "company": request.company,
        "ticker": request.ticker,
        "created_at": datetime.now().isoformat()
    }
    save_tasks()  # Save new task
    
    # Start background task
    background_tasks.add_task(run_crew_analysis, task_id, request.company, request.ticker)
    
    return {"task_id": task_id, "message": "Analysis started"}

@app.get("/api/analysis/status/{task_id}")
async def get_status(task_id: str):
    """Get status of an analysis task"""
    if task_id not in running_tasks:
        # Try to reload tasks from file in case of server restart
        load_tasks()
        if task_id not in running_tasks:
            raise HTTPException(
                status_code=404, 
                detail=f"Task not found. Available tasks: {list(running_tasks.keys())[:5]}"
            )
    
    return running_tasks[task_id]

@app.get("/api/analysis/list")
async def list_analyses():
    """List all analysis tasks"""
    # Reload tasks to ensure we have the latest
    load_tasks()
    return list(running_tasks.values())

@app.get("/api/analysis/debug")
async def debug_info():
    """Debug endpoint to check system status"""
    load_tasks()
    return {
        "total_tasks": len(running_tasks),
        "task_ids": list(running_tasks.keys()),
        "tasks_file_exists": TASKS_FILE.exists(),
        "tasks_file_path": str(TASKS_FILE)
    }

@app.delete("/api/analysis/stop/{task_id}")
async def stop_analysis(task_id: str):
    """Stop a running analysis"""
    if task_id not in running_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if running_tasks[task_id]["status"] == "running":
        running_tasks[task_id]["status"] = "cancelled"
        running_tasks[task_id]["logs"].append("Analysis cancelled by user")
        save_tasks()
        return {"message": "Analysis stopped"}

@app.post("/api/analysis/cleanup")
async def cleanup_stuck_tasks():
    """Clean up tasks that are stuck in running state"""
    cleaned = 0
    for task_id, task in running_tasks.items():
        if task["status"] == "running":
            # Check if task has been running for more than 30 minutes
            created_at = task.get("created_at", "")
            if created_at:
                try:
                    created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    if (datetime.now() - created_time).seconds > TASK_TIMEOUT_MINUTES * 60:
                        task["status"] = "error"
                        task["error"] = "Task timed out"
                        task["logs"].append("Task marked as timed out after 30 minutes")
                        cleaned += 1
                except (ValueError, TypeError) as e:
                    # Log the error but continue processing other tasks
                    print(f"Error parsing task timestamp: {e}")
                    pass
    
    if cleaned > 0:
        save_tasks()
    
    return {"cleaned": cleaned, "message": f"Cleaned {cleaned} stuck tasks"}

@app.delete("/api/analysis/clear")
async def clear_all_tasks() -> Dict[str, str]:
    """Clear all tasks (use with caution).
    
    Returns:
        Status message.
    """
    global running_tasks
    running_tasks = {}
    save_tasks()
    return {"message": "All tasks cleared"}

@app.get("/api/files/input")
async def list_input_files() -> Dict[str, Any]:
    """List available input files organized by ticker.
    
    Returns:
        Dictionary with files organized by ticker.
    """
    def compute_input_files():
        data_dir = Path(__file__).parent.parent / "data"
        if not data_dir.exists():
            return {"filesByTicker": {}}
        
        files_by_ticker = {}
        
        # Scan ticker directories
        for ticker_dir in data_dir.iterdir():
            if ticker_dir.is_dir() and ticker_dir.name.isupper() and ticker_dir.name not in ['__pycache__']:
                ticker_files = []
                for file in ticker_dir.iterdir():
                    if file.suffix in ALLOWED_DOCUMENT_EXTENSIONS:
                        ticker_files.append({
                            "name": file.name,
                            "size": file.stat().st_size,
                            "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                        })
                if ticker_files:
                    files_by_ticker[ticker_dir.name] = ticker_files
        
        return {"filesByTicker": files_by_ticker}
    
    # Use caching for this expensive operation
    return get_cached_or_compute("input_files", compute_input_files)

@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...), ticker: str = Form(...)
) -> Dict[str, Any]:
    """Upload a document to a ticker-specific folder.
    
    Args:
        file: File to upload.
        ticker: Company ticker symbol.
    
    Returns:
        Upload status and file information.
    
    Raises:
        HTTPException: If upload fails or invalid input.
    """
    try:
        # Validate ticker
        ticker = ticker.upper()
        if not ticker or not ticker.isalnum():
            raise HTTPException(
                status_code=400,
                detail="Invalid ticker symbol"
            )
        
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_DOCUMENT_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=(
                    f"Invalid file type. Allowed types: "
                    f"{', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}"
                )
            )
        
        # Create ticker directory if it doesn't exist
        data_dir = Path(__file__).parent.parent / "data" / ticker
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        file_path = data_dir / file.filename
        
        # Check if file already exists
        if file_path.exists():
            # Add timestamp to filename to avoid overwriting
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = file_path.stem
            suffix = file_path.suffix
            file_path = data_dir / f"{stem}_{timestamp}{suffix}"
        
        # Write file content
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Invalidate cache after upload
        if "input_files" in file_cache:
            del file_cache["input_files"]
        
        return {
            "message": "File uploaded successfully",
            "filename": file_path.name,
            "size": len(content),
            "path": str(file_path.relative_to(Path(__file__).parent.parent))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

@app.delete("/api/files/{ticker}/{filename:path}")
async def delete_input_file(ticker: str, filename: str) -> Dict[str, str]:
    """Delete a file from a ticker-specific folder.
    
    Args:
        ticker: Company ticker symbol.
        filename: Name of file to delete.
    
    Returns:
        Deletion status message.
    
    Raises:
        HTTPException: If file not found or invalid input.
    """
    # Validate ticker format
    ticker = ticker.upper()
    if not ticker.replace('.', '').replace('_', '').isalnum():
        raise HTTPException(status_code=400, detail="Invalid ticker format")
    
    # Validate filename doesn't contain path traversal attempts
    if '..' in filename or filename.startswith('/'):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    data_dir = Path(__file__).parent.parent / "data" / ticker
    file_path = data_dir / filename
    
    # Resolve to absolute path and ensure it's within the data directory
    try:
        resolved_path = file_path.resolve()
        data_dir_resolved = data_dir.resolve()
        
        if not str(resolved_path).startswith(str(data_dir_resolved)):
            raise HTTPException(
                status_code=403, 
                detail="Access denied: Path traversal attempt detected"
            )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    if not resolved_path.exists() or not resolved_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        resolved_path.unlink()
        
        # Invalidate cache after deletion
        if "input_files" in file_cache:
            del file_cache["input_files"]
        
        return {"message": f"File {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@app.post("/api/files/convert/{ticker}/{filename:path}")
async def convert_pdf_to_markdown(
    ticker: str, filename: str
) -> Dict[str, Any]:
    """Convert a PDF file to Markdown format in ticker folder.
    
    Args:
        ticker: Company ticker symbol.
        filename: PDF filename to convert.
    
    Returns:
        Conversion status and file information.
    
    Raises:
        HTTPException: If conversion fails or invalid input.
    """
    # Validate ticker format
    ticker = ticker.upper()
    if not ticker.replace('.', '').replace('_', '').isalnum():
        raise HTTPException(status_code=400, detail="Invalid ticker format")
    
    # Validate filename doesn't contain path traversal attempts
    if '..' in filename or filename.startswith('/'):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    data_dir = Path(__file__).parent.parent / "data" / ticker
    pdf_path = data_dir / filename
    
    # Resolve to absolute path and ensure it's within the data directory
    try:
        resolved_path = pdf_path.resolve()
        data_dir_resolved = data_dir.resolve()
        
        if not str(resolved_path).startswith(str(data_dir_resolved)):
            raise HTTPException(
                status_code=403, 
                detail="Access denied: Path traversal attempt detected"
            )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    # Validate file exists and is a PDF
    if not resolved_path.exists() or not resolved_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    if resolved_path.suffix.lower() != '.pdf':
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Create converter instance
        converter = BestPDFToMarkdownConverter()
        
        # Generate output filename
        markdown_filename = resolved_path.stem + "_converted.md"
        markdown_path = data_dir / markdown_filename
        
        # Check if converted file already exists
        if markdown_path.exists():
            # Add timestamp to avoid overwriting
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            markdown_filename = f"{resolved_path.stem}_converted_{timestamp}.md"
            markdown_path = data_dir / markdown_filename
        
        # Convert PDF to Markdown
        markdown_content = converter.convert_pdf_to_markdown(resolved_path)
        
        # Save the converted file
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return {
            "message": "PDF converted successfully",
            "original_file": filename,
            "markdown_file": markdown_filename,
            "size": len(markdown_content),
            "path": str(markdown_path.relative_to(Path(__file__).parent.parent))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert PDF: {str(e)}")

@app.get("/api/files/output")
async def list_output_files() -> Dict[str, List[Dict[str, Any]]]:
    """List generated output files from all ticker folders.
    
    Returns:
        Dictionary with list of output files.
    """
    output_dir = Path(__file__).parent.parent / "output"
    if not output_dir.exists():
        return {"files": []}
    
    files = []
    
    # Look for files in ticker subdirectories
    for ticker_dir in output_dir.iterdir():
        if ticker_dir.is_dir():
            ticker = ticker_dir.name
            for file in ticker_dir.iterdir():
                if file.suffix in ['.md', '.pdf']:
                    files.append({
                        "name": file.name,
                        "ticker": ticker,
                        "path": f"{ticker}/{file.name}",
                        "size": file.stat().st_size,
                        "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                    })
    
    # Also check for any files directly in output (legacy)
    for file in output_dir.iterdir():
        if file.is_file() and file.suffix in ['.md', '.pdf']:
            files.append({
                "name": file.name,
                "ticker": "",
                "path": file.name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    
    return {"files": sorted(files, key=lambda x: x["modified"], reverse=True)}

@app.get("/api/files/output/{filename:path}")
async def get_output_file(filename: str) -> Any:
    """Download an output file (supports ticker/filename format).
    
    Args:
        filename: Path to output file.
    
    Returns:
        File content or FileResponse.
    
    Raises:
        HTTPException: If file not found or invalid path.
    """
    # Validate filename doesn't contain path traversal attempts
    if '..' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    output_dir = Path(__file__).parent.parent / "output"
    
    # Handle both ticker/filename and direct filename formats
    file_path = output_dir / filename
    
    # Resolve to absolute path and ensure it's within the output directory
    try:
        resolved_path = file_path.resolve()
        output_dir_resolved = output_dir.resolve()
        
        if not str(resolved_path).startswith(str(output_dir_resolved)):
            raise HTTPException(
                status_code=403, 
                detail="Access denied: Path traversal attempt detected"
            )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    if not resolved_path.exists() or not resolved_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return markdown content as text for preview
    if filename.endswith('.md'):
        with open(resolved_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return JSONResponse(content=content)
    
    return FileResponse(resolved_path)

@app.get("/api/config/agents")
async def get_agents_config() -> Dict[str, Any]:
    """Get agents configuration.
    
    Returns:
        Agents configuration dictionary.
    """
    config_path = (
        Path(__file__).parent.parent / "src" / 
        "insig_analyst_demo" / "config" / "agents.yaml"
    )
    if not config_path.exists():
        return {"error": "Configuration not found"}
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

@app.put("/api/config/agents")
async def update_agents_config(
    config: Dict[str, Any]
) -> Dict[str, str]:
    """Update agents configuration.
    
    Args:
        config: New agents configuration.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If update fails.
    """
    config_path = (
        Path(__file__).parent.parent / "src" / 
        "insig_analyst_demo" / "config" / "agents.yaml"
    )
    
    # Backup existing config
    backup_path = config_path.with_suffix('.yaml.bak')
    shutil.copy(config_path, backup_path)
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        return {"message": "Agents configuration updated successfully"}
    except Exception as e:
        # Restore backup on error
        shutil.copy(backup_path, config_path)
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to update configuration: {str(e)}"
        )

@app.get("/api/config/tasks")
async def get_tasks_config() -> Dict[str, Any]:
    """Get tasks configuration.
    
    Returns:
        Tasks configuration dictionary.
    """
    config_path = (
        Path(__file__).parent.parent / "src" / 
        "insig_analyst_demo" / "config" / "tasks.yaml"
    )
    if not config_path.exists():
        return {"error": "Configuration not found"}
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

@app.put("/api/config/tasks")
async def update_tasks_config(
    config: Dict[str, Any]
) -> Dict[str, str]:
    """Update tasks configuration.
    
    Args:
        config: New tasks configuration.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If update fails.
    """
    config_path = (
        Path(__file__).parent.parent / "src" / 
        "insig_analyst_demo" / "config" / "tasks.yaml"
    )
    
    # Backup existing config
    backup_path = config_path.with_suffix('.yaml.bak')
    shutil.copy(config_path, backup_path)
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        return {"message": "Tasks configuration updated successfully"}
    except Exception as e:
        # Restore backup on error
        shutil.copy(backup_path, config_path)
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to update configuration: {str(e)}"
        )

# Ratio Configuration Endpoints
@app.get("/api/ratios/{ticker}")
async def get_all_ratios(ticker: str) -> Dict[str, Any]:
    """Get all ratio configurations for a specific company.
    
    Args:
        ticker: Company ticker symbol.
    
    Returns:
        All ratio configurations.
    """
    manager = RatioConfigManager(ticker=ticker)
    return manager.get_all_ratios()

@app.get("/api/ratios/{ticker}/enabled")
async def get_enabled_ratios(ticker: str) -> Dict[str, Any]:
    """Get only enabled ratio configurations for a specific company.
    
    Args:
        ticker: Company ticker symbol.
    
    Returns:
        Enabled ratio configurations.
    """
    manager = RatioConfigManager(ticker=ticker)
    return manager.get_enabled_ratios()

@app.put("/api/ratios/{ticker}")
async def update_all_ratios(
    ticker: str, ratios_config: Dict[str, Any]
) -> Dict[str, str]:
    """Update all ratio configurations for a specific company.
    
    Args:
        ticker: Company ticker symbol.
        ratios_config: New ratio configurations.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If update fails.
    """
    try:
        manager = RatioConfigManager(ticker=ticker)
        success = manager.update_all_ratios(ratios_config)
        if success:
            return {"message": f"Ratio configurations updated successfully for {ticker}"}
        else:
            raise HTTPException(
                status_code=400, 
                detail="Failed to update ratio configurations"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating ratios: {str(e)}"
        )

@app.put("/api/ratios/{ticker}/{category}/{ratio_key}")
async def update_single_ratio(
    ticker: str, category: str, ratio_key: str, config: Dict[str, Any]
) -> Dict[str, str]:
    """Update a single ratio configuration for a specific company.
    
    Args:
        ticker: Company ticker symbol.
        category: Ratio category.
        ratio_key: Specific ratio key.
        config: New ratio configuration.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If ratio not found or update fails.
    """
    try:
        manager = RatioConfigManager(ticker=ticker)
        success = manager.update_ratio(category, ratio_key, config)
        if success:
            return {"message": f"Ratio {ratio_key} updated successfully for {ticker}"}
        else:
            raise HTTPException(
                status_code=404, 
                detail=f"Ratio {category}/{ratio_key} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating ratio: {str(e)}"
        )

@app.post("/api/ratios/{ticker}/{category}/{ratio_key}/enable")
async def enable_ratio(
    ticker: str, category: str, ratio_key: str
) -> Dict[str, str]:
    """Enable a specific ratio for a company.
    
    Args:
        ticker: Company ticker symbol.
        category: Ratio category.
        ratio_key: Specific ratio key.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If ratio not found.
    """
    manager = RatioConfigManager(ticker=ticker)
    success = manager.enable_ratio(category, ratio_key)
    if success:
        return {"message": f"Ratio {ratio_key} enabled for {ticker}"}
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Ratio {category}/{ratio_key} not found"
        )

@app.post("/api/ratios/{ticker}/{category}/{ratio_key}/disable")
async def disable_ratio(
    ticker: str, category: str, ratio_key: str
) -> Dict[str, str]:
    """Disable a specific ratio for a company.
    
    Args:
        ticker: Company ticker symbol.
        category: Ratio category.
        ratio_key: Specific ratio key.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If ratio not found.
    """
    manager = RatioConfigManager(ticker=ticker)
    success = manager.disable_ratio(category, ratio_key)
    if success:
        return {"message": f"Ratio {ratio_key} disabled for {ticker}"}
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Ratio {category}/{ratio_key} not found"
        )

@app.get("/api/archive")
async def list_archive() -> Dict[str, List[Dict[str, Any]]]:
    """List all archived analyses from all tickers.
    
    Returns:
        Dictionary with list of archived analyses.
    """
    archive_dir = Path(__file__).parent.parent / "archive"
    if not archive_dir.exists():
        return {"archives": []}
    
    archives = []
    
    # Look for ticker subdirectories
    for ticker_dir in archive_dir.iterdir():
        if ticker_dir.is_dir():
            ticker = ticker_dir.name
            # Look for timestamp folders within each ticker
            for folder in sorted(ticker_dir.iterdir(), reverse=True):
                if folder.is_dir():
                    files = []
                    for file in folder.iterdir():
                        if file.suffix in ['.md', '.pdf']:
                            files.append({
                                "name": file.name,
                                "size": file.stat().st_size,
                                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                            })
                    
                    archives.append({
                        "ticker": ticker,
                        "timestamp": folder.name,
                        "path": f"{ticker}/{folder.name}",
                        "date": datetime.strptime(folder.name, "%Y%m%d_%H%M%S").isoformat() if '_' in folder.name else folder.name,
                        "files": files,
                        "file_count": len(files)
                    })
    
    return {"archives": sorted(archives, key=lambda x: x["date"], reverse=True)}

@app.get("/api/archive/{path:path}")
async def get_archive_file(path: str) -> Any:
    """Download a file from archive.
    
    Supports ticker/timestamp/filename format.
    
    Args:
        path: Path to archived file.
    
    Returns:
        File content or FileResponse.
    
    Raises:
        HTTPException: If file not found or invalid path.
    """
    # Validate path doesn't contain path traversal attempts
    if '..' in path:
        raise HTTPException(status_code=400, detail="Invalid path")
    
    archive_dir = Path(__file__).parent.parent / "archive"
    archive_path = archive_dir / path
    
    # Resolve to absolute path and ensure it's within the archive directory
    try:
        resolved_path = archive_path.resolve()
        archive_dir_resolved = archive_dir.resolve()
        
        if not str(resolved_path).startswith(str(archive_dir_resolved)):
            raise HTTPException(
                status_code=403, 
                detail="Access denied: Path traversal attempt detected"
            )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    if not resolved_path.exists() or not resolved_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return markdown content as text for preview
    if path.endswith('.md'):
        with open(resolved_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return JSONResponse(content=content)
    
    return FileResponse(resolved_path)

# Rules Management Endpoints
@app.get("/api/rules")
async def get_all_rules() -> Dict[str, Any]:
    """Get all analysis rules.
    
    Returns:
        All analysis rules.
    """
    return rules_manager.get_all_rules()

@app.get("/api/rules/category/{category}")
async def get_rules_by_category(category: str) -> Dict[str, Any]:
    """Get rules for a specific category.
    
    Args:
        category: Rule category name.
    
    Returns:
        Rules in the specified category.
    
    Raises:
        HTTPException: If category not found.
    """
    rules = rules_manager.get_rules_by_category(category)
    if not rules:
        raise HTTPException(
            status_code=404, 
            detail=f"Category '{category}' not found"
        )
    return rules

@app.get("/api/rules/task/{task_name}")
async def get_rules_for_task(task_name: str) -> Dict[str, Any]:
    """Get all rules that apply to a specific task.
    
    Args:
        task_name: Name of the task.
    
    Returns:
        Rules that apply to the task.
    """
    return rules_manager.get_rules_for_task(task_name)

class RuleData(BaseModel):
    """Data model for analysis rules."""
    name: str
    description: str
    category: str
    metric_type: str  # ratio, percentage, qualitative
    thresholds: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    applies_to_tasks: List[str] = []
    enabled: bool = True
    severity: Optional[str] = None  # For red flags
    implication: Optional[str] = None  # For red flags

@app.post("/api/rules/{category}/{rule_id}")
async def add_rule(
    category: str, rule_id: str, rule_data: RuleData
) -> Dict[str, str]:
    """Add a new rule.
    
    Args:
        category: Rule category.
        rule_id: Unique rule identifier.
        rule_data: Rule configuration data.
    
    Returns:
        Status message with category and rule ID.
    
    Raises:
        HTTPException: If rule already exists.
    """
    success = rules_manager.add_rule(category, rule_id, rule_data.dict())
    if not success:
        raise HTTPException(status_code=400, detail="Rule already exists")
    return {"message": "Rule added successfully", "category": category, "rule_id": rule_id}

@app.put("/api/rules/{category}/{rule_id}")
async def update_rule(
    category: str, rule_id: str, rule_data: RuleData
) -> Dict[str, str]:
    """Update an existing rule.
    
    Args:
        category: Rule category.
        rule_id: Unique rule identifier.
        rule_data: Updated rule configuration.
    
    Returns:
        Status message with category and rule ID.
    
    Raises:
        HTTPException: If rule not found.
    """
    success = rules_manager.update_rule(category, rule_id, rule_data.dict())
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Update tasks configuration if needed
    await update_task_rules(rule_id, category, rule_data.applies_to_tasks)
    
    return {"message": "Rule updated successfully", "category": category, "rule_id": rule_id}

@app.delete("/api/rules/{category}/{rule_id}")
async def delete_rule(category: str, rule_id: str) -> Dict[str, str]:
    """Delete a rule.
    
    Args:
        category: Rule category.
        rule_id: Unique rule identifier.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If rule not found.
    """
    success = rules_manager.delete_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule deleted successfully"}

class TaskAssignment(BaseModel):
    """Model for task assignment."""
    task_name: str

@app.post("/api/rules/{category}/{rule_id}/assign")
async def assign_rule_to_task(
    category: str, rule_id: str, assignment: TaskAssignment
) -> Dict[str, str]:
    """Assign a rule to a task.
    
    Args:
        category: Rule category.
        rule_id: Unique rule identifier.
        assignment: Task assignment data.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If rule not found.
    """
    success = rules_manager.assign_rule_to_task(category, rule_id, assignment.task_name)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Update task configuration
    await update_task_with_rule(assignment.task_name, rule_id, category)
    
    return {"message": f"Rule assigned to task {assignment.task_name}"}

@app.post("/api/rules/{category}/{rule_id}/unassign")
async def remove_rule_from_task(
    category: str, rule_id: str, assignment: TaskAssignment
) -> Dict[str, str]:
    """Remove a rule from a task.
    
    Args:
        category: Rule category.
        rule_id: Unique rule identifier.
        assignment: Task assignment data.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If rule not found or not assigned.
    """
    success = rules_manager.remove_rule_from_task(category, rule_id, assignment.task_name)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Rule not found or not assigned to task"
        )
    
    return {"message": f"Rule removed from task {assignment.task_name}"}

@app.post("/api/rules/{category}/{rule_id}/enable")
async def enable_rule(category: str, rule_id: str) -> Dict[str, str]:
    """Enable a rule.
    
    Args:
        category: Rule category.
        rule_id: Unique rule identifier.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If rule not found.
    """
    success = rules_manager.enable_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule enabled"}

@app.post("/api/rules/{category}/{rule_id}/disable")
async def disable_rule(category: str, rule_id: str) -> Dict[str, str]:
    """Disable a rule.
    
    Args:
        category: Rule category.
        rule_id: Unique rule identifier.
    
    Returns:
        Status message.
    
    Raises:
        HTTPException: If rule not found.
    """
    success = rules_manager.disable_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule disabled"}

@app.get("/api/rules/export/{task_name}")
async def export_rules_for_task(task_name: str) -> Dict[str, str]:
    """Export rules for a task as formatted text.
    
    Args:
        task_name: Name of the task.
    
    Returns:
        Task name and formatted rules text.
    """
    rules_text = rules_manager.export_rules_for_task(task_name)
    return {"task_name": task_name, "rules_text": rules_text}

async def update_task_rules(
    rule_id: str, category: str, task_names: List[str]
) -> None:
    """Update task configurations when rules change.
    
    Args:
        rule_id: Unique rule identifier.
        category: Rule category.
        task_names: List of task names to update.
    """
    config_path = (
        Path(__file__).parent.parent / "src" / 
        "insig_analyst_demo" / "config" / "tasks.yaml"
    )
    
    if not config_path.exists():
        return
    
    with open(config_path, 'r') as f:
        tasks_config = yaml.safe_load(f)
    
    # Update each task that uses this rule
    for task_name in task_names:
        if task_name in tasks_config:
            # Add rule reference to task description if not present
            rule_ref = f"\n# Rule: {rule_id} from {category}"
            desc = tasks_config[task_name].get('description', '')
            if rule_ref not in desc:
                # Get the formatted rules for this task
                rules_text = rules_manager.export_rules_for_task(
                    task_name
                )
                if rules_text:
                    tasks_config[task_name]['description'] += (
                        f"\n\n{rules_text}"
                    )
    
    # Save updated configuration
    with open(config_path, 'w') as f:
        yaml.dump(tasks_config, f, default_flow_style=False, sort_keys=False)

async def update_task_with_rule(
    task_name: str, rule_id: str, category: str
) -> None:
    """Update a specific task when a rule is assigned to it.
    
    Args:
        task_name: Name of the task to update.
        rule_id: Unique rule identifier.
        category: Rule category.
    """
    config_path = (
        Path(__file__).parent.parent / "src" / 
        "insig_analyst_demo" / "config" / "tasks.yaml"
    )
    
    if not config_path.exists():
        return
    
    with open(config_path, 'r') as f:
        tasks_config = yaml.safe_load(f)
    
    if task_name in tasks_config:
        # Get all rules for this task
        rules_text = rules_manager.export_rules_for_task(task_name)
        
        # Update task description with rules
        if rules_text:
            # Find and replace existing rules section or add new one
            description = tasks_config[task_name].get('description', '')
            rules_marker = "\n# Rules and Thresholds"
            
            if rules_marker in description:
                # Replace existing rules section
                parts = description.split(rules_marker)
                tasks_config[task_name]['description'] = (
                    parts[0] + "\n" + rules_text
                )
            else:
                # Add new rules section
                tasks_config[task_name]['description'] = (
                    description + "\n\n" + rules_text
                )
    
    # Save updated configuration
    with open(config_path, 'w') as f:
        yaml.dump(tasks_config, f, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)