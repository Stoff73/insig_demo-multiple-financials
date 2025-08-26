# Rules and Thresholds Management System

## Overview
The Rules and Thresholds Management System allows you to configure, manage, and dynamically update the financial analysis criteria used by the CrewAI agents. Rules can be created, edited, deleted, and assigned to specific tasks.

## Features

### 1. Rule Categories
Rules are organized into five main categories:
- **Valuation Metrics**: EV/EBITDA, P/E Ratio, FCF Yield, EV/EBIT
- **Ownership & Insider Signals**: Insider ownership percentages, recent transactions, activist involvement
- **Earnings Quality**: EBITDA-FCF conversion, accruals ratio, adjusted EBITDA variance
- **Balance Sheet Durability**: Leverage ratios, interest coverage, liquidity, debt maturity
- **Red Flags & Warnings**: Qualitative indicators of potential issues

### 2. Rule Types
- **Quantitative Rules**: Numerical thresholds with operators (<, >, between)
- **Qualitative Rules**: Text-based criteria for subjective assessments
- **Red Flags**: Special rules with severity levels and implications

### 3. Threshold System
Each rule can have three threshold levels:
- **Pass** (Green): Indicates a favorable condition
- **Monitor** (Yellow): Requires attention but not critical
- **Fail** (Red): Indicates a concerning condition

## Using the Web Interface

### Accessing Rules Configuration
1. Navigate to the "Rules & Thresholds" section in the left sidebar
2. Select a category tab to view rules in that category

### Creating a New Rule
1. Click "Add New Rule" button
2. Fill in the rule details:
   - Name and description
   - Metric type (ratio, percentage, qualitative)
   - Threshold values or criteria
   - Optional notes
3. Click "Save" to create the rule

### Editing Existing Rules
1. Click the edit icon on any rule card
2. Modify the rule parameters
3. Save changes

### Assigning Rules to Tasks
1. Click the assignment icon on a rule card
2. Select which tasks should use this rule
3. The rule will automatically be included in the task's analysis

### Enabling/Disabling Rules
- Use the toggle switch on each rule card to enable or disable
- Disabled rules won't be applied during analysis

## API Endpoints

### Get All Rules
```
GET /api/rules
```

### Get Rules by Category
```
GET /api/rules/category/{category}
```

### Get Rules for a Specific Task
```
GET /api/rules/task/{task_name}
```

### Create a New Rule
```
POST /api/rules/{category}/{rule_id}
Body: {
  "name": "Rule Name",
  "description": "Description",
  "category": "valuation",
  "metric_type": "ratio",
  "thresholds": {...},
  "applies_to_tasks": ["task_name"],
  "enabled": true
}
```

### Update a Rule
```
PUT /api/rules/{category}/{rule_id}
```

### Delete a Rule
```
DELETE /api/rules/{category}/{rule_id}
```

### Assign Rule to Task
```
POST /api/rules/{category}/{rule_id}/assign
Body: { "task_name": "primary_ratios" }
```

### Enable/Disable Rule
```
POST /api/rules/{category}/{rule_id}/enable
POST /api/rules/{category}/{rule_id}/disable
```

## Rule Integration with Tasks

When rules are assigned to tasks, they are automatically:
1. Exported to a formatted text that agents can understand
2. Included in the task description
3. Applied during analysis execution

### Example Rule Export for Agents
```markdown
# Rules and Thresholds for primary_ratios

## EV/EBITDA
Description: Core operating cash flow before capital intensity

Thresholds:
  - PASS: < 5.0
  - MONITOR: 5.0 - 7.5
  - FAIL: > 7.5
Notes: Unless growth/cyclic case
```

## Default Rules

The system comes pre-configured with rules based on the phase1_analysis.md document. These include:

### Valuation Rules
- EV/EBITDA: Pass < 5.0x, Monitor 5.0-7.5x, Fail > 7.5x
- P/E Ratio: Pass < 10x, Monitor 10-15x, Fail > 15x
- FCF Yield: Pass > 10%, Monitor 6-10%, Fail < 6%
- EV/EBIT: Pass < 7x, Monitor 7-10x, Fail > 10x

### Ownership Rules
- Insider Ownership: Pass > 10%, Monitor 3-10%, Fail < 3%
- Recent Insider Transactions: Qualitative assessment
- Activist Involvement: Qualitative assessment

### Earnings Quality Rules
- EBITDA-FCF Conversion: Pass > 70%, Monitor 40-70%, Fail < 40%
- Net Income-CFO Conversion: Pass > 1.0, Monitor 0.8-1.0, Fail < 0.8
- Adjusted EBITDA Variance: Pass < 10%, Monitor 10-20%, Fail > 20%
- Accruals Ratio: Pass < 10%, Monitor 10-20%, Fail > 20%

### Balance Sheet Rules
- Net Debt/EBITDA: Pass < 2.5x, Monitor 2.5-3.5x, Fail > 3.5x
- Interest Coverage: Pass > 4.0x, Monitor 2.0-4.0x, Fail < 2.0x
- Liquidity: Pass > 1.5x, Monitor 1.0-1.5x, Fail < 1.0x
- Debt Maturity: Pass < 25%, Monitor 25-40%, Fail > 40%

## Updating Rules When Market Conditions Change

1. Navigate to the Rules & Thresholds page
2. Select the category containing the rule to update
3. Click the edit icon on the rule
4. Adjust thresholds based on new market conditions
5. Save changes
6. The updated rules will be applied in the next analysis run

## Best Practices

1. **Regular Review**: Review and update rules quarterly or when market conditions change significantly
2. **Documentation**: Use the notes field to document why thresholds were set or changed
3. **Testing**: Test new rules on historical data before applying to live analysis
4. **Consistency**: Ensure related rules across categories are consistent
5. **Task Assignment**: Only assign rules to tasks where they're relevant

## Troubleshooting

### Rules Not Appearing in Analysis
- Check if the rule is enabled
- Verify the rule is assigned to the correct task
- Ensure the task configuration has been updated

### Rule Changes Not Taking Effect
- The system may need a restart after significant changes
- Check if the rule was saved successfully
- Verify the analysis_rules.yaml file was updated

### Conflicts Between Rules
- Review overlapping threshold ranges
- Ensure qualitative criteria don't contradict
- Check for duplicate rules in the same category

## Configuration File

Rules are stored in `config/analysis_rules.yaml`. This file:
- Is automatically created on first run
- Can be manually edited (with caution)
- Is backed up before any updates
- Should be version controlled

## Future Enhancements

Planned features include:
- Rule templates for different market conditions
- Historical rule performance tracking
- Automated threshold optimization
- Rule dependency management
- Export/import rule sets
- Rule versioning and rollback