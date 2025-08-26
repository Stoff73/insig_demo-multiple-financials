from pathlib import Path
from datetime import datetime
from typing import Dict, List
from .extract_financials import FinancialDataExtractor


class FinancialRatioCalculator:
    """Calculate financial ratios from company financial data"""
    
    def __init__(self, company_ticker: str = 'XPP.L', data_dir: str = 'data'):
        self.ticker = company_ticker
        # Extract base ticker without exchange suffix for folder names
        self.ticker_base = company_ticker.split('.')[0].upper()
        self.data_dir = Path(data_dir)
        self.metrics = {}
        self.thresholds = self._load_thresholds_from_rules()
        self.extractor = FinancialDataExtractor(company_ticker, data_dir)
        self.data_sources = []  # Track data sources used
        
    def _load_thresholds_from_rules(self) -> Dict:
        """Load ratio thresholds from company-specific ratio_rules.md file"""
        # Try company-specific {ticker}_ratio_rules.md first
        company_folder = self.data_dir / self.ticker_base
        company_rules_file = company_folder / f'{self.ticker_base.lower()}_ratio_rules.md'
        # Fallback to global ratio_rules.md if company-specific doesn't exist
        rules_file = company_rules_file if company_rules_file.exists() else self.data_dir / 'ratio_rules.md'
        
        # Default thresholds - ALL DISABLED by default
        # Only ratios found in ratio_rules.md will be enabled
        default_thresholds = {
            'pe_ratio': {'pass': 10, 'monitor': 15, 'enabled': False},
            'ev_ebitda': {'pass': 5.0, 'monitor': 7.5, 'enabled': False},
            'ev_ebit': {'pass': 7, 'monitor': 10, 'enabled': False},
            'net_debt_ebitda': {'pass': 2.5, 'monitor': 3.5, 'enabled': False},
            'interest_coverage': {'pass': 4.0, 'monitor': 2.0, 'enabled': False},
            'fcf_yield': {'pass': 10, 'monitor': 6, 'enabled': False},
            'gross_margin': {'pass': 40, 'monitor': 30, 'enabled': False},
            'operating_margin': {'pass': 15, 'monitor': 5, 'enabled': False},
            'net_margin': {'pass': 5, 'monitor': 0, 'enabled': False},
            'roe': {'pass': 10, 'monitor': 0, 'enabled': False},
            'roce': {'pass': 15, 'monitor': 8, 'enabled': False},
            'current_ratio': {'pass': 1.5, 'monitor': 1.0, 'enabled': False},
            'quick_ratio': {'pass': 1.0, 'monitor': 0.5, 'enabled': False},
            'debt_to_equity': {'pass': 0.5, 'monitor': 1.0, 'enabled': False},
            'cash_conversion': {'pass': 1.0, 'monitor': 0.8, 'enabled': False},
            'accruals_ratio': {'pass': 10, 'monitor': 20, 'enabled': False},
            'ebitda_fcf_conv': {'pass': 70, 'monitor': 40, 'enabled': False},
            'adj_stat_gap': {'pass': 10, 'monitor': 20, 'enabled': False},
            'goodwill_assets': {'pass': 30, 'monitor': 50, 'enabled': False},
            'capex_dep': {'pass_min': 0.8, 'pass_max': 1.2, 'monitor_max': 1.5, 'enabled': False},
            'dso': {'pass': 60, 'monitor': 90, 'enabled': False},
            'inventory_turnover': {'pass': 4, 'monitor': 2, 'enabled': False},
            'roa': {'pass': 5, 'monitor': 0, 'enabled': False},
            'pb_ratio': {'pass': 1.5, 'monitor': 3.0, 'enabled': False},
            'ps_ratio': {'pass': 1.0, 'monitor': 2.0, 'enabled': False},
            'cash_ratio': {'pass': 0.5, 'monitor': 0.2, 'enabled': False},
            'debt_ratio': {'pass': 0.3, 'monitor': 0.5, 'enabled': False},
            'asset_turnover': {'pass': 1.0, 'monitor': 0.5, 'enabled': False},
            'receivables_turnover': {'pass': 6, 'monitor': 4, 'enabled': False},
            'ocf_ratio': {'pass': 0.5, 'monitor': 0.2, 'enabled': False},
            'price_to_fcf': {'pass': 10, 'monitor': 20, 'enabled': False},
            'working_capital': {'pass': 0, 'monitor': -10, 'enabled': False},
            'ev_revenue': {'pass': 1.0, 'monitor': 2.0, 'enabled': False},
            'tangible_book_value': {'pass': 50, 'monitor': 0, 'enabled': False},
            'free_cash_flow': {'pass': 0, 'monitor': -5, 'enabled': False},
        }
        
        if not rules_file.exists():
            print(f"Warning: {rules_file} not found. Using default thresholds.")
            return default_thresholds
        
        try:
            with open(rules_file, 'r') as f:
                content = f.read()
            
            # Parse the markdown file
            thresholds = default_thresholds.copy()
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if line.startswith('| ') and not line.startswith('| Ratio'):
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                    if len(parts) >= 6:  # Ratio | PASS | MONITOR | FAIL | Notes | Enabled
                        ratio_name = parts[0]
                        enabled_str = parts[5] if len(parts) > 5 else 'Yes'
                        enabled = enabled_str.lower() == 'yes'
                        
                        # Map display names to ratio keys
                        name_to_key = {
                            'P/E Ratio': 'pe_ratio',
                            'EV/EBITDA': 'ev_ebitda',
                            'EV/EBIT': 'ev_ebit',
                            'FCF Yield': 'fcf_yield',
                            'P/B Ratio': 'pb_ratio',
                            'P/S Ratio': 'ps_ratio',
                            'EV/Revenue': 'ev_revenue',
                            'Price to FCF': 'price_to_fcf',
                            'Gross Margin': 'gross_margin',
                            'Operating Margin': 'operating_margin',
                            'Net Margin': 'net_margin',
                            'ROE': 'roe',
                            'ROCE': 'roce',
                            'ROA': 'roa',
                            'Current Ratio': 'current_ratio',
                            'Quick Ratio': 'quick_ratio',
                            'Cash Ratio': 'cash_ratio',
                            'Debt-to-Equity': 'debt_to_equity',
                            'Net Debt/EBITDA': 'net_debt_ebitda',
                            'Interest Coverage': 'interest_coverage',
                            'Debt Ratio': 'debt_ratio',
                            'Inventory Turnover': 'inventory_turnover',
                            'Days Sales Outstanding': 'dso',
                            'Asset Turnover': 'asset_turnover',
                            'Receivables Turnover': 'receivables_turnover',
                            'Cash Conversion': 'cash_conversion',
                            'Accruals Ratio': 'accruals_ratio',
                            'EBITDA to FCF Conversion': 'ebitda_fcf_conv',
                            'Adjusted vs Statutory Gap': 'adj_stat_gap',
                            'Goodwill/Assets': 'goodwill_assets',
                            'Capex/Depreciation': 'capex_dep',
                            'Working Capital': 'working_capital',
                            'Operating Cash Flow Ratio': 'ocf_ratio',
                            'Price to FCF': 'price_to_fcf',
                            'Free Cash Flow': 'free_cash_flow',
                            'Tangible Book Value': 'tangible_book_value',
                            'EV/Revenue': 'ev_revenue',
                        }
                        
                        ratio_key = name_to_key.get(ratio_name)
                        if ratio_key and ratio_key in thresholds:
                            # Parse threshold values
                            pass_str = parts[1]
                            monitor_str = parts[2]
                            
                            # Extract numeric values
                            import re
                            
                            if ratio_key == 'capex_dep':
                                # Special handling for range-based ratio
                                pass_match = re.findall(r'[\d.]+', pass_str)
                                if len(pass_match) >= 2:
                                    thresholds[ratio_key]['pass_min'] = float(pass_match[0])
                                    thresholds[ratio_key]['pass_max'] = float(pass_match[1])
                                monitor_match = re.findall(r'[\d.]+', monitor_str)
                                if monitor_match:
                                    thresholds[ratio_key]['monitor_max'] = float(monitor_match[-1])
                            else:
                                # Extract numeric value from strings like "< 10" or "> 5"
                                pass_match = re.search(r'[\d.]+', pass_str)
                                monitor_match = re.search(r'[\d.]+', monitor_str)
                                
                                if pass_match:
                                    thresholds[ratio_key]['pass'] = float(pass_match.group())
                                if monitor_match:
                                    # For monitor, extract the appropriate value based on the range
                                    monitor_values = re.findall(r'[\d.]+', monitor_str)
                                    if len(monitor_values) == 2:
                                        # It's a range, take the higher value for "lower is better" ratios
                                        # and lower value for "higher is better" ratios
                                        if '<' in pass_str:  # Lower is better
                                            thresholds[ratio_key]['monitor'] = float(monitor_values[1])
                                        else:  # Higher is better
                                            thresholds[ratio_key]['monitor'] = float(monitor_values[0])
                                    elif monitor_values:
                                        thresholds[ratio_key]['monitor'] = float(monitor_values[0])
                            
                            thresholds[ratio_key]['enabled'] = enabled
            
            # Count enabled ratios
            enabled_count = sum(1 for v in thresholds.values() if v.get('enabled', False))
            print(f"Loaded ratio thresholds from {rules_file} - {enabled_count} ratios enabled")
            return thresholds
            
        except Exception as e:
            print(f"Error parsing {rules_file}: {e}. Using default thresholds.")
            return default_thresholds
    
    def fetch_market_data(self) -> Dict:
        """Delegate to extractor for market data fetching"""
        return self.extractor.fetch_market_data()
    
    def extract_metrics_from_files(self) -> Dict:
        """Delegate to extractor for file metrics extraction"""
        metrics = self.extractor.extract_metrics_from_files()
        # Track the data source file
        if hasattr(self.extractor, 'last_source_file'):
            self.data_sources.append(self.extractor.last_source_file)
        return metrics
    
    def calculate_ratios(self) -> Dict:
        """Calculate all financial ratios with correct values"""
        # Get market data
        market_data = self.fetch_market_data()
        self.metrics.update(market_data)
        
        # Get financial metrics from files
        file_metrics = self.extract_metrics_from_files()
        self.metrics.update(file_metrics)
        
        # Determine annualization factor (H1 = 6 months, need to double for annual)
        annualization_factor = 2  # H1 data needs doubling, need to expand this as per discussion with Richard, Thursday 21 August 2025, as split may not be 50/50
        
        # Calculate annualized metrics
        self.metrics['Revenue Annual'] = self.metrics.get('Revenue', 0) * annualization_factor
        self.metrics['Operating Profit Annual'] = self.metrics.get('Operating Profit', 0) * annualization_factor
        self.metrics['Net Income Annual'] = self.metrics.get('Net Income', 0) * annualization_factor
        self.metrics['FCF Annual'] = self.metrics.get('Free Cash Flow', 0) * annualization_factor
        self.metrics['Interest Annual'] = self.metrics.get('Interest Expense', 0) * annualization_factor
        
        # Note: Depreciation and Amortization are already LTM figures, no need to annualize
        
        # CORRECT EBIT Calculation: EBIT = EBITDA - Depreciation - Amortization
        # Using LTM EBITDA and LTM D&A for consistency
        if self.metrics.get('LTM Adjusted EBITDA', 0) > 0:
            self.metrics['EBIT Annual'] = (self.metrics.get('LTM Adjusted EBITDA', 0) - 
                                          self.metrics.get('Depreciation', 0) - 
                                          self.metrics.get('Amortization', 0))
            self.metrics['EBIT'] = self.metrics['EBIT Annual'] / 2  # Half-year EBIT estimate
        else:
            # Fallback: Use Operating Profit if EBITDA not available
            self.metrics['EBIT'] = self.metrics.get('Operating Profit', 0)
            self.metrics['EBIT Annual'] = self.metrics['EBIT'] * annualization_factor
        
        # Calculate other derived metrics
        if self.metrics.get('Revenue', 0) > 0 and self.metrics.get('Gross Margin %', 0) > 0:
            self.metrics['Gross Profit'] = self.metrics['Revenue'] * self.metrics['Gross Margin %'] / 100
            self.metrics['COGS'] = self.metrics['Revenue'] - self.metrics['Gross Profit']
        
        self.metrics['Enterprise Value'] = self.metrics.get('market_cap', 0) + self.metrics.get('Net Debt', 0)
        self.metrics['Tangible Book Value'] = self.metrics.get('Total Equity', 0) - self.metrics.get('Intangible Assets', 0) - self.metrics.get('Goodwill', 0)
        
        # Now calculate ratios
        ratios = {}
        
        print("\n========== CALCULATING FINANCIAL RATIOS ==========")
        
        # Valuation Ratios
        if self.metrics.get('Net Income Annual', 0) > 0:
            ratios['pe_ratio'] = self.metrics.get('market_cap', 0) / self.metrics['Net Income Annual']
        else:
            ratios['pe_ratio'] = None
        
        ratios['pb_ratio'] = self.metrics.get('market_cap', 0) / self.metrics.get('Total Equity', 1) if self.metrics.get('Total Equity') else 0
        ratios['ps_ratio'] = self.metrics.get('market_cap', 0) / self.metrics.get('Revenue Annual', 1) if self.metrics.get('Revenue Annual') else 0
        
        # EV/EBITDA - Use LTM Adjusted EBITDA (32.4m)
        if self.metrics.get('LTM Adjusted EBITDA', 0) > 0:
            ratios['ev_ebitda'] = self.metrics.get('Enterprise Value', 0) / self.metrics['LTM Adjusted EBITDA']
            print(f"EV/EBITDA: {ratios['ev_ebitda']:.2f}x (EV: {self.metrics.get('Enterprise Value', 0):.1f}, LTM EBITDA: {self.metrics['LTM Adjusted EBITDA']:.1f})")
        
        if self.metrics.get('EBIT Annual', 0) > 0:
            ratios['ev_ebit'] = self.metrics.get('Enterprise Value', 0) / self.metrics['EBIT Annual']
        else:
            ratios['ev_ebit'] = 0
        
        ratios['ev_revenue'] = self.metrics.get('Enterprise Value', 0) / self.metrics.get('Revenue Annual', 1) if self.metrics.get('Revenue Annual') else 0
        
        if self.metrics.get('FCF Annual', 0) > 0:
            ratios['price_to_fcf'] = self.metrics.get('market_cap', 0) / self.metrics['FCF Annual']
            ratios['fcf_yield'] = (self.metrics['FCF Annual'] / self.metrics.get('market_cap', 1)) * 100 if self.metrics.get('market_cap') else 0
        else:
            ratios['price_to_fcf'] = None
            ratios['fcf_yield'] = 0
        
        # Profitability Ratios
        if self.metrics.get('Revenue', 0) > 0:
            ratios['gross_margin'] = self.metrics.get('Gross Margin %', 0)
            ratios['operating_margin'] = (self.metrics.get('Operating Profit', 0) / self.metrics['Revenue']) * 100
            ratios['net_margin'] = (self.metrics.get('Net Income', 0) / self.metrics['Revenue']) * 100
        
        ratios['roa'] = (self.metrics.get('Net Income Annual', 0) / self.metrics.get('Total Assets', 1)) * 100 if self.metrics.get('Total Assets') else 0
        ratios['roe'] = (self.metrics.get('Net Income Annual', 0) / self.metrics.get('Total Equity', 1)) * 100 if self.metrics.get('Total Equity') else 0
        
        capital_employed = self.metrics.get('Total Assets', 0) - self.metrics.get('Current Liabilities', 0)
        if capital_employed > 0:
            ratios['roce'] = (self.metrics.get('EBIT Annual', 0) / capital_employed) * 100
        else:
            ratios['roce'] = 0
        
        # Efficiency Ratios
        ratios['asset_turnover'] = self.metrics.get('Revenue Annual', 0) / self.metrics.get('Total Assets', 1) if self.metrics.get('Total Assets') else 0
        ratios['inventory_turnover'] = (self.metrics.get('COGS', 0) * annualization_factor) / self.metrics.get('Inventories', 1) if self.metrics.get('Inventories') else 0
        ratios['receivables_turnover'] = self.metrics.get('Revenue Annual', 0) / self.metrics.get('Receivables', 1) if self.metrics.get('Receivables') else 0
        ratios['dso'] = 365 / ratios['receivables_turnover'] if ratios.get('receivables_turnover', 0) > 0 else 0
        
        # Liquidity Ratios
        ratios['current_ratio'] = self.metrics.get('Current Assets', 0) / self.metrics.get('Current Liabilities', 1) if self.metrics.get('Current Liabilities') else 0
        ratios['quick_ratio'] = (self.metrics.get('Current Assets', 0) - self.metrics.get('Inventories', 0)) / self.metrics.get('Current Liabilities', 1) if self.metrics.get('Current Liabilities') else 0
        ratios['cash_ratio'] = self.metrics.get('Cash and Bank Balances', 0) / self.metrics.get('Current Liabilities', 1) if self.metrics.get('Current Liabilities') else 0
        
        # Leverage Ratios
        ratios['debt_to_equity'] = self.metrics.get('Total Debt', 0) / self.metrics.get('Total Equity', 1) if self.metrics.get('Total Equity') else 0
        ratios['debt_ratio'] = self.metrics.get('Total Debt', 0) / self.metrics.get('Total Assets', 1) if self.metrics.get('Total Assets') else 0
        ratios['interest_coverage'] = self.metrics.get('EBIT Annual', 0) / self.metrics.get('Interest Annual', 1) if self.metrics.get('Interest Annual', 0) > 0 else 0
        
        # Net Debt/EBITDA - Use LTM Adjusted EBITDA
        if self.metrics.get('LTM Adjusted EBITDA', 0) > 0:
            ratios['net_debt_ebitda'] = self.metrics.get('Net Debt', 0) / self.metrics['LTM Adjusted EBITDA']
            print(f"Net Debt/EBITDA: {ratios['net_debt_ebitda']:.2f}x (Net Debt: {self.metrics.get('Net Debt', 0):.1f}, LTM EBITDA: {self.metrics['LTM Adjusted EBITDA']:.1f})")
        
        # Cash Flow Ratios
        ratios['ocf_ratio'] = self.metrics.get('Operating Cash Flow', 0) / self.metrics.get('Current Liabilities', 1) if self.metrics.get('Current Liabilities') else 0
        
        # Cash Conversion - use annualized figures for consistency
        net_income_annual = self.metrics.get('Net Income Annual', self.metrics.get('Net Income', 0) * annualization_factor)
        ocf_annual = self.metrics.get('Operating Cash Flow', 0) * annualization_factor
        if net_income_annual != 0:
            ratios['cash_conversion'] = ocf_annual / abs(net_income_annual)
        else:
            ratios['cash_conversion'] = 0
        
        # Earnings Quality Ratios
        # Accruals Ratio - use annualized figures
        if self.metrics.get('Total Assets', 0) > 0:
            net_income_annual = self.metrics.get('Net Income Annual', self.metrics.get('Net Income', 0) * annualization_factor)
            ocf_annual = self.metrics.get('Operating Cash Flow', 0) * annualization_factor
            ratios['accruals_ratio'] = ((net_income_annual - ocf_annual) / self.metrics['Total Assets']) * 100
        else:
            ratios['accruals_ratio'] = 0
        
        # EBITDA to FCF conversion - use LTM EBITDA and annualized FCF for consistency
        if self.metrics.get('LTM Adjusted EBITDA', 0) > 0:
            fcf_annual = self.metrics.get('FCF Annual', 0)
            ratios['ebitda_fcf_conv'] = (fcf_annual / self.metrics['LTM Adjusted EBITDA']) * 100
        elif self.metrics.get('EBITDA', 0) > 0:
            # Fallback to H1 comparison if LTM not available
            ratios['ebitda_fcf_conv'] = (self.metrics.get('Free Cash Flow', 0) / self.metrics['EBITDA']) * 100
        else:
            ratios['ebitda_fcf_conv'] = 0
        
        # Adjusted vs Statutory Gap
        if self.metrics.get('Statutory Operating Profit', 0) and self.metrics.get('Statutory Operating Profit', 0) != 0:
            adj_stat_gap = self.metrics.get('Adjusted Operating Profit', 0) - self.metrics.get('Statutory Operating Profit', 0)
            ratios['adj_stat_gap'] = (adj_stat_gap / self.metrics['Statutory Operating Profit']) * 100
        else:
            ratios['adj_stat_gap'] = 0
        
        # Other Metrics
        if self.metrics.get('Shares Outstanding', 0) > 0:
            ratios['eps'] = self.metrics.get('Net Income', 0) / self.metrics['Shares Outstanding']
        else:
            ratios['eps'] = 0
        
        if self.metrics.get('Total Assets', 0) > 0:
            ratios['goodwill_assets'] = (self.metrics.get('Goodwill', 0) / self.metrics['Total Assets']) * 100
        else:
            ratios['goodwill_assets'] = 0
        
        # Capex/Depreciation ratio - Note: Capex is H1, so annualize it for comparison with LTM depreciation
        if self.metrics.get('Depreciation', 0) > 0:
            annualized_capex = self.metrics.get('Capex', 0) * annualization_factor
            ratios['capex_dep'] = annualized_capex / self.metrics['Depreciation']
        else:
            ratios['capex_dep'] = 0
        
        ratios['working_capital'] = self.metrics.get('Current Assets', 0) - self.metrics.get('Current Liabilities', 0)
        
        # Add metrics that are treated as "ratios" in ratio_rules.md
        ratios['tangible_book_value'] = self.metrics.get('Tangible Book Value', 0)
        ratios['free_cash_flow'] = self.metrics.get('Free Cash Flow', 0)
        
        print("=" * 50)
        
        return ratios
    
    def evaluate_ratio(self, value: float, threshold_key: str) -> str:
        """Evaluate a ratio against thresholds"""
        if value is None:
            return "N/A"
        
        if threshold_key not in self.thresholds:
            return "MONITOR"
        
        threshold = self.thresholds[threshold_key]
        
        # Check if ratio is enabled
        if not threshold.get('enabled', True):
            return "DISABLED"
        
        # Special handling for capex/dep
        if threshold_key == 'capex_dep':
            if threshold['pass_min'] <= value <= threshold['pass_max']:
                return "PASS"
            elif value <= threshold['monitor_max']:
                return "MONITOR"
            else:
                return "FAIL"
        
        # For ratios where lower is better
        if threshold_key in ['pe_ratio', 'ev_ebitda', 'ev_ebit', 'net_debt_ebitda', 'debt_to_equity', 
                             'accruals_ratio', 'adj_stat_gap', 'goodwill_assets', 'dso']:
            if value < threshold['pass']:
                return "PASS"
            elif value <= threshold['monitor']:
                return "MONITOR"
            else:
                return "FAIL"
        
        # For ratios where higher is better
        else:
            if value > threshold['pass']:
                return "PASS"
            elif value >= threshold['monitor']:
                return "MONITOR"
            else:
                return "FAIL"
    
    def generate_all_ratios_file(self, ratios: Dict, company_name: str = None) -> str:
        """Generate the comprehensive all ratios markdown file - shows ALL ratios"""
        if company_name is None:
            company_name = self.metrics.get('company_name', self.ticker)
        
        # Get timestamp
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine data sources dynamically
        data_source_str = "Generated from financial data files\n"
        if self.data_sources:
            source_names = [Path(s).name if isinstance(s, (str, Path)) else str(s) for s in self.data_sources]
            data_source_str += f"Data Sources: {', '.join(set(source_names))}\n\n"
        else:
            # Fallback to looking for files in company directory
            company_dir = self.data_dir / self.ticker_base
            md_files = list(company_dir.glob('*.md'))
            financial_files = [f.name for f in md_files if 'power' in f.name.lower() or 'financial' in f.name.lower()]
            if financial_files:
                data_source_str += f"Data Sources: {', '.join(financial_files)}\n\n"
            else:
                data_source_str += "Data Sources: Financial documents\n\n"
        
        # Build markdown content
        content = f"# {company_name} All Financial Ratios Analysis\n\n"
        content += data_source_str
        
        # Market Data Section
        content += "## **Current Market Data**\n\n"
        content += "| Metric | Value | Source | Retrieved |\n"
        content += "|--------|-------|--------|----------|\n"
        
        currency_symbol = '£' if self.metrics.get('currency') == 'GBP' else '$'
        content += f"| **Share Price** | {currency_symbol}{self.metrics.get('share_price', 0):.2f} | Yahoo Finance | {formatted_time} |\n"
        content += f"| **Market Cap** | {currency_symbol}{self.metrics.get('market_cap', 0):.1f}m | Yahoo Finance | {formatted_time} |\n"
        content += f"| **Enterprise Value** | {currency_symbol}{self.metrics.get('Enterprise Value', 0):.1f}m | Calculated | - |\n"
        content += f"| **Shares Outstanding** | {self.metrics.get('Shares Outstanding', 0):.1f}m | Financial Reports | - |\n\n"
        
        # ALL Valuation Ratios - Show ALL ratios regardless of enabled status
        content += "## **Valuation Ratios**\n\n"
        content += "| Ratio | Formula | Calculation | Value | Outcome |\n"
        content += "|-------|---------|-------------|-------|----------|\n"
        
        # P/E Ratio - always show in all_ratios.md
        if ratios.get('pe_ratio') is not None:
            pe_outcome = self.evaluate_ratio(ratios['pe_ratio'], 'pe_ratio')
            content += f"| **P/E Ratio** | Market Cap / Net Income | {self.metrics.get('market_cap', 0):.1f} / {self.metrics.get('Net Income Annual', 0):.1f} | {ratios['pe_ratio']:.1f}x | {pe_outcome} |\n"
        else:
            content += f"| **P/E Ratio** | Market Cap / Net Income | {self.metrics.get('market_cap', 0):.1f} / {self.metrics.get('Net Income Annual', 0):.1f} | N/A (loss) | FAIL |\n"
        
        pb_outcome = self.evaluate_ratio(ratios['pb_ratio'], 'pb_ratio')
        content += f"| **P/B Ratio** | Market Cap / Equity | {self.metrics.get('market_cap', 0):.1f} / {self.metrics.get('Total Equity', 0):.1f} | {ratios.get('pb_ratio', 0):.2f}x | {pb_outcome} |\n"

        ps_outcome = self.evaluate_ratio(ratios['ps_ratio'], 'ps_ratio')
        content += f"| **P/S Ratio** | Market Cap / Revenue | {self.metrics.get('market_cap', 0):.1f} / {self.metrics.get('Revenue Annual', 0):.1f} | {ratios.get('ps_ratio', 0):.2f}x | {ps_outcome} |\n"
        
        ev_ebitda_outcome = self.evaluate_ratio(ratios.get('ev_ebitda', 0), 'ev_ebitda')
        content += f"| **EV/EBITDA** | EV / LTM EBITDA | {self.metrics.get('Enterprise Value', 0):.1f} / {self.metrics.get('LTM Adjusted EBITDA', 0):.1f} | {ratios.get('ev_ebitda', 0):.1f}x | {ev_ebitda_outcome} |\n"
        
        ev_ebit_outcome = self.evaluate_ratio(ratios.get('ev_ebit', 0), 'ev_ebit')
        content += f"| **EV/EBIT** | EV / EBIT | {self.metrics.get('Enterprise Value', 0):.1f} / {self.metrics.get('EBIT Annual', 0):.1f} | {ratios.get('ev_ebit', 0):.1f}x | {ev_ebit_outcome} |\n"

        ev_revenue_outcome = self.evaluate_ratio(ratios.get('ev_revenue', 0), 'ev_revenue')
        content += f"| **EV/Revenue** | EV / Revenue | {self.metrics.get('Enterprise Value', 0):.1f} / {self.metrics.get('Revenue Annual', 0):.1f} | {ratios.get('ev_revenue', 0):.2f}x | {ev_revenue_outcome} |\n"
        
        if ratios.get('price_to_fcf') is not None:
            price_to_fcf_outcome = self.evaluate_ratio(ratios.get('price_to_fcf', 0), 'price_to_fcf')
            content += f"| **Price/FCF** | Market Cap / FCF | {self.metrics.get('market_cap', 0):.1f} / {self.metrics.get('FCF Annual', 0):.1f} | {ratios['price_to_fcf']:.1f}x | {price_to_fcf_outcome} |\n"
        
        fcf_yield_outcome = self.evaluate_ratio(ratios.get('fcf_yield', 0), 'fcf_yield')
        content += f"| **FCF Yield** | FCF / Market Cap | {self.metrics.get('FCF Annual', 0):.1f} / {self.metrics.get('market_cap', 0):.1f} | {ratios.get('fcf_yield', 0):.1f}% | {fcf_yield_outcome} |\n"
        
        # Profitability Ratios
        content += "\n## **Profitability Ratios**\n\n"
        content += "| Ratio | Formula | Calculation | Value | Outcome |\n"
        content += "|-------|---------|-------------|-------|----------|\n"
        
        gross_outcome = self.evaluate_ratio(ratios.get('gross_margin', 0), 'gross_margin')
        content += f"| **Gross Margin** | Gross Profit / Revenue | {self.metrics.get('Gross Profit', 0):.1f} / {self.metrics.get('Revenue', 0):.1f} | {ratios.get('gross_margin', 0):.1f}% | {gross_outcome} |\n"
        
        op_outcome = self.evaluate_ratio(ratios.get('operating_margin', 0), 'operating_margin')
        content += f"| **Operating Margin** | Operating Profit / Revenue | {self.metrics.get('Operating Profit', 0):.1f} / {self.metrics.get('Revenue', 0):.1f} | {ratios.get('operating_margin', 0):.1f}% | {op_outcome} |\n"
        
        net_outcome = self.evaluate_ratio(ratios.get('net_margin', 0), 'net_margin')
        content += f"| **Net Margin** | Net Income / Revenue | {self.metrics.get('Net Income', 0):.1f} / {self.metrics.get('Revenue', 0):.1f} | {ratios.get('net_margin', 0):.1f}% | {net_outcome} |\n"
        
        roa_outcome = self.evaluate_ratio(ratios.get('roa', 0), 'roa')
        content += f"| **ROA** | Net Income / Assets | {self.metrics.get('Net Income Annual', 0):.1f} / {self.metrics.get('Total Assets', 0):.1f} | {ratios.get('roa', 0):.1f}% | {'FAIL' if ratios.get('roa', 0) < 0 else {roa_outcome}} |\n"
        
        roe_outcome = self.evaluate_ratio(ratios.get('roe', 0), 'roe')
        content += f"| **ROE** | Net Income / Equity | {self.metrics.get('Net Income Annual', 0):.1f} / {self.metrics.get('Total Equity', 0):.1f} | {ratios.get('roe', 0):.1f}% | {roe_outcome} |\n"
        
        roce_outcome = self.evaluate_ratio(ratios.get('roce', 0), 'roce')
        content += f"| **ROCE** | EBIT / Capital Employed | {self.metrics.get('EBIT Annual', 0):.1f} / {(self.metrics.get('Total Assets', 0) - self.metrics.get('Current Liabilities', 0)):.1f} | {ratios.get('roce', 0):.1f}% | {roce_outcome} |\n"
        
        # Efficiency Ratios
        content += "\n## **Efficiency Ratios**\n\n"
        content += "| Ratio | Formula | Calculation | Value | Outcome |\n"
        content += "|-------|---------|-------------|-------|----------|\n"
        
        asset_turnover_outcome = self.evaluate_ratio(ratios.get('asset_turnover', 0), 'asset_turnover')
        content += f"| **Asset Turnover** | Revenue / Assets | {self.metrics.get('Revenue Annual', 0):.1f} / {self.metrics.get('Total Assets', 0):.1f} | {ratios.get('asset_turnover', 0):.2f}x | {asset_turnover_outcome} |\n"
        
        inv_outcome = self.evaluate_ratio(ratios.get('inventory_turnover', 0), 'inventory_turnover')
        content += f"| **Inventory Turnover** | COGS / Inventory | {self.metrics.get('COGS', 0)*2:.1f} / {self.metrics.get('Inventories', 0):.1f} | {ratios.get('inventory_turnover', 0):.1f}x | {inv_outcome} |\n"
        
        receivables_turnover_outcome = self.evaluate_ratio(ratios.get('receivables_turnover', 0), 'receivables_turnover')
        content += f"| **Receivables Turnover** | Revenue / Receivables | {self.metrics.get('Revenue Annual', 0):.1f} / {self.metrics.get('Receivables', 0):.1f} | {ratios.get('receivables_turnover', 0):.1f}x | {receivables_turnover_outcome} |\n"
        
        dso_outcome = self.evaluate_ratio(ratios.get('dso', 0), 'dso')
        content += f"| **DSO** | 365 / Rec Turnover | 365 / {ratios.get('receivables_turnover', 0):.1f} | {ratios.get('dso', 0):.0f} days | {dso_outcome} |\n"
        
        # Liquidity Ratios
        content += "\n## **Liquidity Ratios**\n\n"
        content += "| Ratio | Formula | Calculation | Value | Outcome |\n"
        content += "|-------|---------|-------------|-------|----------|\n"
        
        current_outcome = self.evaluate_ratio(ratios.get('current_ratio', 0), 'current_ratio')
        content += f"| **Current Ratio** | Current Assets / Current Liabilities | {self.metrics.get('Current Assets', 0):.1f} / {self.metrics.get('Current Liabilities', 0):.1f} | {ratios.get('current_ratio', 0):.2f}x | {current_outcome} |\n"
        
        quick_outcome = self.evaluate_ratio(ratios.get('quick_ratio', 0), 'quick_ratio')
        content += f"| **Quick Ratio** | (CA - Inventory) / CL | ({self.metrics.get('Current Assets', 0):.1f} - {self.metrics.get('Inventories', 0):.1f}) / {self.metrics.get('Current Liabilities', 0):.1f} | {ratios.get('quick_ratio', 0):.2f}x | {quick_outcome} |\n"

        cash_outcome = self.evaluate_ratio(ratios.get('cash_ratio', 0), 'cash_ratio')
        content += f"| **Cash Ratio** | Cash / Current Liabilities | {self.metrics.get('Cash and Bank Balances', 0):.1f} / {self.metrics.get('Current Liabilities', 0):.1f} | {ratios.get('cash_ratio', 0):.2f}x | {cash_outcome} |\n"
        
        # Leverage Ratios
        content += "\n## **Leverage Ratios**\n\n"
        content += "| Ratio | Formula | Calculation | Value | Outcome |\n"
        content += "|-------|---------|-------------|-------|----------|\n"
        
        de_outcome = self.evaluate_ratio(ratios.get('debt_to_equity', 0), 'debt_to_equity')
        content += f"| **Debt-to-Equity** | Total Debt / Equity | {self.metrics.get('Total Debt', 0):.1f} / {self.metrics.get('Total Equity', 0):.1f} | {ratios.get('debt_to_equity', 0):.2f}x | {de_outcome} |\n"
        
        debt_outcome = self.evaluate_ratio(ratios.get('debt_ratio', 0), 'debt_ratio')
        content += f"| **Debt Ratio** | Total Debt / Assets | {self.metrics.get('Total Debt', 0):.1f} / {self.metrics.get('Total Assets', 0):.1f} | {ratios.get('debt_ratio', 0):.2f}x | {debt_outcome} |\n"
        
        int_outcome = self.evaluate_ratio(ratios.get('interest_coverage', 0), 'interest_coverage')
        content += f"| **Interest Coverage** | EBIT / Interest | {self.metrics.get('EBIT Annual', 0):.1f} / {self.metrics.get('Interest Annual', 0):.1f} | {ratios.get('interest_coverage', 0):.1f}x | {int_outcome} |\n"
        
        nd_outcome = self.evaluate_ratio(ratios.get('net_debt_ebitda', 0), 'net_debt_ebitda')
        content += f"| **Net Debt/EBITDA** | Net Debt / LTM EBITDA | {self.metrics.get('Net Debt', 0):.1f} / {self.metrics.get('LTM Adjusted EBITDA', 0):.1f} | {ratios.get('net_debt_ebitda', 0):.2f}x | {nd_outcome} |\n"
        
        # Cash Flow Ratios
        content += "\n## **Cash Flow Ratios**\n\n"
        content += "| Ratio | Formula | Calculation | Value | Outcome |\n"
        content += "|-------|---------|-------------|-------|----------|\n"
        
        # Add FCF display using extracted value and evaluate with thresholds
        fcf_annual = self.metrics.get('FCF Annual', 0)
        fcf_outcome = self.evaluate_ratio(fcf_annual, 'free_cash_flow') #check this line?
        content += f"| **Free Cash Flow Annual** | OCF - CapEx | Extracted | {fcf_annual} | {fcf_outcome} |\n"
        
        ocf_outcome = self.evaluate_ratio(ratios.get('ocf_ratio', 0), 'ocf_ratio')
        content += f"| **OCF Ratio** | Op Cash Flow / Current Liabilities | {self.metrics.get('Operating Cash Flow', 0):.1f} / {self.metrics.get('Current Liabilities', 0):.1f} | {ratios.get('ocf_ratio', 0):.2f}x | {ocf_outcome} |\n"
        
        cc_outcome = self.evaluate_ratio(ratios.get('cash_conversion', 0), 'cash_conversion')
        net_income_annual = self.metrics.get('Net Income Annual', self.metrics.get('Net Income', 0) * 2)
        ocf_annual = self.metrics.get('Operating Cash Flow', 0) * 2
        content += f"| **Cash Conversion** | OCF Annual / NI Annual | {ocf_annual:.1f} / {abs(net_income_annual):.1f} | {ratios.get('cash_conversion', 0):.1f}x | {cc_outcome} |\n"
        
        # Earnings Quality Ratios
        content += "\n## **Earnings Quality Ratios**\n\n"
        content += "| Ratio | Formula | Calculation | Value | Outcome |\n"
        content += "|-------|---------|-------------|-------|----------|\n"
        
        acc_outcome = self.evaluate_ratio(abs(ratios.get('accruals_ratio', 0)), 'accruals_ratio')
        net_income_annual = self.metrics.get('Net Income Annual', self.metrics.get('Net Income', 0) * 2)
        ocf_annual = self.metrics.get('Operating Cash Flow', 0) * 2
        content += f"| **Accruals Ratio** | (NI Annual - OCF Annual) / Assets | ({net_income_annual:.1f} - {ocf_annual:.1f}) / {self.metrics.get('Total Assets', 0):.1f} | {ratios.get('accruals_ratio', 0):.1f}% | {acc_outcome} |\n"
        
        efc_outcome = self.evaluate_ratio(ratios.get('ebitda_fcf_conv', 0), 'ebitda_fcf_conv')
        fcf_annual = self.metrics.get('FCF Annual', 0)
        ltm_ebitda = self.metrics.get('LTM Adjusted EBITDA', self.metrics.get('EBITDA', 0))
        content += f"| **EBITDA to FCF** | FCF Annual / LTM EBITDA | {self.metrics.get('FCF Annual', 0):.1f} / {self.metrics.get('LTM Adjusted EBITDA', 0):.1f} | {ratios.get('ebitda_fcf_conv', 0):.1f}% | {efc_outcome} |\n"
        
        asg_outcome = self.evaluate_ratio(abs(ratios.get('adj_stat_gap', 0)), 'adj_stat_gap')
        content += f"| **Adj vs Stat Gap** | (Adj - Stat) / Stat | ({self.metrics.get('Adjusted Operating Profit', 0):.1f} - {self.metrics.get('Statutory Operating Profit', 0):.1f}) / {self.metrics.get('Statutory Operating Profit', 0):.1f} | {ratios.get('adj_stat_gap', 0):.1f}% | {asg_outcome} |\n"
        
        # Asset Quality Ratios
        content += "\n## **Asset Quality Ratios**\n\n"
        content += "| Ratio | Formula | Calculation | Value | Outcome |\n"
        content += "|-------|---------|-------------|-------|----------|\n"
        
        gw_outcome = self.evaluate_ratio(ratios.get('goodwill_assets', 0), 'goodwill_assets')
        content += f"| **Goodwill/Assets** | Goodwill / Total Assets | {self.metrics.get('Goodwill', 0):.1f} / {self.metrics.get('Total Assets', 0):.1f} | {ratios.get('goodwill_assets', 0):.1f}% | {gw_outcome} |\n"
        
        capex_outcome = self.evaluate_ratio(ratios.get('capex_dep', 0), 'capex_dep')
        annualized_capex = self.metrics.get('Capex', 0) * 2  # H1 to annual
        content += f"| **Capex/Depreciation** | Annualized Capex / LTM Depreciation | {annualized_capex:.1f} / {self.metrics.get('Depreciation', 0):.1f} | {ratios.get('capex_dep', 0):.2f}x | {capex_outcome} |\n"
        
        working_capital_outcome = self.evaluate_ratio(ratios.get('working_capital', 0), 'working_capital')
        content += f"| **Working Capital** | CA - CL | {self.metrics.get('Current Assets', 0):.1f} - {self.metrics.get('Current Liabilities', 0):.1f} | £{ratios.get('working_capital', 0):.1f}m | {working_capital_outcome} |\n"
        
        book_value_outcome = self.evaluate_ratio(ratios.get('tangible_book_value', 0), 'tangible_book_value')
        content += f"| **Tangible Book Value** | Equity - Intangibles | {self.metrics.get('Total Equity', 0):.1f} - {self.metrics.get('Intangible Assets', 0) + self.metrics.get('Goodwill', 0):.1f} | £{self.metrics.get('Tangible Book Value', 0):.1f}m | {book_value_outcome} |\n"
        
        # Variables Used Table - COMPREHENSIVE
        content += "\n## **All Variables Used in Calculations**\n\n"
        content += "| Variable | Value | Unit | Source |\n"
        content += "|----------|-------|------|--------|\n"
        
        # Sort and display all metrics
        for key, value in sorted(self.metrics.items()):
            if key not in ['company_name', 'currency']:
                unit = ""
                source = "Extracted"
                
                # Determine unit
                if 'margin' in key.lower() or '%' in key or 'yield' in key.lower():
                    unit = "%"
                elif key in ['share_price']:
                    unit = currency_symbol
                elif key in ['shares_outstanding', 'Shares Outstanding']:
                    unit = "millions"
                elif 'Annual' in key or 'LTM' in key or key in self._get_financial_metrics():
                    unit = f"{currency_symbol}m"
                
                # Determine source with document references
                if key in ['share_price', 'market_cap', 'shares_outstanding']:
                    source = "Yahoo Finance"
                elif 'Annual' in key:
                    source = "Annualized (x2)"
                elif key == 'Enterprise Value':
                    source = "Calculated"
                elif key == 'LTM Adjusted EBITDA':
                    # Include source document if available
                    if self.data_sources:
                        doc_name = Path(self.data_sources[0]).name if self.data_sources else "financial docs"
                        source = f"{doc_name}/Note 5 (LTM)"
                    else:
                        source = "Note 5 (LTM)"
                elif key in ['Revenue', 'EBITDA', 'Operating Profit', 'Net Income', 'Total Assets', 'Total Equity']:
                    # Major financial metrics from documents
                    if self.data_sources:
                        doc_name = Path(self.data_sources[0]).name if self.data_sources else "financial docs"
                        source = doc_name
                    else:
                        source = "Financial Reports"
                
                if isinstance(value, (int, float)):
                    content += f"| {key} | {value:.2f} | {unit} | {source} |\n"
        
        return content
    
    def _get_financial_metrics(self) -> List[str]:
        """List of financial metrics that should be in millions"""
        return ['Revenue', 'EBITDA', 'EBIT', 'Operating Profit', 'Net Income',
                'Total Assets', 'Total Equity', 'Total Debt', 'Net Debt',
                'Current Assets', 'Current Liabilities', 'Cash and Bank Balances',
                'Free Cash Flow', 'Operating Cash Flow', 'Gross Profit', 'COGS']
    
    def run(self, output_dir: str = 'data'):
        """Main execution method"""
        output_path = Path(output_dir)
        
        # Calculate ratios
        ratios = self.calculate_ratios()
        
        # Ensure company folder exists
        company_folder = output_path / self.ticker_base
        company_folder.mkdir(exist_ok=True)
        
        # Generate all ratios file in company folder with ticker prefix
        company_prefix = self.ticker_base.lower()
        ratios_content = self.generate_all_ratios_file(ratios)
        ratios_file = company_folder / f'{company_prefix}_all_ratios.md'
        with open(ratios_file, 'w') as f:
            f.write(ratios_content)
        print(f"\nGenerated all ratios file: {ratios_file}")
        
        # Generate agent_ratios.md in company folder with ticker prefix
        self._generate_agent_ratios(ratios, company_folder, company_prefix)
        
        return ratios, self.metrics
    
    def _generate_agent_ratios(self, ratios: Dict, output_path: Path, ticker_prefix: str):
        """Generate agent_ratios.md with only enabled ratios, their values and evaluations"""
        agent_file = output_path / f'{ticker_prefix}_agent_ratios.md'
        
        # Get timestamp
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        content = []
        content.append(f"# {self.metrics.get('company_name', self.ticker)} Enabled Financial Ratios Analysis")
        content.append("")
        content.append("This document contains ONLY the enabled financial ratios with their calculated values and evaluation outcomes.")
        content.append("Data Source: xp-power.md (H1 2025 Results)")
        content.append("")
        
        # Add Market Data Section (same as financial_ratios.md)
        content.append("## **Current Market Data**")
        content.append("")
        content.append("| Metric | Value | Source | Retrieved |")
        content.append("|--------|-------|--------|----------|")
        
        currency_symbol = '£' if self.metrics.get('currency') == 'GBP' else '$'
        content.append(f"| **Share Price** | {currency_symbol}{self.metrics.get('share_price', 0):.2f} | Yahoo Finance | {formatted_time} |")
        content.append(f"| **Market Cap** | {currency_symbol}{self.metrics.get('market_cap', 0):.1f}m | Yahoo Finance | {formatted_time} |")
        content.append(f"| **Enterprise Value** | {currency_symbol}{self.metrics.get('Enterprise Value', 0):.1f}m | Calculated | - |")
        content.append(f"| **Shares Outstanding** | {self.metrics.get('Shares Outstanding', 0):.1f}m | Financial Reports | - |")
        content.append("")
        
        # Organize ratios by category
        categories = {
            'valuation': 'Valuation Ratios',
            'profitability': 'Profitability Ratios', 
            'liquidity': 'Liquidity Ratios',
            'leverage': 'Leverage Ratios',
            'efficiency': 'Efficiency Ratios',
            'earnings_quality': 'Earnings Quality Ratios',
            'asset_quality': 'Asset Quality Ratios',
            'cash_flow': 'Cash Flow Ratios'
        }
        
        # Map ratio keys to categories - MUST match ratio_rules.md exactly
        ratio_categories = {
            'pe_ratio': 'valuation', 'ev_ebitda': 'valuation', 'ev_ebit': 'valuation',
            'fcf_yield': 'valuation', 'pb_ratio': 'valuation', 'ps_ratio': 'valuation',
            'ev_revenue': 'valuation', 'price_to_fcf': 'valuation',  # Added ev_revenue and moved price_to_fcf
            'gross_margin': 'profitability', 'operating_margin': 'profitability',
            'net_margin': 'profitability', 'roe': 'profitability', 'roce': 'profitability', 'roa': 'profitability',
            'current_ratio': 'liquidity', 'quick_ratio': 'liquidity', 'cash_ratio': 'liquidity',
            'debt_to_equity': 'leverage', 'net_debt_ebitda': 'leverage',
            'interest_coverage': 'leverage', 'debt_ratio': 'leverage',
            'inventory_turnover': 'efficiency', 'dso': 'efficiency',
            'asset_turnover': 'efficiency', 'receivables_turnover': 'efficiency',
            'cash_conversion': 'cash_flow', 'free_cash_flow': 'cash_flow',  # Added free_cash_flow
            'accruals_ratio': 'earnings_quality', 'ebitda_fcf_conv': 'earnings_quality', 'adj_stat_gap': 'earnings_quality',
            'goodwill_assets': 'asset_quality', 'capex_dep': 'asset_quality', 
            'tangible_book_value': 'asset_quality', 'working_capital': 'asset_quality',  # Added tangible_book_value
            'ocf_ratio': 'cash_flow'
        }
        
        has_enabled_ratios = False
        
        for category_key, category_name in categories.items():
            # Collect enabled ratios for this category
            category_ratios = []
            
            for ratio_key, value in ratios.items():
                if (ratio_key in self.thresholds and 
                    self.thresholds[ratio_key].get('enabled', True) and
                    ratio_categories.get(ratio_key) == category_key):
                    
                    outcome = self.evaluate_ratio(value, ratio_key)
                    if outcome != "DISABLED":
                        category_ratios.append((ratio_key, value, outcome))
            
            # Only add category if it has enabled ratios
            if category_ratios:
                has_enabled_ratios = True
                content.append(f"## {category_name}")
                content.append("")
                content.append("| Ratio | Value | Threshold (Pass/Monitor/Fail) | Outcome |")
                content.append("|-------|-------|-------------------------------|---------|")
                
                for ratio_key, value, outcome in category_ratios:
                    display_name = self._get_ratio_display_name(ratio_key)
                    formatted_value = self._format_ratio_value(ratio_key, value)
                    threshold_info = self._get_threshold_info(ratio_key)
                    outcome_display = self._format_outcome(outcome)
                    
                    content.append(f"| {display_name} | {formatted_value} | {threshold_info} | {outcome_display} |")
                
                content.append("")
        
        if not has_enabled_ratios:
            content.append("## No Ratios Enabled")
            content.append("")
            content.append("No financial ratios are currently enabled for analysis.")
            content.append("Please enable ratios in the Ratios Configuration page.")
        else:
            # Add summary section
            content.append("## Summary Statistics")
            content.append("")
            
            # Count outcomes
            pass_count = sum(1 for ratio_key, value in ratios.items() 
                           if ratio_key in self.thresholds and 
                           self.thresholds[ratio_key].get('enabled', True) and
                           self.evaluate_ratio(value, ratio_key) == "PASS")
            monitor_count = sum(1 for ratio_key, value in ratios.items() 
                              if ratio_key in self.thresholds and 
                              self.thresholds[ratio_key].get('enabled', True) and
                              self.evaluate_ratio(value, ratio_key) == "MONITOR")
            fail_count = sum(1 for ratio_key, value in ratios.items() 
                           if ratio_key in self.thresholds and 
                           self.thresholds[ratio_key].get('enabled', True) and
                           self.evaluate_ratio(value, ratio_key) == "FAIL")
            
            total = pass_count + monitor_count + fail_count
            
            content.append(f"- **Total Enabled Ratios**: {total}")
            content.append(f"- **PASS**: {pass_count} ({pass_count*100//max(total,1)}%)")
            content.append(f"- **MONITOR**: {monitor_count} ({monitor_count*100//max(total,1)}%)")
            content.append(f"- **FAIL**: {fail_count} ({fail_count*100//max(total,1)}%)")
        
        content.append("")
        content.append("---")
        content.append("*This file is generated during analysis execution and contains calculated values with evaluations.*")
        
        with open(agent_file, 'w') as f:
            f.write('\n'.join(content))
        
        print(f"Generated agent_ratios.md: {agent_file}")
    
    def _get_threshold_info(self, ratio_key: str) -> str:
        """Get threshold information for display"""
        if ratio_key not in self.thresholds:
            return "N/A"
        
        threshold = self.thresholds[ratio_key]
        
        if ratio_key == 'capex_dep':
            return f"{threshold.get('pass_min', 0)}-{threshold.get('pass_max', 0)} / <{threshold.get('pass_min', 0)} or >{threshold.get('pass_max', 0)} / >{threshold.get('monitor_max', 0)}"
        
        pass_val = threshold.get('pass', 0)
        monitor_val = threshold.get('monitor', 0)
        
        # Determine if lower or higher is better
        if ratio_key in ['pe_ratio', 'ev_ebitda', 'ev_ebit', 'net_debt_ebitda', 'debt_to_equity', 
                         'accruals_ratio', 'adj_stat_gap', 'goodwill_assets', 'dso']:
            # Lower is better
            return f"<{pass_val} / {pass_val}-{monitor_val} / >{monitor_val}"
        else:
            # Higher is better
            return f">{pass_val} / {monitor_val}-{pass_val} / <{monitor_val}"
    
    def _format_outcome(self, outcome: str) -> str:
        """Format outcome for display"""
        if outcome == "PASS":
            return "PASS"
        elif outcome == "MONITOR":
            return "MONITOR"
        elif outcome == "FAIL":
            return "FAIL"
        else:
            return outcome
    
    def _get_ratio_display_name(self, ratio_key: str) -> str:
        """Get display name for a ratio"""
        name_map = {
            'pe_ratio': 'P/E Ratio',
            'ev_ebitda': 'EV/EBITDA',
            'ev_ebit': 'EV/EBIT',
            'fcf_yield': 'FCF Yield',
            'pb_ratio': 'P/B Ratio',
            'ps_ratio': 'P/S Ratio',
            'gross_margin': 'Gross Margin',
            'operating_margin': 'Operating Margin',
            'net_margin': 'Net Margin',
            'roe': 'ROE',
            'roce': 'ROCE',
            'roa': 'ROA',
            'current_ratio': 'Current Ratio',
            'quick_ratio': 'Quick Ratio',
            'cash_ratio': 'Cash Ratio',
            'debt_to_equity': 'Debt-to-Equity',
            'net_debt_ebitda': 'Net Debt/EBITDA',
            'interest_coverage': 'Interest Coverage',
            'debt_ratio': 'Debt Ratio',
            'inventory_turnover': 'Inventory Turnover',
            'dso': 'Days Sales Outstanding',
            'asset_turnover': 'Asset Turnover',
            'receivables_turnover': 'Receivables Turnover',
            'cash_conversion': 'Cash Conversion',
            'accruals_ratio': 'Accruals Ratio',
            'ebitda_fcf_conv': 'EBITDA to FCF Conversion',
            'adj_stat_gap': 'Adjusted vs Statutory Gap',
            'goodwill_assets': 'Goodwill/Assets',
            'capex_dep': 'Capex/Depreciation',
            'working_capital': 'Working Capital',
            'ocf_ratio': 'Operating Cash Flow Ratio',
            'price_to_fcf': 'Price to FCF',
            'ev_revenue': 'EV/Revenue',
            'free_cash_flow': 'Free Cash Flow',
            'tangible_book_value': 'Tangible Book Value',
        }
        return name_map.get(ratio_key, ratio_key.replace('_', ' ').title())
    
    def _format_ratio_value(self, ratio_key: str, value: float) -> str:
        """Format ratio value for display"""
        if value is None:
            return "N/A"
        
        # Determine formatting based on ratio type
        if any(x in ratio_key for x in ['margin', 'yield', 'roe', 'roce', 'roa', 'ratio']) and '%' not in ratio_key:
            return f"{value:.1f}%"
        elif 'days' in ratio_key or ratio_key == 'dso':
            return f"{value:.0f} days"
        elif any(x in ratio_key for x in ['_ratio', 'turnover', 'coverage', 'ev_', 'pe_', 'pb_', 'ps_', 'price_to_fcf']):
            return f"{value:.1f}x"
        elif ratio_key in ['working_capital', 'tangible_book_value', 'free_cash_flow']:
            return f"£{value:.1f}m"
        else:
            return f"{value:.1f}"


if __name__ == "__main__":
    calculator = FinancialRatioCalculator(company_ticker='XPP.L')
    ratios, metrics = calculator.run()
    print("\nRatio calculation complete!")