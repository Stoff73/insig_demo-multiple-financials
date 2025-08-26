# Multi-Company Analysis Feature

## Overview

The XP Power Analysis System now supports analyzing multiple companies simultaneously. You can analyze up to 10 companies in a single batch, with each company's data and results organized in separate folders.

## Key Features

- **Batch Analysis**: Analyze up to 10 companies in one run
- **Company-Specific Organization**: Each company has its own data, output, and archive folders
- **Dynamic File Tools**: Automatic detection and loading of company-specific data files
- **Parallel or Sequential Processing**: Choose between faster parallel analysis or resource-efficient sequential processing
- **Individual Company Reports**: View and manage reports for each company separately
- **Comprehensive UI**: New multi-company analysis interface with progress tracking

## Folder Structure

```
xp_power_demo/
├── data/
│   └── companies/
│       ├── XPP/           # XP Power Limited data
│       │   ├── xp-power.md
│       │   ├── prime-metrics.md
│       │   └── ...
│       ├── AAPL/          # Apple Inc. data
│       │   ├── aapl-financial.md
│       │   └── ...
│       └── MSFT/          # Microsoft data
│           └── ...
├── output/
│   └── companies/
│       ├── XPP/           # XP Power analysis results
│       │   ├── primary-ratios.md
│       │   ├── ownership.md
│       │   └── ...
│       └── ...
└── archive/
    └── companies/
        ├── XPP/           # XP Power archived analyses
        │   └── 20250819_120000/
        └── ...
```

## Usage

### Running the Multi-Company Application

```bash
# Start the multi-company enabled application
python run_app_multi.py

# Or use the original single-company version
python run_app.py
```

### Web Interface

1. **Navigate to Multi-Company Analysis**: Click "Multi-Company" in the sidebar
2. **Add Companies**: 
   - Enter ticker symbol (e.g., XPP, AAPL, MSFT)
   - Enter company name (e.g., XP Power Limited)
   - Click "Add Company" to add more (up to 10)
3. **Configure Options**:
   - Set analysis year
   - Choose parallel processing (faster but uses more resources)
4. **Start Analysis**: Click "Start Analysis" to begin
5. **Monitor Progress**: View real-time status for each company
6. **View Results**: Click "View Results" for any completed company

### API Endpoints

#### Start Multi-Company Analysis
```http
POST /api/analysis/start-multi
Content-Type: application/json

{
  "companies": [
    {"ticker": "XPP", "name": "XP Power Limited"},
    {"ticker": "AAPL", "name": "Apple Inc."},
    {"ticker": "MSFT", "name": "Microsoft Corporation"}
  ],
  "year": "2024",
  "parallel": false
}
```

#### Upload Company-Specific Files
```http
POST /api/files/upload/{ticker}
```

#### Get Company Output Files
```http
GET /api/files/output/company/{ticker}
```

#### List All Companies
```http
GET /api/companies/list
```

### Python API

```python
from xp_power_demo.multi_company_crew import MultiCompanyXpPowerDemo

# Initialize crew for a specific company
crew = MultiCompanyXpPowerDemo(
    company_ticker="XPP",
    company_name="XP Power Limited"
)

# Run analysis
result = crew.kickoff()
```

## File Naming Conventions

For the system to automatically detect and categorize files, use these naming patterns:

- **Financial Data**: `*financial*.md`, `*financials*.md`, `{ticker}*.md`
- **Metrics**: `*metrics*.md`, `*prime-metrics*.md`, `*ratios*.md`
- **Ownership**: `*ownership*.md`, `*insider*.md`, `*shareholders*.md`
- **Screening**: `*screening*.md`, `*initial*.md`, `*analysis*.md`
- **Balance Sheet**: `*balance*.md`, `*balance-sheet*.md`
- **Income**: `*income*.md`, `*earnings*.md`, `*revenue*.md`

## Testing

Run the test script to verify the multi-company setup:

```bash
python test_multi_company.py
```

This will:
1. Set up test data for multiple companies
2. Verify the crew initialization for each company
3. Check the folder structure
4. Confirm file tools are properly configured

## Migration from Single Company

The system maintains backward compatibility. Existing single-company analyses will continue to work:

- Original endpoints remain available
- Single company analysis UI is still accessible
- Existing data in `/data` and `/output` folders is preserved

## Performance Considerations

- **Sequential Processing**: Safer for system resources, processes one company at a time
- **Parallel Processing**: Faster but uses more CPU/memory, processes up to 3 companies simultaneously
- **File Management**: Each company's files are isolated, preventing cross-contamination
- **Memory Management**: Context is cleared between tasks to prevent memory issues

## Troubleshooting

### Company Not Found
- Ensure the ticker is properly sanitized (alphanumeric only)
- Check that data files exist in `/data/companies/{TICKER}/`

### Analysis Fails
- Verify required data files are present for the company
- Check that file naming follows conventions
- Review logs in the task status for specific errors

### Performance Issues
- Use sequential processing instead of parallel
- Reduce the number of companies per batch
- Ensure sufficient system resources (RAM, CPU)

## Future Enhancements

Potential improvements for the multi-company feature:

1. **Comparative Analysis**: Compare metrics across multiple companies
2. **Industry Benchmarking**: Automatic peer comparison
3. **Portfolio View**: Aggregate view of all analyzed companies
4. **Bulk File Upload**: Upload files for multiple companies at once
5. **Export to Excel**: Export multi-company results to a single spreadsheet
6. **Scheduled Analysis**: Automatic periodic re-analysis of companies