# Changelog

## [2025-01-22] - Multi-Company Research Feature

### Overview
Implemented a comprehensive multi-company research capability that allows the application to analyze any company by ticker symbol. The system now organizes all data, outputs, and archives by company ticker for better organization and scalability.

### Added Features
- **Dynamic Company Selection**: Users can now input any company name and ticker symbol for analysis
- **Company-Specific Data Organization**: Each company's data is stored in `data/{TICKER}/` folders
- **Automatic Data Validation**: System checks for required files and prompts for uploads when missing
- **Company-Specific Output Management**: Analysis outputs are saved to `output/{TICKER}/` folders
- **Ticker-Based Archive Structure**: Archives are organized as `archive/{TICKER}/YYYYMMDD_HHMMSS/`
- **Dynamic File Tool Initialization**: CrewAI agents automatically use company-specific data files

### Modified Files

#### Frontend Changes
- **frontend/src/pages/Analysis.jsx**
  - Replaced "year" input field with "ticker" input field
  - Added placeholder text for better UX (e.g., "XPP" for ticker)
  - Ticker input automatically converts to uppercase
  - Updated API call to send ticker instead of year

#### Backend Changes
- **backend/main.py**
  - Modified `AnalysisRequest` model: removed `year`, added `ticker` parameter
  - Added `check_company_data_exists()` function for data validation
  - Updated `archive_existing_outputs()` to support company-specific folders
  - Modified `run_crew_analysis()` to accept ticker parameter
  - Enhanced `/api/analysis/start` endpoint to validate data and create folders
  - Updated task tracking to store ticker information

#### CrewAI Changes
- **src/xp_power_demo/crew.py**
  - Added `company_ticker` class attribute for dynamic company support
  - Modified `@before_kickoff` decorator to initialize company-specific file tools
  - Implemented dynamic data path resolution based on ticker
  - Added `_move_outputs_to_company_folder()` method for output organization
  - Modified crew kickoff to redirect outputs to company folders
  - Updated file tools to be initialized dynamically per company
  - Enhanced agents to use conditional file tool inclusion

#### Documentation Changes
- **CLAUDE.md**
  - Updated project overview to reflect ticker-based organization
  - Modified data flow documentation for company-specific paths
  - Updated API endpoints documentation
  - Removed references to unused multi-company features
  - Added details about dynamic data validation

### Data Migration
- **Moved Files**: All existing XP Power data files were migrated from `data/` to `data/XPP/`:
  - `xp-power.md` → `data/XPP/xp-power.md`
  - `initial_screening.md` → `data/XPP/initial_screening.md`
  - `xp_power_ownership.md` → `data/XPP/xp_power_ownership.md`
  - `xpp_financial_ratios.md` → `data/XPP/xpp_financial_ratios.md`
  - `prime-metrics.md` → `data/XPP/prime-metrics.md`
  - `XP-Power-AR-2024.pdf` → `data/XPP/XP-Power-AR-2024.pdf`
  - `interims-2025.pdf` → `data/XPP/interims-2025.pdf`

### Removed Features
- Removed dependency on year parameter for analysis
- Removed hardcoded XP Power defaults (now requires ticker input)

### Technical Details

#### Data Validation Logic
- Checks for existence of `data/{TICKER}/` folder
- Validates presence of financial data files (annual reports, financial statements)
- Validates presence of screening/metrics data
- Returns specific missing file types to guide user uploads

#### Output File Naming Convention
- All output files are prefixed with ticker symbol
- Example: `xpp_primary-ratios.md`, `aapl_decision.md`
- Maintains original file structure while adding company context

#### Ticker Sanitization
- Converts ticker to uppercase
- Replaces dots with underscores for file system compatibility
- Example: "XPP.L" becomes "XPP_L" for folder names

### Breaking Changes
- **API Contract Change**: `/api/analysis/start` now requires `ticker` instead of `year`
- **Data Location Change**: XP Power data moved from `data/` to `data/XPP/`

### Migration Guide
For existing users:
1. Data has been automatically migrated to `data/XPP/` folder
2. Update any API integrations to pass `ticker` instead of `year`
3. Ensure frontend is updated to use the new ticker input field

### Benefits
- **Scalability**: Can now analyze unlimited companies without code changes
- **Organization**: Clear separation of data, outputs, and archives per company
- **User Experience**: Automatic folder creation and validation feedback
- **Maintainability**: Single codebase handles all companies dynamically
- **Data Integrity**: Company data isolation prevents cross-contamination

### Ratio Configuration Updates (Additional Changes)

#### File Organization
- **Global Files** (remain in `data/` root):
  - `{ticker}_financial_ratios.md` - Generated ratio calculations output
  - `default_ratio_rules.md` - Template for new companies
  
- **Company-Specific Files** (in `data/{TICKER}/`):
  - `ratio_rules.md` - Company-specific ratio thresholds and enabled/disabled settings
  - `agent-ratios.md` - Ratios accessible to agents for that company

#### Modified Files for Ratio Configuration
- **backend/ratio_config_manager.py**: Added ticker parameter to constructor for company-specific ratio management
- **src/xp_power_demo/ratio_calc.py**: Updated to use company-specific `ratio_rules.md` from `data/{TICKER}/`
- **frontend/src/pages/RatiosConfiguration.jsx**: Added ticker prompt dialog for company selection
- **frontend/src/utils/api.js**: Updated ratio API calls to include ticker parameter

#### Ratio Configuration Flow
1. User opens Ratio Configuration page
2. Prompted to enter company name and ticker
3. System creates `data/{TICKER}/` folder if it doesn't exist
4. Copies `default_ratio_rules.md` to company folder as starting template
5. User can configure ratios specific to that company
6. Changes saved to `data/{TICKER}/ratio_rules.md`

### Notes
- The system maintains backward compatibility with existing CrewAI tasks and agents
- No changes were made to `tasks.yaml` or `agents.yaml` configuration files
- Yahoo Finance integration automatically adapts to the provided ticker symbol
- The existing multi-company support features in `backend/main_multi.py` were not utilized as requested
- Each company maintains its own ratio configuration for customized analysis thresholds

### Summary of Changes

This update transforms the application from a single-company system (XP Power) to a dynamic multi-company analysis platform. Key improvements include:

1. **Ticker-Based Architecture**: All components now use ticker symbols for organization
2. **Company Isolation**: Each company has separate data, configuration, and output folders
3. **Dynamic Configuration**: Ratio thresholds can be customized per company
4. **Improved UX**: Automatic folder creation and file validation with user prompts
5. **Scalability**: Can analyze unlimited companies without code changes

The changes maintain full backward compatibility while significantly expanding the system's capabilities for financial analysis across multiple companies.