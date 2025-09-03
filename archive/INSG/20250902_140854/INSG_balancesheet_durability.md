### Table of Metrics Used for Assessment

| Metric               | Source File               | Value           | Threshold / Interpretation                 |
|----------------------|---------------------------|-----------------|--------------------------------------------|
| P/E Ratio            | INSG_agent_ratios.md       | N/A             | Not meaningful due to net loss              |
| EV/EBIT              | INSG_agent_ratios.md       | 0.0x            | Pass (<7 = good)                            |
| EV/Revenue           | INSG_agent_ratios.md       | 42.0x           | Pass (>1 = good, but caution due to losses)|
| Price to FCF         | INSG_agent_ratios.md       | N/A             | Not meaningful due to negative cash flow   |
| FCF Yield            | INSG_agent_ratios.md       | 0.0%            | Fail (<6% is poor cash conversion)          |
| Gross Margin         | INSG_agent_ratios.md       | 100.0%          | Pass (>40% is good but context-specific)    |
| Operating Margin     | INSG_agent_ratios.md       | -567.3%         | Fail (deeply negative, unsustainable)       |
| Net Margin           | INSG_agent_ratios.md       | -4307.7%        | Fail (deep negative loss)                    |
| ROE                  | INSG_agent_ratios.md       | -2031.3%        | Fail (massive value destruction)            |
| ROCE                 | INSG_agent_ratios.md       | -157.2%         | Fail (negative capital returns)             |
| Current Ratio        | INSG_agent_ratios.md       | 0.1%            | Fail (poor liquidity)                        |
| Quick Ratio          | INSG_agent_ratios.md       | 0.1%            | Fail (very poor liquidity)                   |
| Debt-to-Equity       | INSG_agent_ratios.md       | 1.0             | Monitor (high leverage borderline)          |
| Interest Coverage    | INSG_agent_ratios.md       | -16.6x          | Fail (unable to cover interest expense)     |
| Revenue              | INSG_income_statement.md   | £369,860        | Very low revenue                             |
| Operating Loss       | INSG_income_statement.md   | (£17,609,491)   | Huge loss relative to revenue                |
| Administrative Expenses | INSG_income_statement.md | (£2,562,208)    | Large overhead                               |
| Impairments          | INSG_income_statement.md   | (£15,317,338)   | Significant non-cash charge                  |
| Cash and Cash Equivalents | INSG_balancesheet_statement.md | £37,847  | Minimal liquidity                            |
| Net Operating Cash Flow | INSG_cashflow_statement.md | (£299,394)    | Negative cash flow from operations           |
| Net Investing Cash Flow | INSG_cashflow_statement.md | (£832,475)    | Significant cash used                        |
| Net Financing Cash Flow | INSG_cashflow_statement.md | £889,132      | Mainly from share capital issuance           |
| Directors’ Equity Ownership | INSG_notes.md           | Largest: 18.6% by Richard Bernstein | Concentrated insider ownership |

---

### Assessment Table

| Metric               | Assessment                                                                       | Verdict                          |
|----------------------|---------------------------------------------------------------------------------|---------------------------------|
| Valuation Ratios     | EV/EBIT and EV/Revenue look superficially attractive but misleading due to losses | Pass on EV multiples; caution   |
| Profitability Ratios | Operating and net margins, ROE, ROCE show catastrophic losses and value destruction | Fail                           |
| Liquidity Ratios     | Current and quick ratios indicate severe liquidity stress                        | Fail                           |
| Leverage Ratios      | Debt-to-equity high and interest coverage negative, showing inability to service debt | Monitor/Fail                  |
| Cash Flow Metrics    | Cash burn evident in operating and investing cash flow; financing only partially offsets | Fail                        |
| Earnings Quality    | Large impairments, no aggressive revenue recognition, no capitalization issues    | Quality weak due to impairments |
| Ownership Structure | Concentrated insider ownership, especially by largest shareholder/director         | Potential control benefits and risks |

---

### Detailed Analysis Summary

**Valuation & Market Metrics:**  
The valuation multiples—EV/EBIT at 0.0x and EV/Revenue at 42x—appear positive superficially. However, the EV/EBIT is zero mainly because EBIT is heavily negative and does not reflect operational strength. The high EV/Revenue multiple is distorted by the very low revenue base (£369,860). P/E and Price to FCF ratios are not applicable due to losses. Thus, valuation multiples should be interpreted with skepticism in this context.

**Profitability & Returns:**  
Insig AI is operating at a severe loss (operating margin -567%, net margin -4307%), mainly driven by very high administrative expenses (£2.56m) and massive asset impairments of £15.3m, which are non-cash but indicative of past overvaluation or impaired business prospects. Returns on equity and capital employed are deeply negative (ROE -2031%, ROCE -157%), meaning shareholder wealth is being destroyed and capital poorly employed.

**Liquidity & Leverage:**  
Current and quick ratios at 0.1% reveal critical liquidity stress; the company cannot cover current liabilities with available liquid assets. The debt-to-equity ratio of 1.0 suggests leverage is high, and the negative interest coverage ratio (-16.6x) indicates inability to cover interest expenses from operating earnings, highlighting financial distress.

**Cash Flow:**  
Operating cash flow is negative (£299k), investing cash flow negative (£832k), and only financing cash inflows (£889k), mainly from equity issuance, sustains liquidity. Cash reserves at year-end are minimal (£37,847), signaling precarious cash position and potential risk of short-term cash shortfalls.

**Earnings Quality:**  
The notes reveal that impairments primarily drive the losses. There is no evidence of aggressive revenue recognition or capitalization that inflates earnings artificially. The gross margin of 100% results from zero cost of sales reported but is overshadowed by huge overhead and impairment charges.

**Ownership & Governance:**  
Insig AI has concentrated ownership, with the largest shareholder Richard Bernstein holding 18.6% plus significant options, indicating tight insider control with aligned incentives but limited broader shareholder influence. Several directors hold shares and options, though some resignations and a director death may impact governance dynamics.

**Auditor Opinion & Material Uncertainty:**  
The auditor report confirms financial statements are fairly presented but highlights a material uncertainty regarding going concern, given the company’s cash burn and funding needs, balanced only by management’s plans for further financing and tax credits.

---

### Conclusion

Insig AI is in a state of significant financial distress characterized by large operating losses driven by impairments and overhead, extremely poor profitability and returns, critical liquidity shortages, negative cash flows, and high financial leverage. Valuation multiples are distorted by low revenue and substantial losses, limiting their usefulness.

The company’s concentrated insider ownership may allow decisive management action but with inherent governance risks. No aggressive accounting gimmicks are apparent, and impairment charges reflect economic realities rather than earnings manipulation.

Investors face high risk due to the precarious cash position and material uncertainty on the company’s ability to continue as a going concern without further financing. Only speculative investment based on a potential turnaround or unforeseen growth prospects would be prudent.

Further documents are adequate for this analysis; no additional files on ownership or financial quality were found in the specified set.

---

Report prepared by: Daniel Osei  
Date: 2025-09-02  
Time: 13:57:56

---

Sources:  
- INSG_agent_ratios.md (full ratio table and assessments)  
- INSG_auditor_report.md (audit opinion, material uncertainty, going concern)  
- INSG_notes.md (ownership details, accounting policies)  
- INSG_income_statement.md (income details)  
- INSG_cashflow_statement.md (cash flow details)  
- INSG_balancesheet_statement.md (key balance sheet figures)  
- INSG_company_ownership.md (director/shareholder interests)