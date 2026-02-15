# Tax Prep Skill

## Description
Calculate quarterly estimated tax and prepare for payment.

## When to Use
- 30 days before quarterly deadline
- Q1: Mar 15 (for Jan-Mar), Q2: Jun 15 (Apr-May), Q3: Sep 15 (Jun-Aug), Q4: Jan 15 (Sep-Dec)
- When user asks "how much do I owe in taxes?"
- During quarterly financial review

## MCP Tools Used
- `llc_ops_server.get_tax_estimate` - Quarterly tax calculation
- `llc_ops_server.get_profit_loss` - P&L for the quarter
- `llc_ops_server.log_expense` - Log expenses if missing

## Quarterly Tax Deadlines
- **Q1 2026:** April 15, 2026 (Jan-Mar income)
- **Q2 2026:** June 17, 2026 (Apr-May income)
- **Q3 2026:** September 15, 2026 (Jun-Aug income)
- **Q4 2026:** January 15, 2027 (Sep-Dec income)

## Process

1. **Determine current quarter**
2. **Get P&L for quarter**
   ```
   get_profit_loss(
     start_date="2026-01-01",
     end_date="2026-03-31"
   )
   ```

3. **Calculate tax estimate**
   ```
   get_tax_estimate(year=2026, quarter=1)
   ```

4. **Review deductions**
5. **Provide payment instructions**

## Output Format

```markdown
📊 Q1 2026 TAX ESTIMATE

## 💰 FINANCIAL SUMMARY (Jan 1 - Mar 31)

**Revenue:** $45,600
- Acme Corp: $28,000
- Tech Startup: $12,500
- Legacy Inc: $5,100

**Expenses:** $8,450
- Software: $1,200
- Hardware: $2,500
- Office: $800
- Travel: $1,200
- Marketing: $950
- Other: $1,800

**Net Profit:** $37,150

## 🧮 TAX CALCULATION

**Taxable Income:** $37,150
**Estimated Tax Rate:** 25% (Federal + State + Self-Employment)
**Estimated Tax Due:** **$9,287.50**

### Breakdown
- Federal Income Tax (22%): $8,173
- Self-Employment Tax (15.3%): $5,684
- State Tax (5%): $1,858
- Total: $15,715
- Less: Quarterly payment 1 of 4: **$9,288**

(Note: This is a simplified estimate. Actual rates vary by income level and deductions.)

## 📅 PAYMENT INFORMATION

**Deadline:** April 15, 2026 (30 days from today)
**Payment Amount:** $9,287.50

**How to Pay:**
1. **EFTPS** (Electronic Federal Tax Payment System)
   - https://www.eftps.gov
   - Enroll if first time (takes 5-7 days)
   - Free, secure, direct from bank

2. **IRS Direct Pay**
   - https://www.irs.gov/payments/direct-pay
   - No enrollment needed
   - Free

3. **Mail Check**
   - Form 1040-ES (voucher for Q1)
   - Make check payable to "United States Treasury"
   - Include SSN/EIN and "2026 Form 1040-ES"

**State Tax:** [Your state instructions]

## ✅ PRE-FLIGHT CHECKLIST

Before paying, ensure:
- [ ] All Q1 expenses logged
- [ ] All Q1 invoices created
- [ ] Reviewed deductions (complete list below)
- [ ] Confirmed bank account has funds
- [ ] Saved copy of this calculation

## 💡 TAX DEDUCTIONS USED

Review these categories - anything missing?

**Deducted ($8,450):**
- ✅ Software & subscriptions: $1,200
- ✅ Computer & equipment: $2,500
- ✅ Home office: $800
- ✅ Business travel: $1,200
- ✅ Marketing & advertising: $950
- ✅ Professional services: $0
- ✅ Insurance: $0
- ✅ Education & training: $0
- ✅ Meals (50% deductible): $0
- ✅ Other: $1,800

**Potentially Missing:**
- ❓ Health insurance premiums?
- ❓ Retirement contributions (SEP IRA)?
- ❓ Phone/internet (business %)?
- ❓ Professional memberships?
- ❓ Books, courses, conferences?

Want to log any additional expenses? They could reduce your tax bill.

## 🎯 CASH FLOW PLANNING

**Cash on Hand:** [Check with user]
**Tax Payment:** $9,288
**Remaining:** [Calculate]

**Next Quarter Projection:**
Based on current revenue pace ($15K/month), expect Q2 tax of ~$9,000-10,000.

**Recommendation:**
- Set aside 25-30% of each invoice for taxes
- Transfer $X per month to tax savings account
- Review quarterly to adjust

## 📝 RECORD KEEPING

After payment:
1. Save payment confirmation
2. Update vault/05-Areas/Finance/tax/Q1-2026-Payment.md
3. Calendar Q2 deadline (Jun 17) with 30-day reminder
4. Calendar Q2 review (Jun 1)

## 🤔 SHOULD YOU HIRE AN ACCOUNTANT?

Consider hiring a CPA if:
- Revenue >$100K annually
- Complex deductions (real estate, depreciation)
- Multi-state operations
- S-Corp or complex structure
- Just don't want to deal with it

**Cost:** $500-2000 for tax prep
**Value:** Peace of mind, maximized deductions, IRS representation

---

**Questions?**
- Want me to log additional expenses?
- Need help with EFTPS enrollment?
- Want to review deduction categories?
```

## Example Usage

**User:** "What do I owe in taxes this quarter?"

**Claude:**
```
📊 Q1 2026 TAX ESTIMATE (Due April 15)

You made $37,150 in profit this quarter (Jan-Mar).

**Estimated tax:** **$9,287.50**

This is based on:
- Revenue: $45,600
- Expenses: $8,450
- Tax rate: ~25% (Federal + State + Self-Employment)

**Deadline:** April 15, 2026 (29 days from today)

I noticed your expense total seems low for a quarter. Have you logged:
- Health insurance premiums?
- Retirement contributions?
- Phone/internet (business portion)?
- Any courses or certifications?

Every dollar in legitimate expenses saves you ~$0.25 in taxes.

Want me to:
1. Review expense categories for anything missing?
2. Show you how to pay via EFTPS?
3. Project Q2 tax based on current pace?
```

## Tax Rate Guidance

**Freelancer Tax Burden:**
- Federal Income Tax: 10-37% (based on income)
- Self-Employment Tax: 15.3% (Social Security + Medicare)
- State Income Tax: 0-13% (varies by state)
- **Total effective rate:** Typically 25-35%

**Safe Harbor Rule:**
If you paid 100% of prior year's tax (110% if high earner), you avoid underpayment penalties.

## Deduction Categories

Remind user of common deductions:
- Office equipment & software
- Home office (simplified or actual)
- Internet & phone (business %)
- Professional development
- Insurance (health, liability)
- Retirement contributions
- Business travel & meals (50%)
- Marketing & advertising
- Contract services
- Professional memberships

## Follow-Up Actions

After tax calculation:
- Log any missing expenses
- Make payment before deadline
- Save confirmation
- Set next quarter reminder
- Update financial projections

## Tips
- Run 30 days before deadline
- Always round up estimates
- Save 30% of each payment for taxes
- Max out deductions legally
- Keep receipts for everything
- Consider quarterly CPA review
