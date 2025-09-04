---

# Insig AI Plc - Forensic Accounting & Earnings Quality Analysis

## Table 1: Metrics Used to Assess Insig AI

| Category           | Metric                     | Value / Description                          | Source File & Line Reference |
|--------------------|----------------------------|----------------------------------------------|------------------------------|
| Valuation Ratios   | P/E Ratio                  | N/A                                          | INSG_agent_ratios.md          |
|                    | EV/EBIT                   | 0.0x (Pass)                                  | INSG_agent_ratios.md          |
|                    | EV/Revenue                | 42.0x (Pass)                                 | INSG_agent_ratios.md          |
|                    | Price to FCF              | N/A                                          | INSG_agent_ratios.md          |
|                    | FCF Yield                 | 0.0% (Fail)                                  | INSG_agent_ratios.md          |
| Profitability      | Gross Margin              | 100.0% (Pass)                                | INSG_agent_ratios.md          |
|                    | Operating Margin          | -567.3% (Fail)                               | INSG_agent_ratios.md          |
|                    | Net Margin                | -4307.7% (Fail)                              | INSG_agent_ratios.md          |
|                    | ROE                       | -2031.3% (Fail)                              | INSG_agent_ratios.md          |
|                    | ROCE                      | -157.2% (Fail)                               | INSG_agent_ratios.md          |
| Liquidity          | Current Ratio             | 0.1% (Fail)                                  | INSG_agent_ratios.md          |
|                    | Quick Ratio               | 0.1% (Fail)                                  | INSG_agent_ratios.md          |
| Leverage           | Debt-to-Equity            | 1.0 (Monitor)                                | INSG_agent_ratios.md          |
|                    | Interest Coverage         | -16.6x (Fail)                                | INSG_agent_ratios.md          |
| Efficiency         | Inventory Turnover        | 0.0x (Fail)                                  | INSG_agent_ratios.md          |
|                    | Days Sales Outstanding    | 38 days (Pass)                               | INSG_agent_ratios.md          |
| Earnings Quality   | Accruals Ratio            | -686.8% (Pass)                               | INSG_agent_ratios.md          |
|                    | EBITDA to FCF Conversion  | 0.0 (Fail)                                   | INSG_agent_ratios.md          |
|                    | Adjusted vs Statutory Gap | -0.0 (Pass)                                  | INSG_agent_ratios.md          |
| Asset Quality      | Goodwill/Assets           | 0.0 (Pass)                                   | INSG_agent_ratios.md          |
|                    | Capex/Depreciation        | 0.0 (Monitor)                                | INSG_agent_ratios.md          |
|                    | Tangible Book Value       | £-2.8m (Fail)                                | INSG_agent_ratios.md          |
| Cash Flow          | Cash Conversion           | -0.0 (Fail)                                  | INSG_agent_ratios.md          |
|                    | Free Cash Flow            | £-1.3m (Fail)                                | INSG_agent_ratios.md          |
| Ownership          | Largest Shareholder       | Richard Bernstein 18.6%                       | INSG_notes.md (ownership section) |
|                    | Directors' Options/Warrants| Present (e.g., Bernstein 1.67m options)      | INSG_notes.md (ownership section) |
|                    | Board Changes             | Resignations and death noted                   | INSG_notes.md (ownership section) |

---

## Table 2: Assessment and Verdict of Metrics

| Metric                     | Assessment Summary                                                                 | Verdict (Sustainable/Repeatable/Cash-Convertible/Inflated)          |
|----------------------------|------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| EV/EBIT                    | 0.0x due to negative EBIT, misleadingly low multiple                              | Inflated (misleading)                                                |
| EV/Revenue                 | Very high at 42.0x, indicating market expectations not supported by fundamentals  | Inflated                                                           |
| FCF Yield                  | 0.0%, no free cash flow generation                                                | Not cash-convertible                                                |
| Gross Margin               | 100%, inflated due to zero cost of sales                                          | Inflated                                                           |
| Operating Margin           | -567.3%, severe operating losses                                                  | Not sustainable                                                   |
| Net Margin                 | -4307.7%, severe net losses                                                       | Not sustainable                                                   |
| ROE                        | -2031.3%, negative returns on equity                                              | Not sustainable                                                   |
| ROCE                       | -157.2%, negative returns on capital employed                                    | Not sustainable                                                   |
| Current Ratio              | 0.1%, critically low liquidity                                                   | Not sustainable, liquidity risk                                   |
| Quick Ratio                | 0.1%, critically low liquidity                                                   | Not sustainable, liquidity risk                                   |
| Debt-to-Equity             | 1.0, moderate leverage at upper monitor limit                                    | Moderate risk, monitor                                            |
| Interest Coverage          | -16.6x, cannot cover interest expenses                                           | Not sustainable                                                   |
| Inventory Turnover         | 0.0x, no inventory or poor management                                            | Not sustainable                                                   |
| Days Sales Outstanding     | 38 days, reasonable receivables collection                                      | Sustainable                                                      |
| Accruals Ratio             | -686.8%, no aggressive accruals                                                  | Sustainable                                                      |
| EBITDA to FCF Conversion   | 0.0, poor conversion of earnings to cash flow                                   | Not cash-convertible                                              |
| Adjusted vs Statutory Gap  | -0.0, no large adjustments                                                       | Sustainable                                                      |
| Goodwill/Assets            | 0.0%, no goodwill risk                                                           | Sustainable                                                      |
| Capex/Depreciation         | 0.0, low reinvestment relative to depreciation                                   | Monitor (risk of underinvestment)                                |
| Tangible Book Value        | Negative £2.8m, negative tangible equity                                         | Not sustainable                                                 |
| Cash Conversion            | -0.0, negative cash conversion                                                  | Not cash-convertible                                              |
| Free Cash Flow             | Negative £1.3m, cash consuming                                                  | Not cash-convertible                                              |
| Ownership Concentration    | Largest shareholder holds 18.6%, directors hold options/warrants, recent board changes | Governance risk, insider control, potential dilution risk        |

---

## Summary Analysis

**Valuation Ratios:**  
The EV/EBIT ratio of 0.0x is misleading due to negative EBIT, giving a false impression of cheap valuation. The EV/Revenue ratio is extremely high at 42.0x, indicating the market values the company highly relative to revenue, likely due to growth expectations or intangible assets. However, the lack of positive earnings and cash flow yield (0.0%) confirms no current cash generation.

**Profitability:**  
Profitability metrics are severely negative, with operating margin at -567.3% and net margin at -4307.7%, reflecting significant losses. Returns on equity and capital employed are deeply negative, indicating the company is burning capital and not generating economic profits. The gross margin of 100% is inflated due to zero cost of sales, which is not sustainable.

**Liquidity:**  
Liquidity ratios are critically low, with current and quick ratios at 0.1%, indicating the company has very limited short-term assets to cover liabilities. This raises concerns about solvency and operational continuity without external financing.

**Leverage:**  
Debt-to-equity is at 1.0, at the upper limit of the monitor range, indicating moderate leverage. Interest coverage is negative (-16.6x), showing the company cannot service its debt from earnings, increasing financial risk.

**Efficiency:**  
Inventory turnover is zero, possibly reflecting no inventory or operational issues. Days sales outstanding at 38 days is reasonable, indicating decent receivables management.

**Earnings Quality:**  
Accruals ratio and adjusted vs statutory gap pass, indicating no aggressive accounting adjustments. However, EBITDA to free cash flow conversion is zero, highlighting poor cash realization from earnings.

**Asset Quality:**  
No goodwill is reported, which is positive. Capex to depreciation is zero, suggesting underinvestment in assets, and tangible book value is negative £2.8m, indicating net tangible liabilities.

**Cash Flow:**  
Cash conversion and free cash flow are negative, confirming the company is consuming cash rather than generating it.

**Ownership and Governance:**  
Ownership is concentrated with the largest shareholder holding 18.6%, and directors hold significant options and warrants, aligning incentives but also posing dilution and governance risks. Recent board changes due to resignation and death add governance uncertainty.

**Going Concern and Auditor's Opinion:**  
The auditor's report highlights a material uncertainty related to going concern due to the need for further working capital and uncertainties over future revenue growth. The directors have a reasonable expectation to raise finance to continue operations, but this remains a significant risk.

---

## Conclusion

Insig AI is currently in a distressed financial position characterized by severe operating losses, negative profitability metrics, poor liquidity, negative cash flows, and negative tangible equity. Valuation multiples are distorted by losses and low revenue, with market expectations not supported by current fundamentals. The company relies on financing activities to sustain operations, as evidenced by net cash inflows from financing and the auditor's material uncertainty on going concern.

Ownership concentration and recent board changes pose governance risks. The company’s turnaround depends on successful execution of management plans, improved operational performance, and securing additional funding. Investors should exercise caution and consider the high financial and operational risks before investing.

Additional information needed includes detailed management plans for turnaround, future cash flow projections, and governance arrangements post board changes.

---

Victoria Clarke  
Financial Modeling & Valuation Expert  
2025-09-04 12:39:59