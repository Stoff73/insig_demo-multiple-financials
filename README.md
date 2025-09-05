# Financial Analysis System

A sophisticated financial analysis platform powered by CrewAI that combines multi-agent AI analysis with financial data to evaluate any company. The system uses ticker-based organization with company-specific configurations and data management.

## Code Quality

This codebase follows the **Google Python Style Guide** with:
- Comprehensive docstrings (Google format) for all modules, classes, and functions
- Type hints for all function parameters and returns
- Properly organized imports (standard library, third-party, local)
- Line length limits (80-100 characters)
- Specific exception handling (no bare except clauses)
- Consistent naming conventions (module_name, ClassName, function_name, CONSTANT_NAME)

## Features

- **Multi-Agent AI Analysis**: Three specialized AI agents (Financial Modeling, Forensic Accounting, Investment Decision-Making) collaborate to analyze financial documents
- **JSON-Based Data Input**: All financial and market data must be provided via JSON files in standardized format
- **Dynamic Company Support**: Analyze any company by entering ticker symbol - system automatically organizes data by company using provided JSON and MD files
- **Company-Specific Configuration**: Each company has its own ratio thresholds and analysis settings
- **Web Interface**: React-based dashboard with enhanced filtering and report organization
  - Dashboard shows filtered recent analyses and key reports only
  - Reports tab separates current analysis from archives
  - 5 key report types: Valuation, Ownership, Earnings Quality, Balance Sheet, Final Analysis
- **PDF to Markdown Conversion**: Automatic conversion of financial PDFs for AI processing
- **Financial Ratio Calculation**: 30+ financial metrics with company-specific PASS/MONITOR/FAIL thresholds
- **Ticker-Based Organization**: All data, outputs, and archives organized by company ticker
- **Task Management**: Persistent task tracking with automatic cleanup of stuck/timed-out analyses
- **Automatic Data Validation**: System checks for required files and prompts for uploads when missing

## Additional companies

- **Current company data**: This is in the data folder, so you can run an analysis by typing the company name and ticker
- **Adding a company**: To add a company:
  1. Create a folder in `data/{TICKER}/`
  2. Add the required `{ticker}.json` file with financial and market data
  3. Add any additional MD files for analysis
  4. Enter the company name and ticker in the frontend

## System Requirements

### Required Software
- **Python**: Version 3.10, 3.11, or 3.12 (Python 3.13+ is not supported and causes compatibility issues)
- **Node.js**: Version 16 or higher with npm
- **Git**: For cloning the repository
- **Operating System**: macOS, Linux, or Windows

### Code Quality Tools (Optional)
- **pylint**: For Python style checking against Google Style Guide
- **mypy**: For static type checking
- **black**: For code formatting (optional)

### Python Dependencies (automatically installed)
- FastAPI - Web framework for the backend API
- Uvicorn - ASGI server for FastAPI
- CrewAI - Multi-agent AI framework
- Pydantic - Data validation
- pdfplumber - PDF text extraction (switching to docling, not in this version)
- pandas & numpy - Data processing
- python-dotenv - Environment variable management

### Frontend Dependencies (automatically installed)
- React 18 - UI framework
- Material-UI - Component library
- Vite - Build tool and dev server
- Axios - HTTP client

## Quick Start

### Prerequisites

- Python 3.10-3.12 (3.13+ not supported - causes compatibility issues)
- Node.js 16+ and npm
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd insig_analyst_demo
```

2. **Create and activate Python virtual environment**
```bash
# Create virtual environment if it doesn't exist
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

3. **Install Python dependencies**
```bash
# Install uv package manager (recommended)
pip install uv

# Install all Python dependencies from requirements.txt
uv pip install -r requirements.txt

# Install CrewAI CLI tools
crewai install
```

4. **Set up Frontend**
```bash
cd frontend
npm install
cd ..
```

5. **Configure environment variables**
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-api-key-here" > .env
echo "MODEL=gpt-4" >> .env  # Optional: specify model (defaults to gpt-4)
```

6. **Verify installation**
```bash
# Check Python dependencies
python -c "import fastapi, crewai, yfinance; print('Python dependencies OK')"

# Check Node.js setup
cd frontend && npm list react && cd ..
```

7. **Optional: Install code quality tools**
```bash
# Install linting and type checking tools
pip install pylint mypy black

# Run style checks
pylint src/ backend/ --disable=C0114,C0115,C0116  # Disable docstring warnings for initial check
mypy src/ backend/ --ignore-missing-imports
```

## Running the Application

### Full Application (Recommended)

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Start both backend and frontend
python run_app.py
# Or directly with venv Python:
.venv/bin/python run_app.py
```

The application will start:
- Backend API at http://localhost:8000
- Frontend at http://localhost:5173 (Vite shows port 3000 but actually uses 5173)
- API Docs at http://localhost:8000/docs

Open your browser and navigate to http://localhost:3000 to access the web interface.

### Manual Startup

**Terminal 1 - Backend:**
```bash
# Start the API server (without --reload to avoid subprocess issues)
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Direct CrewAI Execution

```bash
# Run crew analysis directly (without web interface)
crewai run

# Test with specific parameters
insig_analyst_demo test --n_iterations 3 --eval_llm gpt-4
```

## Data Flow

The system follows a structured data flow to ensure accurate and up-to-date financial analysis:

1. **User Input**: Company name and ticker symbol entered in the web interface
2. **Data Directory Setup**: Creates `data/{TICKER}/` folder if it doesn't exist
3. **Financial Data Processing**:
   - Requires `data/{TICKER}/{ticker}.json` file with financial and market data
   - JSON must contain market_data, income_statement, balance_sheet, and cash_flow sections
   - Handles GBp (pence) to GBP (pounds) conversion for UK stocks automatically
4. **Ratio Calculation**:
   - `FinancialRatioCalculator` reads ONLY from the JSON file
   - Generates `{ticker}_all_ratios.md` with all calculated ratios
   - Creates `{ticker}_agent_ratios.md` with enabled ratios for AI agents
5. **Validation**:
   - Checks that >80% of ratios have values (warns if data is incomplete)
   - Verifies required financial documents exist in the ticker folder
6. **AI Analysis**:
   - CrewAI agents analyze documents and ratios
   - Generate 5 key reports:
     - `{ticker}_valuation.md` - Valuation analysis
     - `{ticker}_ownership.md` - Ownership structure
     - `{ticker}_earning_quality.md` - Earnings quality
     - `{ticker}_balancesheet_durability.md` - Balance sheet strength
     - `{ticker}_final_analysis.md` - Investment decision
7. **Archiving**: Previous outputs automatically archived to `archive/{TICKER}/YYYYMMDD_HHMMSS/`
8. **Task Persistence**: All analysis tasks stored in `backend/tasks.json` for history tracking

### Important Architecture Notes

- **All financial data must be provided via JSON files** - no external data fetching in current version
- **`ratio_calc.py` works exclusively with local JSON files** - maintains data isolation
- JSON files must include comprehensive financial data (market data, statements, cash flows)
- All data is stored in ticker-specific folders organized by company ticker
- Task history persisted in `backend/tasks.json` for tracking and recovery
- Automatic cleanup of stuck tasks (>30 minutes in running state)

## Project Structure

```
insig_analyst_demo/
├── run_app.py                 # Application launcher (handles both services)
├── backend/                    # FastAPI backend (Google Style Guide compliant)
│   ├── main.py                # API server with comprehensive docstrings & type hints
│   ├── pdf_converter_best.py  # PDF to Markdown converter
│   ├── rules_manager.py       # Analysis rules management
│   ├── ratio_config_manager.py # Company-specific ratio configuration
│   └── core/                  # Core utilities with full documentation
│       ├── task_runner.py     # Task management with type hints
│       ├── config.py          # Configuration constants
│       └── archive.py         # Archive management
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main application
│   │   ├── pages/
│   │   │   ├── Analysis.jsx  # Company analysis (ticker input)
│   │   │   └── RatiosConfiguration.jsx # Company ratio config
│   │   └── components/        # UI components
│   └── package.json
├── src/insig_analyst_demo/     # CrewAI implementation (Google Style Guide)
│   ├── crew.py                # Dynamic company crew with type hints
│   ├── ratio_calc.py          # Financial ratio calculator (30+ metrics)
│   ├── main.py                # CLI entry point with proper main guard
│   └── config/
│       ├── agents.yaml        # Agent configurations
│       └── tasks.yaml         # Task definitions
├── data/                      # Input data directory
│   ├── {TICKER}/              # Company-specific folders
│   │   ├── *.md/*.pdf        # Financial documents
│   │   ├── {ticker}.json     # Comprehensive financial data from yfinance
│   │   ├── {ticker}_ratio_rules.md    # Company ratio thresholds
│   │   ├── {ticker}_all_ratios.md     # All calculated ratios
│   │   └── {ticker}_agent_ratios.md   # Agent-accessible ratios
│   ├── {ticker}_financial_ratios.md  # Generated ratios (global)
│   └── default_ratio_rules.md # Template for new companies
├── output/                    # Analysis results
│   └── {TICKER}/              # Company-specific outputs
│       ├── {ticker}_valuation.md
│       ├── {ticker}_ownership.md
│       ├── {ticker}_earning_quality.md
│       ├── {ticker}_balancesheet_durability.md
│       └── {ticker}_final_analysis.md
├── archive/                   # Historical analyses
│   └── {TICKER}/              # Company-specific archives
│       └── YYYYMMDD_HHMMSS/  # Timestamped folders with all 5 reports
├── backend/
│   └── tasks.json            # Persistent task history
└── config/
    └── analysis_rules.yaml    # Global analysis thresholds

```

## Using the Web Interface

### Running an Analysis

1. **Navigate to Run Analysis**
2. **Enter Company Information**:
   - Company Name (e.g., "Insig AI", "Apple Inc.")
   - Ticker Symbol (e.g., "XPP", "AAPL")
3. **System Validation**:
   - Checks if `data/{TICKER}/` folder exists
   - Validates required files are present
   - Creates folder and prompts for uploads if missing
4. **Start Analysis** - The system will:
   - Use company-specific data from `data/{TICKER}/`
   - Apply company-specific ratio thresholds
   - Generate outputs in `output/{TICKER}/`
   - Archive previous results to `archive/{TICKER}/`

### Configuring Ratios

1. **Navigate to Ratio Configuration**
2. **Enter Company Details** when prompted:
   - Company Name and Ticker Symbol
   - System creates `data/{TICKER}/` if needed
   - Copies default ratio rules as starting template
3. **Configure Thresholds**:
   - Enable/disable specific ratios
   - Set PASS/MONITOR/FAIL thresholds
   - Changes saved to `data/{TICKER}/ratio_rules.md`

### Managing Companies

Each company you analyze will have:
- **Data Folder**: `data/{TICKER}/` containing:
  - **`{ticker}.json`** - REQUIRED: Financial and market data
  - Financial documents (PDFs, Markdown files)
  - `ratio_rules.md` - Company-specific ratio configuration
  - `agent-ratios.md` - Ratios accessible to AI agents
- **Output Folder**: `output/{TICKER}/` with analysis results
- **Archive Folder**: `archive/{TICKER}/` with historical analyses

### JSON Data Format

The `{ticker}.json` file must follow this structure:
```json
{
  "ticker": "XPP.L",
  "timestamp": "2025-08-29T11:10:35.734765",
  "source": "Financial Data Provider",
  "data": {
    "market_data": {
      "market_cap": 262925888,
      "share_price": 920.0,
      "shares_outstanding": 27932200,
      "currency": "GBP",
      "company_name": "XP Power"
    },
    "2024": {
      "income_statement": {
        "revenue": 247300000.0,
        "gross_profit": 97000000.0,
        "operating_profit": 3600000.0,
        "net_income": -9600000.0,
        "ebitda": 15000000.0
      },
      "balance_sheet": {
        "total_assets": 416200000.0,
        "current_assets": 160700000.0,
        "total_liabilities": 270300000.0,
        "total_equity": 145900000.0,
        "total_debt": 163200000.0
      },
      "cash_flow": {
        "operating_cash_flow": 55400000.0,
        "capital_expenditure": -20100000.0,
        "free_cash_flow": 35300000.0
      }
    }
  }
}
```

## API Documentation

### Core Endpoints

- `POST /api/analysis/start` - Start company analysis (requires company name and ticker)
- `GET /api/analysis/status/{task_id}` - Check analysis progress
- `GET /api/analysis/list` - List all analysis tasks with status
- `POST /api/analysis/cleanup` - Clean up stuck tasks (>30 min in running state)
- `DELETE /api/analysis/clear` - Clear all task history
- `DELETE /api/analysis/stop/{task_id}` - Cancel a running analysis
- `GET /api/files/output` - List analysis results
- `POST /api/files/upload` - Upload documents to company folder
- `POST /api/files/convert/{filename}` - Convert PDF to Markdown

### Configuration

- `GET/PUT /api/config/agents` - Manage agent configurations
- `GET/PUT /api/config/tasks` - Manage task configurations
- `GET/POST/PUT/DELETE /api/rules` - Manage analysis rules
- `GET /api/ratios/{ticker}` - Get company ratio configuration
- `PUT /api/ratios/{ticker}` - Update company ratio configuration

## Configuration Files

### Agent Configuration (`src/insig_analyst_demo/config/agents.yaml`)
Defines the three AI agents:
- **victoria_clarke**: Financial Modeling & Valuation Expert
- **daniel_osei**: Forensic Accounting & Earnings Quality Specialist
- **richard**: Investment Decision Maker

### Task Configuration (`src/insig_analyst_demo/config/tasks.yaml`)
Defines the five-step analysis pipeline that generates 5 key reports:
1. **Valuation Analysis** → `{ticker}_valuation.md`
2. **Ownership Review** → `{ticker}_ownership.md`
3. **Earnings Assessment** → `{ticker}_earning_quality.md`
4. **Balance Sheet Check** → `{ticker}_balancesheet_durability.md`
5. **Investment Decision** → `{ticker}_final_analysis.md`

### Ratio Rules (`data/{TICKER}/ratio_rules.md`)
Company-specific ratio configurations:
- P/E Ratio, EV/EBITDA, FCF Yield, etc.
- Each ratio can be enabled/disabled per company
- Company-specific PASS/MONITOR/FAIL thresholds
- Template: `data/default_ratio_rules.md` for new companies

## Financial Thresholds

Default thresholds (configurable via API):
- **P/E Ratio**: <10x = PASS, 10-15x = MONITOR, >15x = FAIL
- **EV/EBITDA**: <5.0x = PASS, 5.0-7.5x = MONITOR, >7.5x = FAIL
- **Net Debt/EBITDA**: <2.5x = PASS, 2.5-3.5x = MONITOR, >3.5x = FAIL
- **Interest Coverage**: >4.0x = PASS, 2.0-4.0x = MONITOR, <2.0x = FAIL
- **FCF Yield**: >10% = PASS, 6-10% = MONITOR, <6% = FAIL

## Testing

```bash
# Run crew analysis directly
crewai run

# Test ratio calculation with provided JSON
python -c "from src.insig_analyst_demo.crew import InsigAnalystDemo; crew = InsigAnalystDemo(); crew.calculate_financial_ratios({'ticker': 'XPP.L'})"
```

## Troubleshooting

### Common Issues

1. **FileNotFoundError: {ticker}.json not found**
   - Ensure the JSON file is placed in `data/{TICKER}/` folder
   - File must be named exactly as `{ticker}.json` (e.g., `xpp.json` for XPP ticker)
   - JSON must contain required sections (market_data, income_statement, etc.)
   - Currency should be specified (GBP for UK stocks, USD for US stocks)

2. **Port already in use**
   ```bash
   # Kill processes using the ports
   lsof -ti:8000 | xargs kill -9
   lsof -ti:5173 | xargs kill -9
   pkill -f uvicorn
   pkill -f "node|npm|vite"
   # Or use different ports in the configuration
   ```

3. **Application shuts down immediately after starting**
   - **Cause**: The `--reload` flag with uvicorn creates a subprocess that exits, causing the script to think the backend stopped
   - **Solution**: The `run_app.py` script has been updated to:
     - Run uvicorn without the `--reload` flag
     - Wait properly for the backend to start (20 second timeout)
     - Monitor both backend and frontend processes continuously
     - Handle shutdown gracefully with signal handlers
   - **Note**: Pydantic deprecation warnings from CrewAI are normal and safe to ignore

4. **API key issues**
   - Verify `.env` file exists in project root
   - Ensure it contains valid `OPENAI_API_KEY`
   - Check there are no extra spaces or quotes in the key

5. **Module not found errors**
   ```bash
   # Always ensure virtual environment is activated
   source .venv/bin/activate  # On macOS/Linux
   # Reinstall dependencies
   uv pip install -r requirements.txt
   ```

6. **Rollup/Vite build errors on macOS**
   If you see `Cannot find module @rollup/rollup-darwin-x64` or code signature issues:
   ```bash
   # Fix by removing and reinstalling frontend dependencies
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   cd ..
   ```

7. **Missing or incomplete JSON data**
   - Ensure JSON file contains all required sections:
     - `data.market_data` (share_price, market_cap, etc.)
     - `data.{year}.income_statement`
     - `data.{year}.balance_sheet`
     - `data.{year}.cash_flow`
   - Check that numeric values are properly formatted

8. **Stuck or "Running" Tasks**
   If tasks show as perpetually "running" in the dashboard:
   ```bash
   # Clean up stuck tasks via API
   curl -X POST http://localhost:8000/api/analysis/cleanup
   
   # Or clear all task history (use with caution)
   curl -X DELETE http://localhost:8000/api/analysis/clear
   ```

9. **Pydantic deprecation warnings**
   These warnings from the CrewAI library are safe to ignore:
   ```
   PydanticDeprecatedSince20: Using extra keyword arguments...
   PydanticDeprecatedSince20: Support for class-based `config` is deprecated...
   ```
   They indicate future changes in Pydantic v3 but don't affect functionality.

10. **Frontend shows wrong port**
    - Vite displays "Local: http://localhost:3000/" but actually runs on port 5173
    - Access the frontend at: http://localhost:5173
    - The backend API is at: http://localhost:8000

### Debug Mode

```bash
# Run backend with debug logging (without --reload)
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --log-level debug

# Check task status
curl http://localhost:8000/api/analysis/status/{task_id}

# View all tasks
curl http://localhost:8000/api/analysis/list

# Debug system state
curl http://localhost:8000/api/analysis/debug
```

## Development

### Code Style Guidelines

All Python code follows the Google Python Style Guide:

```python
def calculate_ratio(numerator: float, denominator: float) -> float:
    """Calculate a financial ratio.
    
    Args:
        numerator: The top value in the ratio.
        denominator: The bottom value in the ratio.
    
    Returns:
        The calculated ratio value.
    
    Raises:
        ValueError: If denominator is zero.
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    return numerator / denominator
```

### Adding New Financial Ratios

1. Edit `backend/ratio_config_manager.py` to add ratio definition
2. Update `src/insig_analyst_demo/ratio_calc.py` to implement calculation
3. Add to `data/ratio_rules.md` to enable for agents
4. Follow Google Style Guide for all new code

### Customizing AI Agents

1. Edit `src/insig_analyst_demo/config/agents.yaml` for agent personalities
2. Modify `src/insig_analyst_demo/config/tasks.yaml` for task definitions
3. Update `src/insig_analyst_demo/crew.py` for custom logic
4. Ensure all Python changes include proper docstrings and type hints

### Running Code Quality Checks

```bash
# Check style compliance
pylint src/ backend/

# Check type hints
mypy src/ backend/ --ignore-missing-imports

# Format code (optional)
black src/ backend/ --line-length 80
```

## Contributing

When contributing to this project:
1. Follow the Google Python Style Guide
2. Add comprehensive docstrings to all new functions/classes
3. Use type hints for all parameters and returns
4. Keep line length under 80-100 characters
5. Test that all existing functionality still works

## License

[Your License Here]

## Support

For issues or questions:
- c.jones@csjones.co
