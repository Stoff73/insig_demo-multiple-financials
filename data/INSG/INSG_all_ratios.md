# INSG.L All Financial Ratios Analysis

Generated from financial data files
Data Sources: INSG.json

## **Current Market Data**

| Metric | Value | Source | Retrieved |
|--------|-------|--------|----------|
| **Share Price** | £0.24 | Yahoo Finance | 2025-09-02 17:09:29 |
| **Market Cap** | £29.6m | Yahoo Finance | 2025-09-02 17:09:29 |
| **Enterprise Value** | £31.1m | Calculated | - |
| **Shares Outstanding** | 0.0m | Financial Reports | - |

## **Valuation Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **P/E Ratio** | Market Cap / Net Income | 29.6 / -31.9 | N/A (loss) | FAIL |
| **P/B Ratio** | Market Cap / Equity | 29.6 / 1.6 | 18.87x | DISABLED |
| **P/S Ratio** | Market Cap / Revenue | 29.6 / 0.7 | 40.01x | DISABLED |
| **EV/EBITDA** | EV / LTM EBITDA | 31.1 / -16.0 | 0.0x | PASS |
| **EV/EBIT** | EV / EBIT | 31.1 / -4.2 | 0.0x | PASS |
| **EV/Revenue** | EV / Revenue | 31.1 / 0.7 | 42.05x | PASS |
| **FCF Yield** | FCF / Market Cap | -2.6 / 29.6 | 0.0% | FAIL |

## **Profitability Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Gross Margin** | Gross Profit / Revenue | 0.4 / 0.4 | 100.0% | PASS |
| **Operating Margin** | Operating Profit / Revenue | -2.1 / 0.4 | -567.3% | FAIL |
| **Net Margin** | Net Income / Revenue | -15.9 / 0.4 | -4307.7% | FAIL |
| **ROA** | Net Income / Assets | -31.9 / 4.6 | -700.0% | FAIL |
| **ROE** | Net Income / Equity | -31.9 / 1.6 | -2031.3% | FAIL |
| **ROCE** | EBIT / Capital Employed | -4.2 / 2.7 | -157.2% | FAIL |

## **Efficiency Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Asset Turnover** | Revenue / Assets | 0.7 / 4.6 | 0.16x | DISABLED |
| **Inventory Turnover** | COGS / Inventory | 0.0 / 0.0 | 0.0x | FAIL |
| **Receivables Turnover** | Revenue / Receivables | 0.7 / 0.1 | 9.6x | DISABLED |
| **DSO** | 365 / Rec Turnover | 365 / 9.6 | 38 days | PASS |

## **Liquidity Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Current Ratio** | Current Assets / Current Liabilities | 0.1 / 1.9 | 0.08x | FAIL |
| **Quick Ratio** | (CA - Inventory) / CL | (0.1 - 0.0) / 1.9 | 0.08x | FAIL |
| **Cash Ratio** | Cash / Current Liabilities | 0.0 / 1.9 | 0.02x | DISABLED |

## **Leverage Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Debt-to-Equity** | Total Debt / Equity | 1.5 / 1.6 | 0.98x | MONITOR |
| **Debt Ratio** | Total Debt / Assets | 1.5 / 4.6 | 0.34x | DISABLED |
| **Interest Coverage** | EBIT / Interest | -4.2 / 0.3 | -16.6x | FAIL |
| **Net Debt/EBITDA** | Net Debt / LTM EBITDA | 1.5 / -16.0 | 0.00x | PASS |

## **Cash Flow Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Free Cash Flow Annual** | OCF - CapEx | Extracted | -2.63982 | FAIL |
| **OCF Ratio** | Op Cash Flow / Current Liabilities | -0.3 / 1.9 | -0.16x | DISABLED |
| **Cash Conversion** | OCF Annual / NI Annual | -0.6 / 31.9 | -0.0x | FAIL |

## **Earnings Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Accruals Ratio** | (NI Annual - OCF Annual) / Assets | (-31.9 - -0.6) / 4.6 | -686.8% | FAIL |
| **EBITDA to FCF** | FCF Annual / LTM EBITDA | -2.6 / -16.0 | 0.0% | FAIL |
| **Adj vs Stat Gap** | (Adj - Stat) / Stat | (-2.1 - -2.1) / -2.1 | -0.0% | PASS |

## **Asset Quality Ratios**

| Ratio | Formula | Calculation | Value | Outcome |
|-------|---------|-------------|-------|----------|
| **Goodwill/Assets** | Goodwill / Total Assets | 0.0 / 4.6 | 0.0% | PASS |
| **Capex/Depreciation** | Annualized Capex / LTM Depreciation | 0.0 / 1.6 | 0.00x | MONITOR |
| **Working Capital** | CA - CL | 0.1 - 1.9 | £-1.7m | DISABLED |
| **Tangible Book Value** | Equity - Intangibles | 1.6 - 4.4 | £-2.8m | FAIL |

## **All Variables Used in Calculations**

| Variable | Value | Unit | Source |
|----------|-------|------|--------|
| Adjusted Operating Profit | -2.10 |  | Extracted |
| Amortization | 0.00 |  | Extracted |
| COGS | 0.00 | £m | Extracted |
| Capital Expenditure | 1.02 |  | Extracted |
| Cash and Bank Balances | 0.04 | £m | Extracted |
| Current Assets | 0.14 | £m | Extracted |
| Current Liabilities | 1.88 | £m | Extracted |
| Depreciation | 1.58 |  | Extracted |
| EBIT | -2.10 | £m | Extracted |
| EBIT Annual | -4.20 | £m | Annualized (x2) |
| EBITDA | -16.03 | £m | INSG.json |
| Enterprise Value | 31.10 |  | Calculated |
| FCF Annual | -2.64 | £m | Annualized (x2) |
| Free Cash Flow | -1.32 | £m | Extracted |
| Goodwill | 0.00 |  | Extracted |
| Gross Margin % | 100.00 | % | Extracted |
| Gross Profit | 0.37 | £m | Extracted |
| Intangible Assets | 4.40 |  | Extracted |
| Interest Annual | 0.25 | £m | Annualized (x2) |
| Interest Expense | 0.13 |  | Extracted |
| Inventories | 0.00 |  | Extracted |
| LTM Adjusted EBITDA | -16.03 | £m | INSG.json/Note 5 (LTM) |
| Net Debt | 1.51 | £m | Extracted |
| Net Income | -15.93 | £m | INSG.json |
| Net Income Annual | -31.86 | £m | Annualized (x2) |
| Operating Cash Flow | -0.30 | £m | Extracted |
| Operating Profit | -2.10 | £m | INSG.json |
| Operating Profit Annual | -4.20 | £m | Annualized (x2) |
| Receivables | 0.08 |  | Extracted |
| Revenue | 0.37 | £m | INSG.json |
| Revenue Annual | 0.74 | £m | Annualized (x2) |
| Statutory Operating Profit | -2.10 |  | Extracted |
| Tangible Book Value | -2.84 |  | Extracted |
| Total Assets | 4.55 | £m | INSG.json |
| Total Debt | 1.54 | £m | Extracted |
| Total Equity | 1.57 | £m | INSG.json |
| Total Liabilities | 2.98 |  | Extracted |
| enterprise_value | 27.83 |  | Extracted |
| market_cap | 29.60 |  | Yahoo Finance |
| share_price | 0.24 | £ | Yahoo Finance |
| shares_outstanding | 120.81 | millions | Yahoo Finance |
