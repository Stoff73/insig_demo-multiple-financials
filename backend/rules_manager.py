"""
Rules and Thresholds Management System
Handles CRUD operations for financial analysis rules and their integration with tasks
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml
import json
from datetime import datetime
import shutil
from enum import Enum

class RuleStatus(Enum):
    PASS = "pass"
    MONITOR = "monitor"
    FAIL = "fail"

class RuleCategory(Enum):
    VALUATION = "valuation"
    OWNERSHIP = "ownership"
    EARNINGS_QUALITY = "earnings_quality"
    BALANCE_SHEET = "balance_sheet"
    RED_FLAGS = "red_flags"

class RulesManager:
    def __init__(self, rules_file: Path = None):
        if rules_file is None:
            self.rules_file = Path(__file__).parent.parent / "config" / "analysis_rules.yaml"
        else:
            self.rules_file = rules_file
        
        # Create config directory if it doesn't exist
        self.rules_file.parent.mkdir(exist_ok=True)
        
        # Initialize with default rules if file doesn't exist
        if not self.rules_file.exists():
            self._initialize_default_rules()
        
        self.rules = self._load_rules()
    
    def _initialize_default_rules(self):
        """Initialize with default rules from phase1_analysis.md"""
        default_rules = {
            "valuation": {
                "ev_ebitda": {
                    "name": "EV/EBITDA",
                    "description": "Core operating cash flow before capital intensity",
                    "category": "valuation",
                    "metric_type": "ratio",
                    "thresholds": {
                        "pass": {"operator": "<", "value": 5.0},
                        "monitor": {"operator": "between", "min": 5.0, "max": 7.5},
                        "fail": {"operator": ">", "value": 7.5}
                    },
                    "notes": "Unless growth/cyclic case",
                    "applies_to_tasks": ["primary_ratios"],
                    "enabled": True
                },
                "pe_ratio": {
                    "name": "P/E Ratio",
                    "description": "Earnings multiple",
                    "category": "valuation",
                    "metric_type": "ratio",
                    "thresholds": {
                        "pass": {"operator": "<", "value": 10},
                        "monitor": {"operator": "between", "min": 10, "max": 15},
                        "fail": {"operator": ">", "value": 15}
                    },
                    "notes": "Unless secular growth",
                    "applies_to_tasks": ["primary_ratios"],
                    "enabled": True
                },
                "fcf_yield": {
                    "name": "FCF Yield",
                    "description": "Capital return potential (FCF/EV)",
                    "category": "valuation",
                    "metric_type": "percentage",
                    "thresholds": {
                        "pass": {"operator": ">", "value": 10},
                        "monitor": {"operator": "between", "min": 6, "max": 10},
                        "fail": {"operator": "<", "value": 6}
                    },
                    "notes": "Or negative FCF",
                    "applies_to_tasks": ["primary_ratios"],
                    "enabled": True
                },
                "ev_ebit": {
                    "name": "EV/EBIT",
                    "description": "Operating profit base",
                    "category": "valuation",
                    "metric_type": "ratio",
                    "thresholds": {
                        "pass": {"operator": "<", "value": 7},
                        "monitor": {"operator": "between", "min": 7, "max": 10},
                        "fail": {"operator": ">", "value": 10}
                    },
                    "notes": "Unless margin upside evident",
                    "applies_to_tasks": ["primary_ratios"],
                    "enabled": True
                }
            },
            "ownership": {
                "insider_ownership": {
                    "name": "Insider Ownership %",
                    "description": "Aggregate % held by board & execs",
                    "category": "ownership",
                    "metric_type": "percentage",
                    "thresholds": {
                        "pass": {"operator": ">", "value": 10},
                        "monitor": {"operator": "between", "min": 3, "max": 10},
                        "fail": {"operator": "<", "value": 3}
                    },
                    "notes": "Unless family or legacy founder",
                    "applies_to_tasks": ["ownership_task"],
                    "enabled": True
                },
                "recent_insider_buys": {
                    "name": "Recent Insider Transactions",
                    "description": "Last 6-12 months director buys/sells",
                    "category": "ownership",
                    "metric_type": "qualitative",
                    "thresholds": {
                        "pass": {"criteria": "Multiple open-market buys, esp. post-earnings"},
                        "monitor": {"criteria": "1-2 individuals buying"},
                        "fail": {"criteria": "Regular option cash-ins or cluster sales"}
                    },
                    "applies_to_tasks": ["ownership_task"],
                    "enabled": True
                },
                "activist_involvement": {
                    "name": "Activist Involvement",
                    "description": "Presence of activist investors",
                    "category": "ownership",
                    "metric_type": "qualitative",
                    "thresholds": {
                        "pass": {"criteria": "Constructive activist, <12m window"},
                        "monitor": {"criteria": "Passive or hostile activist"},
                        "fail": {"criteria": "Historic failure, forced exits"}
                    },
                    "applies_to_tasks": ["ownership_task"],
                    "enabled": True
                }
            },
            "earnings_quality": {
                "ebitda_fcf_conversion": {
                    "name": "EBITDA-FCF Conversion",
                    "description": "FCF / EBITDA ratio",
                    "category": "earnings_quality",
                    "metric_type": "percentage",
                    "thresholds": {
                        "pass": {"operator": ">", "value": 70},
                        "monitor": {"operator": "between", "min": 40, "max": 70},
                        "fail": {"operator": "<", "value": 40}
                    },
                    "notes": "Or negative FCF",
                    "applies_to_tasks": ["earnings_quality_task"],
                    "enabled": True
                },
                "net_income_cfo_conversion": {
                    "name": "Net Income-CFO Conversion",
                    "description": "OCF / Net Income ratio",
                    "category": "earnings_quality",
                    "metric_type": "ratio",
                    "thresholds": {
                        "pass": {"operator": ">", "value": 1.0},
                        "monitor": {"operator": "between", "min": 0.8, "max": 1.0},
                        "fail": {"operator": "<", "value": 0.8}
                    },
                    "notes": "< 0.8 indicates aggressive accruals",
                    "applies_to_tasks": ["earnings_quality_task"],
                    "enabled": True
                },
                "adjusted_ebitda_variance": {
                    "name": "Recurring vs Adjusted EBITDA",
                    "description": "Compare management-adjusted to statutory",
                    "category": "earnings_quality",
                    "metric_type": "percentage",
                    "thresholds": {
                        "pass": {"operator": "<", "value": 10},
                        "monitor": {"operator": "between", "min": 10, "max": 20},
                        "fail": {"operator": ">", "value": 20}
                    },
                    "notes": "Percentage difference in adjustments",
                    "applies_to_tasks": ["earnings_quality_task"],
                    "enabled": True
                },
                "accruals_ratio": {
                    "name": "Accruals Ratio",
                    "description": "(Net Income - CFO) / Assets",
                    "category": "earnings_quality",
                    "metric_type": "percentage",
                    "thresholds": {
                        "pass": {"operator": "<", "value": 10},
                        "monitor": {"operator": "between", "min": 10, "max": 20},
                        "fail": {"operator": ">", "value": 20}
                    },
                    "notes": "> 20% indicates earnings manipulation risk",
                    "applies_to_tasks": ["earnings_quality_task"],
                    "enabled": True
                }
            },
            "balance_sheet": {
                "net_debt_ebitda": {
                    "name": "Net Debt / EBITDA",
                    "description": "Leverage ratio",
                    "category": "balance_sheet",
                    "metric_type": "ratio",
                    "thresholds": {
                        "pass": {"operator": "<", "value": 2.5},
                        "monitor": {"operator": "between", "min": 2.5, "max": 3.5},
                        "fail": {"operator": ">", "value": 3.5}
                    },
                    "notes": "Or negative EBITDA",
                    "applies_to_tasks": ["balance_sheet_durability_task"],
                    "enabled": True
                },
                "interest_coverage": {
                    "name": "Interest Coverage",
                    "description": "EBIT / Interest Expense",
                    "category": "balance_sheet",
                    "metric_type": "ratio",
                    "thresholds": {
                        "pass": {"operator": ">", "value": 4.0},
                        "monitor": {"operator": "between", "min": 2.0, "max": 4.0},
                        "fail": {"operator": "<", "value": 2.0}
                    },
                    "applies_to_tasks": ["balance_sheet_durability_task"],
                    "enabled": True
                },
                "liquidity_ratio": {
                    "name": "Liquidity",
                    "description": "Cash + undrawn RCF / 12m obligations",
                    "category": "balance_sheet",
                    "metric_type": "ratio",
                    "thresholds": {
                        "pass": {"operator": ">", "value": 1.5},
                        "monitor": {"operator": "between", "min": 1.0, "max": 1.5},
                        "fail": {"operator": "<", "value": 1.0}
                    },
                    "applies_to_tasks": ["balance_sheet_durability_task"],
                    "enabled": True
                },
                "debt_maturity": {
                    "name": "Debt Maturity Profile",
                    "description": "% of debt due within 24 months",
                    "category": "balance_sheet",
                    "metric_type": "percentage",
                    "thresholds": {
                        "pass": {"operator": "<", "value": 25},
                        "monitor": {"operator": "between", "min": 25, "max": 40},
                        "fail": {"operator": ">", "value": 40}
                    },
                    "applies_to_tasks": ["balance_sheet_durability_task"],
                    "enabled": True
                }
            },
            "red_flags": {
                "declining_fcf": {
                    "name": "Declining FCF despite revenue growth",
                    "description": "FCF trend vs revenue trend",
                    "category": "red_flags",
                    "metric_type": "qualitative",
                    "severity": "high",
                    "implication": "Unsustainable model or poor cost control",
                    "applies_to_tasks": ["primary_ratios", "earnings_quality_task"],
                    "enabled": True
                },
                "frequent_one_offs": {
                    "name": "Frequent one-off adjustments",
                    "description": "Adjusted EBITDA with recurring one-offs",
                    "category": "red_flags",
                    "metric_type": "qualitative",
                    "severity": "medium",
                    "implication": "Masking structural margin issues",
                    "applies_to_tasks": ["earnings_quality_task"],
                    "enabled": True
                },
                "working_capital_balloon": {
                    "name": "Ballooning working capital",
                    "description": "Working capital or inventory growth outpacing revenue",
                    "category": "red_flags",
                    "metric_type": "qualitative",
                    "severity": "high",
                    "implication": "Channel stuffing, demand misread",
                    "applies_to_tasks": ["balance_sheet_durability_task"],
                    "enabled": True
                },
                "share_dilution": {
                    "name": "Share count creep",
                    "description": "Share count increasing without accretive ROI",
                    "category": "red_flags",
                    "metric_type": "qualitative",
                    "severity": "medium",
                    "implication": "Poor capital discipline",
                    "applies_to_tasks": ["ownership_task"],
                    "enabled": True
                }
            }
        }
        
        with open(self.rules_file, 'w') as f:
            yaml.dump(default_rules, f, default_flow_style=False, sort_keys=False)
    
    def _load_rules(self) -> Dict[str, Any]:
        """Load rules from YAML file"""
        with open(self.rules_file, 'r') as f:
            return yaml.safe_load(f) or {}
    
    def _save_rules(self):
        """Save rules to YAML file with backup"""
        # Create backup
        backup_path = self.rules_file.with_suffix('.yaml.bak')
        if self.rules_file.exists():
            shutil.copy(self.rules_file, backup_path)
        
        # Save rules
        with open(self.rules_file, 'w') as f:
            yaml.dump(self.rules, f, default_flow_style=False, sort_keys=False)
    
    def get_all_rules(self) -> Dict[str, Any]:
        """Get all rules organized by category"""
        return self.rules
    
    def get_rules_by_category(self, category: str) -> Dict[str, Any]:
        """Get rules for a specific category"""
        return self.rules.get(category, {})
    
    def get_rules_for_task(self, task_name: str) -> List[Dict[str, Any]]:
        """Get all rules that apply to a specific task"""
        applicable_rules = []
        for category, rules in self.rules.items():
            for rule_id, rule in rules.items():
                if task_name in rule.get('applies_to_tasks', []):
                    rule_with_id = rule.copy()
                    rule_with_id['id'] = rule_id
                    rule_with_id['category'] = category
                    applicable_rules.append(rule_with_id)
        return applicable_rules
    
    def add_rule(self, category: str, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """Add a new rule"""
        if category not in self.rules:
            self.rules[category] = {}
        
        if rule_id in self.rules[category]:
            return False  # Rule already exists
        
        self.rules[category][rule_id] = rule_data
        self._save_rules()
        return True
    
    def update_rule(self, category: str, rule_id: str, rule_data: Dict[str, Any]) -> bool:
        """Update an existing rule"""
        if category not in self.rules or rule_id not in self.rules[category]:
            return False
        
        self.rules[category][rule_id] = rule_data
        self._save_rules()
        return True
    
    def delete_rule(self, category: str, rule_id: str) -> bool:
        """Delete a rule"""
        if category not in self.rules or rule_id not in self.rules[category]:
            return False
        
        del self.rules[category][rule_id]
        self._save_rules()
        return True
    
    def assign_rule_to_task(self, category: str, rule_id: str, task_name: str) -> bool:
        """Assign a rule to a task"""
        if category not in self.rules or rule_id not in self.rules[category]:
            return False
        
        rule = self.rules[category][rule_id]
        if 'applies_to_tasks' not in rule:
            rule['applies_to_tasks'] = []
        
        if task_name not in rule['applies_to_tasks']:
            rule['applies_to_tasks'].append(task_name)
            self._save_rules()
        
        return True
    
    def remove_rule_from_task(self, category: str, rule_id: str, task_name: str) -> bool:
        """Remove a rule from a task"""
        if category not in self.rules or rule_id not in self.rules[category]:
            return False
        
        rule = self.rules[category][rule_id]
        if 'applies_to_tasks' in rule and task_name in rule['applies_to_tasks']:
            rule['applies_to_tasks'].remove(task_name)
            self._save_rules()
            return True
        
        return False
    
    def enable_rule(self, category: str, rule_id: str) -> bool:
        """Enable a rule"""
        if category not in self.rules or rule_id not in self.rules[category]:
            return False
        
        self.rules[category][rule_id]['enabled'] = True
        self._save_rules()
        return True
    
    def disable_rule(self, category: str, rule_id: str) -> bool:
        """Disable a rule"""
        if category not in self.rules or rule_id not in self.rules[category]:
            return False
        
        self.rules[category][rule_id]['enabled'] = False
        self._save_rules()
        return True
    
    def export_rules_for_task(self, task_name: str) -> str:
        """Export rules for a task as formatted text for agent consumption"""
        rules = self.get_rules_for_task(task_name)
        if not rules:
            return ""
        
        output = []
        output.append(f"# Rules and Thresholds for {task_name}\n")
        
        for rule in rules:
            if not rule.get('enabled', True):
                continue
            
            output.append(f"\n## {rule.get('name', rule.get('id'))}")
            output.append(f"Description: {rule.get('description', '')}")
            
            if 'thresholds' in rule:
                thresholds = rule['thresholds']
                if rule.get('metric_type') == 'qualitative':
                    output.append("\nThresholds:")
                    for status, criteria in thresholds.items():
                        output.append(f"  - {status.upper()}: {criteria.get('criteria', '')}")
                else:
                    output.append("\nThresholds:")
                    for status, threshold in thresholds.items():
                        if 'operator' in threshold:
                            op = threshold['operator']
                            if op == '<':
                                output.append(f"  - {status.upper()}: < {threshold['value']}")
                            elif op == '>':
                                output.append(f"  - {status.upper()}: > {threshold['value']}")
                            elif op == 'between':
                                output.append(f"  - {status.upper()}: {threshold.get('min', 0)} - {threshold.get('max', 100)}")
            
            if rule.get('notes'):
                output.append(f"Notes: {rule['notes']}")
        
        return "\n".join(output)