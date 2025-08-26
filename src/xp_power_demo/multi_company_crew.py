from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Dict, Any, Optional
from crewai_tools import FileReadTool
from pathlib import Path
import os
import yfinance as yf

def clear_context_callback(output):
    """Callback to clear context after each task"""
    if hasattr(output, 'agent') and hasattr(output.agent, 'crew'):
        crew_instance = output.agent.crew
        if crew_instance:
            crew_instance.reset_memories(command_type='all')
    return output

@CrewBase
class MultiCompanyXpPowerDemo():
    """Multi-company analysis crew"""
    
    agents: List[BaseAgent]
    tasks: List[Task]
    company_ticker: str
    company_name: str
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self, company_ticker: str, company_name: str):
        """Initialize crew for a specific company"""
        super().__init__()
        self.company_ticker = company_ticker.upper()
        self.company_name = company_name
        
        # Set up company-specific data paths
        self.data_dir = Path(f"data/companies/{self.company_ticker}")
        self.output_dir = Path(f"output/companies/{self.company_ticker}")
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize file read tools with company-specific paths
        self._setup_file_tools()
    
    def _setup_file_tools(self):
        """Setup FileReadTools for company-specific data files"""
        # Look for standard file patterns in company data directory
        self.file_tools = {}
        
        # Standard file patterns to look for
        file_patterns = {
            'financial_data': ['*financial*.md', '*financials*.md', f'{self.company_ticker.lower()}*.md'],
            'metrics': ['*metrics*.md', '*prime-metrics*.md', '*ratios*.md'],
            'ownership': ['*ownership*.md', '*insider*.md', '*shareholders*.md'],
            'screening': ['*screening*.md', '*initial*.md', '*analysis*.md'],
            'balance_sheet': ['*balance*.md', '*balance-sheet*.md'],
            'income': ['*income*.md', '*earnings*.md', '*revenue*.md']
        }
        
        # Find and create tools for existing files
        for category, patterns in file_patterns.items():
            for pattern in patterns:
                matching_files = list(self.data_dir.glob(pattern))
                if matching_files:
                    # Use the first matching file for each category
                    file_path = matching_files[0]
                    self.file_tools[category] = FileReadTool(file_path=str(file_path))
                    break
        
        # Also create generic tools for any .md files in the directory
        all_md_files = list(self.data_dir.glob("*.md"))
        for md_file in all_md_files:
            tool_name = md_file.stem.replace('-', '_').replace(' ', '_')
            if tool_name not in self.file_tools:
                self.file_tools[tool_name] = FileReadTool(file_path=str(md_file))
    
    def _get_available_tools(self, required_categories: List[str]) -> List:
        """Get available tools for specified categories"""
        tools = []
        for category in required_categories:
            if category in self.file_tools:
                tools.append(self.file_tools[category])
            # Also check for tools by file name
            for tool_name, tool in self.file_tools.items():
                if category in tool_name.lower():
                    if tool not in tools:
                        tools.append(tool)
        return tools if tools else list(self.file_tools.values())[:3]  # Return first 3 tools if none match
    
    @before_kickoff
    def fetch_market_data(self, inputs):
        """Fetch real-time market data from Yahoo Finance before analysis starts"""
        
        # Use the company ticker for Yahoo Finance lookup
        ticker_symbol = self.company_ticker
        
        print(f"\n========== FETCHING MARKET DATA ==========")
        print(f"Company: {self.company_name}")
        print(f"Ticker Symbol: {ticker_symbol}")
        print(f"Source: Yahoo Finance API")
        
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            
            # Get share price and market cap
            share_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
            market_cap_raw = info.get('marketCap', 0)
            currency = info.get('currency', 'USD')
            company_name = info.get('longName', self.company_name)
            
            # Handle different currencies
            if currency in ['GBp', 'GBX']:
                # Price is in pence, convert to pounds
                share_price = share_price / 100
                currency_symbol = '£'
            elif currency == 'USD':
                currency_symbol = '$'
            elif currency == 'EUR':
                currency_symbol = '€'
            else:
                currency_symbol = currency
            
            # Convert market cap to millions
            if market_cap_raw > 0:
                market_cap = market_cap_raw / 1_000_000  # Convert to millions
            else:
                # Market cap not available
                market_cap = 0
            
            # Save market data to a file for agents to access
            market_data_path = self.data_dir / f"{self.company_ticker.lower()}_market_data.md"
            with open(market_data_path, 'w') as f:
                f.write(f"# {company_name} Market Data\n\n")
                f.write(f"**Ticker**: {ticker_symbol}\n")
                f.write(f"**Share Price**: {currency_symbol}{share_price:.2f}\n")
                f.write(f"**Market Cap**: {currency_symbol}{market_cap:.1f}m\n")
                f.write(f"**Currency**: {currency}\n")
                f.write(f"**Data Source**: Yahoo Finance\n")
                f.write(f"**Retrieved**: Real-time\n")
            
            # Add the market data file to tools
            self.file_tools['market_data'] = FileReadTool(file_path=str(market_data_path))
            
            print(f"Company: {company_name}")
            print(f"Share Price: {currency_symbol}{share_price:.2f}")
            print(f"Market Cap: {currency_symbol}{market_cap:.1f}m")
            print(f"Data Successfully Retrieved!")
            print("==========================================\n")
            
        except Exception as e:
            print(f"Warning: Could not fetch Yahoo Finance data for {ticker_symbol}")
            print(f"Error: {e}")
            print("Continuing without real-time market data...")
            print("==========================================\n")
        
        return inputs
    
    @agent
    def victoria_clarke(self) -> Agent:
        # Get tools relevant for financial analysis
        tools = self._get_available_tools(['financial_data', 'metrics', 'ownership', 'balance_sheet'])
        
        return Agent(
            config=self.agents_config['victoria_clarke'],
            verbose=True,
            tools=tools
        )
    
    @agent
    def daniel_osei(self) -> Agent:
        # Get tools relevant for forensic accounting
        tools = self._get_available_tools(['financial_data', 'balance_sheet', 'income', 'metrics'])
        
        return Agent(
            config=self.agents_config['daniel_osei'],
            verbose=True,
            tools=tools
        )
    
    @agent
    def richard(self) -> Agent:
        # Get tools relevant for investment decision
        tools = self._get_available_tools(['screening', 'financial_data', 'metrics'])
        
        return Agent(
            config=self.agents_config['richard'],
            verbose=True,
            tools=tools
        )
    
    def _create_task_with_dynamic_paths(self, task_config: Dict[str, Any], output_filename: str) -> Task:
        """Create a task with company-specific file paths"""
        # Update task description to use company-specific paths
        description = task_config.get('description', '')
        
        # Replace generic data folder references with company-specific ones
        description = description.replace('data/', f'data/companies/{self.company_ticker}/')
        description = description.replace('Read the following files in the data folder', 
                                        f'Read the following files in the {self.company_ticker} data folder')
        
        # Update with actual available files
        available_files = [f.name for f in self.data_dir.glob("*.md")]
        if available_files:
            files_list = "\n".join([f"    {f}" for f in available_files[:5]])  # List first 5 files
            description = f"{description}\n\nAvailable files in {self.company_ticker} folder:\n{files_list}"
        
        # Create task with updated configuration
        updated_config = task_config.copy()
        updated_config['description'] = description
        updated_config['output_file'] = str(self.output_dir / output_filename)
        
        return Task(
            config=updated_config,
            callback=clear_context_callback
        )
    
    @task
    def primary_ratios(self) -> Task:
        return self._create_task_with_dynamic_paths(
            self.tasks_config['primary_ratios'],
            'primary-ratios.md'
        )
    
    @task
    def ownership_task(self) -> Task:
        return self._create_task_with_dynamic_paths(
            self.tasks_config['ownership_task'],
            'ownership.md'
        )
    
    @task
    def earnings_quality_task(self) -> Task:
        return self._create_task_with_dynamic_paths(
            self.tasks_config['earnings_quality_task'],
            'earning-quality.md'
        )
    
    @task
    def balance_sheet_durability_task(self) -> Task:
        return self._create_task_with_dynamic_paths(
            self.tasks_config['balance_sheet_durability_task'],
            'balancesheet-durability.md'
        )
    
    @task
    def decision_task(self) -> Task:
        return self._create_task_with_dynamic_paths(
            self.tasks_config['decision_task'],
            'decision.md'
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the multi-company analysis crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=False,
            verbose=True,
        )
    
    def kickoff(self, inputs: Optional[Dict[str, Any]] = None) -> Any:
        """Run the crew analysis for the company"""
        if inputs is None:
            inputs = {}
        
        # Add company-specific information to inputs
        inputs.update({
            'company': self.company_name,
            'company_ticker': self.company_ticker,
            'data_folder': str(self.data_dir),
            'output_folder': str(self.output_dir)
        })
        
        crew_instance = self.crew()
        return crew_instance.kickoff(inputs=inputs)