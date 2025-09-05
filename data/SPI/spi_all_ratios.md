# SPI.L All Financial Ratios Analysis

Generated from financial data files
Data Sources: SPI.json

## **Current Market Data**

| Metric | Value | Source | Retrieved |
|--------|-------|--------|----------|
| **Share Price** | £2.08 | Yahoo Finance | 2025-09-05 09:22:47 |
| **Market Cap** | £871.1m | Yahoo Finance | 2025-09-05 09:22:47 |
| **Enterprise Value** | £2109.8m | Calculated | - |
| **Shares Outstanding** | 0.0m | Financial Reports | - |

## **Valuation Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **P/E Ratio** | Market Cap / Net Income | 871.1 / 50.8 | 17.1x | FAIL |
| **P/B Ratio** | Market Cap / Equity | 871.1 / 746.2 | 1.17x | DISABLED |
| **P/S Ratio** | Market Cap / Revenue | 871.1 / 3022.4 | 0.29x | DISABLED |
| **EV/EBITDA** | EV / LTM EBITDA | 2109.8 / 248.9 | 8.5x | FAIL |
| **EV/EBIT** | EV / EBIT | 2109.8 / 136.7 | 15.4x | FAIL |
| **EV/Revenue** | EV / Revenue | 2109.8 / 3022.4 | 0.70x | FAIL |
| **Price/FCF** | Market Cap / FCF | 871.1 / 247.2 | 3.5x | FAIL |
| **FCF Yield** | FCF / Market Cap | 247.2 / 871.1 | 28.4% | PASS |

## **Profitability Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Gross Margin** | Gross Profit / Revenue | 683.6 / 1511.2 | 45.2% | PASS |
| **Operating Margin** | Operating Profit / Revenue | 141.3 / 1511.2 | 9.4% | MONITOR |
| **Net Margin** | Net Income / Revenue | 25.4 / 1511.2 | 1.7% | MONITOR |
| **ROA** | Net Income / Assets | 50.8 / 2343.2 | 2.2% | {'DISABLED'} |
| **ROE** | Net Income / Equity | 50.8 / 746.2 | 6.8% | MONITOR |
| **ROCE** | EBIT / Capital Employed | 136.7 / 2001.5 | 6.8% | FAIL |

## **Efficiency Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Asset Turnover** | Revenue / Assets | 3022.4 / 2343.2 | 1.29x | DISABLED |
| **Inventory Turnover** | COGS / Inventory | 1655.2 / 46.6 | 35.5x | PASS |
| **Receivables Turnover** | Revenue / Receivables | 3022.4 / 76.9 | 39.3x | DISABLED |
| **DSO** | 365 / Rec Turnover | 365 / 39.3 | 9 days | PASS |

## **Liquidity Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Current Ratio** | Current Assets / Current Liabilities | 225.3 / 341.7 | 0.66x | FAIL |
| **Quick Ratio** | (CA - Inventory) / CL | (225.3 - 46.6) / 341.7 | 0.52x | MONITOR |
| **Cash Ratio** | Cash / Current Liabilities | 41.2 / 341.7 | 0.12x | DISABLED |

## **Leverage Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Debt-to-Equity** | Total Debt / Equity | 1279.9 / 746.2 | 1.72x | FAIL |
| **Debt Ratio** | Total Debt / Assets | 1279.9 / 2343.2 | 0.55x | DISABLED |
| **Interest Coverage** | EBIT / Interest | 136.7 / 196.8 | 0.7x | FAIL |
| **Net Debt/EBITDA** | Net Debt / LTM EBITDA | 1238.7 / 248.9 | 4.98x | FAIL |

## **Cash Flow Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Free Cash Flow Annual** | OCF - CapEx | Extracted | 247.2 | PASS |
| **OCF Ratio** | Op Cash Flow / Current Liabilities | 235.7 / 341.7 | 0.69x | DISABLED |
| **Cash Conversion** | OCF Annual / NI Annual | 471.4 / 50.8 | 9.3x | PASS |

## **Earnings Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Accruals Ratio** | (NI Annual - OCF Annual) / Assets | (50.8 - 471.4) / 2343.2 | -17.9% | MONITOR |
| **EBITDA to FCF** | FCF Annual / LTM EBITDA | 247.2 / 248.9 | 99.3% | PASS |
| **Adj vs Stat Gap** | (Adj - Stat) / Stat | (141.3 - 141.3) / 141.3 | 0.0% | PASS |

## **Asset Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Goodwill/Assets** | Goodwill / Total Assets | 411.6 / 2343.2 | 17.6% | PASS |
| **Capex/Depreciation** | Annualized Capex / LTM Depreciation | 0.0 / 112.2 | 0.00x | MONITOR |
| **Working Capital** | CA - CL | 225.3 - 341.7 | £-116.4m | DISABLED |
| **Tangible Book Value** | Equity - Intangibles | 746.2 - 437.4 | £308.8m | PASS |

## **All Variables Used in Calculations**

| Variable | Value | Unit | Source |
|----------|-------|------|--------|
| Adjusted Operating Profit | 141.30 |  | Extracted |
| Amortization | 0.00 |  | Extracted |
| COGS | 827.60 | £m | Extracted |
| Capital Expenditure | 112.10 |  | Extracted |
| Cash and Bank Balances | 41.20 | £m | Extracted |
| Current Assets | 225.30 | £m | Extracted |
| Current Liabilities | 341.70 | £m | Extracted |
| Depreciation | 112.20 |  | Extracted |
| EBIT | 68.35 | £m | Extracted |
| EBIT Annual | 136.70 | £m | Annualized (x2) |
| EBITDA | 248.90 | £m | SPI.json |
| Enterprise Value | 2109.76 |  | Calculated |
| FCF Annual | 247.20 | £m | Annualized (x2) |
| Free Cash Flow | 123.60 | £m | Extracted |
| Goodwill | 411.60 |  | Extracted |
| Gross Margin % | 45.24 | % | Extracted |
| Gross Profit | 683.60 | £m | Extracted |
| Intangible Assets | 25.80 |  | Extracted |
| Interest Annual | 196.80 | £m | Annualized (x2) |
| Interest Expense | 98.40 |  | Extracted |
| Inventories | 46.60 |  | Extracted |
| LTM Adjusted EBITDA | 248.90 | £m | SPI.json/Note 5 (LTM) |
| Net Debt | 1238.70 | £m | Extracted |
| Net Income | 25.40 | £m | SPI.json |
| Net Income Annual | 50.80 | £m | Annualized (x2) |
| Operating Cash Flow | 235.70 | £m | Extracted |
| Operating Profit | 141.30 | £m | SPI.json |
| Operating Profit Annual | 282.60 | £m | Annualized (x2) |
| Receivables | 76.90 |  | Extracted |
| Revenue | 1511.20 | £m | SPI.json |
| Revenue Annual | 3022.40 | £m | Annualized (x2) |
| Statutory Operating Profit | 141.30 |  | Extracted |
| Tangible Book Value | 308.80 |  | Extracted |
| Total Assets | 2343.20 | £m | SPI.json |
| Total Debt | 1279.90 | £m | Extracted |
| Total Equity | 746.20 | £m | SPI.json |
| Total Liabilities | 1597.00 |  | Extracted |
| enterprise_value | 2109.33 |  | Extracted |
| market_cap | 871.06 |  | Yahoo Finance |
| share_price | 2.08 | £ | Yahoo Finance |
| shares_outstanding | 402.37 | millions | Yahoo Finance |
