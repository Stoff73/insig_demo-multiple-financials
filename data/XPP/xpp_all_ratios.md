# XPP.L All Financial Ratios Analysis

Generated from financial data files
Data Sources: None

## **Current Market Data**

| Metric | Value | Source | Retrieved |
|--------|-------|--------|----------|
| **Share Price** | £9.15 | Yahoo Finance | 2025-08-26 16:32:21 |
| **Market Cap** | £180.0m | Yahoo Finance | 2025-08-26 16:32:21 |
| **Enterprise Value** | £180.0m | Calculated | - |
| **Shares Outstanding** | 0.0m | Financial Reports | - |

## **Valuation Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **P/E Ratio** | Market Cap / Net Income | 180.0 / 0.0 | N/A (loss) | FAIL |
| **P/B Ratio** | Market Cap / Equity | 180.0 / 0.0 | 0.00x | FAIL |
| **P/S Ratio** | Market Cap / Revenue | 180.0 / 0.0 | 0.00x | FAIL |
| **EV/EBITDA** | EV / LTM EBITDA | 180.0 / 0.0 | 0.0x | PASS |
| **EV/EBIT** | EV / EBIT | 180.0 / 0.0 | 0.0x | PASS |
| **EV/Revenue** | EV / Revenue | 180.0 / 0.0 | 0.00x | FAIL |
| **FCF Yield** | FCF / Market Cap | 0.0 / 180.0 | 0.0% | FAIL |

## **Profitability Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Gross Margin** | Gross Profit / Revenue | 0.0 / 0.0 | 0.0% | FAIL |
| **Operating Margin** | Operating Profit / Revenue | 0.0 / 0.0 | 0.0% | FAIL |
| **Net Margin** | Net Income / Revenue | 0.0 / 0.0 | 0.0% | MONITOR |
| **ROA** | Net Income / Assets | 0.0 / 0.0 | 0.0% | {'MONITOR'} |
| **ROE** | Net Income / Equity | 0.0 / 0.0 | 0.0% | MONITOR |
| **ROCE** | EBIT / Capital Employed | 0.0 / 0.0 | 0.0% | FAIL |

## **Efficiency Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Asset Turnover** | Revenue / Assets | 0.0 / 0.0 | 0.00x | FAIL |
| **Inventory Turnover** | COGS / Inventory | 0.0 / 0.0 | 0.0x | FAIL |
| **Receivables Turnover** | Revenue / Receivables | 0.0 / 0.0 | 0.0x | FAIL |
| **DSO** | 365 / Rec Turnover | 365 / 0.0 | 0 days | PASS |

## **Liquidity Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Current Ratio** | Current Assets / Current Liabilities | 0.0 / 0.0 | 0.00x | FAIL |
| **Quick Ratio** | (CA - Inventory) / CL | (0.0 - 0.0) / 0.0 | 0.00x | FAIL |
| **Cash Ratio** | Cash / Current Liabilities | 0.0 / 0.0 | 0.00x | FAIL |

## **Leverage Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Debt-to-Equity** | Total Debt / Equity | 0.0 / 0.0 | 0.00x | PASS |
| **Debt Ratio** | Total Debt / Assets | 0.0 / 0.0 | 0.00x | FAIL |
| **Interest Coverage** | EBIT / Interest | 0.0 / 0.0 | 0.0x | FAIL |
| **Net Debt/EBITDA** | Net Debt / LTM EBITDA | 0.0 / 0.0 | 0.00x | PASS |

## **Cash Flow Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Free Cash Flow Annual** | OCF - CapEx | Extracted | 0 | FAIL |
| **OCF Ratio** | Op Cash Flow / Current Liabilities | 0.0 / 0.0 | 0.00x | FAIL |
| **Cash Conversion** | OCF Annual / NI Annual | 0.0 / 0.0 | 0.0x | FAIL |

## **Earnings Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Accruals Ratio** | (NI Annual - OCF Annual) / Assets | (0.0 - 0.0) / 0.0 | 0.0% | PASS |
| **EBITDA to FCF** | FCF Annual / LTM EBITDA | 0.0 / 0.0 | 0.0% | FAIL |
| **Adj vs Stat Gap** | (Adj - Stat) / Stat | (0.0 - 0.0) / 0.0 | 0.0% | PASS |

## **Asset Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Goodwill/Assets** | Goodwill / Total Assets | 0.0 / 0.0 | 0.0% | PASS |
| **Capex/Depreciation** | Annualized Capex / LTM Depreciation | 0.0 / 0.0 | 0.00x | MONITOR |
| **Working Capital** | CA - CL | 0.0 - 0.0 | £0.0m | FAIL |
| **Tangible Book Value** | Equity - Intangibles | 0.0 - 0.0 | £0.0m | MONITOR |

## **All Variables Used in Calculations**

| Variable | Value | Unit | Source |
|----------|-------|------|--------|
| EBIT | 0.00 | £m | Extracted |
| EBIT Annual | 0.00 | £m | Annualized (x2) |
| Enterprise Value | 180.00 |  | Calculated |
| FCF Annual | 0.00 | £m | Annualized (x2) |
| Interest Annual | 0.00 | £m | Annualized (x2) |
| Net Income Annual | 0.00 | £m | Annualized (x2) |
| Operating Profit Annual | 0.00 | £m | Annualized (x2) |
| Revenue Annual | 0.00 | £m | Annualized (x2) |
| Tangible Book Value | 0.00 |  | Extracted |
| market_cap | 180.00 |  | Yahoo Finance |
| share_price | 9.15 | £ | Yahoo Finance |
| shares_outstanding | 19.70 | millions | Yahoo Finance |
