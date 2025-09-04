"""CrewAI implementation for Insig Analyst financial analysis.

This module defines the crew structure with specialized agents and tasks
for analyzing company financial data. It uses a sequential process with
memory disabled to prevent context contamination between tasks.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, before_kickoff, crew, task
from crewai_tools import FileReadTool
from dotenv import load_dotenv
from .ratio_calc import FinancialRatioCalculator

# Create a structured output for Richard, so the report looks the same everytime
class RichardOutput(BaseModel):
    company: str = Field(description="The company being analysed")
    findings: str = Field(description="Your key findings about the company")
    relevance: str = Field(description="Why these findings are relevant or important")
    conclusion: str = Field(description="Your conclusion for the company based on your findings")


# Load environment variables from .env file
load_dotenv()

# Set the model and temperature for all agents
llm = LLM(
    model="gpt-4.1-mini",
    temperature=0,
)

# Instantiate file reading tools for data access
agent_ratios_read_tool = FileReadTool(
    file_path='./data/{ticker}/{ticker}_agent_ratios.md'
)
income_read_tool = FileReadTool(
    file_path='./data/{ticker}/{ticker}_income_statement.md'
)
cashflow_read_tool = FileReadTool(
    file_path='./data/{ticker}/{ticker}_cashflow_statement.md'
)
balance_sheet_read_tool = FileReadTool(
    file_path='./data/{ticker}/{ticker}_balancesheet_statement.md'
)
notes_read_tool = FileReadTool(
    file_path='./data/{ticker}/{ticker}_notes.md'
)
auditor_read_tool = FileReadTool(
    file_path='./data/{ticker}/{ticker}_auditor_report.md'
)
ceo_read_tool = FileReadTool(
    file_path='./data/{ticker}/{ticker}_ceo_report.md'
)
ownership_analysis_read_tool = FileReadTool(
    file_path='./data/{ticker}/{ticker}_company_ownership.md'
)
durability_read_tool = FileReadTool(
    file_path='./output/{ticker}/{ticker}_balancesheet_durability.md'
)
quality_read_tool = FileReadTool(
    file_path='./output/{ticker}/{ticker}_earning_quality.md'
)
valuation_read_tool = FileReadTool(
    file_path='./output/{ticker}/{ticker}_ownership.md'
)
ownership_read_tool = FileReadTool(
    file_path='./output/{ticker}/{ticker}_valuation.md'
)

def clear_context_callback(output: Any) -> Any:
    """Callback to clear context after each task.
    
    This prevents context contamination between tasks by resetting
    the crew's memory after each task completes.
    
    Args:
        output: The output from the completed task.
    
    Returns:
        The unchanged task output.
    """
    # Access the crew instance and reset memories
    if hasattr(output, 'agent') and hasattr(output.agent, 'crew'):
        crew_instance = output.agent.crew
        if crew_instance:
            crew_instance.reset_memories(command_type='all')
    return output

# Global variables for current analysis context
current_ticker: Optional[str] = None
current_data_dir: Optional[str] = None

@CrewBase
class InsigAnalystDemo():
    """Insig Analyst crew for financial analysis.
    
    This crew performs sequential analysis of company financial data
    using specialized agents for different aspects of financial analysis.
    
    Attributes:
        company_ticker: The ticker symbol for the company being analyzed.
        company_name: The full name of the company.
        agents_config: Path to agents configuration file.
        tasks_config: Path to tasks configuration file.
    """
    
    company_ticker: Optional[str] = None  # Will be set by backend
    company_name: Optional[str] = None  # Will be set by backend

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @before_kickoff
    def calculate_financial_ratios(
        self, inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate financial ratios before crew execution.
        
        This method implements the appflow.md requirements:
        1. Check for {ticker}.json file
        2. Fetch market data if JSON exists, or all data if not
        3. Save data to {ticker}.json
        4. Calculate all ratios and create {ticker}_all_ratios.md
        5. Create {ticker}_agent_ratios.md based on rules
        6. Validate ratios (check if >20% are 0 or missing)
        7. Check for required financial documents
        
        Args:
            inputs: Input parameters including ticker and company.
        
        Returns:
            Updated inputs dictionary.
        
        Raises:
            ValueError: If ticker symbol is not provided.
        """
        
        global current_ticker, current_data_dir
        
        # Get ticker and company from inputs - required parameters
        ticker_input = inputs.get('ticker')
        company_name = inputs.get('company', 'Unknown Company')
        
        if not ticker_input:
            raise ValueError(
                "Ticker symbol is required but not provided in inputs. "
                "Please specify a ticker."
            )
        
        self.company_ticker = ticker_input
        self.company_name = company_name
        
        # Determine ticker format and data directory
        # Remove exchange suffix for folder name (e.g., XPP.L -> XPP)
        if '.' in ticker_input:
            ticker = ticker_input.split('.')[0].upper()
        else:
            ticker = ticker_input.upper()
        
        data_dir = f'data/{ticker}'
        data_path = Path(data_dir)
        
        # Create data directory if it doesn't exist
        data_path.mkdir(parents=True, exist_ok=True)
        
        output_dir = f'output/{ticker}'
        current_ticker = ticker
        current_data_dir = data_dir
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Step 1: Check for {ticker}.json file (as per appflow.md)
        json_file_path = data_path / f'{ticker.lower()}.json'
        ticker_symbol = (
            ticker_input.upper() if '.' in ticker_input 
            else f'{ticker_input.upper()}.L'
        )
        
        # Step 2-3: Data fetching logic (not implementing tools yet)
        # For now, we just check if JSON exists
        if not json_file_path.exists():
            print(
                f"\nWarning: {json_file_path} not found. "
                f"Please provide financial data in JSON format."
            )
            print(
                f"The JSON file should contain market_data, "
                f"income_statement, balance_sheet, and cash_flow sections."
            )
        else:
            print(f"\nFound financial data: {json_file_path}")
        
        # Step 4-5: Calculate ratios using FinancialRatioCalculator
        print(f"\nCalculating financial ratios for {ticker_symbol}...")
        calculator = FinancialRatioCalculator(company_ticker=ticker_symbol, data_dir='data')
        
        try:
            # This will create both {ticker}_all_ratios.md and {ticker}_agent_ratios.md
            calculator.run()
            
            # Step 6: Validate ratios (check if >20% are 0 or missing)
            all_ratios_file = data_path / f'{ticker.lower()}_all_ratios.md'
            if all_ratios_file.exists():
                with open(all_ratios_file, 'r') as f:
                    content = f.read()
                    # Simple validation: count ratio lines and check for zeros
                    ratio_lines = [line for line in content.split('\n') if '|' in line and 'Ratio' not in line and '---' not in line]
                    total_ratios = len(ratio_lines)
                    zero_or_missing = sum(1 for line in ratio_lines if ' 0.00 ' in line or ' N/A ' in line or ' - ' in line)
                    
                    if total_ratios > 0 and zero_or_missing / total_ratios > 0.2:
                        warning_msg = f"\nWarning: More than 20% of ratios ({zero_or_missing}/{total_ratios}) are zero or missing."
                        warning_msg += "\nThis may indicate incomplete financial data. Please verify the input data."
                        print(warning_msg)
                        # Store warning in inputs for potential UI display
                        inputs['ratio_validation_warning'] = warning_msg
        except Exception as e:
            print(f"\nError calculating ratios: {e}")
            # Don't fail the crew, just note the error
            inputs['ratio_calculation_error'] = str(e)
        
        # Step 7: Check for required financial documents
        required_patterns = ['results', 'finance', 'report', 'balance', 'cash', 'income', 'statement']
        found_docs = []
        for pattern in required_patterns:
            matching_files = list(data_path.glob(f'*{pattern}*.md'))
            found_docs.extend(matching_files)
        
        found_docs = list(set(found_docs))  # Remove duplicates
        
        if len(found_docs) < 3:  # Arbitrary minimum, adjust as needed
            print(f"\nWarning: Only found {len(found_docs)} financial documents in {data_dir}")
            print("Consider adding more financial documents for comprehensive analysis.")
            print("Looking for files with patterns: *results*.md, *finance*.md, *report*.md, etc.")
        
        ticker_prefix = ticker.lower()
        agent_ratios_path = f'{data_dir}/{ticker_prefix}_agent_ratios.md'
        
        print(f"\n=== Crew Configuration Summary ===")
        print(f"Company: {company_name} (Ticker: {ticker})")
        print(f"Data directory: {data_dir}")
        print(f"Output directory: {output_dir}")
        print(f"\nData Status:")
        print(f"  JSON data: {'✓ Found' if json_file_path.exists() else '✗ Missing - please provide'}") 
        print(f"  Financial documents: {len(found_docs)} found")
        print(f"\nKey files:")
        print(f"  JSON data: {json_file_path}")
        print(f"  Agent ratios: {agent_ratios_path}")
        print(f"  All ratios: {data_dir}/{ticker_prefix}_all_ratios.md")
        print(f"  Ratio rules: {data_dir}/{ticker_prefix}_ratio_rules.md")
        print(f"===================================\n")
        
        return inputs
    
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def victoria_clarke(self) -> Agent:
        """Financial modeling and valuation expert"""
        return Agent(
            config=self.agents_config['victoria_clarke'], # type: ignore[index]
            tools=[
                agent_ratios_read_tool,
                income_read_tool,
                cashflow_read_tool,
                balance_sheet_read_tool,
                ownership_analysis_read_tool,
            ],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    @agent
    def daniel_osei(self) -> Agent:
        """Forensic accounting specialist"""
        return Agent(
            config=self.agents_config['daniel_osei'], # type: ignore[index]
            tools=[
                agent_ratios_read_tool,
                income_read_tool,
                cashflow_read_tool,
                balance_sheet_read_tool,
                notes_read_tool,
                ceo_read_tool,
                auditor_read_tool,
            ],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    @agent
    def richard(self) -> Agent:
        """Investment decision maker who reads other agents' reports"""
        return Agent(
            config=self.agents_config['richard'], # type: ignore[index]
            tools=[
                durability_read_tool,
                quality_read_tool,
                ownership_read_tool,
                valuation_read_tool,
            ],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )
    
    @agent
    def formatter(self) -> Agent:
        """Transform research reports into beautifully formatted, readable markdown documents"""
        return Agent(
            config=self.agents_config['formatter'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def primary_ratios(self) -> Task:
        return Task(
            config=self.tasks_config['primary_ratios'], # type: ignore[index]
            callback=clear_context_callback  # Clear context after this task
        )
    
    @task
    def ownership_task(self) -> Task:
        return Task(
            config=self.tasks_config['ownership_task'], # type: ignore[index]
            callback=clear_context_callback  # Clear context after this task
        )
    
    @task
    def earnings_quality_task(self) -> Task:
        return Task(
            config=self.tasks_config['earnings_quality_task'], # type: ignore[index]
            callback=clear_context_callback  # Clear context after this task
        )
    
    @task
    def balance_sheet_durability_task(self) -> Task:
        return Task(
            config=self.tasks_config['balance_sheet_durability_task'], # type: ignore[index]
            callback=clear_context_callback  # Clear context after this task
        )
    
    @task
    def final_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_analysis_task'], # type: ignore[index]
            callback=clear_context_callback,  # Clear context after this task
            output_json=RichardOutput, # Structured output for JSON file
        )
    
    @task
    def formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config['formatting_task'], # type: ignore[index]
            callback=clear_context_callback,  # Clear context after this task
        )

    @crew
    def crew(self) -> Crew:
        """Creates the InsigAnalystDemo crew
        
        Configured to run sequentially with memory disabled to prevent
        context contamination between tasks.
        """
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            process=Process.sequential,
            memory=False,  # Disabled to prevent context contamination
            verbose=True,
        )