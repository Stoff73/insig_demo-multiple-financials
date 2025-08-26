"""
Rules management API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from pathlib import Path
import sys
import yaml

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))
from rules_manager import RulesManager

router = APIRouter()
rules_manager = RulesManager()

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

class TaskAssignment(BaseModel):
    task_name: str

@router.get("")
async def get_all_rules():
    """Get all analysis rules"""
    return rules_manager.get_all_rules()

@router.get("/category/{category}")
async def get_rules_by_category(category: str):
    """Get rules for a specific category"""
    rules = rules_manager.get_rules_by_category(category)
    if not rules:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    return rules

@router.get("/task/{task_name}")
async def get_rules_for_task(task_name: str):
    """Get all rules that apply to a specific task"""
    return rules_manager.get_rules_for_task(task_name)

@router.post("/{category}/{rule_id}")
async def add_rule(category: str, rule_id: str, rule_data: RuleData):
    """Add a new rule"""
    success = rules_manager.add_rule(category, rule_id, rule_data.dict())
    if not success:
        raise HTTPException(status_code=400, detail="Rule already exists")
    return {"message": "Rule added successfully", "category": category, "rule_id": rule_id}

@router.put("/{category}/{rule_id}")
async def update_rule(category: str, rule_id: str, rule_data: RuleData):
    """Update an existing rule"""
    success = rules_manager.update_rule(category, rule_id, rule_data.dict())
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Update tasks configuration if needed
    await update_task_rules(rule_id, category, rule_data.applies_to_tasks)
    
    return {"message": "Rule updated successfully", "category": category, "rule_id": rule_id}

@router.delete("/{category}/{rule_id}")
async def delete_rule(category: str, rule_id: str):
    """Delete a rule"""
    success = rules_manager.delete_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule deleted successfully"}

@router.post("/{category}/{rule_id}/assign")
async def assign_rule_to_task(category: str, rule_id: str, assignment: TaskAssignment):
    """Assign a rule to a task"""
    success = rules_manager.assign_rule_to_task(category, rule_id, assignment.task_name)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    # Update task configuration
    await update_task_with_rule(assignment.task_name, rule_id, category)
    
    return {"message": f"Rule assigned to task {assignment.task_name}"}

@router.post("/{category}/{rule_id}/unassign")
async def remove_rule_from_task(category: str, rule_id: str, assignment: TaskAssignment):
    """Remove a rule from a task"""
    success = rules_manager.remove_rule_from_task(category, rule_id, assignment.task_name)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found or not assigned to task")
    
    return {"message": f"Rule removed from task {assignment.task_name}"}

@router.post("/{category}/{rule_id}/enable")
async def enable_rule(category: str, rule_id: str):
    """Enable a rule"""
    success = rules_manager.enable_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule enabled"}

@router.post("/{category}/{rule_id}/disable")
async def disable_rule(category: str, rule_id: str):
    """Disable a rule"""
    success = rules_manager.disable_rule(category, rule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"message": "Rule disabled"}

@router.get("/export/{task_name}")
async def export_rules_for_task(task_name: str):
    """Export rules for a task as formatted text"""
    rules_text = rules_manager.export_rules_for_task(task_name)
    return {"task_name": task_name, "rules_text": rules_text}

# Helper functions for task configuration updates
async def update_task_rules(rule_id: str, category: str, task_names: List[str]):
    """Update task configurations when rules change"""
    config_path = Path(__file__).parent.parent.parent / "src" / "xp_power_demo" / "config" / "tasks.yaml"
    
    if not config_path.exists():
        return
    
    with open(config_path, 'r') as f:
        tasks_config = yaml.safe_load(f)
    
    # Update each task that uses this rule
    for task_name in task_names:
        if task_name in tasks_config:
            # Get the formatted rules for this task
            rules_text = rules_manager.export_rules_for_task(task_name)
            if rules_text:
                tasks_config[task_name]['description'] += f"\n\n{rules_text}"
    
    # Save updated configuration
    with open(config_path, 'w') as f:
        yaml.dump(tasks_config, f, default_flow_style=False, sort_keys=False)

async def update_task_with_rule(task_name: str, rule_id: str, category: str):
    """Update a specific task when a rule is assigned to it"""
    config_path = Path(__file__).parent.parent.parent / "src" / "xp_power_demo" / "config" / "tasks.yaml"
    
    if not config_path.exists():
        return
    
    with open(config_path, 'r') as f:
        tasks_config = yaml.safe_load(f)
    
    if task_name in tasks_config:
        # Get all rules for this task
        rules_text = rules_manager.export_rules_for_task(task_name)
        
        # Update task description with rules
        if rules_text:
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