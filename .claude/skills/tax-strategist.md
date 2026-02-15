# Tax Strategist Skill

## Description
Manage tax planning, track quarterly estimates, monitor deductions, and ensure LLC compliance using the LLC Ops Server.

## When to Use This Skill
- Planning quarterly estimated tax payments
- Tracking tax deadlines
- Categorizing business expenses for deductions
- Managing compliance requirements
- Preparing for tax season
- Organizing business documents

## MCP Servers Used
- **llc_ops_server**: Primary server for tax and compliance
- **billing_server**: For revenue and expense data
- **client_server**: For 1099 tracking

## Step-by-Step Instructions

### 1. Entity Management
Set up and maintain LLC information:

```
1. Update entity info using update_entity_info()
2. Include:
   - LLC name and EIN
   - State of formation
   - Business address
   - Formation date
   - Tax classification
3. Keep information current
4. Review annually
```

**Example Prompts:**
- "Update LLC entity information with my EIN"
- "Set LLC state registration to Delaware"
- "Show me current entity information"

### 2. Tax Deadline Tracking
Stay on top of tax obligations:

```
1. Get tax deadlines using get_tax_deadlines()
2. Review upcoming quarterly estimates
3. Mark deadlines on calendar
4. Set reminders 2 weeks before due dates
5. Complete tax items on time
6. Track completed vs pending
```

**Example Prompts:**
- "What are my upcoming tax deadlines?"
- "Show me Q2 estimated tax deadline"
- "Which tax deadlines have I missed?"

**Key Dates:**
- **April 15**: Q1 estimate + prior year return
- **June 15**: Q2 estimate
- **September 15**: Q3 estimate
- **January 15**: Q4 estimate (following year)

### 3. Quarterly Tax Estimates
Calculate and pay estimated taxes:

```
1. Use calculate_quarterly_estimate()
2. Provide projected revenue and expenses
3. Review calculation breakdown:
   - Self-employment tax (15.3%)
   - Income tax (based on tax rate)
   - Total quarterly payment
4. Make payment to IRS and state
5. Document payment confirmation
6. Update records
```

**Example Prompts:**
- "Calculate Q2 estimated tax with $45,000 revenue and $12,000 expenses"
- "What should my Q3 tax estimate be?"
- "Show me tax calculation for this quarter"

**Calculation Components:**
```
Net Income = Revenue - Expenses
SE Tax Base = Net Income × 92.35%
SE Tax = SE Tax Base × 15.3%
Income Tax = Net Income × Tax Rate
Quarterly Payment = (SE Tax + Income Tax) / 4
```

### 4. Expense Categorization
Track deductible business expenses:

```
1. Record expenses via billing_server
2. Categorize by IRS categories
3. Keep receipts and documentation
4. Track billable vs non-billable
5. Review monthly for accuracy
6. Ensure proper allocation
```

**Example Prompts:**
- "List all expenses for this tax year"
- "Show expenses by category for Q2"
- "What are my deductible software expenses?"

**Major Deduction Categories:**
- Home office (if qualified)
- Equipment and supplies
- Software and subscriptions
- Professional development
- Insurance
- Legal and professional fees
- Travel and meals (with limits)

### 5. Compliance Management
Track required filings and compliance:

```
1. Add compliance items using add_compliance_item()
2. Set due dates and priorities
3. Review checklist regularly
4. Complete items on time
5. Document completion
6. Handle recurring items
```

**Example Prompts:**
- "Add annual LLC filing requirement for my state"
- "Show compliance checklist for this quarter"
- "Mark state business license renewal as complete"

### 6. Document Management
Organize business and tax documents:

```
1. Upload documents using upload_document()
2. Categorize by type:
   - Contracts
   - W-9s
   - 1099s
   - Tax returns
   - Business licenses
3. Tag by year and client
4. Keep organized and accessible
```

**Example Prompts:**
- "Register contract with AcmeCorp dated 2024-03-15"
- "List all 1099 forms for 2023 tax year"
- "Show documents for tax filing"

## Tax Planning Strategies

### Throughout the Year

**Quarterly Actions:**
- Calculate and pay estimates
- Review income and expenses
- Adjust withholding if needed
- Track deductible purchases
- Save receipts digitally

**Monthly Actions:**
- Categorize all expenses
- Review profit margins
- Set aside tax savings (30-35%)
- Update financial projections
- Track mileage if applicable

### Year-End Tax Moves

**Timing Income:**
- Delay December invoicing to January (if beneficial)
- Accelerate receivables if lower tax bracket

**Accelerating Deductions:**
- Purchase needed equipment before December 31
- Pay January expenses in December
- Prepay insurance or subscriptions
- Make retirement contributions

**Documentation:**
- Organize all receipts
- Reconcile bank statements
- Prepare 1099s for contractors
- Gather tax forms

## Major Tax Deductions for Freelancers

### Home Office Deduction

**Requirements:**
- Regular and exclusive business use
- Principal place of business

**Two Methods:**
1. **Simplified**: $5/sq ft (max 300 sq ft = $1,500)
2. **Actual Expense**: Percentage of home expenses

**Deductible Home Expenses:**
- Mortgage interest/rent
- Property taxes
- Utilities
- Insurance
- Repairs and maintenance

### Vehicle Expenses

**Two Methods:**
1. **Standard Mileage**: $0.655/mile (2023 rate)
2. **Actual Expenses**: Gas, insurance, repairs × business %

**Documentation Required:**
- Business mileage log
- Trip purpose
- Start/end locations
- Odometer readings

### Health Insurance

- Self-employed health insurance deduction
- 100% deductible if:
  - You're not eligible for employer plan
  - Business shows profit
  - For yourself, spouse, dependents

### Retirement Contributions

- **Solo 401(k)**: Up to $66,000 (2023)
- **SEP IRA**: Up to 25% of net self-employment income
- **Traditional IRA**: Up to $6,500 ($7,500 if 50+)

### Professional Development

- Courses and training
- Industry conferences
- Books and publications
- Certifications
- Professional memberships

### Technology & Equipment

- Computer and peripherals
- Software subscriptions
- Phones and service
- Internet service (business %)
- Office furniture and equipment

## Tax Rate Planning

### Self-Employment Tax

**15.3% of net self-employment income:**
- 12.4% Social Security (on first $160,200 in 2023)
- 2.9% Medicare (no limit)
- Applied to 92.35% of net income

**Deduction:**
- Deduct 50% of SE tax from income
- Reduces taxable income

### Federal Income Tax

**Marginal Tax Brackets (2023 - Single):**
- 10%: $0 - $11,000
- 12%: $11,001 - $44,725
- 22%: $44,726 - $95,375
- 24%: $95,376 - $182,100
- 32%: $182,101 - $231,250
- 35%: $231,251 - $578,125
- 37%: $578,126+

**Effective Tax Rate:**
- Your actual average tax rate
- Usually much lower than marginal rate
- Total tax / Total income

### State Income Tax

- Varies by state (0% - 13.3%)
- Some cities have additional tax
- May have different rules than federal

## Tax Savings Tips

### Throughout the Year

1. **Track Everything**
   - Every expense, every mile
   - Use apps to capture receipts
   - Log business use immediately

2. **Separate Business & Personal**
   - Dedicated business bank account
   - Business credit card
   - Clear documentation

3. **Save for Taxes**
   - Set aside 30-35% of income
   - Transfer to savings after each payment
   - Don't touch tax savings

4. **Make Quarterly Payments**
   - Avoid underpayment penalties
   - Spread tax burden over year
   - Adjust as income fluctuates

5. **Maximize Deductions**
   - Take advantage of all eligible deductions
   - Keep excellent records
   - Document business purpose

### Working with a CPA

**When to Hire:**
- First year of business
- Complex income sources
- Significant deductions
- Multi-state operations
- Estate planning needs

**What to Provide:**
- All 1099s and income statements
- Categorized expense reports
- Mileage logs
- Home office calculations
- Retirement contributions
- Health insurance payments

**CPA Cost:**
- $500-$2,000 for basic return
- Worth it for complex situations
- Tax advice valuable year-round

## Compliance Checklist

### Annual Requirements

- [ ] File Schedule C (Form 1040)
- [ ] File state income tax return
- [ ] Issue 1099-NEC to contractors ($600+)
- [ ] File state LLC annual report
- [ ] Renew business licenses
- [ ] Review and update entity info
- [ ] Organize tax documents

### Quarterly Requirements

- [ ] Calculate estimated tax
- [ ] Pay federal estimated tax
- [ ] Pay state estimated tax
- [ ] Review income and expenses
- [ ] Adjust estimates if needed

### Monthly Requirements

- [ ] Categorize expenses
- [ ] Review profit/loss
- [ ] Save tax portion
- [ ] Update financial projections

## Error Handling

### Common Errors

**"Invalid tax year"**
- Provide current or past year
- Cannot calculate for future years

**"Insufficient data for calculation"**
- Provide revenue and expense amounts
- Pull from billing server if available

**"Deadline not found"**
- Verify correct year
- Check if deadline already passed

## Integration with Other Skills

- **Invoice Handler**: Pull revenue and expense data
- **Project Manager**: Track business vs billable time
- **LLC Ops**: Stay on top of compliance
- **Weekly Reviewer**: Include tax planning in reviews

## Success Metrics

- Pay estimates on time: 100%
- Maximize deductions: Track everything
- Avoid penalties: Calculate accurately
- Tax savings rate: 30-35% of gross income
- CPA preparation time: <2 hours with good records

## Example Workflows

### Quarterly Tax Preparation
```
1. Pull revenue from billing server
2. Get expense totals by category
3. Calculate quarterly estimate
4. Make federal payment
5. Make state payment
6. Document payments
7. Update tax tracking
```

### Annual Tax Filing
```
1. Generate annual revenue report
2. Export categorized expenses
3. Calculate home office deduction
4. Compile mileage logs
5. Gather retirement contributions
6. Organize all 1099s
7. Meet with CPA
8. File returns
9. Pay any balance due
```

---

**Remember:** Proactive tax planning saves money. Track everything, pay on time, and don't be afraid to invest in professional advice for complex situations.
