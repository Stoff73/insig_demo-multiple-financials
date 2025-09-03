---

# Insig AI Forensic Financial Analysis Report  
**Prepared by:** Daniel Osei, Forensic Accounting & Earnings Quality Specialist  
**Date:** 2025-09-02 17:02:47  

---

## Table 1: Metrics Used for Assessment

| Metric Category       | Metric                    | Source File                  | Exact Value / Figure                |
|-----------------------|---------------------------|------------------------------|-----------------------------------|
| **Valuation Ratios**  | P/E Ratio                 | INSG_agent_ratios.md          | N/A                               |
|                       | EV/EBIT                   | INSG_agent_ratios.md          | 0.0x                              |
|                       | EV/Revenue                | INSG_agent_ratios.md          | 42.0x                             |
|                       | Price to FCF              | INSG_agent_ratios.md          | N/A                               |
|                       | FCF Yield                 | INSG_agent_ratios.md          | 0.0%                              |
| **Profitability**     | Gross Margin              | INSG_agent_ratios.md          | 100.0%                            |
|                       | Operating Margin          | INSG_agent_ratios.md          | -567.3%                           |
|                       | Net Margin                | INSG_agent_ratios.md          | -4307.7%                          |
|                       | ROE                       | INSG_agent_ratios.md          | -2031.3%                         |
|                       | ROCE                      | INSG_agent_ratios.md          | -157.2%                          |
| **Liquidity**         | Current Ratio             | INSG_agent_ratios.md          | 0.1%                             |
|                       | Quick Ratio               | INSG_agent_ratios.md          | 0.1%                             |
| **Leverage**          | Debt-to-Equity            | INSG_agent_ratios.md, INSG_balancesheet_statement.md | 1.0 (Monitor)                     |
|                       | Interest Coverage         | INSG_agent_ratios.md          | -16.6x                           |
| **Efficiency**        | Inventory Turnover        | INSG_agent_ratios.md          | 0.0x                             |
|                       | Days Sales Outstanding    | INSG_agent_ratios.md          | 38 days                          |
| **Earnings Quality**  | Accruals Ratio            | INSG_agent_ratios.md          | -686.8%                          |
|                       | EBITDA to FCF Conversion  | INSG_agent_ratios.md          | 0.0                              |
|                       | Adjusted vs Statutory Gap | INSG_agent_ratios.md          | -0.0                             |
| **Asset Quality**     | Goodwill/Assets           | INSG_agent_ratios.md, INSG_balancesheet_statement.md | 0.0                              |
|                       | Capex/Depreciation        | INSG_agent_ratios.md          | 0.0                              |
|                       | Tangible Book Value       | INSG_agent_ratios.md, INSG_balancesheet_statement.md | £-2.8m                           |
| **Cash Flow Ratios**  | Cash Conversion           | INSG_agent_ratios.md          | -0.0                             |
|                       | Free Cash Flow            | INSG_agent_ratios.md          | £-1.3m                           |
| **Balance Sheet Key Figures** | Total Assets          | INSG_balancesheet_statement.md | £4,552,239 (2024), £21,375,616 (2023) |
|                       | Total Liabilities         | INSG_balancesheet_statement.md | £2,983,562 (2024), £5,808,046 (2023)  |
|                       | Equity (Net Assets)       | INSG_balancesheet_statement.md | £1,568,677 (2024), £15,567,570 (2023) |
| **Auditor Opinion**   | Going Concern Material Uncertainty | INSG_auditor_report.md        | Present, emphasized with no modification |
| **Ownership**          | Insider Ownership Levels  | (Ownership file extract)      | Bernstein 18.6%, Cracknell 5.8%, Others as noted |

---

## Table 2: Assessment and Verdict on Metrics

| Metric Category       | Metric                   | Value                       | Verdict                              | Notes / Risks |
|-----------------------|--------------------------|-----------------------------|------------------------------------|--------------|
| Valuation Ratios      | EV/EBIT                  | 0.0x                        | Inflated / data artifact           | Operating loss ~£17.6m makes 0.0x EV/EBIT nonsensical |
|                       | EV/Revenue               | 42.0x                       | Inflated/high valuation            | Implies very high market premium despite losses |
|                       | FCF Yield                | 0.0%                        | Fail / poor cash flow generation   | No meaningful free cash flow yield |
| Profitability         | Gross Margin             | 100.0%                      | Pass / typical for software/AI     | No cost of sales reported |
|                       | Operating Margin         | -567.3%                     | Fail / unsustainable losses        | Massive negative margin |
|                       | Net Margin               | -4307.7%                    | Fail / unsustainable losses        | Deep net losses |
|                       | ROE                      | -2031.3%                   | Fail / negative returns            | Equity losses too |
|                       | ROCE                     | -157.2%                    | Fail / negative returns            | Capital not generating returns |
| Liquidity             | Current Ratio            | 0.1%                        | Fail / critical liquidity risk     | Unable to cover current liabilities |
|                       | Quick Ratio              | 0.1%                        | Fail / critical liquidity risk     | Minimal quick assets |
| Leverage              | Debt-to-Equity           | 1.0                         | Monitor / moderate leverage        | Convertible debt sizable |
|                       | Interest Coverage        | -16.6x                      | Fail / distress / default risk     | Unable to cover interest costs |
| Efficiency            | Inventory Turnover       | 0.0x                        | Neutral/Not applicable              | AI/software, no inventory |
|                       | Days Sales Outstanding   | 38 days                    | Pass / efficient receivables       | Adequate receivable management |
| Earnings Quality      | Accruals Ratio           | -686.8%                    | Pass / conservative accounting     | No aggressive accruals |
|                       | EBITDA to FCF Conversion | 0.0                         | Fail / poor cash conversion        | Reported EBITDA never converts |
|                       | Adj. vs Statutory Gap   | -0.0                        | Pass / no earnings manipulation    | Consistent with quality |
| Asset Quality         | Goodwill/Assets          | 0.0                         | Pass / clean asset base             | No goodwill risk |
|                       | Capex/Depreciation       | 0.0                         | Monitor / minimal reinvestment     | Questions sustainability of asset base |
|                       | Tangible Book Value      | £-2.8m                      | Fail / negative tangible equity    | Large impairments, negative net tangible assets |
| Cash Flow             | Cash Conversion          | -0.0                        | Fail / failed cash conversion      | Cash burn consistent with losses |
|                       | Free Cash Flow           | £-1.3m                      | Fail / severe cash burn             | Negative FCF |
| Auditor Report        | Going Concern Uncertainty| Present                     | Material uncertainty disclosed     | Notes going concern risk, but unmodified opinion |
| Ownership             | Insider Ownership        | Bernstein 18.6%, others     | Significant insider control        | Potential for aligned incentives or governance risk |

---

## Analytical Summary

**Valuation**: Insig AI's valuation metrics reflect an extreme disconnect between market capitalization and fundamental earnings or cash flow reality. The EV/Revenue multiple at 42x and EV/EBIT at 0.0x are red flags, suggesting expectations of a technology premium that current economic results do not support. Lack of meaningful P/E and price to FCF ratios further point to reliance on speculative growth.

**Profitability**: The company operates at deep operating and net losses with huge negative margins far beyond typical start-up burn rates, signifying unsustainable expense structures and/or impairments. Negative ROE and ROCE highlight destruction of shareholder value.

**Liquidity and Leverage**: Critically low liquidity ratios and a debt-to-equity ratio at the upper monitor range indicate financial fragility, compounded by negative interest coverage suggesting inability to service debt from earnings. Convertible debt forms a significant portion of liabilities.

**Efficiency & Earnings Quality**: Inventory turnover is irrelevant for an AI firm. Receivables collection remains reasonable at 38 days DSO. Earnings quality metrics, including the accruals ratio and adjusted vs statutory gap, indicate a lack of aggressive accounting or earnings manipulation, increasing confidence in reported results despite poor performance.

**Asset Quality**: The absence of goodwill is a positive sign, but the significant drop in intangible assets from ~£20m in 2023 to ~£4.4m in 2024 suggests major impairments, leading to negative tangible book value (£-2.8m), undermining the asset base and equity.

**Cash Flow**: Cash flow metrics confirm the company burns cash with no earnings converting into cash, shown by zero EBITDA to free cash flow conversion and negative free cash flow of £1.3m.

**Auditor & Going Concern**: The auditor confirms material uncertainty on going concern, with emphasis on funding needs and cash flow pressures, but provides an unqualified opinion, reflecting transparency of risks without qualification.

**Ownership and Governance**: The ownership is concentrated among insiders, principally Richard Bernstein (18.6%) and other directors. This may align management incentives with shareholders, but also concentrate control, which in the context of financial distress, can impact governance and decision-making transparency around capital raises and strategic shifts.

---

## Conclusion

Insig AI demonstrates severe financial distress with persistent operating losses, declining asset base due to impairments, negative equity in tangible terms, and critical liquidity and leverage risks. Valuation multiples present in the market appear disconnected from the economic reality, likely driven by growth speculation rather than current earnings or cash flows.

Earnings quality shows no evidence of manipulation, providing some confidence in the data integrity, but economic reality is stark: negative margins, poor cash flow, and deteriorating balance sheet quality. The going concern risk is significant, highlighting dependency on further capital to sustain operations.

The significant insider ownership underscores potential alignment but also governance risk amid financial vulnerability. Investors must exercise caution and require clear signs of operational turnaround, improved profitability, liquidity stabilization, and sustainable cash flow before considering the equity investable.

This company currently represents a value trap from a forensic accounting and earnings quality perspective, with financial and operational risks overshadowing any speculative valuation upside.

---

Report prepared and signed:

Daniel Osei  
Forensic Accounting & Earnings Quality Specialist  
2025-09-02 17:02:47

---

References:  
- Financial Ratios and thresholds: ./data/INSG/INSG_agent_ratios.md  
- Balance Sheet Extract: ./data/INSG/INSG_balancesheet_statement.md lines 1-40  
- Auditor Report Excerpt: ./data/INSG/INSG_auditor_report.md lines 1-40  
- Notes summary: ./data/INSG/INSG_notes.md lines 1-50  
- Ownership data summarized from provided excerpt in task context