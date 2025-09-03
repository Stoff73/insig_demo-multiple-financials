```
Ratios Used in Analysis (from data/INSG/INSG_agent_ratios.md):

| Category            | Ratio                      | Value         | Threshold (Pass/Monitor/Fail)        | Outcome |
|---------------------|----------------------------|--------------|------------------------------------|---------|
| Valuation Ratios    | P/E Ratio                  | N/A          | <10.0 / 10.0-15.0 / >15.0          | N/A     |
|                     | EV/EBIT                   | 0.0x         | <7.0 / 7.0-10.0 / >10.0             | PASS    |
|                     | EV/Revenue                | 42.0x        | >1.0 / 2.0-1.0 / <2.0               | PASS    |
|                     | Price to FCF              | N/A          | >15.0 / 30.0-15.0 / <30.0           | N/A     |
|                     | FCF Yield                 | 0.0%         | >10.0 / 6.0-10.0 / <6.0             | FAIL    |
| Profitability Ratios | Gross Margin              | 100.0%       | >40.0 / 30.0-40.0 / <30.0           | PASS    |
|                     | Operating Margin          | -567.3%      | >15.0 / 5.0-15.0 / <5.0             | FAIL    |
|                     | Net Margin                | -4307.7%     | >5.0 / 0.0-5.0 / <0.0               | FAIL    |
|                     | ROE                      | -2031.3%     | >10.0 / 0.0-10.0 / <0.0             | FAIL    |
|                     | ROCE                     | -157.2%      | >15.0 / 8.0-15.0 / <8.0             | FAIL    |
| Liquidity Ratios    | Current Ratio             | 0.1%         | >1.5 / 1.0-1.5 / <1.0               | FAIL    |
|                     | Quick Ratio               | 0.1%         | >1.0 / 0.5-1.0 / <0.5               | FAIL    |
| Leverage Ratios     | Debt-to-Equity            | 1.0          | <0.5 / 0.5-1.0 / >1.0               | MONITOR |
|                     | Interest Coverage         | -16.6x       | >4.0 / 2.0-4.0 / <2.0               | FAIL    |
| Efficiency Ratios   | Inventory Turnover        | 0.0x         | >4.0 / 2.0-4.0 / <2.0               | FAIL    |
|                     | Days Sales Outstanding    | 38 days      | <60.0 / 60.0-90.0 / >90.0           | PASS    |
| Earnings Quality    | Accruals Ratio            | -686.8%      | <10.0 / 10.0-20.0 / >20.0           | PASS    |
|                     | EBITDA to FCF Conversion  | 0.0          | >70.0 / 40.0-70.0 / <40.0           | FAIL    |
|                     | Adjusted vs Statutory Gap | -0.0         | <10.0 / 10.0-20.0 / >20.0           | PASS    |
| Asset Quality      | Goodwill/Assets           | 0.0          | <30.0 / 30.0-50.0 / >50.0           | PASS    |
|                     | Capex/Depreciation        | 0.0          | 0.8-1.2 / <0.8 or >1.2 / >1.5       | MONITOR |
|                     | Tangible Book Value       | £-2.8m       | >50.0 / 0.0-50.0 / <0.0             | FAIL    |
| Cash Flow Ratios    | Cash Conversion           | -0.0         | >1.0 / 0.8-1.0 / <0.8               | FAIL    |
|                     | Free Cash Flow            | £-1.3m       | >0.0 / 5.0-0.0 / <5.0               | FAIL    |


Financial Information Used in Analysis (from data/INSG folder):

| Financial Metric                       | Value (Year ended 31 March 2024) | Previous Year (31 March 2023) |
|--------------------------------------|---------------------------------|------------------------------|
| Revenue                             | £369,860                        | £693,734                    |
| Cost of sales                       | £0 (note minor previous year)  | (£50)                        |
| Gross profit                       | £369,860                       | £693,684                    |
| Administrative expenses             | (£2,562,208)                   | (£5,474,077)                |
| Other gains/(losses)                | (£102,965)                     | (£15,796)                   |
| Other income                       | £3,160                        | £0                          |
| Impairments                       | (£15,317,338)                   | (£16,558,296)               |
| Operating loss                     | (£17,609,491)                   | (£21,354,485)               |
| Finance income                    | £263                          | £101                        |
| Finance costs                    | (£126,390)                    | (£80,072)                   |
| Loss before income tax             | (£17,735,618)                  | (£21,434,456)               |
| Tax credit/(charge)                | £1,615,430                    | £2,865,865                  |
| Loss for the year after income tax| (£16,120,188)                 | (£18,568,591)               |
| Profit from discontinued operations| £210,085                     | £6,245                      |
| Group loss for the year            | (£15,910,103)                 | (£18,562,346)               |
| Basic and diluted loss per share   | (17.50)p                      | (17.88)p                   |
| Cash and cash equivalents (end)   | £37,847                       | £280,584                    |
| Net cash used in operating activities| (£299,394)                 | (£967,195)                  |
| Net cash used in investing activities| (£832,475)                 | (£1,465,224)                |
| Net cash generated from financing activities| £889,132            | £2,239,613                  |
| Net decrease in cash and equivalents| (£242,737)                   | (£192,806)                  |


Analysis Summary:

Valuation Metrics:
- The EV/EBIT ratio of 0.0x and EV/Revenue of 42.0x indicate a very low valuation relative to EBIT (likely due to very negative EBIT) but a high multiple on revenue, reflecting very low profitability and a potentially overvalued revenue multiple or uncertainty on earnings. P/E ratios are not available, likely due to net losses.
- Free cash flow metrics fail with a 0.0% FCF yield and negative free cash flow, showing the company is not generating free cash flow.

Profitability:
- Although Insig AI shows a strong gross margin of 100%, administrative expenses and impairments lead to a very high operating loss margin (-567.3%) and net margin (-4307.7%). Return on equity (ROE) and return on capital employed (ROCE) are deeply negative, showing no profitability.
- The losses are consistent with an early-stage or heavily investing technology company with high impairments and operating losses.

Liquidity and Leverage:
- Liquidity ratios are critically poor, with a very low current ratio (0.1%) and quick ratio (0.1%), indicating potential short-term financial distress or reliance on short-term financing.
- Debt-to-equity at 1.0 is at the monitor threshold, suggesting moderate leverage, but interest coverage is negative (-16.6x), showing inability to cover interest expenses from earnings.

Efficiency:
- Inventory turnover is 0.0x, failing the efficiency test, which is expected for a technology company with likely negligible inventory.
- Days sales outstanding at 38 days is a positive, healthy metric reflecting reasonable collection times.

Earnings Quality and Asset Quality:
- Despite heavy losses, accruals ratios and adjusted vs statutory gaps pass, indicating reasonable quality of accounting.
- Asset quality is weak with negative tangible book value (£-2.8m), but with no goodwill impairment concerns.

Cash Flow:
- Cash conversion and free cash flow both fail, confirming the company is burning cash.
- Net cash used in operating and investing activities greatly exceeds cash generated from financing, reflecting heavy capital requirements.

Conclusion:
Insig AI is currently in a distressed financial position with large operating losses, negative margins, poor liquidity, and negative cash flow from operations. Although valuation ratios such as EV/EBIT appear attractive due to large negative EBIT, this reflects deep underlying fundamental weakness. The company is not generating free cash flow and relies heavily on financing activities for liquidity. Profitability is nonexistent, and returns on equity and capital employed are deeply negative. The strong gross margin is overshadowed by the high administrative expenses and impairments. The company also carries moderate leverage with poor interest coverage, which is a risk.

Overall, the financial fundamentals indicate that Insig AI is significantly overvalued relative to its current earnings and cash flow performance, and it faces severe liquidity and profitability challenges. Investors should monitor closely for turnaround signs or increased risks of capital raising and operational restructuring. Insig AI's valuation and ratios suggest it is an early-stage technology firm with high cash burn and losses, requiring further operational improvements and capital infusion for viability.

No additional documents are necessary as all required financials and ratios were available.

Victoria Clarke  
2025-09-02 14:08:54
```