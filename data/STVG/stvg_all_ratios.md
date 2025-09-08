# STVG.L All Financial Ratios Analysis

Generated from financial data files
Data Sources: STVG.json

## **Current Market Data**

| Metric | Value | Source | Retrieved |
|--------|-------|--------|----------|
| **Share Price** | £1.25 | Yahoo Finance | 2025-09-08 11:57:20 |
| **Market Cap** | £56.9m | Yahoo Finance | 2025-09-08 11:57:20 |
| **Enterprise Value** | £113.0m | Calculated | - |
| **Shares Outstanding** | 0.0m | Financial Reports | - |

## **Valuation Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **P/E Ratio** | Market Cap / Net Income | 56.9 / 21.6 | 2.6x | PASS |
| **P/B Ratio** | Market Cap / Equity | 56.9 / -12.9 | -4.41x | DISABLED |
| **P/S Ratio** | Market Cap / Revenue | 56.9 / 376.0 | 0.15x | DISABLED |
| **EV/EBITDA** | EV / LTM EBITDA | 113.0 / 19.2 | 5.9x | MONITOR |
| **EV/EBIT** | EV / EBIT | 113.0 / 19.2 | 5.9x | PASS |
| **EV/Revenue** | EV / Revenue | 113.0 / 376.0 | 0.30x | FAIL |
| **Price/FCF** | Market Cap / FCF | 56.9 / 14.6 | 3.9x | FAIL |
| **FCF Yield** | FCF / Market Cap | 14.6 / 56.9 | 25.7% | PASS |

## **Profitability Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Gross Margin** | Gross Profit / Revenue | 85.7 / 188.0 | 45.6% | PASS |
| **Operating Margin** | Operating Profit / Revenue | 16.7 / 188.0 | 8.9% | MONITOR |
| **Net Margin** | Net Income / Revenue | 10.8 / 188.0 | 5.7% | PASS |
| **ROA** | Net Income / Assets | 21.6 / 169.7 | 12.7% | {'DISABLED'} |
| **ROE** | Net Income / Equity | 21.6 / -12.9 | -167.4% | FAIL |
| **ROCE** | EBIT / Capital Employed | 19.2 / 110.6 | 17.4% | PASS |

## **Efficiency Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Asset Turnover** | Revenue / Assets | 376.0 / 169.7 | 2.22x | DISABLED |
| **Inventory Turnover** | COGS / Inventory | 204.6 / 28.8 | 7.1x | PASS |
| **Receivables Turnover** | Revenue / Receivables | 376.0 / 16.3 | 23.1x | DISABLED |
| **DSO** | 365 / Rec Turnover | 365 / 23.1 | 16 days | PASS |

## **Liquidity Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Current Ratio** | Current Assets / Current Liabilities | 87.9 / 59.1 | 1.49x | MONITOR |
| **Quick Ratio** | (CA - Inventory) / CL | (87.9 - 28.8) / 59.1 | 1.00x | PASS |
| **Cash Ratio** | Cash / Current Liabilities | 11.1 / 59.1 | 0.19x | DISABLED |

## **Leverage Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Debt-to-Equity** | Total Debt / Equity | 67.2 / -12.9 | -5.21x | PASS |
| **Debt Ratio** | Total Debt / Assets | 67.2 / 169.7 | 0.40x | DISABLED |
| **Interest Coverage** | EBIT / Interest | 19.2 / 12.6 | 1.5x | FAIL |
| **Net Debt/EBITDA** | Net Debt / LTM EBITDA | 56.1 / 19.2 | 2.92x | MONITOR |

## **Cash Flow Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Free Cash Flow Annual** | OCF - CapEx | Extracted | 14.6 | PASS |
| **OCF Ratio** | Op Cash Flow / Current Liabilities | 8.7 / 59.1 | 0.15x | DISABLED |
| **Cash Conversion** | OCF Annual / NI Annual | 17.4 / 21.6 | 0.8x | MONITOR |

## **Earnings Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Accruals Ratio** | (NI Annual - OCF Annual) / Assets | (21.6 - 17.4) / 169.7 | 2.5% | PASS |
| **EBITDA to FCF** | FCF Annual / LTM EBITDA | 14.6 / 19.2 | 76.0% | PASS |
| **Adj vs Stat Gap** | (Adj - Stat) / Stat | (16.7 - 16.7) / 16.7 | 0.0% | PASS |

## **Asset Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Goodwill/Assets** | Goodwill / Total Assets | 20.3 / 169.7 | 12.0% | PASS |
| **Capex/Depreciation** | Annualized Capex / LTM Depreciation | 0.0 / 0.0 | 0.00x | MONITOR |
| **Working Capital** | CA - CL | 87.9 - 59.1 | £28.8m | DISABLED |
| **Tangible Book Value** | Equity - Intangibles | -12.9 - 20.3 | £-33.2m | FAIL |

## **All Variables Used in Calculations**

| Variable | Value | Unit | Source |
|----------|-------|------|--------|
| Adjusted Operating Profit | 16.70 |  | Extracted |
| Amortization | 0.00 |  | Extracted |
| COGS | 102.30 | £m | Extracted |
| Capital Expenditure | 1.40 |  | Extracted |
| Cash and Bank Balances | 11.10 | £m | Extracted |
| Current Assets | 87.90 | £m | Extracted |
| Current Liabilities | 59.10 | £m | Extracted |
| Depreciation | 0.00 |  | Extracted |
| EBIT | 9.60 | £m | Extracted |
| EBIT Annual | 19.20 | £m | Annualized (x2) |
| EBITDA | 19.20 | £m | STVG.json |
| Enterprise Value | 112.98 |  | Calculated |
| FCF Annual | 14.60 | £m | Annualized (x2) |
| Free Cash Flow | 7.30 | £m | Extracted |
| Goodwill | 20.30 |  | Extracted |
| Gross Margin % | 45.59 | % | Extracted |
| Gross Profit | 85.70 | £m | Extracted |
| Intangible Assets | 0.00 |  | Extracted |
| Interest Annual | 12.60 | £m | Annualized (x2) |
| Interest Expense | 6.30 |  | Extracted |
| Inventories | 28.80 |  | Extracted |
| LTM Adjusted EBITDA | 19.20 | £m | STVG.json/Note 5 (LTM) |
| Net Debt | 56.10 | £m | Extracted |
| Net Income | 10.80 | £m | STVG.json |
| Net Income Annual | 21.60 | £m | Annualized (x2) |
| Operating Cash Flow | 8.70 | £m | Extracted |
| Operating Profit | 16.70 | £m | STVG.json |
| Operating Profit Annual | 33.40 | £m | Annualized (x2) |
| Receivables | 16.30 |  | Extracted |
| Revenue | 188.00 | £m | STVG.json |
| Revenue Annual | 376.00 | £m | Annualized (x2) |
| Statutory Operating Profit | 16.70 |  | Extracted |
| Tangible Book Value | -33.20 |  | Extracted |
| Total Assets | 169.70 | £m | STVG.json |
| Total Debt | 67.20 | £m | Extracted |
| Total Equity | -12.90 | £m | STVG.json |
| Total Liabilities | 182.60 |  | Extracted |
| enterprise_value | 101.98 |  | Extracted |
| market_cap | 56.88 |  | Yahoo Finance |
| share_price | 1.25 | £ | Yahoo Finance |
| shares_outstanding | 45.69 | millions | Yahoo Finance |
