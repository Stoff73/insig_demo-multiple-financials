"""Task runner for crew analysis.

This module centralizes the logic for running analyses and tracking
their progress, providing persistence and status management.
"""

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add src to path for crew imports
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from .config import ANALYSIS_TASKS
from .archive import archive_existing_outputs, archive_company_outputs
from .file_utils import sanitize_ticker


class TaskRunner:
    """Manages crew analysis tasks and their persistence.
    
    Handles creation, updating, and persistence of analysis tasks
    with support for progress tracking and error management.
    
    Attributes:
        tasks_file: Path to the JSON file for task persistence.
        running_tasks: Dictionary of active tasks.
    """
    
    def __init__(self, tasks_file: Optional[Path] = None) -> None:
        """Initialize the task runner.
        
        Args:
            tasks_file: Optional path to tasks persistence file.
        """
        self.tasks_file = (
            tasks_file or Path(__file__).parent.parent / "tasks.json"
        )
        self.running_tasks: Dict[str, Dict[str, Any]] = {}
        self.load_tasks()
    
    def save_tasks(self) -> None:
        """Save tasks to file for persistence."""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.running_tasks, f, indent=2, default=str)
    
    def load_tasks(self) -> None:
        """Load tasks from file if exists."""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    self.running_tasks = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading tasks: {e}")
                self.running_tasks = {}
    
    def create_task(
        self, company: str, year: str, ticker: Optional[str] = None
    ) -> str:
        """Create a new analysis task.
        
        Args:
            company: Company name.
            year: Year for analysis.
            ticker: Optional ticker symbol.
        
        Returns:
            Unique task identifier.
        """
        task_id = str(uuid.uuid4())
        
        created_at = datetime.now().isoformat()
        task_data = {
            "task_id": task_id,
            "status": "initializing",
            "progress": 0,
            "logs": [f"Task {task_id} created at {created_at}"],
            "result": None,
            "error": None,
            "company": company,
            "year": year,
            "created_at": created_at
        }
        
        if ticker:
            task_data["ticker"] = sanitize_ticker(ticker)
        
        self.running_tasks[task_id] = task_data
        self.save_tasks()
        
        return task_id
    
    def update_task_status(
        self, task_id: str, status: str, message: Optional[str] = None
    ) -> None:
        """Update task status.
        
        Args:
            task_id: Unique task identifier.
            status: New status value.
            message: Optional log message.
        """
        if task_id in self.running_tasks:
            self.running_tasks[task_id]["status"] = status
            if message:
                self.running_tasks[task_id]["logs"].append(message)
            self.save_tasks()
    
    def update_task_progress(
        self, task_id: str, progress: int, message: Optional[str] = None
    ) -> None:
        """Update task progress.
        
        Args:
            task_id: Unique task identifier.
            progress: Progress percentage (0-100).
            message: Optional log message.
        """
        if task_id in self.running_tasks:
            self.running_tasks[task_id]["progress"] = progress
            if message:
                self.running_tasks[task_id]["logs"].append(message)
            self.save_tasks()
    
    def set_task_result(
        self, 
        task_id: str, 
        result: Any, 
        archive_timestamp: Optional[str] = None
    ) -> None:
        """Set task result and mark as completed.
        
        Args:
            task_id: Unique task identifier.
            result: Task result data.
            archive_timestamp: Optional archive timestamp.
        """
        if task_id in self.running_tasks:
            self.running_tasks[task_id]["status"] = "completed"
            self.running_tasks[task_id]["progress"] = 100
            self.running_tasks[task_id]["result"] = (
                str(result) if result else "Analysis completed"
            )
            self.running_tasks[task_id]["logs"].append(
                "Analysis completed successfully"
            )
            
            if archive_timestamp:
                self.running_tasks[task_id]["archive_timestamp"] = archive_timestamp
            
            self.save_tasks()
    
    def set_task_error(self, task_id: str, error: str) -> None:
        """Set task error.
        
        Args:
            task_id: Unique task identifier.
            error: Error message.
        """
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
    
    def run_single_company_analysis(
        self, task_id: str, company: str, year: str
    ) -> None:
        """Run crew analysis for a single company.
        
        Args:
            task_id: Unique task identifier.
            company: Company name.
            year: Year for analysis.
        """
        try:
            from src.insig_analyst_demo.crew import InsigAnalystDemo
            
            # Archive existing outputs
            archive_timestamp = archive_existing_outputs()
            if archive_timestamp:
                self.update_task_status(
                    task_id, "running", 
                    f"Archived previous outputs to: "
                    f"archive/{archive_timestamp}"
                )
            else:
                self.update_task_status(
                    task_id, "running", 
                    f"Starting analysis for {company} ({year})"
                )
            
            # Initialize crew
            crew_instance = InsigAnalystDemo()
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
