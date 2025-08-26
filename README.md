# Financial Analysis System

A financial analysis platform powered by CrewAI that combines multi-agent AI analysis with real-time market data to evaluate any company. The system uses ticker-based organization for analyzing multiple companies with company-specific configurations and data management.

## Features

- **Multi-Agent AI Analysis**: Three specialized AI agents (Financial Modeling, Forensic Accounting, Investment Decision-Making) collaborate to analyze financial documents
- **Real-Time Market Data**: Integration with Yahoo Finance API for live share prices and market capitalization
- **Dynamic Company Support**: Analyze any company by entering ticker symbol - system automatically organizes data by company if this is provided to the system, currently in MD format
- **Company-Specific Configuration**: Each company has its own ratio thresholds and analysis settings
- **Web Interface**: React-based dashboard for managing analyses, viewing reports, and configuring settings
- **PDF to Markdown Conversion**: Automatic conversion of financial PDFs for AI processing - this will use docling in the future, this is blunt at the moment, but works
- **Financial Ratio Calculation**: 30+ financial metrics with company-specific PASS/MONITOR/FAIL thresholds
- **Ticker-Based Organization**: All data, outputs, and archives organized by company ticker
- **Automatic Data Validation**: System checks for required files and prompts for uploads when missing, not for everything just empty folders

## Additional companies

- **Current company data**: This is in the data folder, so you can run an analysis by typing the company name and ticker
- **Adding a company**: To add a company, add a folder and the md files to the data folder, and type the company nae and ticker in the frontend.

## System Requirements

### Required Software
- **Python**: Version 3.10, 3.11, 3.12, or 3.13 (Python 3.14 is not supported by CrewAI)
- **Node.js**: Version 16 or higher with npm
- **Git**: For cloning the repository
- **Operating System**: macOS, Linux, or Windows

### Python Dependencies (automatically installed)
- FastAPI - Web framework for the backend API
- Uvicorn - ASGI server for FastAPI
- CrewAI - Multi-agent AI framework
- Pydantic - Data validation
- yfinance - Yahoo Finance market data
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

- Python 3.10-3.13 (3.14 not supported by CrewAI)
- Node.js 16+ and npm
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd xp_power_demo-multiple-financials
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

## Running the Application

### Full Application (Recommended)

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Start both backend and frontend
python run_app.py
```

The application will start:
- Backend API at http://localhost:8000
- Frontend at http://localhost:3000

Open your browser and navigate to http://localhost:3000 to access the web interface.

### Manual Startup

**Terminal 1 - Backend:**
```bash
# Start the API server
python -m uvicorn backend.main:app --reload --port 8000
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
xp_power_demo test --n_iterations 3 --eval_llm gpt-4
```

## Project Structure

```
xp_power_demo/
├── backend/                    # FastAPI backend
│   ├── main.py                # API server with ticker support
│   ├── pdf_converter_best.py  # PDF to Markdown converter
│   ├── rules_manager.py       # Analysis rules management
│   └── ratio_config_manager.py # Company-specific ratio configuration
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main application
│   │   ├── pages/
│   │   │   ├── Analysis.jsx  # Company analysis (ticker input)
│   │   │   └── RatiosConfiguration.jsx # Company ratio config
│   │   └── components/        # UI components
│   └── package.json
├── src/xp_power_demo/         # CrewAI implementation
│   ├── crew.py                # Dynamic company crew
│   ├── ratio_calc.py          # Financial ratio calculator
│   ├── extract_financials.py  # Data extraction
│   └── config/
│       ├── agents.yaml        # Agent configurations
│       └── tasks.yaml         # Task definitions
├── data/                      # Input data directory
│   ├── {TICKER}/              # Company-specific folders
│   │   ├── *.md/*.pdf        # Financial documents
│   │   ├── ratio_rules.md    # Company ratio thresholds
│   │   └── agent-ratios.md   # Agent-accessible ratios
│   ├── {ticker}_financial_ratios.md  # Generated ratios (global)
│   └── default_ratio_rules.md # Template for new companies
├── output/                    # Analysis results
│   └── {TICKER}/              # Company-specific outputs
│       └── {ticker}_*.md      # Prefixed output files
├── archive/                   # Historical analyses
│   └── {TICKER}/              # Company-specific archives
│       └── YYYYMMDD_HHMMSS/  # Timestamped folders
└── config/
    └── analysis_rules.yaml    # Global analysis thresholds

```

## Using the Web Interface

### Running an Analysis

1. **Navigate to Run Analysis**
2. **Enter Company Information**:
   - Company Name (e.g., "XP Power", "Apple Inc.")
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
  - Financial documents (PDFs, Markdown files)
  - `ratio_rules.md` - Company-specific ratio configuration
  - `agent-ratios.md` - Ratios accessible to AI agents
- **Output Folder**: `output/{TICKER}/` with analysis results
- **Archive Folder**: `archive/{TICKER}/` with historical analyses

## API Documentation

### Core Endpoints

- `POST /api/analysis/start` - Start company analysis (requires ticker)
- `GET /api/analysis/status/{task_id}` - Check analysis progress
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

### Agent Configuration (`src/xp_power_demo/config/agents.yaml`)
Defines the three AI agents:
- **victoria_clarke**: Financial Modeling & Valuation Expert
- **daniel_osei**: Forensic Accounting & Earnings Quality Specialist
- **richard**: Investment Decision Maker

### Task Configuration (`src/xp_power_demo/config/tasks.yaml`)
Defines the five-step analysis pipeline:
1. Primary ratios analysis
2. Ownership structure review
3. Earnings quality assessment
4. Balance sheet durability check
5. Investment decision

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
# Test multi-company setup
python test_multi_company.py

# Test Yahoo Finance integration
python -c "from src.xp_power_demo.crew import XpPowerDemo; crew = XpPowerDemo(); crew.calculate_financial_ratios({'ticker': 'XPP.L'})"
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'yfinance'**
   ```bash
   # Make sure all dependencies are installed
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

2. **Port already in use**
   ```bash
   # Kill processes using the ports
   pkill -f "python.*run_app"
   pkill -f "node|npm|vite"
   # Or use different ports in the configuration
   ```

3. **API key issues**
   - Verify `.env` file exists in project root
   - Ensure it contains valid `OPENAI_API_KEY`
   - Check there are no extra spaces or quotes in the key

4. **Module not found errors**
   ```bash
   # Always ensure virtual environment is activated
   source .venv/bin/activate  # On macOS/Linux
   # Reinstall dependencies
   uv pip install -r requirements.txt
   ```

5. **Rollup/Vite build errors on macOS**
   If you see `Cannot find module @rollup/rollup-darwin-x64` or code signature issues:
   ```bash
   # Fix by removing and reinstalling frontend dependencies
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   cd ..
   ```

6. **Yahoo Finance connection errors**
   - Check internet connection
   - Verify ticker symbol format (e.g., "XPP.L" for London Stock Exchange)
   - API might be temporarily unavailable, system will use fallback estimates

7. **Pydantic deprecation warnings**
   These warnings from the CrewAI library are safe to ignore:
   ```
   PydanticDeprecatedSince20: Using extra keyword arguments...
   ```
   They indicate future changes in Pydantic v3 but don't affect functionality.

### Debug Mode

```bash
# Run backend with debug logging
uvicorn backend.main:app --reload --log-level debug

# Check task status
curl http://localhost:8000/api/analysis/status/{task_id}
```

## Development

### Adding New Financial Ratios

1. Edit `backend/ratio_config_manager.py` to add ratio definition
2. Update `src/xp_power_demo/ratio_calc.py` to implement calculation
3. Add to `data/ratio_rules.md` to enable for agents

### Customizing AI Agents

1. Edit `src/xp_power_demo/config/agents.yaml` for agent personalities
2. Modify `src/xp_power_demo/config/tasks.yaml` for task definitions
3. Update `src/xp_power_demo/crew.py` for custom logic

## License

[Your License Here]

## Support

For issues or questions:
- c.jones@csjones.co
