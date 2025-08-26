"""
Refactored single-company analysis API
Uses shared core modules to reduce redundancy
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
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

# Add src to path for crew imports
sys.path.append(str(Path(__file__).parent.parent / "src"))
from xp_power_demo.crew import XpPowerDemo

# Import core modules
from core.config import (
    BASE_DIR, DATA_DIR, OUTPUT_DIR, CONFIG_DIR,
    CORS_ORIGINS, ALLOWED_DOCUMENT_EXTENSIONS, 
    OUTPUT_EXTENSIONS, ANALYSIS_TASKS
)
from core.archive import (
    archive_existing_outputs, list_archives, 
    get_archive_file_content
)
from core.file_utils import (
    list_files_in_directory, save_file_with_timestamp,
    save_text_file_with_timestamp, read_markdown_file,
    validate_file_extension
)
from core.yaml_utils import read_yaml_config, update_yaml_config
from core.pdf_converter import PDFToMarkdownConverter
from rules_manager import RulesManager
from ratio_config_manager import RatioConfigManager

app = FastAPI(title="XP Power Analysis API", version="1.0.0")

# Initialize managers
rules_manager = RulesManager()
ratio_config_manager = RatioConfigManager()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
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
    company: str = "XP Power"
    year: str = "2024"

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    logs: List[str]
    result: Optional[str] = None
    error: Optional[str] = None

def run_crew_analysis(task_id: str, company: str, year: str):
    """Run crew analysis in background"""
    try:
        # Archive existing outputs
        archive_timestamp = archive_existing_outputs()
        if archive_timestamp:
            running_tasks[task_id]["logs"].append(f"Archived previous outputs to: archive/{archive_timestamp}")
        save_tasks()
        
        # Update status
        running_tasks[task_id]["status"] = "running"
        running_tasks[task_id]["logs"].append(f"Starting analysis for {company} ({year})")
        save_tasks()
        
        # Initialize crew
        crew_instance = XpPowerDemo()
        crew = crew_instance.crew()
        
        # Track progress through tasks
        for i, task_name in enumerate(ANALYSIS_TASKS):
            running_tasks[task_id]["progress"] = int((i / len(ANALYSIS_TASKS)) * 100)
            running_tasks[task_id]["logs"].append(f"Executing: {task_name}")
            save_tasks()
        
        # Run the crew
        from datetime import datetime
        current_datetime = datetime.now()
        inputs = {
            'company': company,
            'current_year': year,
            'current_date': current_datetime.strftime('%Y-%m-%d'),
            'current_time': current_datetime.strftime('%H:%M:%S')
        }
        
        result = crew.kickoff(inputs=inputs)
        
        # Update completion
        running_tasks[task_id]["status"] = "completed"
        running_tasks[task_id]["progress"] = 100
        running_tasks[task_id]["result"] = str(result) if result else "Analysis completed"
        running_tasks[task_id]["logs"].append("Analysis completed successfully")
        running_tasks[task_id]["archive_timestamp"] = archive_timestamp
        save_tasks()
        
    except Exception as e:
        running_tasks[task_id]["status"] = "error"
        running_tasks[task_id]["error"] = str(e)
        running_tasks[task_id]["logs"].append(f"Error: {str(e)}")
        save_tasks()

@app.get("/")
async def root():
    return {"message": "XP Power Analysis API", "status": "running"}

@app.post("/api/analysis/start")
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Start a new analysis"""
    task_id = str(uuid.uuid4())
    
    # Initialize task tracking
    running_tasks[task_id] = {
        "task_id": task_id,
        "status": "initializing",
        "progress": 0,
        "logs": [f"Task {task_id} created at {datetime.now().isoformat()}"],
        "result": None,
        "error": None,
        "company": request.company,
        "year": request.year,
        "created_at": datetime.now().isoformat()
    }
    save_tasks()
    
    # Start background task
    background_tasks.add_task(run_crew_analysis, task_id, request.company, request.year)
    
    return {"task_id": task_id, "message": "Analysis started"}

@app.get("/api/analysis/status/{task_id}")
async def get_status(task_id: str):
    """Get status of an analysis task"""
    if task_id not in running_tasks:
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
    """List available input files"""
    files = list_files_in_directory(DATA_DIR, ALLOWED_DOCUMENT_EXTENSIONS)
    return {"files": files}

@app.post("/api/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a document to the data folder"""
    try:
        # Validate file extension
        if not validate_file_extension(file.filename, ALLOWED_DOCUMENT_EXTENSIONS):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}"
            )
        
        # Create data directory if it doesn't exist
        DATA_DIR.mkdir(exist_ok=True)
        
        # Read and save file
        content = await file.read()
        file_path = DATA_DIR / file.filename
        actual_path = save_file_with_timestamp(file_path, content)
        
        return {
            "message": "File uploaded successfully",
            "filename": actual_path.name,
            "size": len(content),
            "path": str(actual_path.relative_to(BASE_DIR))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

@app.delete("/api/files/input/{filename}")
async def delete_input_file(filename: str):
    """Delete a file from the data folder"""
    file_path = DATA_DIR / filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        file_path.unlink()
        return {"message": f"File {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@app.post("/api/files/convert/{filename}")
async def convert_pdf_to_markdown(filename: str):
    """Convert a PDF file to Markdown format"""
    pdf_path = DATA_DIR / filename
    
    if not pdf_path.exists() or not pdf_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    if pdf_path.suffix.lower() != '.pdf':
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Create converter instance
        converter = PDFToMarkdownConverter()
        
        # Convert PDF to Markdown
        markdown_content = converter.convert_pdf_to_markdown(pdf_path)
        
        # Generate output filename and save
        markdown_filename = pdf_path.stem + "_converted.md"
        markdown_path = DATA_DIR / markdown_filename
        actual_path = save_text_file_with_timestamp(markdown_path, markdown_content)
        
        return {
            "message": "PDF converted successfully",
            "original_file": filename,
            "markdown_file": actual_path.name,
            "size": len(markdown_content),
            "path": str(actual_path.relative_to(BASE_DIR))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert PDF: {str(e)}")

@app.get("/api/files/output")
async def list_output_files():
    """List generated output files"""
    files = list_files_in_directory(OUTPUT_DIR, OUTPUT_EXTENSIONS)
    return {"files": files}

@app.get("/api/files/output/{filename}")
async def get_output_file(filename: str):
    """Download an output file"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return markdown content as text for preview
    content = read_markdown_file(file_path)
    if content is not None:
        return JSONResponse(content=content)
    
    return FileResponse(file_path)

@app.get("/api/config/agents")
async def get_agents_config():
    """Get agents configuration"""
    config_path = CONFIG_DIR / "agents.yaml"
    return read_yaml_config(config_path)

@app.put("/api/config/agents")
async def update_agents_config(config: Dict[str, Any]):
    """Update agents configuration"""
    config_path = CONFIG_DIR / "agents.yaml"
    try:
        update_yaml_config(config_path, config)
        return {"message": "Agents configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")

@app.get("/api/config/tasks")
async def get_tasks_config():
    """Get tasks configuration"""
    config_path = CONFIG_DIR / "tasks.yaml"
    return read_yaml_config(config_path)

@app.put("/api/config/tasks")
async def update_tasks_config(config: Dict[str, Any]):
    """Update tasks configuration"""
    config_path = CONFIG_DIR / "tasks.yaml"
    try:
        update_yaml_config(config_path, config)
        return {"message": "Tasks configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")

# Ratio Configuration Endpoints
@app.get("/api/ratios")
async def get_all_ratios():
    """Get all ratio configurations"""
    return ratio_config_manager.get_all_ratios()

@app.get("/api/ratios/enabled")
async def get_enabled_ratios():
    """Get only enabled ratio configurations"""
    return ratio_config_manager.get_enabled_ratios()

@app.put("/api/ratios")
async def update_all_ratios(ratios_config: Dict[str, Any]):
    """Update all ratio configurations"""
    try:
        success = ratio_config_manager.update_all_ratios(ratios_config)
        if success:
            return {"message": "Ratio configurations updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update ratio configurations")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ratios: {str(e)}")

@app.put("/api/ratios/{category}/{ratio_key}")
async def update_single_ratio(category: str, ratio_key: str, config: Dict[str, Any]):
    """Update a single ratio configuration"""
    try:
        success = ratio_config_manager.update_ratio(category, ratio_key, config)
        if success:
            return {"message": f"Ratio {ratio_key} updated successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Ratio {category}/{ratio_key} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ratio: {str(e)}")

@app.post("/api/ratios/{category}/{ratio_key}/enable")
async def enable_ratio(category: str, ratio_key: str):
    """Enable a specific ratio"""
    success = ratio_config_manager.enable_ratio(category, ratio_key)
    if success:
        return {"message": f"Ratio {ratio_key} enabled"}
    else:
        raise HTTPException(status_code=404, detail=f"Ratio {category}/{ratio_key} not found")

@app.post("/api/ratios/{category}/{ratio_key}/disable")
async def disable_ratio(category: str, ratio_key: str):
    """Disable a specific ratio"""
    success = ratio_config_manager.disable_ratio(category, ratio_key)
    if success:
        return {"message": f"Ratio {ratio_key} disabled"}
    else:
        raise HTTPException(status_code=404, detail=f"Ratio {category}/{ratio_key} not found")

@app.get("/api/archive")
async def list_archive():
    """List all archived analyses"""
    from core.config import ARCHIVE_DIR
    archives = list_archives(ARCHIVE_DIR)
    return {"archives": archives}

@app.get("/api/archive/{timestamp}/{filename}")
async def get_archive_file(timestamp: str, filename: str):
    """Download a file from archive"""
    from core.config import ARCHIVE_DIR
    
    # Try to get markdown content
    content = get_archive_file_content(ARCHIVE_DIR, timestamp, filename)
    if content is not None:
        return JSONResponse(content=content)
    
    # Otherwise return file
    archive_path = ARCHIVE_DIR / timestamp / filename
    if not archive_path.exists() or not archive_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(archive_path)

# Rules Management Endpoints (simplified imports)
from backend.api.rules import router as rules_router
app.include_router(rules_router, prefix="/api/rules")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)