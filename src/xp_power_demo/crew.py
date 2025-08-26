from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import FileReadTool
from .ratio_calc import FinancialRatioCalculator
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

def clear_context_callback(output):
    """Callback to clear context after each task"""
    # Access the crew instance and reset memories
    if hasattr(output, 'agent') and hasattr(output.agent, 'crew'):
        crew_instance = output.agent.crew
        if crew_instance:
            crew_instance.reset_memories(command_type='all')
    return output

# These will be initialized dynamically based on company ticker
read_results = None
read_screening = None
read_ratios = None
read_agent_ratios = None  # Will be initialized per company

# These are hardcoded, as these files will always be created by the agents and read by Richard.
read_valuation = FileReadTool(file_path="output/{ticker}/{ticker}-valuation.md")
read_ownership = FileReadTool(file_path="output/{ticker}/{ticker}-ownership.md")
read_earnings = FileReadTool(file_path="output/{ticker}/{ticker}-earning-quality.md")
read_balancesheet = FileReadTool(file_path="output/{ticker}/{ticker}-balancesheet-durability.md")

@CrewBase
class XpPowerDemo():
    """XP crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    company_ticker: str = None  # Will be set by backend

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @before_kickoff
    def calculate_financial_ratios(self, inputs):
        """Calculate financial ratios and set up file tools for the specific company"""
        
        # Get ticker from inputs
        ticker = inputs.get('ticker', 'XPP')
        ticker = ticker.upper().replace('.', '_')  # Sanitize ticker
        
        # Set up company-specific data paths
        data_dir = f'data/{ticker}'
        output_dir = f'output/{ticker}'
        
        # Create output directory if it doesn't exist
        from pathlib import Path
        import shutil
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize file tools for company-specific data
        global read_results, read_screening, read_ratios, read_agent_ratios
        
        # Set up company-specific agent_ratios.md (note: underscore, not hyphen)
        ticker_lower = ticker.lower()
        agent_ratios_path = f'{data_dir}/{ticker_lower}_agent_ratios.md'
        if Path(agent_ratios_path).exists():
            read_agent_ratios = FileReadTool(file_path=agent_ratios_path)
        else:
            # Will be created by FinancialRatioCalculator below
            read_agent_ratios = None
        
        # Look for company financial data files
        data_path = Path(data_dir)
        for file in data_path.iterdir():
            if file.is_file():
                file_lower = file.name.lower()
                if any(term in file_lower for term in ['financial', 'annual', 'report', 'power']):
                    read_results = FileReadTool(file_path=str(file))
                elif any(term in file_lower for term in ['screening', 'metrics', 'initial']):
                    read_screening = FileReadTool(file_path=str(file))
        
        # If no files found, use fallback
        if read_results is None:
            # Try to find any markdown file
            for file in data_path.glob('*.md'):
                if 'ratio' not in file.name.lower() and 'agent' not in file.name.lower():
                    read_results = FileReadTool(file_path=str(file))
                    break
        
        if read_screening is None:
            # Use the same file as results if no screening file found
            read_screening = read_results
        
        # Use ticker with .L suffix for Yahoo Finance (UK stocks)
        ticker_symbol = f"{ticker.replace('_', '.')}"
        if '.' not in ticker_symbol:
            ticker_symbol = f"{ticker_symbol}.L"  # Default to London Stock Exchange
        
        # Use the FinancialRatioCalculator to generate ratio files
        # The calculator will use company-specific ratio_rules.md from data/{ticker}/
        calculator = FinancialRatioCalculator(company_ticker=ticker_symbol)
        calculator.run()  # Generates ratio files
        
        # The all_ratios.md file is generated in company folder
        ticker_prefix = ticker.lower()
        all_ratios_path = f'{data_dir}/{ticker_prefix}_all_ratios.md'
        
        # Make the all ratios file available to agents
        if Path(all_ratios_path).exists():
            read_ratios = FileReadTool(file_path=all_ratios_path)
        
        # Also ensure agent_ratios.md is available from company folder
        company_agent_ratios = f'{data_dir}/{ticker_prefix}_agent_ratios.md'
        if Path(company_agent_ratios).exists():
            read_agent_ratios = FileReadTool(file_path=company_agent_ratios)
        
        print(f"Financial ratios calculated and saved to {all_ratios_path}")
        print(f"Using data from: {data_dir}")
        print(f"Using ratio rules from: {data_dir}/{ticker_prefix}_ratio_rules.md")
        print(f"Output will be saved to: {output_dir}")
        
        return inputs
    
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def victoria_clarke(self) -> Agent:
        tools = []
        if read_agent_ratios is not None:
            tools.append(read_agent_ratios)
        if read_results is not None:
            tools.append(read_results)
        return Agent(
            config=self.agents_config['victoria_clarke'], # type: ignore[index]
            verbose=True,
            tools=tools
        )
    
    @agent
    def daniel_osei(self) -> Agent:
        tools = []
        if read_agent_ratios is not None:
            tools.append(read_agent_ratios)
        if read_results is not None:
            tools.append(read_results)
        return Agent(
            config=self.agents_config['daniel_osei'], # type: ignore[index]
            verbose=True,
            tools=tools
        )
    
    @agent
    def richard(self) -> Agent:
        return Agent(
            config=self.agents_config['richard'], # type: ignore[index]
            verbose=True,
            tools=(
                read_earnings,
                read_balancesheet,
                read_valuation,
                read_ownership,
        )
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
    def decision_task(self) -> Task:
        return Task(
            config=self.tasks_config['decision_task'], # type: ignore[index]
            callback=clear_context_callback  # Clear context after this task
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TestAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            memory=False,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )