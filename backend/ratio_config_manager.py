"""
Ratio Configuration Manager
Handles financial ratio configuration, thresholds, and enables/disables
Saves configuration to ratio_rules.md for use by ratio_calc.py
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml
import json
from datetime import datetime
from enum import Enum

class RatioCategory(Enum):
    VALUATION = "valuation"
    PROFITABILITY = "profitability"
    LIQUIDITY = "liquidity"
    LEVERAGE = "leverage"
    EFFICIENCY = "efficiency"
    EARNINGS_QUALITY = "earnings_quality"
    ASSET_QUALITY = "asset_quality"
    CASH_FLOW = "cash_flow"

class RatioConfigManager:
    def __init__(self, ticker: str = None, rules_file: Path = None):
        self.ticker = ticker
        
        if rules_file is None:
            if ticker:
                # Use company-specific {ticker}_ratio_rules.md
                # Extract base ticker without exchange suffix for folder names
                ticker_base = ticker.split('.')[0].upper()
                ticker_lower = ticker_base.lower()
                self.rules_file = Path(__file__).parent.parent / "data" / ticker_base / f"{ticker_lower}_ratio_rules.md"
            else:
                # Fallback to global ratio_rules.md
                self.rules_file = Path(__file__).parent.parent / "data" / "ratio_rules.md"
        else:
            self.rules_file = rules_file
        
        # Don't create directory automatically - will be created when needed
        # Check if file exists to load from it
        if ticker and self.rules_file.exists():
            # Load existing rules
            self.ratios = self._load_or_initialize_ratios()
        elif ticker and self.rules_file.parent.exists():
            # Parent directory exists but file doesn't - create default
            self._create_default_ratio_rules()
            self.ratios = self._load_or_initialize_ratios()
        else:
            # Directory doesn't exist or no ticker - use defaults
            self.ratios = self._get_default_ratios()
    
    def _create_default_ratio_rules(self):
        """Create default ratio_rules.md for a new company"""
        # Create directory when creating default rules
        self.rules_file.parent.mkdir(parents=True, exist_ok=True)
        
        default_file = Path(__file__).parent.parent / "data" / "default_ratio_rules.md"
        if default_file.exists():
            import shutil
            shutil.copy(default_file, self.rules_file)
        else:
            # Create from scratch if default doesn't exist
            self._save_to_markdown(self._get_default_ratios())
    
    def _get_default_ratios(self) -> Dict[str, Any]:
        """Get default ratio configurations"""
        return {
            "valuation": {
                "pe_ratio": {
                    "name": "P/E Ratio",
                    "description": "Price to Earnings ratio",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 10,
                        "monitor": 15
                    }
                },
                "ev_ebitda": {
                    "name": "EV/EBITDA",
                    "description": "Enterprise Value to EBITDA",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 5.0,
                        "monitor": 7.5
                    }
                },
                "ev_ebit": {
                    "name": "EV/EBIT",
                    "description": "Enterprise Value to EBIT",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 7,
                        "monitor": 10
                    }
                },
                "fcf_yield": {
                    "name": "FCF Yield",
                    "description": "Free Cash Flow Yield",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 10,
                        "monitor": 6
                    }
                },
                "price_to_fcf": {
                    "name": "Price to FCF",
                    "description": "Market Cap / Free Cash Flow",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 15,
                        "monitor": 30
                    }
                },
                "ev_revenue": {
                    "name": "EV/Revenue",
                    "description": "Enterprise Value to Revenue",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 1.0,
                        "monitor": 2.0
                    }
                },
                "pb_ratio": {
                    "name": "P/B Ratio",
                    "description": "Price to Book ratio",
                    "enabled": False,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 1.5,
                        "monitor": 3.0
                    }
                },
                "ps_ratio": {
                    "name": "P/S Ratio",
                    "description": "Price to Sales ratio",
                    "enabled": False,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 1.0,
                        "monitor": 2.0
                    }
                }
            },
            "profitability": {
                "gross_margin": {
                    "name": "Gross Margin",
                    "description": "Gross Profit Margin %",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 40,
                        "monitor": 30
                    }
                },
                "operating_margin": {
                    "name": "Operating Margin",
                    "description": "Operating Profit Margin %",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 15,
                        "monitor": 5
                    }
                },
                "net_margin": {
                    "name": "Net Margin",
                    "description": "Net Profit Margin %",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 5,
                        "monitor": 0
                    }
                },
                "roe": {
                    "name": "ROE",
                    "description": "Return on Equity %",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 10,
                        "monitor": 0
                    }
                },
                "roce": {
                    "name": "ROCE",
                    "description": "Return on Capital Employed %",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 15,
                        "monitor": 8
                    }
                },
                "roa": {
                    "name": "ROA",
                    "description": "Return on Assets %",
                    "enabled": False,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 5,
                        "monitor": 0
                    }
                }
            },
            "liquidity": {
                "current_ratio": {
                    "name": "Current Ratio",
                    "description": "Current Assets / Current Liabilities",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 1.5,
                        "monitor": 1.0
                    }
                },
                "quick_ratio": {
                    "name": "Quick Ratio",
                    "description": "(Current Assets - Inventory) / Current Liabilities",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 1.0,
                        "monitor": 0.5
                    }
                },
                "cash_ratio": {
                    "name": "Cash Ratio",
                    "description": "Cash / Current Liabilities",
                    "enabled": False,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 0.5,
                        "monitor": 0.2
                    }
                }
            },
            "leverage": {
                "debt_to_equity": {
                    "name": "Debt-to-Equity",
                    "description": "Total Debt / Total Equity",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 0.5,
                        "monitor": 1.0
                    }
                },
                "net_debt_ebitda": {
                    "name": "Net Debt/EBITDA",
                    "description": "Net Debt / EBITDA",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 2.5,
                        "monitor": 3.5
                    }
                },
                "interest_coverage": {
                    "name": "Interest Coverage",
                    "description": "EBIT / Interest Expense",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 4.0,
                        "monitor": 2.0
                    }
                },
                "debt_ratio": {
                    "name": "Debt Ratio",
                    "description": "Total Debt / Total Assets",
                    "enabled": False,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 0.3,
                        "monitor": 0.5
                    }
                }
            },
            "efficiency": {
                "inventory_turnover": {
                    "name": "Inventory Turnover",
                    "description": "COGS / Average Inventory",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 4,
                        "monitor": 2
                    }
                },
                "dso": {
                    "name": "Days Sales Outstanding",
                    "description": "Days to collect receivables",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 60,
                        "monitor": 90
                    }
                },
                "asset_turnover": {
                    "name": "Asset Turnover",
                    "description": "Revenue / Total Assets",
                    "enabled": False,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 1.0,
                        "monitor": 0.5
                    }
                },
                "receivables_turnover": {
                    "name": "Receivables Turnover",
                    "description": "Revenue / Average Receivables",
                    "enabled": False,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 6,
                        "monitor": 4
                    }
                }
            },
            "earnings_quality": {
                "accruals_ratio": {
                    "name": "Accruals Ratio",
                    "description": "(Net Income - OCF) / Total Assets %",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 10,
                        "monitor": 20
                    }
                },
                "ebitda_fcf_conv": {
                    "name": "EBITDA to FCF Conversion",
                    "description": "FCF / EBITDA %",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 70,
                        "monitor": 40
                    }
                },
                "adj_stat_gap": {
                    "name": "Adjusted vs Statutory Gap",
                    "description": "Gap between adjusted and statutory profits %",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 10,
                        "monitor": 20
                    }
                }
            },
            "asset_quality": {
                "goodwill_assets": {
                    "name": "Goodwill/Assets",
                    "description": "Goodwill / Total Assets %",
                    "enabled": True,
                    "lower_is_better": True,
                    "thresholds": {
                        "pass": 30,
                        "monitor": 50
                    }
                },
                "capex_dep": {
                    "name": "Capex/Depreciation",
                    "description": "Capital Expenditure / Depreciation",
                    "enabled": True,
                    "special_range": True,
                    "thresholds": {
                        "pass_min": 0.8,
                        "pass_max": 1.2,
                        "monitor_max": 1.5
                    }
                },
                "working_capital": {
                    "name": "Working Capital",
                    "description": "Current Assets - Current Liabilities",
                    "enabled": False,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 0,
                        "monitor": -10
                    }
                },
                "tangible_book_value": {
                    "name": "Tangible Book Value",
                    "description": "Equity minus Intangibles",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 50,
                        "monitor": 0
                    }
                }
            },
            "cash_flow": {
                "ocf_ratio": {
                    "name": "Operating Cash Flow Ratio",
                    "description": "Operating Cash Flow / Current Liabilities",
                    "enabled": False,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 0.5,
                        "monitor": 0.2
                    }
                },
                "cash_conversion": {
                    "name": "Cash Conversion",
                    "description": "Operating Cash Flow / Net Income",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 1.0,
                        "monitor": 0.8
                    }
                },
                "free_cash_flow": {
                    "name": "Free Cash Flow",
                    "description": "OCF - Capital Expenditures",
                    "enabled": True,
                    "lower_is_better": False,
                    "thresholds": {
                        "pass": 0,
                        "monitor": -5
                    }
                }
            }
        }
    
    def _load_or_initialize_ratios(self) -> Dict[str, Any]:
        """Load ratios from markdown file or initialize with defaults"""
        if self.rules_file.exists():
            return self._parse_markdown_rules()
        else:
            # Initialize with defaults and save
            default_ratios = self._get_default_ratios()
            self._save_to_markdown(default_ratios)
            return default_ratios
    
    def _parse_markdown_rules(self) -> Dict[str, Any]:
        """Parse ratio rules from markdown file"""
        ratios = self._get_default_ratios()
        
        if not self.rules_file.exists():
            return ratios
        
        with open(self.rules_file, 'r') as f:
            content = f.read()
        
        # Parse markdown content and update ratios
        # This is a simplified parser - enhance as needed
        current_category = None
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('## ') and 'Thresholds' in line:
                # Extract category from heading
                category_map = {
                    'Valuation': 'valuation',
                    'Profitability': 'profitability',
                    'Liquidity': 'liquidity',
                    'Leverage': 'leverage',
                    'Efficiency': 'efficiency',
                    'Earnings Quality': 'earnings_quality',
                    'Asset Quality': 'asset_quality',
                    'Cash Flow': 'cash_flow'
                }
                for key, val in category_map.items():
                    if key in line:
                        current_category = val
                        break
            
            elif line.startswith('| ') and current_category and not line.startswith('| Ratio'):
                # Parse table row
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 5:  # Ratio | PASS | MONITOR | FAIL | Notes
                    ratio_name = parts[0]
                    # Map display name to ratio key
                    for cat_ratios in ratios.get(current_category, {}).values():
                        if cat_ratios.get('name') == ratio_name:
                            # Update thresholds from parsed values
                            pass
        
        return ratios
    
    def _save_to_markdown(self, ratios: Dict[str, Any]):
        """Save ratio configuration to ratio_rules.md file ONLY"""
        # Create directory only when saving (not on every read)
        self.rules_file.parent.mkdir(parents=True, exist_ok=True)
        
        content = []
        content.append("# Financial Ratio Thresholds and Rules")
        content.append("")
        content.append("This document defines the thresholds used to evaluate financial ratios.")
        content.append("Each ratio is evaluated as PASS, MONITOR, or FAIL based on these criteria.")
        content.append("")
        
        category_names = {
            "valuation": "Valuation Ratio",
            "profitability": "Profitability Ratio",
            "liquidity": "Liquidity Ratio",
            "leverage": "Leverage Ratio",
            "efficiency": "Efficiency Ratio",
            "earnings_quality": "Earnings Quality",
            "asset_quality": "Asset Quality",
            "cash_flow": "Cash Flow Ratio"
        }
        
        for category, category_ratios in ratios.items():
            # Only include categories with enabled ratios
            enabled_ratios = {k: v for k, v in category_ratios.items() if v.get('enabled', False)}
            
            if enabled_ratios:
                content.append(f"## {category_names.get(category, category.title())} Thresholds")
                content.append("")
                content.append("| Ratio | PASS | MONITOR | FAIL | Notes | Enabled |")
                content.append("|-------|------|---------|------|-------|---------|")
                
                for ratio_key, ratio_config in enabled_ratios.items():
                    name = ratio_config['name']
                    thresholds = ratio_config.get('thresholds', {})
                    enabled = "Yes" if ratio_config.get('enabled', False) else "No"
                    
                    if ratio_config.get('special_range'):
                        # Special handling for capex/depreciation
                        pass_val = f"{thresholds.get('pass_min', 0)}-{thresholds.get('pass_max', 0)}x"
                        monitor_val = f"< {thresholds.get('pass_min', 0)}x or {thresholds.get('pass_max', 0)}-{thresholds.get('monitor_max', 0)}x"
                        fail_val = f"> {thresholds.get('monitor_max', 0)}x"
                        notes = "Optimal range indicates sustainable investment"
                    else:
                        lower_is_better = ratio_config.get('lower_is_better', False)
                        pass_thresh = thresholds.get('pass', 0)
                        monitor_thresh = thresholds.get('monitor', 0)
                        
                        if lower_is_better:
                            pass_val = f"< {pass_thresh}"
                            monitor_val = f"{pass_thresh}-{monitor_thresh}"
                            fail_val = f"> {monitor_thresh}"
                            notes = "Lower is better"
                        else:
                            pass_val = f"> {pass_thresh}"
                            monitor_val = f"{monitor_thresh}-{pass_thresh}"
                            fail_val = f"< {monitor_thresh}"
                            notes = "Higher is better"
                        
                        # Add units
                        if 'margin' in ratio_key or 'yield' in ratio_key or 'ratio' in name.lower() and '%' in ratio_config.get('description', ''):
                            pass_val += "%"
                            monitor_val = monitor_val.replace('-', '%-') + "%"
                            fail_val += "%"
                        elif 'days' in name.lower() or ratio_key == 'dso':
                            pass_val += " days"
                            monitor_val = monitor_val.replace('-', ' days-') + " days"
                            fail_val += " days"
                        elif any(x in ratio_key for x in ['_ratio', 'turnover', 'coverage']):
                            pass_val += "x"
                            monitor_val = monitor_val.replace('-', 'x-') + "x"
                            fail_val += "x"
                    
                    content.append(f"| {name} | {pass_val} | {monitor_val} | {fail_val} | {notes} | {enabled} |")
                
                content.append("")
        
        # Save to file
        with open(self.rules_file, 'w') as f:
            f.write('\n'.join(content))
    
    def _generate_agent_ratios_REMOVED(self, ratios: Dict[str, Any]):
        """Generate agent-ratios.md with only enabled ratios for agent use"""
        agent_file = self.rules_file.parent / 'agent-ratios.md'
        
        content = []
        content.append("# Financial Ratios for Agent Analysis")
        content.append("")
        content.append("This document contains ONLY the enabled financial ratios that should be calculated and evaluated.")
        content.append("Generated from ratio_rules.md - DO NOT EDIT DIRECTLY")
        content.append("")
        
        category_names = {
            "valuation": "Valuation Ratios",
            "profitability": "Profitability Ratios",
            "liquidity": "Liquidity Ratios",
            "leverage": "Leverage Ratios",
            "efficiency": "Efficiency Ratios",
            "earnings_quality": "Earnings Quality Ratios",
            "asset_quality": "Asset Quality Ratios",
            "cash_flow": "Cash Flow Ratios"
        }
        
        # Track if we have any enabled ratios
        has_enabled_ratios = False
        
        for category, category_ratios in ratios.items():
            # Only include categories with enabled ratios
            enabled_ratios = {k: v for k, v in category_ratios.items() if v.get('enabled', False)}
            
            if enabled_ratios:
                has_enabled_ratios = True
                content.append(f"## {category_names.get(category, category.title())}")
                content.append("")
                content.append("| Ratio | Description | PASS | MONITOR | FAIL | Evaluation Criteria |")
                content.append("|-------|-------------|------|---------|------|---------------------|")
                
                for ratio_key, ratio_config in enabled_ratios.items():
                    name = ratio_config['name']
                    description = ratio_config['description']
                    thresholds = ratio_config.get('thresholds', {})
                    
                    if ratio_config.get('special_range'):
                        # Special handling for capex/depreciation
                        pass_val = f"{thresholds.get('pass_min', 0)}-{thresholds.get('pass_max', 0)}"
                        monitor_val = f"Outside optimal range"
                        fail_val = f"> {thresholds.get('monitor_max', 0)}"
                        criteria = "Optimal range indicates sustainable investment"
                    else:
                        lower_is_better = ratio_config.get('lower_is_better', False)
                        pass_thresh = thresholds.get('pass', 0)
                        monitor_thresh = thresholds.get('monitor', 0)
                        
                        if lower_is_better:
                            pass_val = f"< {pass_thresh}"
                            monitor_val = f"{pass_thresh}-{monitor_thresh}"
                            fail_val = f"> {monitor_thresh}"
                            criteria = "Lower values indicate better performance"
                        else:
                            pass_val = f"> {pass_thresh}"
                            monitor_val = f"{monitor_thresh}-{pass_thresh}"
                            fail_val = f"< {monitor_thresh}"
                            criteria = "Higher values indicate better performance"
                    
                    content.append(f"| {name} | {description} | {pass_val} | {monitor_val} | {fail_val} | {criteria} |")
                
                content.append("")
        
        if not has_enabled_ratios:
            content.append("## ⚠️ No Ratios Enabled")
            content.append("")
            content.append("No financial ratios are currently enabled for analysis.")
            content.append("Please enable ratios in the Ratios Configuration page.")
        
        # Add summary section
        content.append("## Summary")
        content.append("")
        enabled_count = sum(
            sum(1 for r in cat_ratios.values() if r.get('enabled', False))
            for cat_ratios in ratios.values()
        )
        total_count = sum(len(cat_ratios) for cat_ratios in ratios.values())
        
        content.append(f"**Total Enabled Ratios:** {enabled_count} out of {total_count}")
        content.append("")
        
        # Add category breakdown
        content.append("### Enabled Ratios by Category:")
        content.append("")
        for category, category_ratios in ratios.items():
            enabled_in_cat = sum(1 for r in category_ratios.values() if r.get('enabled', False))
            total_in_cat = len(category_ratios)
            if enabled_in_cat > 0:
                content.append(f"- **{category_names.get(category, category.title())}:** {enabled_in_cat}/{total_in_cat}")
        
        content.append("")
        content.append("---")
        content.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        # Save to file
        with open(agent_file, 'w') as f:
            f.write('\n'.join(content))
    
    def get_all_ratios(self) -> Dict[str, Any]:
        """Get all ratio configurations"""
        return self.ratios
    
    def update_ratio(self, category: str, ratio_key: str, config: Dict[str, Any]) -> bool:
        """Update a specific ratio configuration"""
        if category not in self.ratios:
            return False
        
        if ratio_key not in self.ratios[category]:
            return False
        
        # Update the ratio configuration
        self.ratios[category][ratio_key].update(config)
        
        # Save to markdown
        self._save_to_markdown(self.ratios)
        
        return True
    
    def update_all_ratios(self, ratios_config: Dict[str, Any]) -> bool:
        """Update all ratio configurations at once"""
        self.ratios = ratios_config
        self._save_to_markdown(self.ratios)
        return True
    
    def enable_ratio(self, category: str, ratio_key: str) -> bool:
        """Enable a specific ratio"""
        if category in self.ratios and ratio_key in self.ratios[category]:
            self.ratios[category][ratio_key]['enabled'] = True
            self._save_to_markdown(self.ratios)
            return True
        return False
    
    def disable_ratio(self, category: str, ratio_key: str) -> bool:
        """Disable a specific ratio"""
        if category in self.ratios and ratio_key in self.ratios[category]:
            self.ratios[category][ratio_key]['enabled'] = False
            self._save_to_markdown(self.ratios)
            return True
        return False
    
    def get_enabled_ratios(self) -> Dict[str, Any]:
        """Get only enabled ratios"""
        enabled = {}
        for category, category_ratios in self.ratios.items():
            enabled_in_category = {
                k: v for k, v in category_ratios.items() 
                if v.get('enabled', False)
            }
            if enabled_in_category:
                enabled[category] = enabled_in_category
        return enabled