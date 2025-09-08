---

### Table 1: Key Financial Ratios Used in Analysis (Source: data/SPI/SPI_agent_ratios.md)

| Ratio Category       | Ratio                  | Value     | Threshold (Pass/Monitor/Fail) | Outcome  |
|---------------------|------------------------|-----------|-------------------------------|----------|
| **Valuation Ratios** | P/E Ratio              | 17.1x     | <10.0 / 10.0-15.0 / >15.0     | FAIL     |
|                     | EV/EBITDA              | 8.5x      | <5.0 / 5.0-7.5 / >7.5         | FAIL     |
|                     | EV/EBIT                | 15.4x     | <7.0 / 7.0-10.0 / >10.0       | FAIL     |
|                     | EV/Revenue             | 0.7x      | >1.0 / 2.0-1.0 / <2.0         | FAIL     |
|                     | Price to FCF           | 3.5x      | >15.0 / 30.0-15.0 / <30.0     | FAIL     |
|                     | FCF Yield              | 28.4%     | >10.0 / 6.0-10.0 / <6.0       | PASS     |
| **Profitability**    | Gross Margin           | 45.2%     | >40.0 / 30.0-40.0 / <30.0     | PASS     |
|                     | Operating Margin       | 9.4%      | >15.0 / 5.0-15.0 / <5.0       | MONITOR  |
|                     | Net Margin             | 1.7%      | >5.0 / 0.0-5.0 / <0.0         | MONITOR  |
|                     | ROE                    | 6.8%      | >10.0 / 0.0-10.0 / <0.0       | MONITOR  |
|                     | ROCE                   | 6.8%      | >15.0 / 8.0-15.0 / <8.0       | FAIL     |
| **Liquidity**        | Current Ratio          | 0.7       | >1.5 / 1.0-1.5 / <1.0         | FAIL     |
|                     | Quick Ratio            | 0.5       | >1.0 / 0.5-1.0 / <0.5         | MONITOR  |
| **Leverage**         | Debt-to-Equity         | 1.7       | <0.5 / 0.5-1.0 / >1.0         | FAIL     |
|                     | Interest Coverage      | 0.7x      | >4.0 / 2.0-4.0 / <2.0         | FAIL     |
|                     | Net Debt/EBITDA        | 5.0       | <2.5 / 2.5-3.5 / >3.5         | FAIL     |
| **Efficiency**       | Inventory Turnover     | 35.5x     | >4.0 / 2.0-4.0 / <2.0         | PASS     |
|                     | Days Sales Outstanding | 9 days    | <60.0 / 60.0-90.0 / >90.0     | PASS     |
| **Earnings Quality** | Accruals Ratio         | -17.9%    | <10.0 / 10.0-20.0 / >20.0     | PASS     |
|                     | EBITDA to FCF Conversion | 99.3%   | >70.0 / 40.0-70.0 / <40.0     | PASS     |
|                     | Adjusted vs Statutory Gap | 0.0    | <10.0 / 10.0-20.0 / >20.0     | PASS     |
| **Asset Quality**    | Goodwill/Assets        | 17.6%     | <30.0 / 30.0-50.0 / >50.0     | PASS     |
|                     | Capex/Depreciation     | 0.0       | 0.8-1.2 / <0.8 or >1.2 / >1.5 | MONITOR  |
|                     | Tangible Book Value    | £308.8m   | >50.0 / 0.0-50.0 / <0.0       | PASS     |
| **Cash Flow**        | Cash Conversion        | 9.3       | >1.0 / 0.8-1.0 / <0.8         | PASS     |
|                     | Free Cash Flow         | £123.6m   | >0.0 / 5.0-0.0 / <5.0         | PASS     |

---

### Table 2: Key Financial Information from Financial Statements (Source: data/SPI folder)

| Metric                          | 2024 (£m)       | 2023 (£m)       | Source File                  |
|--------------------------------|-----------------|-----------------|------------------------------|
| **Income Statement**            |                 |                 | SPI_income_statement.md       |
| Revenue                        | 1,511.2         | 1,359.0         | Income Statement, line 7      |
| Cost of Sales                 | (827.6)         | (734.8)         | Income Statement, line 8      |
| Gross Profit                  | 683.6           | 624.2           | Income Statement, line 9      |
| Operating Profit (EBIT)       | 137.5           | 126.2           | Income Statement, line 13     |
| Profit Before Tax             | 38.3            | 34.6            | Income Statement, line 18     |
| Profit for the Year           | 26.0            | 27.9            | Income Statement, line 22     |
| Basic EPS (pence)             | 6.3             | 6.8             | Income Statement, line 26     |
| **Cash Flow Statement**         |                 |                 | SPI_cashflow_statement.md     |
| Net Cash from Operating Activities | 235.7       | 215.5           | Cash Flow Statement, line 7   |
| Net Cash Used in Investing Activities | (99.0)    | (157.2)         | Cash Flow Statement, line 15  |
| Net Cash Used in Financing Activities | (145.1)   | (82.9)          | Cash Flow Statement, line 27  |
| Net Increase/(Decrease) in Cash | (8.4)          | (24.6)          | Cash Flow Statement, line 31  |
| Cash and Cash Equivalents at Year End | 41.2      | 49.6            | Cash Flow Statement, line 34  |
| **Balance Sheet (Consolidated)** |                 |                 | SPI_balancesheet_statement.md |
| Total Assets                 | 2,343.2         | 2,288.1         | Balance Sheet, line 26         |
| Total Equity                 | 746.2           | 737.8           | Balance Sheet, line 38         |
| Total Liabilities            | 1,597.0         | 1,550.3         | Balance Sheet, line 37         |
| Net Debt (Bank borrowings + Lease liabilities - Cash) | 1,237.7 (363.5+811.0+101.8+3.6 - 41.2) | 1,207.0 (361.9+793.3+98.4+3.4 - 49.6) | Calculated from Balance Sheet |
| Share Capital                | 4.0             | 4.0             | Balance Sheet, line 29         |
| Share Premium                | 830.0           | 830.0           | Balance Sheet, line 30         |

---

### Analysis Summary

**Valuation Ratios:** Spire Health's valuation multiples such as P/E (17.1x), EV/EBITDA (8.5x), and EV/EBIT (15.4x) are above the thresholds for a "pass," indicating the stock is relatively expensive compared to typical valuation benchmarks. The EV/Revenue ratio is low at 0.7x, which is below the pass threshold, suggesting the market values the company at less than one times revenue, which is unusual and may reflect market concerns or sector-specific factors. The Price to Free Cash Flow ratio is very low at 3.5x, which is a fail by the thresholds but the Free Cash Flow Yield is very strong at 28.4%, indicating the company generates significant cash relative to its market price, a positive sign for investors.

**Profitability:** Gross margin is strong at 45.2%, indicating good control over cost of sales. Operating margin at 9.4% and net margin at 1.7% are moderate and flagged as monitor, suggesting some pressure on profitability possibly from operating costs or finance costs. Return on Equity (6.8%) and Return on Capital Employed (6.8%) are below desired levels, indicating moderate returns on invested capital.

**Liquidity:** The current ratio of 0.7 and quick ratio of 0.5 indicate liquidity concerns, as the company has less than one times current assets to cover current liabilities, which could be a risk factor for short-term obligations.

**Leverage:** Debt-to-equity ratio of 1.7 and net debt/EBITDA of 5.0x indicate high leverage, which is a risk factor. Interest coverage ratio of 0.7x is very low, suggesting the company struggles to cover interest expenses from operating earnings, a significant red flag.

**Efficiency:** Inventory turnover is very high at 35.5x and days sales outstanding is low at 9 days, indicating efficient management of working capital.

**Earnings Quality:** Accruals ratio is negative (-17.9%), EBITDA to FCF conversion is very high (99.3%), and adjusted vs statutory gap is zero, all indicating high quality and reliability of earnings and cash flows.

**Asset Quality:** Goodwill to assets ratio is moderate at 17.6%, tangible book value is strong at £308.8m, and capex to depreciation ratio is zero (monitor), suggesting capital expenditure may be low relative to depreciation, which could impact future asset base.

**Cash Flow:** Cash conversion ratio is very strong at 9.3, and free cash flow is positive at £123.6m, supporting the strong FCF yield and indicating good cash generation.

---

### Conclusion

Spire Health demonstrates strong cash flow generation and efficient working capital management, with high-quality earnings and a solid gross margin. However, the company faces challenges with profitability margins, liquidity, and high leverage, as evidenced by low interest coverage and high debt ratios. The valuation multiples suggest the market prices the company at a premium on earnings but a discount on revenue, reflecting mixed investor sentiment possibly due to financial risk concerns.

The strong free cash flow yield and cash conversion ratios are positives, indicating potential undervaluation from a cash flow perspective, but the financial risk from leverage and liquidity constraints warrants caution.

Overall, Spire Health appears to be a company with solid operational cash flow but financial risk concerns that may limit upside without deleveraging or margin improvement. Investors should monitor leverage reduction and profitability improvements to justify valuation multiples.

---

Victoria Clarke  
Financial Modeling & Valuation Expert  
2025-09-08 06:33:45