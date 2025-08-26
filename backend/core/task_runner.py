"""
Task runner for crew analysis
Centralizes the logic for running analyses and tracking progress
"""
import uuid
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import sys

# Add src to path for crew imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from .config import ANALYSIS_TASKS
from .archive import archive_existing_outputs, archive_company_outputs
from .file_utils import sanitize_ticker


class TaskRunner:
    """Manages crew analysis tasks and their persistence"""
    
    def __init__(self, tasks_file: Path = None):
        self.tasks_file = tasks_file or Path(__file__).parent.parent / "tasks.json"
        self.running_tasks: Dict[str, Dict[str, Any]] = {}
        self.load_tasks()
    
    def save_tasks(self):
        """Save tasks to file for persistence"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.running_tasks, f, indent=2, default=str)
    
    def load_tasks(self):
        """Load tasks from file if exists"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    self.running_tasks = json.load(f)
            except Exception as e:
                print(f"Error loading tasks: {e}")
                self.running_tasks = {}
    
    def create_task(self, company: str, year: str, ticker: Optional[str] = None) -> str:
        """Create a new analysis task"""
        task_id = str(uuid.uuid4())
        
        task_data = {
            "task_id": task_id,
            "status": "initializing",
            "progress": 0,
            "logs": [f"Task {task_id} created at {datetime.now().isoformat()}"],
            "result": None,
            "error": None,
            "company": company,
            "year": year,
            "created_at": datetime.now().isoformat()
        }
        
        if ticker:
            task_data["ticker"] = sanitize_ticker(ticker)
        
        self.running_tasks[task_id] = task_data
        self.save_tasks()
        
        return task_id
    
    def update_task_status(self, task_id: str, status: str, message: str = None):
        """Update task status"""
        if task_id in self.running_tasks:
            self.running_tasks[task_id]["status"] = status
            if message:
                self.running_tasks[task_id]["logs"].append(message)
            self.save_tasks()
    
    def update_task_progress(self, task_id: str, progress: int, message: str = None):
        """Update task progress"""
        if task_id in self.running_tasks:
            self.running_tasks[task_id]["progress"] = progress
            if message:
                self.running_tasks[task_id]["logs"].append(message)
            self.save_tasks()
    
    def set_task_result(self, task_id: str, result: Any, archive_timestamp: Optional[str] = None):
        """Set task result and mark as completed"""
        if task_id in self.running_tasks:
            self.running_tasks[task_id]["status"] = "completed"
            self.running_tasks[task_id]["progress"] = 100
            self.running_tasks[task_id]["result"] = str(result) if result else "Analysis completed"
            self.running_tasks[task_id]["logs"].append("Analysis completed successfully")
            
            if archive_timestamp:
                self.running_tasks[task_id]["archive_timestamp"] = archive_timestamp
            
            self.save_tasks()
    
    def set_task_error(self, task_id: str, error: str):
        """Set task error"""
        if task_id in self.running_tasks:
            self.running_tasks[task_id]["status"] = "error"
            self.running_tasks[task_id]["error"] = str(error)
            self.running_tasks[task_id]["logs"].append(f"Error: {str(error)}")
            self.save_tasks()
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task data"""
        return self.running_tasks.get(task_id)
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks"""
        return list(self.running_tasks.values())
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task"""
        if task_id in self.running_tasks:
            if self.running_tasks[task_id]["status"] == "running":
                self.running_tasks[task_id]["status"] = "cancelled"
                self.running_tasks[task_id]["logs"].append("Analysis cancelled by user")
                self.save_tasks()
                return True
        return False
    
    def run_single_company_analysis(self, task_id: str, company: str, year: str):
        """Run crew analysis for a single company"""
        try:
            from xp_power_demo.crew import XpPowerDemo
            
            # Archive existing outputs
            archive_timestamp = archive_existing_outputs()
            if archive_timestamp:
                self.update_task_status(task_id, "running", 
                    f"Archived previous outputs to: archive/{archive_timestamp}")
            else:
                self.update_task_status(task_id, "running", 
                    f"Starting analysis for {company} ({year})")
            
            # Initialize crew
            crew_instance = XpPowerDemo()
            crew = crew_instance.crew()
            
            # Track progress through tasks
            for i, task_name in enumerate(ANALYSIS_TASKS):
                self.update_task_progress(
                    task_id, 
                    int((i / len(ANALYSIS_TASKS)) * 100),
                    f"Executing: {task_name}"
                )
            
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
            self.set_task_result(task_id, result, archive_timestamp)
            
        except Exception as e:
            self.set_task_error(task_id, str(e))
    
    def run_multi_company_analysis(self, task_id: str, company_info: Dict[str, str], year: str):
        """Run crew analysis for a company in multi-company mode"""
        try:
            from xp_power_demo.multi_company_crew import MultiCompanyXpPowerDemo
            
            ticker = sanitize_ticker(company_info['ticker'])
            
            # Archive existing outputs for this company
            archive_timestamp = archive_company_outputs(ticker)
            if archive_timestamp:
                self.update_task_status(task_id, "running",
                    f"Archived previous {ticker} outputs to: archive/companies/{ticker}/{archive_timestamp}")
            else:
                self.update_task_status(task_id, "running",
                    f"Starting analysis for {company_info['name']} ({ticker})")
            
            # Initialize multi-company crew
            crew_instance = MultiCompanyXpPowerDemo(
                company_ticker=ticker,
                company_name=company_info['name']
            )
            
            # Track progress through tasks
            for i, task_name in enumerate(ANALYSIS_TASKS):
                self.update_task_progress(
                    task_id,
                    int((i / len(ANALYSIS_TASKS)) * 100),
                    f"{ticker}: Executing {task_name}"
                )
            
            # Run the crew
            from datetime import datetime
            current_datetime = datetime.now()
            inputs = {
                'company': company_info['name'],
                'company_ticker': ticker,
                'current_year': year,
                'current_date': current_datetime.strftime('%Y-%m-%d'),
                'current_time': current_datetime.strftime('%H:%M:%S')
            }
            
            result = crew_instance.kickoff(inputs=inputs)
            
            # Update completion
            self.running_tasks[task_id]["output_path"] = f"output/companies/{ticker}"
            self.set_task_result(task_id, result, archive_timestamp)
            
        except Exception as e:
            self.set_task_error(task_id, str(e))