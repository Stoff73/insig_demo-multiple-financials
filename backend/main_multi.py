from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
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
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path for crew imports
sys.path.append(str(Path(__file__).parent.parent / "src"))
from xp_power_demo.crew import XpPowerDemo
from xp_power_demo.multi_company_crew import MultiCompanyXpPowerDemo

# Add backend to path for modules
sys.path.append(str(Path(__file__).parent))

# Import from core modules for cleaner architecture
try:
    from core.pdf_converter import PDFToMarkdownConverter as BestPDFToMarkdownConverter
    from core.archive import archive_company_outputs as core_archive_company
    from core.file_utils import sanitize_ticker as core_sanitize_ticker, list_files_in_directory
    USE_CORE_MODULES = True
except ImportError:
    # Fallback to original imports if core modules not available
    from pdf_converter_best import BestPDFToMarkdownConverter
    USE_CORE_MODULES = False
    core_sanitize_ticker = None
    core_archive_company = None

from rules_manager import RulesManager

app = FastAPI(title="Multi-Company XP Power Analysis API", version="2.0.0")

# Initialize rules manager
rules_manager = RulesManager()

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

# Store active analyses by company
active_company_analyses: Dict[str, List[str]] = {}

class CompanyInfo(BaseModel):
    ticker: str = Field(..., description="Company ticker symbol (e.g., XPP, AAPL)")
    name: str = Field(..., description="Company full name")
    
class MultiCompanyAnalysisRequest(BaseModel):
    companies: List[CompanyInfo] = Field(..., min_items=1, max_items=10)
    year: str = Field(default="2024", description="Analysis year")
    parallel: bool = Field(default=False, description="Run analyses in parallel")

class SingleCompanyAnalysisRequest(BaseModel):
    company: str = "XP Power"
    ticker: str = "XPP"
    year: str = "2024"

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: int
    logs: List[str]
    result: Optional[str] = None
    error: Optional[str] = None
    company: Optional[str] = None
    ticker: Optional[str] = None

def sanitize_ticker(ticker: str) -> str:
    """Sanitize ticker symbol for use in file paths"""
    if USE_CORE_MODULES and core_sanitize_ticker:
        return core_sanitize_ticker(ticker)
    else:
        # Remove any non-alphanumeric characters and convert to uppercase
        return re.sub(r'[^A-Za-z0-9]', '', ticker).upper()

def archive_company_outputs(ticker: str):
    """Archive existing output files for a specific company before new analysis"""
    ticker = sanitize_ticker(ticker)
    
    if USE_CORE_MODULES and core_archive_company:
        return core_archive_company(ticker)
    else:
        # Original implementation
        output_dir = Path(__file__).parent.parent / "output" / "companies" / ticker
        archive_dir = Path(__file__).parent.parent / "archive" / "companies" / ticker
        
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
        
        return timestamp

def run_single_company_analysis(task_id: str, company_info: CompanyInfo, year: str):
    """Run crew analysis for a single company"""
    try:
        ticker = sanitize_ticker(company_info.ticker)
        
        # Archive existing outputs for this company
        archive_timestamp = archive_company_outputs(ticker)
        if archive_timestamp:
            running_tasks[task_id]["logs"].append(
                f"Archived previous {ticker} outputs to: archive/companies/{ticker}/{archive_timestamp}"
            )
        
        # Update status
        running_tasks[task_id]["status"] = "running"
        running_tasks[task_id]["logs"].append(f"Starting analysis for {company_info.name} ({ticker})")
        
        # Initialize multi-company crew
        crew_instance = MultiCompanyXpPowerDemo(
            company_ticker=ticker,
            company_name=company_info.name
        )
        
        # Track progress through tasks
        tasks = [
            "Analyzing primary ratios",
            "Checking ownership structure",
            "Evaluating earnings quality",
            "Assessing balance sheet durability",
            "Making investment decision"
        ]
        
        for i, task_name in enumerate(tasks):
            running_tasks[task_id]["progress"] = int((i / len(tasks)) * 100)
            running_tasks[task_id]["logs"].append(f"{ticker}: Executing {task_name}")
        
        # Run the crew with date/time
        from datetime import datetime
        current_datetime = datetime.now()
        inputs = {
            'company': company_info.name,
            'company_ticker': ticker,
            'current_year': year,
            'current_date': current_datetime.strftime('%Y-%m-%d'),
            'current_time': current_datetime.strftime('%H:%M:%S')
        }
        
        result = crew_instance.kickoff(inputs=inputs)
        
        # Update completion
        running_tasks[task_id]["status"] = "completed"
        running_tasks[task_id]["progress"] = 100
        running_tasks[task_id]["result"] = str(result) if result else f"Analysis completed for {company_info.name}"
        running_tasks[task_id]["logs"].append(f"Analysis completed successfully for {ticker}")
        running_tasks[task_id]["archive_timestamp"] = archive_timestamp
        running_tasks[task_id]["output_path"] = f"output/companies/{ticker}"
        
    except Exception as e:
        running_tasks[task_id]["status"] = "error"
        running_tasks[task_id]["error"] = str(e)
        running_tasks[task_id]["logs"].append(f"Error analyzing {company_info.name}: {str(e)}")

def run_multi_company_analysis(parent_task_id: str, companies: List[CompanyInfo], year: str, parallel: bool):
    """Orchestrate analysis for multiple companies"""
    try:
        running_tasks[parent_task_id]["status"] = "running"
        running_tasks[parent_task_id]["logs"].append(
            f"Starting multi-company analysis for {len(companies)} companies"
        )
        
        # Create sub-tasks for each company
        sub_task_ids = []
        for company in companies:
            sub_task_id = str(uuid.uuid4())
            ticker = sanitize_ticker(company.ticker)
            
            running_tasks[sub_task_id] = {
                "task_id": sub_task_id,
                "parent_task_id": parent_task_id,
                "status": "pending",
                "progress": 0,
                "logs": [f"Sub-task created for {company.name} ({ticker})"],
                "result": None,
                "error": None,
                "company": company.name,
                "ticker": ticker,
                "year": year
            }
            sub_task_ids.append(sub_task_id)
            
            # Track active analysis for this company
            if ticker not in active_company_analyses:
                active_company_analyses[ticker] = []
            active_company_analyses[ticker].append(sub_task_id)
        
        running_tasks[parent_task_id]["sub_tasks"] = sub_task_ids
        
        # Run analyses
        if parallel:
            # Run all companies in parallel (be careful with resource usage)
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for i, (company, sub_task_id) in enumerate(zip(companies, sub_task_ids)):
                    future = executor.submit(run_single_company_analysis, sub_task_id, company, year)
                    futures.append(future)
                
                # Wait for all to complete
                concurrent.futures.wait(futures)
        else:
            # Run sequentially
            for i, (company, sub_task_id) in enumerate(zip(companies, sub_task_ids)):
                running_tasks[parent_task_id]["progress"] = int((i / len(companies)) * 100)
                running_tasks[parent_task_id]["logs"].append(f"Processing company {i+1}/{len(companies)}: {company.name}")
                run_single_company_analysis(sub_task_id, company, year)
        
        # Check if all sub-tasks completed successfully
        all_completed = all(
            running_tasks[sub_id]["status"] == "completed" 
            for sub_id in sub_task_ids
        )
        
        if all_completed:
            running_tasks[parent_task_id]["status"] = "completed"
            running_tasks[parent_task_id]["progress"] = 100
            running_tasks[parent_task_id]["logs"].append("All company analyses completed successfully")
            
            # Compile summary results
            summary = []
            for sub_id in sub_task_ids:
                sub_task = running_tasks[sub_id]
                summary.append({
                    "company": sub_task["company"],
                    "ticker": sub_task["ticker"],
                    "status": sub_task["status"],
                    "output_path": sub_task.get("output_path", "")
                })
            running_tasks[parent_task_id]["summary"] = summary
        else:
            running_tasks[parent_task_id]["status"] = "partial_completion"
            failed_companies = [
                running_tasks[sub_id]["company"] 
                for sub_id in sub_task_ids 
                if running_tasks[sub_id]["status"] == "error"
            ]
            running_tasks[parent_task_id]["logs"].append(
                f"Analysis completed with errors. Failed companies: {', '.join(failed_companies)}"
            )
        
    except Exception as e:
        running_tasks[parent_task_id]["status"] = "error"
        running_tasks[parent_task_id]["error"] = str(e)
        running_tasks[parent_task_id]["logs"].append(f"Error in multi-company analysis: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Multi-Company XP Power Analysis API", "status": "running", "version": "2.0.0"}

@app.post("/api/analysis/start")
async def start_analysis(request: SingleCompanyAnalysisRequest, background_tasks: BackgroundTasks):
    """Start a single company analysis (backward compatibility)"""
    task_id = str(uuid.uuid4())
    ticker = sanitize_ticker(request.ticker)
    
    # Initialize task tracking
    running_tasks[task_id] = {
        "task_id": task_id,
        "status": "initializing",
        "progress": 0,
        "logs": [f"Task {task_id} created at {datetime.now().isoformat()}"],
        "result": None,
        "error": None,
        "company": request.company,
        "ticker": ticker,
        "year": request.year
    }
    
    # Track active analysis
    if ticker not in active_company_analyses:
        active_company_analyses[ticker] = []
    active_company_analyses[ticker].append(task_id)
    
    # Start background task
    company_info = CompanyInfo(ticker=request.ticker, name=request.company)
    background_tasks.add_task(run_single_company_analysis, task_id, company_info, request.year)
    
    return {"task_id": task_id, "message": f"Analysis started for {request.company}"}

@app.post("/api/analysis/start-multi")
async def start_multi_company_analysis(request: MultiCompanyAnalysisRequest, background_tasks: BackgroundTasks):
    """Start analysis for multiple companies"""
    if len(request.companies) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 companies allowed per analysis")
    
    task_id = str(uuid.uuid4())
    
    # Initialize parent task tracking
    running_tasks[task_id] = {
        "task_id": task_id,
        "status": "initializing",
        "progress": 0,
        "logs": [f"Multi-company task {task_id} created at {datetime.now().isoformat()}"],
        "result": None,
        "error": None,
        "companies": [{"name": c.name, "ticker": c.ticker} for c in request.companies],
        "year": request.year,
        "parallel": request.parallel
    }
    
    # Start background task
    background_tasks.add_task(
        run_multi_company_analysis, 
        task_id, 
        request.companies, 
        request.year,
        request.parallel
    )
    
    return {
        "task_id": task_id, 
        "message": f"Multi-company analysis started for {len(request.companies)} companies",
        "companies": [c.dict() for c in request.companies]
    }

@app.get("/api/analysis/status/{task_id}")
async def get_status(task_id: str):
    """Get status of an analysis task"""
    if task_id not in running_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data = running_tasks[task_id].copy()
    
    # Include sub-task information if this is a parent task
    if "sub_tasks" in task_data:
        sub_task_statuses = []
        for sub_id in task_data["sub_tasks"]:
            if sub_id in running_tasks:
                sub_task = running_tasks[sub_id]
                sub_task_statuses.append({
                    "task_id": sub_id,
                    "company": sub_task.get("company"),
                    "ticker": sub_task.get("ticker"),
                    "status": sub_task.get("status"),
                    "progress": sub_task.get("progress"),
                    "error": sub_task.get("error")
                })
        task_data["sub_task_statuses"] = sub_task_statuses
    
    return task_data

@app.get("/api/analysis/list")
async def list_analyses():
    """List all analysis tasks"""
    # Filter to show only parent tasks and standalone tasks
    tasks = []
    for task_id, task_data in running_tasks.items():
        if "parent_task_id" not in task_data:  # Not a sub-task
            tasks.append(task_data)
    return tasks

@app.get("/api/analysis/company/{ticker}")
async def get_company_analyses(ticker: str):
    """Get all analyses for a specific company"""
    ticker = sanitize_ticker(ticker)
    
    if ticker not in active_company_analyses:
        return {"ticker": ticker, "analyses": []}
    
    analyses = []
    for task_id in active_company_analyses[ticker]:
        if task_id in running_tasks:
            analyses.append(running_tasks[task_id])
    
    return {"ticker": ticker, "analyses": analyses}

@app.post("/api/files/upload/{ticker}")
async def upload_company_file(ticker: str, file: UploadFile = File(...)):
    """Upload a document for a specific company"""
    try:
        ticker = sanitize_ticker(ticker)
        
        # Validate file extension
        allowed_extensions = ['.md', '.pdf', '.txt', '.csv', '.xlsx', '.docx']
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Create company-specific data directory
        data_dir = Path(__file__).parent.parent / "data" / "companies" / ticker
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Save the file
        file_path = data_dir / file.filename
        
        # Check if file already exists
        if file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = file_path.stem
            suffix = file_path.suffix
            file_path = data_dir / f"{stem}_{timestamp}{suffix}"
        
        # Write file content
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return {
            "message": f"File uploaded successfully for {ticker}",
            "filename": file_path.name,
            "ticker": ticker,
            "size": len(content),
            "path": str(file_path.relative_to(Path(__file__).parent.parent))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

@app.get("/api/files/company/{ticker}")
async def list_company_files(ticker: str):
    """List files for a specific company"""
    ticker = sanitize_ticker(ticker)
    data_dir = Path(__file__).parent.parent / "data" / "companies" / ticker
    
    if not data_dir.exists():
        return {"ticker": ticker, "files": []}
    
    files = []
    for file in data_dir.iterdir():
        if file.is_file() and file.suffix in ['.md', '.pdf', '.txt', '.csv', '.xlsx', '.docx']:
            files.append({
                "name": file.name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    
    return {"ticker": ticker, "files": files}

@app.delete("/api/files/company/{ticker}/{filename}")
async def delete_company_file(ticker: str, filename: str):
    """Delete a file from a company's data folder"""
    ticker = sanitize_ticker(ticker)
    data_dir = Path(__file__).parent.parent / "data" / "companies" / ticker
    file_path = data_dir / filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        file_path.unlink()
        return {"message": f"File {filename} deleted successfully for {ticker}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@app.post("/api/files/convert/company/{ticker}/{filename}")
async def convert_company_pdf_to_markdown(ticker: str, filename: str):
    """Convert a company's PDF file to Markdown format"""
    ticker = sanitize_ticker(ticker)
    data_dir = Path(__file__).parent.parent / "data" / "companies" / ticker
    pdf_path = data_dir / filename
    
    if not pdf_path.exists() or not pdf_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    if pdf_path.suffix.lower() != '.pdf':
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        converter = BestPDFToMarkdownConverter()
        
        # Generate output filename
        markdown_filename = pdf_path.stem + "_converted.md"
        markdown_path = data_dir / markdown_filename
        
        if markdown_path.exists():
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
            "ticker": ticker,
            "original_file": filename,
            "markdown_file": markdown_filename,
            "size": len(markdown_content),
            "path": str(markdown_path.relative_to(Path(__file__).parent.parent))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert PDF: {str(e)}")

@app.get("/api/files/output/company/{ticker}")
async def list_company_output_files(ticker: str):
    """List generated output files for a specific company"""
    ticker = sanitize_ticker(ticker)
    output_dir = Path(__file__).parent.parent / "output" / "companies" / ticker
    
    if not output_dir.exists():
        return {"ticker": ticker, "files": []}
    
    files = []
    for file in output_dir.iterdir():
        if file.suffix in ['.md', '.pdf']:
            files.append({
                "name": file.name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    
    return {"ticker": ticker, "files": sorted(files, key=lambda x: x["modified"], reverse=True)}

@app.get("/api/files/output/company/{ticker}/{filename}")
async def get_company_output_file(ticker: str, filename: str):
    """Download an output file for a specific company"""
    ticker = sanitize_ticker(ticker)
    output_dir = Path(__file__).parent.parent / "output" / "companies" / ticker
    file_path = output_dir / filename
    
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    if filename.endswith('.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return JSONResponse(content={"content": content, "ticker": ticker, "filename": filename})
    
    return FileResponse(file_path)

@app.get("/api/archive/company/{ticker}")
async def list_company_archive(ticker: str):
    """List all archived analyses for a specific company"""
    ticker = sanitize_ticker(ticker)
    archive_dir = Path(__file__).parent.parent / "archive" / "companies" / ticker
    
    if not archive_dir.exists():
        return {"ticker": ticker, "archives": []}
    
    archives = []
    for folder in sorted(archive_dir.iterdir(), reverse=True):
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
                "timestamp": folder.name,
                "date": datetime.strptime(folder.name, "%Y%m%d_%H%M%S").isoformat() if '_' in folder.name else folder.name,
                "files": files,
                "file_count": len(files)
            })
    
    return {"ticker": ticker, "archives": archives}

@app.get("/api/archive/company/{ticker}/{timestamp}/{filename}")
async def get_company_archive_file(ticker: str, timestamp: str, filename: str):
    """Download a file from a company's archive"""
    ticker = sanitize_ticker(ticker)
    archive_path = Path(__file__).parent.parent / "archive" / "companies" / ticker / timestamp / filename
    
    if not archive_path.exists() or not archive_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    if filename.endswith('.md'):
        with open(archive_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return JSONResponse(content={"content": content, "ticker": ticker, "filename": filename})
    
    return FileResponse(archive_path)

@app.get("/api/companies/list")
async def list_all_companies():
    """List all companies with data in the system"""
    companies = set()
    
    # Check data directory
    data_companies_dir = Path(__file__).parent.parent / "data" / "companies"
    if data_companies_dir.exists():
        for ticker_dir in data_companies_dir.iterdir():
            if ticker_dir.is_dir():
                companies.add(ticker_dir.name)
    
    # Check output directory
    output_companies_dir = Path(__file__).parent.parent / "output" / "companies"
    if output_companies_dir.exists():
        for ticker_dir in output_companies_dir.iterdir():
            if ticker_dir.is_dir():
                companies.add(ticker_dir.name)
    
    # Check archive directory
    archive_companies_dir = Path(__file__).parent.parent / "archive" / "companies"
    if archive_companies_dir.exists():
        for ticker_dir in archive_companies_dir.iterdir():
            if ticker_dir.is_dir():
                companies.add(ticker_dir.name)
    
    # Get company details
    company_list = []
    for ticker in sorted(companies):
        company_info = {
            "ticker": ticker,
            "has_data": (data_companies_dir / ticker).exists(),
            "has_output": (output_companies_dir / ticker).exists(),
            "has_archive": (archive_companies_dir / ticker).exists(),
        }
        
        # Count files
        if company_info["has_data"]:
            data_dir = data_companies_dir / ticker
            company_info["data_file_count"] = len(list(data_dir.glob("*")))
        
        if company_info["has_output"]:
            output_dir = output_companies_dir / ticker
            company_info["output_file_count"] = len(list(output_dir.glob("*.md")))
        
        if company_info["has_archive"]:
            archive_dir = archive_companies_dir / ticker
            company_info["archive_count"] = len(list(archive_dir.iterdir()))
        
        company_list.append(company_info)
    
    return {"companies": company_list, "total": len(company_list)}

# Keep all existing endpoints for backward compatibility
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
    
    backup_path = config_path.with_suffix('.yaml.bak')
    shutil.copy(config_path, backup_path)
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        return {"message": "Agents configuration updated successfully"}
    except Exception as e:
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
    
    backup_path = config_path.with_suffix('.yaml.bak')
    shutil.copy(config_path, backup_path)
    
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        return {"message": "Tasks configuration updated successfully"}
    except Exception as e:
        shutil.copy(backup_path, config_path)
        raise HTTPException(status_code=500, detail=f"Failed to update configuration: {str(e)}")

# Include all rules management endpoints from original main.py
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)