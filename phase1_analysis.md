Many mispricings occur **because conventional metrics fail to reflect true value**.

---

# 1: Valuation Profile — Full Diagnostic Toolkit

## **Primary Ratios (Standard Entry Point)**

| Metric        | What It Captures                                  | When It Fails                                        |
| ------------- | ------------------------------------------------- | ---------------------------------------------------- |
| **EV/EBITDA** | Core operating cash flow before capital intensity | Capital-light SaaS, capex-heavy infra, or distressed |
| **P/E**       | Earnings multiple                                 | Loss-makers, high amortization, exceptional items    |
| **FCF Yield** | Capital return potential                          | Large capex cycles or cyclically depressed           |
| **EV/EBIT**   | True operational profitability                    | Works better than EBITDA in industrials, utilities   |

## **Valuation Pass/Fail Criteria by Method**

| Valuation Method                 | Key Metric(s)            | PASS (Compelling)             | MONITOR (Neutral/Contextual) | FAIL (Avoid/Watchlist)               |
| -------------------------------- | ------------------------ | ----------------------------- | ---------------------------- | ------------------------------------ |
| **EV/EBITDA**                    | LTM and NTM              | < 5.0x                        | 5.0x – 7.5x                  | > 7.5x unless growth/cyclic case     |
| **P/E**                          | LTM, 1Y Forward          | < 10x                         | 10–15x                       | > 15x unless secular growth          |
| **FCF Yield**                    | FCF / EV                 | > 10%                         | 6–10%                        | < 6% or negative FCF                 |
| **EV/EBIT**                      | Operating Profit Base    | < 7x                          | 7–10x                        | > 10x unless margin upside evident   |

---

### Notes on Interpretation

* **Fail ≠ automatic discard**, especially in early screens. If it fails *but other signals scream “mispriced”*, I log it as **watchlist** or seek *alt valuation confirmation*.
* **Monitor = "Prove It" stage**. Usually needs catalyst, insider alignment, or reorg underway.
* **Pass = green light for deeper due diligence**, and if paired with catalysts, moves to deep dive queue.

---

### Additional Failure Filters (Across All Metrics)

| Factor                                   | Immediate Red Flag                       |
| ---------------------------------------- | ---------------------------------------- |
| Declining FCF despite revenue growth     | Unsustainable model or poor cost control |
| Frequent “adjusted EBITDA” with one-offs | Masking structural margin issues         |
| Ballooning working capital or inventory  | Channel stuffing, demand misread         |
| Share count creep without accretive ROI  | Poor capital discipline                  |
| Disclosures inconsistent across filings  | Governance or reporting quality issue    |

## Interpretation Framework

Is the valuation depressed cyclically or structurally broken?
Are we looking at compressed multiples due to fixable issues (e.g., temporary margin pressure), or is it a terminal value trap?

## Checks

Compare against 3-year historical band
Peer comp table (Bloomberg RV function)
Historical reversion analysis

## Team: 

*Victoria Clarke* analysis of the ratios in line with the pass/fail/monitor metrics and produces her report, adjusted for calendarization and IFRS distortions.

## Output

A table showing the metrics, value, pass/fail/monitor saved as primary-ratios.md

---

# 2: Ownership & Insider Signal Layer

---

### **Why It Matters**

1. **Insider skin in the game** → Increases likelihood of shareholder-aligned decisions.
2. **Cluster buying** → Stronger signal than one-off token buys.
3. **Activist activity or new strategic holders** → Indicates potential for change.
4. **Recent insider selling / dilution** → Red flags governance or cash stress.

This is about finding **alignment, intent, and direction of travel**—well before the financials even change.

---

## **Ownership Diagnostic Matrix**

| Dimension                       | What We Examine                         | Thresholds / Red Flags                                                                                                             | Tools & Team                                                 |                       |
| ------------------------------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | --------------------- |
| **Insider Ownership %**         | Aggregate % held by board & execs       | ✅ Pass: >10% <br> ⚠️ Watch: 3–10% <br> 🚫 Fail: <3% unless family or legacy founder                                                | *Bloomberg HDS*, filings, RNS <br> **Victoria Clarke**       |                       |
| **Recent Insider Transactions** | Last 6–12 months’ director buys/sells   | ✅ Pass: Multiple open-market buys, esp. post-earnings <br> 🚫 Fail: Regular option cash-ins or cluster sales                       | *RNS*, *Insider Monkey*, Bloomberg <br> **Sarah van Dijk**   |                       |
| **Ownership Changes (Top 20)**  | Entry/exit of institutions or activists | ✅ Pass: Reputable activist or strategic holding >3% <br> 🚫 Fail: Forced selling, passive outflows, fund liquidation               | *13D/G*, *RNS*, TR-1 forms <br> **Myself + broker networks** |                       |


---

## **Insider Transactions – Signal Dissection**

| Type                                            | Interpretation                                | Signal Strength        |
| ----------------------------------------------- | --------------------------------------------- | ---------------------- |
| **Open-market purchases (non-scheduled)**       | Confidence post-disclosure blackout           | 🔥 Very Strong         |
| **Cluster buying (3+ insiders within weeks)**   | Coordinated confidence, internal optimism     | 🔥 Strong              |
| **New director buys post-appointment**          | Early vote of confidence or deal expectations | 🔥 Strong              |
| **Exercise-and-sell or outright sales**         | Could signal near-term weakness or cash need  | 🚩 Weak / Negative     |
| **Option grants (without performance hurdles)** | Dilutive unless tied to FCF, ROCE, TSR        | 🚩 Neutral to Negative |

---

## **Catalyst Mapping from Ownership Shifts**

| Event                                              | Implication                                          | Action                                          |
| -------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------- |
| New 3–5% stake from activist fund                  | Activism likely imminent                             | Track public statements, possible 13D           |
| PE firm enters at discount                         | Take-private or divestiture play possible            | Watch AGM, cash flow                            |
| Family/founder buying back                         | Potential take-private or undervaluation recognition | Review historical patterns                      |
| Strategic buyer (competitor, supplier) accumulates | Vertical integration or JV ahead                     | Watch for regulatory filings                    |
| Large holder exits quietly                         | Red flag or temporary rebalancing                    | Check fund mandate, cross with sector sentiment |

---

## **Execution Toolkit & Roles**

### Data Sources:

* **Capital IQ** – Instant cap table, changes in real time
* **RNS / TR-1 Forms** – UK’s most valuable resource for tracking stakes
* **Companies House** – For private ownership background checks

### Team Tasks:

* **Sarah van Dijk** → Legal review: poison pills, share class protections, takeover rules
* **Victoria Clarke** → Compiles historical ownership trendline vs. performance
* **Louis Ramirez** → Cross-check incentive structures with governance misalignment

---

## Pass/Fail Threshold Summary

| Signal               | Pass                      | Monitor                   | Fail                           |
| -------------------- | ------------------------- | ------------------------- | ------------------------------ |
| Insider Ownership    | >10%                      | 3–10%                     | <3%                            |
| Recent Buys          | Clustered, open-market    | 1–2 individuals           | None or only option-based      |
| Activist Involvement | Constructive, <12m window | Passive or hostile        | Historic failure, forced exits |
| Incentive Alignment  | Equity tied to ROCE/TSR   | Standard RSUs             | Cash-heavy, short-vesting      |
| Control Structures   | 1 share = 1 vote          | Moderate control layering | Dual-class, poison pill        |

---

## Output

A paragraph, with each signal and pass/monitor/fail on a new line, with a final verdict given for this section

# 3: Earnings Quality & Accounting Risk

**Led by**: *Daniel Osei*, Forensic Accountant
**Supported by**: *Victoria Clarke* (model reconciliation), *Richard Bernstein* (strategic thesis validation)

---

### **Core Objective**

To assess whether reported profits are **sustainable, repeatable, and cash-convertible**—or inflated through:

* Non-cash adjustments
* Accounting tricks
* One-off benefits masked as core earnings
* Overly optimistic accruals or revenue recognition

---

## **Key Metrics and Diagnostic Flags**

| Area                              | Metric / Check                          | PASS (Clean)                      | MONITOR (Questionable)        | FAIL (Red Flag)                            |
| --------------------------------- | --------------------------------------- | --------------------------------- | ----------------------------- | ------------------------------------------ |
| **EBITDA–FCF Conversion**         | FCF / EBITDA                            | >70%                              | 40–70%                        | <40% or negative FCF                       |
| **Net Income–CFO Conversion**     | OCF / Net Income                        | >1.0                              | 0.8–1.0                       | <0.8 = aggressive accruals                 |
| **Recurring vs. Adjusted EBITDA** | Compare mgmt-adjusted to statutory      | <10% difference                   | 10–20%                        | >20% “adjustments”                         |
| **Accruals Ratio**                | (Net Income – CFO) / Assets             | <10%                              | 10–20%                        | >20% = earnings manipulation risk          |
| **One-Off Items**                 | Restructuring, goodwill gains, FX, etc. | Clearly disclosed & non-recurring | Labeled “adjusted” but repeat | Frequent & high materiality                |
| **Capex Trends**                  | Capex / Depreciation                    | 0.8–1.2x                          | 1.2–1.5x or <0.8x             | >1.5x in flat revenue firms                |
| **Working Capital Movements**     | AR, AP, inventory changes               | Matches revenue flow              | Lagged or reverse patterns    | Big build-ups = pre-earnings spike         |
| **Tax Rate Stability**            | Effective tax vs. statutory             | 5–10% variance max                | 10–20%                        | <10% eff. tax or deferred tax ballooning   |
| **Revenue Recognition Method**    | IFRS 15 or GAAP ASC606                  | Match substance over form         | Too early or bundled          | % completion w/o proof or channel stuffing |
| **Segment Consistency**           | Segment profit consistency over years   | Stable margin and disclosures     | Minor inconsistencies         | Frequent restatements or segment hiding    |

---

### **Daniel Osei’s Forensic Playbook**

1. **Audit Segment-Level P\&L Trends**

   * Look for sudden profitability shifts, new “Other” line items
   * Segment reporting opacity = often a smokescreen

2. **Reconcile Management Adjusted Figures**

   * Map bridge from IFRS/GAAP to adjusted EBITDA
   * Flag any “one-off” items appearing in 3+ consecutive periods

3. **Review Working Capital Build-Up**

   * Inventory spikes without sales = demand overstatement
   * DSO (Days Sales Outstanding) trending up = aggressive revenue

4. **Examine Capitalization Practices**

   * Is R\&D or software development being capitalized too aggressively?
   * Are lease liabilities or pension obligations buried off-B/S?

5. **Assess Auditor Quality & Tenure**

   * Big 4 with long tenure: ⚠️ entrenchment risk
   * Mid-tier + sudden changes: 🚩 concealment risk

---

### **Source Documents Used**

* Full Annual Report (especially Notes to Financials)
* MD\&A (Management Discussion & Analysis)
* Segmental Data
* Remuneration Report (to understand earnings-linked incentives)
* Auditor Report (incl. key risk areas)
* Governance Disclosures (for red flag crosschecks)

---

## Common Red Flags by Category

| Category                  | Red Flag                                           | Implication                                                |
| ------------------------- | -------------------------------------------------- | ---------------------------------------------------------- |
| **Cash Flow**             | Low EBITDA-to-FCF                                  | EBITDA overstated or capex too high                        |
| **Revenue Quality**       | % of revenue from related parties or bundled deals | Likely manipulation                                        |
| **Expense Normalisation** | “One-offs” every quarter                           | Operational underperformance                               |
| **Tax Strategy**          | Deferred tax assets growing faster than earnings   | Unsustainable earnings or tax loss carryforward dependence |
| **Inventory Swells**      | +15% YoY inventory w/ flat revenue                 | Channel stuffing                                           |
| **Frequent Adjustments**  | EBIT adjustments >20% of base                      | Earnings window-dressing                                   |
| **Pension Assumptions**   | Unusual discount rate or return assumption         | Artificially boosting net income                           |
| **Audit Flag**            | Going concern language or scope limitations        | Material financial risk                                    |

---

## Pass/Fail Threshold Summary

| Signal Type               | Pass                         | Monitor                | Fail                    |
| ------------------------- | ---------------------------- | ---------------------- | ----------------------- |
| Earnings vs. Cash Flow    | FCF/EBITDA > 70%             | 40–70%                 | < 40%                   |
| Adjusted EBITDA Integrity | Adjustments < 10% of total   | 10–20%                 | > 20% recurring         |
| Revenue Recognition       | Substance-aligned, disclosed | Minor bundling         | % completion w/o assets |
| Segment Profit Quality    | Transparent & consistent     | Some realignment       | Frequent restatements   |
| Auditor Notes             | No material flags, Big 4     | Risk flagged, mid-tier | Scope limits, churn     |

---

## Output

A table, showing all the metrics with the pass/monitor/fail status and values, with final verdict at the end being either **sustainable, repeatable, and cash-convertible**—or inflated through:

* Non-cash adjustments
* Accounting tricks
* One-off benefits masked as core earnings
* Overly optimistic accruals or revenue recognition

---

# 4: Balance Sheet Durability

**Led by**: *Daniel Osei* (Forensic Accountant)
**Supported by**: *Victoria Clarke* (model implications) and *Richard Bernstein* (strategic funding scenario)

---

### **Core Objective**

To determine whether the company has:

* **Sufficient liquidity** to operate and invest
* **Sustainable leverage** to manage downturns
* **Low refinancing or default risk**
* **Transparent liabilities**, including pensions and leases

---

## **Durability Metrics & Stress Tests**

| Category                       | Metric / Test                        | PASS                                     | MONITOR                         | FAIL                                   |
| ------------------------------ | ------------------------------------ | ---------------------------------------- | ------------------------------- | -------------------------------------- |
| **Leverage**                   | Net Debt / EBITDA                    | < 2.5x                                   | 2.5–3.5x                        | > 3.5x or negative EBITDA              |
| **Interest Coverage**          | EBIT / Interest Expense              | > 4.0x                                   | 2.0–4.0x                        | < 2.0x                                 |
| **Liquidity**                  | Cash + undrawn RCF / 12m obligations | > 1.5x                                   | 1.0–1.5x                        | < 1.0x                                 |
| **Maturity Profile**           | % of debt due within 24 months       | < 25%                                    | 25–40%                          | > 40%                                  |
| **Refinancing Risk**           | Credit rating, bank group stability  | Investment grade or stable banking lines | Non-rated or bank concentration | No disclosed facility, covenant breach |
| **Working Capital Volatility** | YoY change in WC / revenue           | < 5%                                     | 5–10%                           | > 10% or negative WC cycle             |
| **Pension Deficit**            | Net liability as % of equity         | < 10%                                    | 10–25%                          | > 25% or funding holiday               |
| **Lease Adjustments**          | IFRS 16 adjustments consistent?      | Yes, stable                              | Minor variance                  | Increasing fast or inconsistent        |
| **Asset Backing**              | Tangible assets / Total assets       | > 50%                                    | 30–50%                          | < 30% (IP-heavy or goodwill masking)   |

---

## **Balance Sheet Red Flag Checklist**

| Red Flag                                       | Implication                                       |
| ---------------------------------------------- | ------------------------------------------------- |
| Ballooning net debt vs. flat EBITDA            | Growth without returns, or unsustainable leverage |
| Negative working capital with slow revenue     | Cash stress likely in downturns                   |
| High interest burden from legacy debt          | Needs refinancing catalyst                        |
| Off-balance sheet items (JVs, leases) material | Masking true leverage                             |
| Non-cash interest or PIK debt                  | Delayed pain—risk of sudden cash call             |
| Covenant-heavy debt structure                  | Limits flexibility and future capex               |
| Constant equity raises or convertibles         | Signals structural cash shortfall                 |

---

### **Daniel Osei’s Forensic Tasks**

1. **Debt Breakdown**

   * By tranche, interest rate, maturity, covenants
   * Identify bullets vs. amortizing structure
   * Check if debt tied to specific assets (ring-fenced or enterprise-wide)

2. **Covenant Exposure**

   * Examine RCF or term loan agreements for EBITDA/net debt, fixed charge coverage, or liquidity tests
   * Flag any risk of breach given projected figures

3. **Pension & Lease Review**

   * Assess actuarial assumptions: discount rate, growth, mortality
   * IFRS 16 lease treatment: Right-of-use assets vs liabilities

4. **Contingent Liabilities**

   * Look for legal provisions, guarantees, environmental costs, tax disputes
   * Often buried in footnotes or interim disclosures

5. **Asset Quality Check**

   * Goodwill to total assets: >30% = impairment risk
   * PP\&E composition: Is it truly productive or outdated?

---

## **Team Inputs & Data Sources**

| Source                              | Description                                                 |
| ----------------------------------- | ----------------------------------------------------------- |
| **Annual Report**                   | Full financials, notes on borrowings, pensions, provisions  |
| **RNS Announcements**               | Updates on credit lines, debt refinancing, covenant waivers |
| **Capital IQ**                      | Quick leverage and liquidity snapshot                       |
| **Debt Prospectus (if applicable)** | Covenant language and credit structure                      |
| **Auditor Notes**                   | Warnings on going concern or debt viability                 |
| **Banking Facilities Note**         | Check for expiry, covenants, drawdowns                      |

---

## Pass/Fail Summary for Balance Sheet

| Test                         | PASS   | MONITOR  | FAIL   |
| ---------------------------- | ------ | -------- | ------ |
| Net Debt / EBITDA            | < 2.5x | 2.5–3.5x | > 3.5x |
| Interest Cover               | > 4.0x | 2.0–4.0x | < 2.0x |
| Debt Maturity (2yr)          | < 25%  | 25–40%   | > 40%  |
| Liquidity Coverage           | > 1.5x | 1.0–1.5x | < 1.0x |
| Pension Deficit / Equity     | < 10%  | 10–25%   | > 25%  |
| FCF Coverage of Debt Service?| > 100% | 80–100%  | < 80%  |
| Goodwill / Assets            | < 30%  | 30–50%   | > 50%  |

---

## Output

A table showing all metrics, values and pass/monitor/fail values as above.

---

# 5: Initial Investment Snapshot — Deep Construction Protocol

**Owner**: *Richard Bernstein*
**Collaborators**: *Victoria Clarke (financial snapshot)*, *Daniel Osei (accounting filter)*, *Alexei Popov (sentiment scrape, if used)*

---

### **Purpose**

* Codify why the stock is being considered now
* Highlight mispricing signals (valuation, sentiment, catalysts)
* Flag red flags and required further work
* Force clarity: **Pass / Watch / Advance** decision
* It’s **not** a full investment memo—it’s the *last gate before we commit team resources* to a full deep dive.

---

## **Snapshot Document Structure (Standard Template)**

| Section                        | Content                                                         | Detail                                                                                                                  |
| ------------------------------ | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Header**                     | Company name, ticker, share price, market cap, sector, exchange | Use Insig for consistency                                                                                   |
| **Thesis Hook (2–3 lines)**    | “Why now?” summary of mispricing, catalyst, and conviction      | E.g., “Post-reorg industrial with new CEO trading at 4.5x EBITDA and 15% FCFY—market still anchored to 2023 loss year.” |
| **Valuation Snapshot**         | P/E, EV/EBITDA, FCF yield vs. sector median + historical band   | Charts or simple 3-column comp table from *Victoria Clarke*                                                             |
| **Balance Sheet Summary**      | Net debt / EBITDA, interest cover, pension liability            | Flag any refinancing risk or cash burn                                                                                  |
| **Insider/Ownership Angle**    | Insider buying, activist entries, ownership trends              | From RNS, Bloomberg, *Sarah van Dijk*                                                                                   |
| **Narrative Dislocation**      | Market perception vs. operating reality                         | One paragraph, qualitative + data signals (*Alexei Popov*)                                                              |
| **Catalyst Map (3–12 months)** | Earnings, AGM, divestment, refi, CEO move, regulatory decision  | Date-driven timeline with confidence scores                                                                             |
| **Known Red Flags**            | Accounting, governance, cash, litigation, cyclicality           | From *Daniel Osei*, highlight forensic alerts                                                                           |
| **Summary Rating**             | 🟢 Advance (Deep Dive) <br> 🟡 Watch & Wait <br> 🔴 Pass        | Final judgement based on risk-reward profile                                                                            |

---

## **Scoring Methodology Embedded in Snapshot**

Each candidate is scored across **five vectors** using a traffic light system:

| Vector                     | Green (🟢)                                 | Amber (🟡)               | Red (🔴)                      |
| -------------------------- | ------------------------------------------ | ------------------------ | ----------------------------- |
| Valuation                  | >30% discount vs. peers                    | 10–30%                   | <10% or fully valued          |
| Quality of Earnings        | High FCF conversion, clean adjustments     | Some noise               | Material red flags            |
| Insider / Ownership Signal | Cluster buys, >10% board holding, activist | Neutral                  | Selling, dilution, no skin    |
| Balance Sheet Durability   | Net debt < 2.5x, >4x interest cover        | Manageable but leveraged | Stress risk or funding need   |
| Narrative Dislocation      | Deep market misread + near-term trigger    | Midterm or lagging       | No clear misread or priced in |

**→ Total scoring determines "Advance / Monitor / Pass" call**

---

## **Sources Integrated**

* **Capital IQ**: Price, volume, metrics, peer table
* **RNS / Company Filings**: Insider trades, director bios, guidance
* **Annual Report**: Notes for leases, pensions, segmental views
* **Earnings Calls / Transcripts**: Tone, strategy, alignment
* **Alexei’s NLP model**: Optional sentiment/trend layer
* **Sell-Side Notes**: For consensus view vs. internal outlook

---

## **Workflow**

1. **Richard initiates snapshot** after initial filter hits
2. **Victoria** inputs financials, comps, FCF metrics
3. **Daniel** flags any accounting alerts or non-cash distortion
4. **Alexei (if required)** adds sentiment divergence table
5. **Richard completes** narrative + catalyst map
6. Snapshot reviewed in internal meeting or async via Slack/Dropbox

---

## Output Format

* **1–2 Page PDF/Word snapshot**
* **Filed as intialscreenreport_{date}_{company}.md**
* **Version-controlled for iteration if Watchlisted**
