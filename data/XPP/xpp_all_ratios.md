# XPP.L All Financial Ratios Analysis

Generated from financial data files
Data Sources: XPP.json

## **Current Market Data**

| Metric | Value | Source | Retrieved |
|--------|-------|--------|----------|
| **Share Price** | £9.20 | Yahoo Finance | 2025-09-05 13:41:19 |
| **Market Cap** | £262.9m | Yahoo Finance | 2025-09-05 13:41:19 |
| **Enterprise Value** | £412.2m | Calculated | - |
| **Shares Outstanding** | 0.0m | Financial Reports | - |

## **Valuation Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **P/E Ratio** | Market Cap / Net Income | 262.9 / -19.2 | N/A (loss) | FAIL |
| **P/B Ratio** | Market Cap / Equity | 262.9 / 145.9 | 1.80x | DISABLED |
| **P/S Ratio** | Market Cap / Revenue | 262.9 / 494.6 | 0.53x | DISABLED |
| **EV/EBITDA** | EV / LTM EBITDA | 412.2 / 6.1 | 67.6x | FAIL |
| **EV/EBIT** | EV / EBIT | 412.2 / 6.1 | 67.6x | FAIL |
| **EV/Revenue** | EV / Revenue | 412.2 / 494.6 | 0.83x | FAIL |
| **Price/FCF** | Market Cap / FCF | 262.9 / 70.6 | 3.7x | FAIL |
| **FCF Yield** | FCF / Market Cap | 70.6 / 262.9 | 26.9% | PASS |

## **Profitability Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Gross Margin** | Gross Profit / Revenue | 97.0 / 247.3 | 39.2% | MONITOR |
| **Operating Margin** | Operating Profit / Revenue | 3.6 / 247.3 | 1.5% | FAIL |
| **Net Margin** | Net Income / Revenue | -9.6 / 247.3 | -3.9% | FAIL |
| **ROA** | Net Income / Assets | -19.2 / 416.2 | -4.6% | FAIL |
| **ROE** | Net Income / Equity | -19.2 / 145.9 | -13.2% | FAIL |
| **ROCE** | EBIT / Capital Employed | 6.1 / 318.3 | 1.9% | FAIL |

## **Efficiency Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Asset Turnover** | Revenue / Assets | 494.6 / 416.2 | 1.19x | DISABLED |
| **Inventory Turnover** | COGS / Inventory | 300.6 / 71.1 | 4.2x | PASS |
| **Receivables Turnover** | Revenue / Receivables | 494.6 / 30.2 | 16.4x | DISABLED |
| **DSO** | 365 / Rec Turnover | 365 / 16.4 | 22 days | PASS |

## **Liquidity Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Current Ratio** | Current Assets / Current Liabilities | 160.7 / 97.9 | 1.64x | PASS |
| **Quick Ratio** | (CA - Inventory) / CL | (160.7 - 71.1) / 97.9 | 0.92x | MONITOR |
| **Cash Ratio** | Cash / Current Liabilities | 13.9 / 97.9 | 0.14x | DISABLED |

## **Leverage Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Debt-to-Equity** | Total Debt / Equity | 163.2 / 145.9 | 1.12x | FAIL |
| **Debt Ratio** | Total Debt / Assets | 163.2 / 416.2 | 0.39x | DISABLED |
| **Interest Coverage** | EBIT / Interest | 6.1 / 26.0 | 0.2x | FAIL |
| **Net Debt/EBITDA** | Net Debt / LTM EBITDA | 149.3 / 6.1 | 24.50x | FAIL |

## **Cash Flow Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Free Cash Flow Annual** | OCF - CapEx | Extracted | 70.6 | PASS |
| **OCF Ratio** | Op Cash Flow / Current Liabilities | 55.4 / 97.9 | 0.57x | DISABLED |
| **Cash Conversion** | OCF Annual / NI Annual | 110.8 / 19.2 | 5.8x | PASS |

## **Earnings Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Accruals Ratio** | (NI Annual - OCF Annual) / Assets | (-19.2 - 110.8) / 416.2 | -31.2% | FAIL |
| **EBITDA to FCF** | FCF Annual / LTM EBITDA | 70.6 / 6.1 | 1158.3% | PASS |
| **Adj vs Stat Gap** | (Adj - Stat) / Stat | (3.6 - 3.6) / 3.6 | 0.0% | PASS |

## **Asset Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Goodwill/Assets** | Goodwill / Total Assets | 73.2 / 416.2 | 17.6% | PASS |
| **Capex/Depreciation** | Annualized Capex / LTM Depreciation | 0.0 / 0.0 | 0.00x | MONITOR |
| **Working Capital** | CA - CL | 160.7 - 97.9 | £62.8m | DISABLED |
| **Tangible Book Value** | Equity - Intangibles | 145.9 - 73.2 | £72.7m | PASS |

## **All Variables Used in Calculations**

| Variable | Value | Unit | Source |
|----------|-------|------|--------|
| Adjusted Operating Profit | 3.60 |  | Extracted |
| Amortization | 0.00 |  | Extracted |
| COGS | 150.30 | £m | Extracted |
| Capital Expenditure | 20.10 |  | Extracted |
| Cash and Bank Balances | 13.90 | £m | Extracted |
| Current Assets | 160.70 | £m | Extracted |
| Current Liabilities | 97.90 | £m | Extracted |
| Depreciation | 0.00 |  | Extracted |
| EBIT | 3.05 | £m | Extracted |
| EBIT Annual | 6.09 | £m | Annualized (x2) |
| EBITDA | 6.09 | £m | XPP.json |
| Enterprise Value | 412.23 |  | Calculated |
| FCF Annual | 70.60 | £m | Annualized (x2) |
| Free Cash Flow | 35.30 | £m | Extracted |
| Goodwill | 73.20 |  | Extracted |
| Gross Margin % | 39.22 | % | Extracted |
| Gross Profit | 97.00 | £m | Extracted |
| Intangible Assets | 0.00 |  | Extracted |
| Interest Annual | 26.00 | £m | Annualized (x2) |
| Interest Expense | 13.00 |  | Extracted |
| Inventories | 71.10 |  | Extracted |
| LTM Adjusted EBITDA | 6.09 | £m | XPP.json/Note 5 (LTM) |
| Net Debt | 149.30 | £m | Extracted |
| Net Income | -9.60 | £m | XPP.json |
| Net Income Annual | -19.20 | £m | Annualized (x2) |
| Operating Cash Flow | 55.40 | £m | Extracted |
| Operating Profit | 3.60 | £m | XPP.json |
| Operating Profit Annual | 7.20 | £m | Annualized (x2) |
| Receivables | 30.20 |  | Extracted |
| Revenue | 247.30 | £m | XPP.json |
| Revenue Annual | 494.60 | £m | Annualized (x2) |
| Statutory Operating Profit | 3.60 |  | Extracted |
| Tangible Book Value | 72.70 |  | Extracted |
| Total Assets | 416.20 | £m | XPP.json |
| Total Debt | 163.20 | £m | Extracted |
| Total Equity | 145.90 | £m | XPP.json |
| Total Liabilities | 270.30 |  | Extracted |
| enterprise_value | 351.55 |  | Extracted |
| market_cap | 262.93 |  | Yahoo Finance |
| share_price | 9.20 | £ | Yahoo Finance |
| shares_outstanding | 27.93 | millions | Yahoo Finance |
