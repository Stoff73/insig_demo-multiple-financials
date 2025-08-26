from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import uuid
from datetime import datetime
from pathlib import Path
import sys
import json
import os
import shutil
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path for crew imports
sys.path.append(str(Path(__file__).parent.parent / "src"))
from xp_power_demo.crew import XpPowerDemo

# Add backend to path for modules
sys.path.append(str(Path(__file__).parent))

# Import from core modules for cleaner architecture
try:
    from core.pdf_converter import PDFToMarkdownConverter as BestPDFToMarkdownConverter
    from core.archive import archive_existing_outputs as core_archive_outputs
    from core.file_utils import list_files_in_directory, save_file_with_timestamp
    USE_CORE_MODULES = True
except ImportError:
    # Fallback to original imports if core modules not available
    from pdf_converter_best import BestPDFToMarkdownConverter
    USE_CORE_MODULES = False

from rules_manager import RulesManager
from ratio_config_manager import RatioConfigManager

app = FastAPI(title="XP Power Analysis API", version="1.0.0")

# Initialize rules manager
rules_manager = RulesManager()

# Initialize ratio config manager (will be created per company)
ratio_config_manager = None

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store running tasks
running_tasks: Dict[str, Dict[str, Any]] = {}

# Task persistence file
TASKS_FILE = Path(__file__).parent / "tasks.json"

def save_tasks():
    """Save tasks to file for persistence"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(running_tasks, f, indent=2, default=str)

def load_tasks():
    """Load tasks from file if exists"""
    global running_tasks
    if TASKS_FILE.exists():
        try:
            with open(TASKS_FILE, 'r') as f:
                running_tasks = json.load(f)
        except Exception as e:
            print(f"Error loading tasks: {e}")
            running_tasks = {}

# Load tasks on startup
load_tasks()

class AnalysisRequest(BaseModel):
    company: str
    ticker: str

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    logs: List[str]
    result: Optional[str] = None
    error: Optional[str] = None

def check_company_data_exists(ticker: str) -> tuple[bool, list]:
    """Check if required data files exist for a company"""
    ticker = ticker.upper().replace('.', '_')  # Sanitize ticker
    data_dir = Path(__file__).parent.parent / "data" / ticker
    
    missing_files = []
    
    # Check if directory exists
    if not data_dir.exists():
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
    ticker = ticker.upper().replace('.', '_')  # Sanitize ticker
    
    output_dir = Path(__file__).parent.parent / "output" / ticker
    archive_dir = Path(__file__).parent.parent / "archive" / ticker
    
    if not output_dir.exists():
        return None
    
    # Create archive directory if it doesn't exist
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Create timestamped subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_subdir = archive_dir / timestamp
    archive_subdir.mkdir(exist_ok=True)
    
    # Move all files from output to archive
    for file in output_dir.iterdir():
        if file.is_file() and file.suffix in ['.md', '.pdf']:
            shutil.move(str(file), str(archive_subdir / file.name))
    
    # Also move any subdirectories
    for subdir in output_dir.iterdir():
        if subdir.is_dir() and subdir.name != '__pycache__':
            shutil.move(str(subdir), str(archive_subdir / subdir.name))
    
    return timestamp

def run_crew_analysis(task_id: str, company: str, ticker: str):
    """Run crew analysis in background"""
    try:
        print(f"Starting crew analysis for {company} ({ticker})")
        
        # Archive existing outputs for this company
        archive_timestamp = archive_existing_outputs(ticker)
        if archive_timestamp:
            running_tasks[task_id]["logs"].append(f"Archived previous outputs to: archive/{ticker}/{archive_timestamp}")
        save_tasks()  # Save after update
        
        # Update status
        running_tasks[task_id]["status"] = "running"
        running_tasks[task_id]["logs"].append(f"Starting analysis for {company} ({ticker})")
        running_tasks[task_id]["progress"] = 10
        save_tasks()  # Save after update
        
        print("Initializing crew...")
        # Initialize crew with company-specific parameters
        crew_instance = XpPowerDemo()
        crew_instance.company_ticker = ticker  # Set the ticker for the crew
        crew = crew_instance.crew()
        
        running_tasks[task_id]["logs"].append("Crew initialized, starting analysis...")
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
        result = crew.kickoff(inputs=inputs)
        print(f"Crew completed with result: {result}")
        
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
    
    # Check if company data exists
    ticker = request.ticker.upper().replace('.', '_')
    data_exists, missing_files = check_company_data_exists(ticker)
    
    if not data_exists:
        # Create the data folder if it doesn't exist
        data_dir = Path(__file__).parent.parent / "data" / ticker
        data_dir.mkdir(parents=True, exist_ok=True)
        
        return {
            "task_id": None,
            "status": "error",
            "message": f"Data folder created for {ticker}. Please upload required files.",
            "missing_files": missing_files
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
        return {"message": "Analysis stopped"}
    
    return {"message": "Analysis not running"}

@app.get("/api/files/input")
async def list_input_files():
    """List available input files organized by ticker"""
    data_dir = Path(__file__).parent.parent / "data"
    if not data_dir.exists():
        return {"filesByTicker": {}}
    
    files_by_ticker = {}
    
    # Scan ticker directories
    for ticker_dir in data_dir.iterdir():
        if ticker_dir.is_dir() and ticker_dir.name.isupper() and ticker_dir.name not in ['__pycache__']:
            ticker_files = []
            for file in ticker_dir.iterdir():
                if file.suffix in ['.md', '.pdf', '.txt', '.csv', '.xlsx', '.docx']:
                    ticker_files.append({
                        "name": file.name,
                        "size": file.stat().st_size,
                        "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                    })
            if ticker_files:
                files_by_ticker[ticker_dir.name] = ticker_files
    
    return {"filesByTicker": files_by_ticker}

@app.post("/api/files/upload")
async def upload_file(file: UploadFile = File(...), ticker: str = Form(...)):
    """Upload a document to a ticker-specific folder"""
    try:
        # Validate ticker
        ticker = ticker.upper()
        if not ticker or not ticker.isalnum():
            raise HTTPException(
                status_code=400,
                detail="Invalid ticker symbol"
            )
        
        # Validate file extension
        allowed_extensions = ['.md', '.pdf', '.txt', '.csv', '.xlsx', '.docx']
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
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
        
        return {
            "message": "File uploaded successfully",
            "filename": file_path.name,
            "size": len(content),
            "path": str(file_path.relative_to(Path(__file__).parent.parent))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

@app.delete("/api/files/{ticker}/{filename:path}")
async def delete_input_file(ticker: str, filename: str):
    """Delete a file from a ticker-specific folder"""
    ticker = ticker.upper()
    data_dir = Path(__file__).parent.parent / "data" / ticker
    file_path = data_dir / filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        file_path.unlink()
        return {"message": f"File {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@app.post("/api/files/convert/{ticker}/{filename:path}")
async def convert_pdf_to_markdown(ticker: str, filename: str):
    """Convert a PDF file to Markdown format in ticker folder"""
    ticker = ticker.upper()
    data_dir = Path(__file__).parent.parent / "data" / ticker
    pdf_path = data_dir / filename
    
    # Validate file exists and is a PDF
    if not pdf_path.exists() or not pdf_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    if pdf_path.suffix.lower() != '.pdf':
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Create converter instance
        converter = BestPDFToMarkdownConverter()
        
        # Generate output filename
        markdown_filename = pdf_path.stem + "_converted.md"
        markdown_path = data_dir / markdown_filename
        
        # Check if converted file already exists
        if markdown_path.exists():
            # Add timestamp to avoid overwriting
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            markdown_filename = f"{pdf_path.stem}_converted_{timestamp}.md"
            markdown_path = data_dir / markdown_filename
        
        # Convert PDF to Markdown
        markdown_content = converter.convert_pdf_to_markdown(pdf_path)
        
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
async def list_output_files():
    """List generated output files from all ticker folders"""
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
async def get_output_file(filename: str):
    """Download an output file (supports ticker/filename format)"""
    output_dir = Path(__file__).parent.parent / "output"
    
    # Handle both ticker/filename and direct filename formats
    file_path = output_dir / filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return markdown content as text for preview
    if filename.endswith('.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return JSONResponse(content=content)
    
    return FileResponse(file_path)

@app.get("/api/config/agents")
async def get_agents_config():
    """Get agents configuration"""
    config_path = Path(__file__).parent.parent / "src" / "xp_power_demo" / "config" / "agents.yaml"
    if not config_path.exists():
        return {"error": "Configuration not found"}
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

@app.put("/api/config/agents")
async def update_agents_config(config: Dict[str, Any]):
    """Update agents configuration"""
    config_path = Path(__file__).parent.parent / "src" / "xp_power_demo" / "config" / "agents.yaml"
    
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
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")

@app.get("/api/config/tasks")
async def get_tasks_config():
    """Get tasks configuration"""
    config_path = Path(__file__).parent.parent / "src" / "xp_power_demo" / "config" / "tasks.yaml"
    if not config_path.exists():
        return {"error": "Configuration not found"}
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config

@app.put("/api/config/tasks")
async def update_tasks_config(config: Dict[str, Any]):
    """Update tasks configuration"""
    config_path = Path(__file__).parent.parent / "src" / "xp_power_demo" / "config" / "tasks.yaml"
    
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
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")

# Ratio Configuration Endpoints
@app.get("/api/ratios/{ticker}")
async def get_all_ratios(ticker: str):
    """Get all ratio configurations for a specific company"""
    manager = RatioConfigManager(ticker=ticker)
    return manager.get_all_ratios()

@app.get("/api/ratios/{ticker}/enabled")
async def get_enabled_ratios(ticker: str):
    """Get only enabled ratio configurations for a specific company"""
    manager = RatioConfigManager(ticker=ticker)
    return manager.get_enabled_ratios()

@app.put("/api/ratios/{ticker}")
async def update_all_ratios(ticker: str, ratios_config: Dict[str, Any]):
    """Update all ratio configurations for a specific company"""
    try:
        manager = RatioConfigManager(ticker=ticker)
        success = manager.update_all_ratios(ratios_config)
        if success:
            return {"message": f"Ratio configurations updated successfully for {ticker}"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update ratio configurations")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ratios: {str(e)}")

@app.put("/api/ratios/{ticker}/{category}/{ratio_key}")
async def update_single_ratio(ticker: str, category: str, ratio_key: str, config: Dict[str, Any]):
    """Update a single ratio configuration for a specific company"""
    try:
        manager = RatioConfigManager(ticker=ticker)
        success = manager.update_ratio(category, ratio_key, config)
        if success:
            return {"message": f"Ratio {ratio_key} updated successfully for {ticker}"}
        else:
            raise HTTPException(status_code=404, detail=f"Ratio {category}/{ratio_key} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ratio: {str(e)}")

@app.post("/api/ratios/{ticker}/{category}/{ratio_key}/enable")
async def enable_ratio(ticker: str, category: str, ratio_key: str):
    """Enable a specific ratio for a company"""
    manager = RatioConfigManager(ticker=ticker)
    success = manager.enable_ratio(category, ratio_key)
    if success:
        return {"message": f"Ratio {ratio_key} enabled for {ticker}"}
    else:
        raise HTTPException(status_code=404, detail=f"Ratio {category}/{ratio_key} not found")

@app.post("/api/ratios/{ticker}/{category}/{ratio_key}/disable")
async def disable_ratio(ticker: str, category: str, ratio_key: str):
    """Disable a specific ratio for a company"""
    manager = RatioConfigManager(ticker=ticker)
    success = manager.disable_ratio(category, ratio_key)
    if success:
        return {"message": f"Ratio {ratio_key} disabled for {ticker}"}
    else:
        raise HTTPException(status_code=404, detail=f"Ratio {category}/{ratio_key} not found")

@app.get("/api/archive")
async def list_archive():
    """List all archived analyses from all tickers"""
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
async def get_archive_file(path: str):
    """Download a file from archive (supports ticker/timestamp/filename format)"""
    archive_path = Path(__file__).parent.parent / "archive" / path
    
    if not archive_path.exists() or not archive_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return markdown content as text for preview
    if path.endswith('.md'):
        with open(archive_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return JSONResponse(content=content)
    
    return FileResponse(archive_path)

# Rules Management Endpoints
@app.get("/api/rules")
async def get_all_rules():
    """Get all analysis rules"""
    return rules_manager.get_all_rules()

@app.get("/api/rules/category/{category}")
async def get_rules_by_category(category: str):
    """Get rules for a specific category"""
    rules = rules_manager.get_rules_by_category(category)
    if not rules:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    return rules

@app.get("/api/rules/task/{task_name}")
async def get_rules_for_task(task_name: str):
    """Get all rules that apply to a specific task"""
    return rules_manager.get_rules_for_task(task_name)

class RuleData(BaseModel):
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
async def add_rule(category: str, rule_id: str, rule_data: RuleData):
    """Add a new rule"""
    success = rules_manager.add_rule(category, rule_id, rule_data.dict())
    if not success:
        raise HTTPException(status_code=400, detail="Rule already exists")
    return {"message": "Rule added successfully", "category": category, "rule_id": rule_id}

@app.put("/api/rules/{category}/{rule_id}")
async def update_rule(category: str, rule_id: str, rule_data: RuleData):
    """Update an existing rule"""
    success = rules_manager.update_rule(category, rule_id, rule_data.dict())
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Update tasks configuration if needed
    await update_task_rules(rule_id, category, rule_data.applies_to_tasks)
    
    return {"message": "Rule updated successfully", "category": category, "rule_id": rule_id}

@app.delete("/api/rules/{category}/{rule_id}")
async def delete_rule(category: str, rule_id: str):
    """Delete a rule"""
    success = rules_manager.delete_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule deleted successfully"}

class TaskAssignment(BaseModel):
    task_name: str

@app.post("/api/rules/{category}/{rule_id}/assign")
async def assign_rule_to_task(category: str, rule_id: str, assignment: TaskAssignment):
    """Assign a rule to a task"""
    success = rules_manager.assign_rule_to_task(category, rule_id, assignment.task_name)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Update task configuration
    await update_task_with_rule(assignment.task_name, rule_id, category)
    
    return {"message": f"Rule assigned to task {assignment.task_name}"}

@app.post("/api/rules/{category}/{rule_id}/unassign")
async def remove_rule_from_task(category: str, rule_id: str, assignment: TaskAssignment):
    """Remove a rule from a task"""
    success = rules_manager.remove_rule_from_task(category, rule_id, assignment.task_name)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found or not assigned to task")
    
    return {"message": f"Rule removed from task {assignment.task_name}"}

@app.post("/api/rules/{category}/{rule_id}/enable")
async def enable_rule(category: str, rule_id: str):
    """Enable a rule"""
    success = rules_manager.enable_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule enabled"}

@app.post("/api/rules/{category}/{rule_id}/disable")
async def disable_rule(category: str, rule_id: str):
    """Disable a rule"""
    success = rules_manager.disable_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule disabled"}

@app.get("/api/rules/export/{task_name}")
async def export_rules_for_task(task_name: str):
    """Export rules for a task as formatted text"""
    rules_text = rules_manager.export_rules_for_task(task_name)
    return {"task_name": task_name, "rules_text": rules_text}

async def update_task_rules(rule_id: str, category: str, task_names: List[str]):
    """Update task configurations when rules change"""
    config_path = Path(__file__).parent.parent / "src" / "xp_power_demo" / "config" / "tasks.yaml"
    
    if not config_path.exists():
        return
    
    with open(config_path, 'r') as f:
        tasks_config = yaml.safe_load(f)
    
    # Update each task that uses this rule
    for task_name in task_names:
        if task_name in tasks_config:
            # Add rule reference to task description if not already present
            rule_ref = f"\n# Rule: {rule_id} from {category}"
            if rule_ref not in tasks_config[task_name].get('description', ''):
                # Get the formatted rules for this task
                rules_text = rules_manager.export_rules_for_task(task_name)
                if rules_text:
                    tasks_config[task_name]['description'] += f"\n\n{rules_text}"
    
    # Save updated configuration
    with open(config_path, 'w') as f:
        yaml.dump(tasks_config, f, default_flow_style=False, sort_keys=False)

async def update_task_with_rule(task_name: str, rule_id: str, category: str):
    """Update a specific task when a rule is assigned to it"""
    config_path = Path(__file__).parent.parent / "src" / "xp_power_demo" / "config" / "tasks.yaml"
    
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
                tasks_config[task_name]['description'] = parts[0] + "\n" + rules_text
            else:
                # Add new rules section
                tasks_config[task_name]['description'] = description + "\n\n" + rules_text
    
    # Save updated configuration
    with open(config_path, 'w') as f:
        yaml.dump(tasks_config, f, default_flow_style=False, sort_keys=False)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)