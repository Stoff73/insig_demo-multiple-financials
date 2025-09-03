---

### Insig AI (INSG) Financial Ratios (from data/INSG/INSG_agent_ratios.md)

| Ratio Category       | Ratio                   | Value         | Threshold (Pass/Monitor/Fail)          | Outcome |
|----------------------|-------------------------|---------------|---------------------------------------|---------|
| **Valuation Ratios**  | P/E Ratio               | N/A           | <10 / 10–15 / >15                     | N/A     |
|                      | EV/EBIT                 | 0.0x          | <7 / 7–10 / >10                       | PASS    |
|                      | EV/Revenue              | 42.0x         | >1 / 2–1 / <2                        | PASS    |
|                      | Price to FCF            | N/A           | >15 / 30–15 / <30                     | N/A     |
|                      | FCF Yield               | 0.0%          | >10 / 6–10 / <6                       | FAIL    |
| **Profitability Ratios** | Gross Margin          | 100.0%        | >40 / 30–40 / <30                     | PASS    |
|                      | Operating Margin        | -567.3%       | >15 / 5–15 / <5                       | FAIL    |
|                      | Net Margin              | -4307.7%      | >5 / 0–5 / <0                         | FAIL    |
|                      | ROE                     | -2031.3%      | >10 / 0–10 / <0                       | FAIL    |
|                      | ROCE                    | -157.2%       | >15 / 8–15 / <8                       | FAIL    |
| **Liquidity Ratios**  | Current Ratio           | 0.1%          | >1.5 / 1.0–1.5 / <1.0                 | FAIL    |
|                      | Quick Ratio             | 0.1%          | >1 / 0.5–1 / <0.5                     | FAIL    |
| **Leverage Ratios**  | Debt-to-Equity          | 1.0           | <0.5 / 0.5–1.0 / >1.0                 | MONITOR |
|                      | Interest Coverage       | -16.6x        | >4 / 2–4 / <2                         | FAIL    |
| **Efficiency Ratios** | Inventory Turnover      | 0.0x          | >4 / 2–4 / <2                        | FAIL    |
|                      | Days Sales Outstanding  | 38 days       | <60 / 60–90 / >90                     | PASS    |
| **Earnings Quality**  | Accruals Ratio          | -686.8%       | <10 / 10–20 / >20                     | PASS    |

(Source: data/INSG/INSG_agent_ratios.md)

---

### Key Financials Used in Analysis (from Income Statement, Cash Flow, and Balance Sheet)

| Metric                           | 31 March 2024 (£)   | 31 March 2023 (£)   | Notes                     |
|---------------------------------|---------------------|---------------------|---------------------------|
| **Income Statement**             |                     |                     |                           |
| Revenue                         | 369,860             | 693,734             | data/INSG/INSG_income_statement.md |
| Cost of sales                   | -                   | (50)                |                           |
| Gross profit                   | 369,860             | 693,684             |                           |
| Administrative expenses         | (2,562,208)         | (5,474,077)         |                           |
| Operating loss                 | (17,609,491)         | (21,354,485)        |                           |
| Finance income                 | 263                 | 101                 |                           |
| Finance costs                 | (126,390)           | (80,072)            |                           |
| Loss before tax               | (17,735,618)         | (21,434,456)        |                           |
| Tax credit                    | 1,615,430           | 2,865,865           |                           |
| Loss after tax               | (16,120,188)         | (18,568,591)        |                           |
| Loss attributable to owners    | (15,932,380)         | (18,563,996)        |                           |
| Basic and Diluted EPS (p)  Total | (17.50)p           | (17.88)p            |                           |

| Metric                           | 31 March 2024 (£)   | 31 March 2023 (£)   | Notes                     |
|---------------------------------|---------------------|---------------------|---------------------------|
| **Cash Flow Statement**          |                     |                     |                           |
| Net cash used in operating activities | (299,394)          | (967,195)           |                           |
| Net cash used in investing activities | (832,475)          | (1,465,224)         |                           |
| Net cash generated from financing activities | 889,132          | 2,239,613           |                           |
| Net decrease in cash           | (242,737)           | (192,806)           |                           |
| Cash and cash equivalents (end) | 37,847              | 280,584             |                           |

| Metric                           | 31 March 2024 (£)   | 31 March 2023 (£)   | Notes                     |
|---------------------------------|---------------------|---------------------|---------------------------|
| **Balance Sheet (Consolidated)** |                     |                     |                           |
| Total Assets                  | 4,552,239           | 21,375,616          |                           |
| Current Assets                | 142,587             | 1,000,424           |                           |
| Non-Current Assets            | 4,409,652           | 20,375,192          |                           |
| Total Liabilities             | 2,983,562           | 5,808,046           |                           |
| Current Liabilities           | 1,882,562           | 3,205,082           |                           |
| Non-Current Liabilities       | 1,101,000           | 2,602,964           |                           |
| Net Assets (Equity)            | 1,568,677           | 15,567,570          |                           |
| Share Capital                | 3,149,058           | 3,109,804           |                           |
| Retained Losses              | (42,880,866)        | (26,964,846)        |                           |

(Sources: data/INSG/INSG_income_statement.md, data/INSG/INSG_cashflow_statement.md, data/INSG/INSG_balancesheet_statement.md)

---

### Analysis Summary

**Valuation:**  
Insig AI’s valuation ratios show some concerning signals. The P/E ratio is not available due to the net loss situation. However, the EV/EBIT ratio is reported at 0.0x which technically passes the threshold but this is likely because EBIT is deeply negative, distorting the ratio. The EV/Revenue ratio is at an extremely high 42.0x, which typically flags potential overvaluation versus revenue generating capacity. Free cash flow metrics are not informative as the company has a zero FCF yield and no available Price to FCF ratio.

**Profitability:**  
Profitability metrics are heavily negative. Despite an ideal gross margin of 100% (likely due to little or no cost of sales), the operating margin of -567.3% and net margin of -4307.7% illustrate huge operating losses far exceeding revenues. ROE and ROCE are deeply negative, in the thousands of percentage points negative, highlighting a lack of profitability and capital efficiency.

**Liquidity:**  
Liquidity ratios are significantly below acceptable levels with a current ratio and quick ratio around 0.1, drastically below the pass thresholds of 1.5 and 1.0. This shows potential liquidity risk, meaning the company may struggle to meet short-term obligations.

**Leverage:**  
Debt-to-equity at 1.0 is on the higher end of monitor range, indicating a balanced but watchful stance on leverage. Interest coverage is negative (-16.6x), signifying the company cannot cover interest expenses from operating income, reflecting financial stress.

**Efficiency:**  
Inventory turnover is zero, presumably due to no significant inventory activity, hence failing the threshold for efficiency. However, days sales outstanding at 38 days is acceptable and passes thresholds, indicating decent collections of receivables.

**Earnings Quality:**  
An accruals ratio of -686.8% passing the thresholds suggests that earnings quality may be acceptable from an accrual perspective, but given the overall losses, the quality is overshadowed by magnitude of losses.

**Financial Position and Cash Flows:**  
Insig AI incurred significant losses of over £15 million in FY2024, down from over £18 million in FY2023, with revenues declining also. Operating cash flow remains negative though the net cash used decreased substantially, supported by financing inflows, primarily from equity issuance (£900k) and previous borrowings. The balance sheet shows a heavy decline in net assets from over £15 million to just under £1.6 million, highlighting asset write-downs and retained losses (over £42 million negative retained earnings). Significant intangible impairments (over £15 million) contribute to this.

---

### Conclusion

Based on the financial ratios and statements positioned at fiscal year ending March 31, 2024, Insig AI is demonstrating severe financial distress, with significant operating losses, weak liquidity, negative cash flows from operations, and substantial impairments to assets. While some valuation measures such as EV/EBIT pass thresholds, this is likely due to negative earnings distorting the metric and should be treated cautiously. The very high EV/Revenue multiple is a red flag from a valuation perspective. Low liquidity and negative interest coverage ratios signal potential solvency risks.

Overall, Insig AI’s fundamentals suggest the company is currently overvalued relative to its earnings and cash flow generation capacity, and financially vulnerable. Without a clear path to profitability and improved cash flows, the intrinsic value does not support an investment at current market prices. Additional information such as management’s operational plans, revenue growth projections, and cost restructuring initiatives would be necessary to assess future prospects properly.

---

Victoria Clarke  
Financial Modeling & Valuation Expert  
2025-09-02 17:09:29