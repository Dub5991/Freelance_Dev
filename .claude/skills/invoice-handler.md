# Invoice Handler Skill

## Description
Create, track, and manage invoices, record payments, and ensure timely collection using the Billing Server with Stripe integration.

## When to Use This Skill
- Creating invoices for completed work
- Tracking payment status
- Recording received payments
- Sending payment reminders
- Generating revenue reports
- Managing overdue invoices

## MCP Servers Used
- **billing_server**: Primary server for invoicing and payments
- **work_server**: For billable hours data
- **client_server**: For client contact information

## Step-by-Step Instructions

### 1. Invoice Creation
When billing a client:

```
1. Gather billable hours from work_server
2. Create invoice using create_invoice()
3. Include detailed line items with:
   - Description of work
   - Quantity (hours/units)
   - Rate
4. Add tax if applicable
5. Apply discounts if negotiated
6. Set due date (default: 30 days)
7. Review invoice before sending
```

**Example Prompts:**
- "Create an invoice for AcmeCorp for 40 hours at $150/hour"
- "Generate an invoice for the API integration project with TechCorp"
- "Create a project-based invoice for $5,000 for the website redesign"

### 2. Invoice Management
For tracking invoice status:

```
1. List invoices by status using list_invoices()
2. Update invoice status as it progresses:
   - draft → sent → paid
3. Track overdue invoices
4. Monitor outstanding amounts
5. Review collection rates
```

**Example Prompts:**
- "Show all unpaid invoices"
- "List all invoices for AcmeCorp"
- "Update invoice INV-2024-0123 status to sent"
- "Which invoices are overdue?"

### 3. Payment Recording
When receiving payment:

```
1. Record payment using record_payment()
2. Specify payment amount
3. Include payment method (Stripe, check, wire, etc.)
4. Add transaction ID if available
5. System auto-updates invoice status
6. Verify invoice marked as paid when full amount received
```

**Example Prompts:**
- "Record a $3,000 payment on invoice INV-2024-0123"
- "Log payment received via Stripe for invoice INV-2024-0156"
- "Mark invoice as partially paid with $1,500"

### 4. Payment Reminders
For overdue invoices:

```
1. Get overdue invoices using get_overdue_invoices()
2. Review aging buckets:
   - 0-30 days: Friendly reminder
   - 31-60 days: Firm reminder
   - 61-90 days: Urgent follow-up
   - 90+ days: Final notice/collections
3. Send reminder using send_payment_reminder()
4. Track reminder count
5. Escalate if needed
```

**Example Prompts:**
- "Show me all overdue invoices"
- "Send payment reminder for invoice INV-2024-0089"
- "Which invoices are 60+ days overdue?"

### 5. Revenue Reporting
For financial analysis:

```
1. Generate revenue reports using get_revenue_report()
2. Select period:
   - current_month
   - last_month
   - current_quarter
   - ytd (year-to-date)
3. Review by client breakdown
4. Analyze trends
5. Calculate collection rate
```

**Example Prompts:**
- "Show me revenue for the current month"
- "Generate a quarterly revenue report"
- "What's my year-to-date revenue?"
- "Break down revenue by client for Q2"

### 6. Expense Tracking
For managing business expenses:

```
1. Record expenses using create_expense()
2. Categorize per IRS categories
3. Include receipt/documentation
4. Tag if billable to client
5. Track by tax year
6. Review for deductions
```

**Example Prompts:**
- "Record a $50 software subscription expense"
- "Log $120 client dinner expense for AcmeCorp"
- "List all expenses for this tax year"

## Invoice Best Practices

### Invoice Creation
- ✅ Send invoices promptly after work completion
- ✅ Use clear, detailed line item descriptions
- ✅ Include payment terms and methods
- ✅ Add invoice number for tracking
- ✅ Specify due date clearly
- ❌ Don't delay invoicing
- ❌ Don't use vague descriptions
- ❌ Don't forget tax when applicable

### Payment Terms
- ✅ Net 30 is standard for most clients
- ✅ Offer Net 15 for quick-pay discount
- ✅ Require deposit for large projects
- ✅ Set up recurring invoices for retainers
- ✅ Accept multiple payment methods
- ❌ Don't extend terms without reason
- ❌ Don't start work without clear terms

### Collections
- ✅ Send friendly reminder at 7 days overdue
- ✅ Send firm reminder at 15 days overdue
- ✅ Call client at 30 days overdue
- ✅ Stop work at 45 days overdue
- ✅ Consider collections at 90 days
- ❌ Don't be aggressive too early
- ❌ Don't continue work with chronic late payers

## Payment Collection Strategy

### Timing of Reminders

**Day 0 (Due Date):**
- No action if payment not yet received
- Many clients pay on due date

**Day 3 (After Due Date):**
- Friendly check-in email
- "Just checking if you received the invoice..."

**Day 7:**
- Gentle reminder
- "Following up on invoice #XXX due last week..."

**Day 14:**
- Firmer reminder
- Include late fee notice if applicable
- CC accounting department

**Day 30:**
- Phone call to accounting/client
- Express concern
- Understand any issues
- Set payment deadline

**Day 45:**
- Pause additional work
- Formal notice
- Payment plan offer if appropriate

**Day 60:**
- Final notice
- Mention potential legal action
- Consider small claims court

**Day 90+:**
- Collections agency or write-off
- Terminate relationship
- Learn from experience

### Email Templates

**First Reminder (Day 3):**
```
Subject: Invoice #[NUMBER] - Friendly Reminder

Hi [Client],

I hope this email finds you well! I wanted to follow up on 
invoice #[NUMBER] for $[AMOUNT] that was due on [DATE].

Just checking to make sure you received it and if you have 
any questions about the billing.

Let me know if you need anything!

Best regards,
[Your Name]
```

**Second Reminder (Day 14):**
```
Subject: Past Due: Invoice #[NUMBER]

Hi [Client],

I'm following up on invoice #[NUMBER] for $[AMOUNT] which 
is now [X] days past due.

Please let me know when I can expect payment, or if there 
are any issues we need to discuss.

Thank you,
[Your Name]
```

## IRS Expense Categories

Track expenses in these categories:

1. **Advertising & Marketing** - Website, ads, business cards
2. **Car & Truck** - Mileage, gas, maintenance (business use)
3. **Commissions & Fees** - Sales commissions, payment processing
4. **Contract Labor** - Subcontractors, freelancers
5. **Insurance** - Business liability, E&O insurance
6. **Legal & Professional** - Lawyers, accountants, consultants
7. **Office Expenses** - Supplies, postage, printing
8. **Rent or Lease** - Office space, equipment rental
9. **Repairs & Maintenance** - Equipment repairs
10. **Supplies** - Business supplies and materials
11. **Taxes & Licenses** - Business licenses, permits
12. **Travel** - Business travel expenses
13. **Meals** - Business meals (50% deductible)
14. **Utilities** - Phone, internet (business portion)
15. **Home Office** - Portion of home expenses
16. **Software & Subscriptions** - Business software
17. **Education & Training** - Courses, conferences

## Financial Metrics

Monitor these key metrics:

| Metric | Formula | Target |
|--------|---------|--------|
| Collection Rate | (Paid / Total Billed) × 100 | >95% |
| Days Sales Outstanding | Avg Outstanding / (Annual Rev / 365) | <45 days |
| Outstanding AR | Sum of unpaid invoices | Minimize |
| Monthly Revenue | Sum of invoices issued | Grow steadily |
| Profit Margin | (Revenue - Expenses) / Revenue | >60% |

## Error Handling

### Common Errors

**"Invoice must have at least one item"**
- Add at least one line item
- Include description, quantity, and rate

**"Stripe not configured"**
- Set STRIPE_API_KEY in environment
- Install stripe Python package
- Verify API key is valid

**"Invoice not found"**
- Check invoice ID is correct
- List invoices to find correct ID

**"Cannot mark as paid, amount doesn't match"**
- Verify payment amount
- Record partial payment if less than total

## Integration with Other Skills

- **Project Manager**: Pull billable hours for invoicing
- **Client Advisor**: Consider client health before collections
- **Tax Strategist**: Ensure proper expense categorization
- **Weekly Reviewer**: Include financial metrics in reviews

## Success Metrics

- **Average Days to Payment**: Target <30 days
- **% Invoices Paid On Time**: Target >80%
- **% Requiring Reminders**: Target <20%
- **Write-offs as % of Revenue**: Target <2%

## Example Workflows

### Monthly Invoicing Cycle
```
1. Pull billable hours for past month
2. Group by client
3. Create invoices with detailed breakdown
4. Review for accuracy
5. Send to clients
6. Set reminders for follow-up
```

### Weekly Collections Check
```
1. Review all overdue invoices
2. Age invoices into buckets
3. Send appropriate reminders
4. Follow up on past reminders
5. Record any payments received
6. Update cash flow projections
```

### Quarter-End Financial Review
```
1. Generate quarterly revenue report
2. Review profit margins by client
3. Analyze collection rates
4. Review expense categories
5. Identify areas for improvement
6. Prepare tax estimates
```

---

**Remember:** Consistent, professional invoicing and timely follow-up are essential for healthy cash flow. Don't be afraid to enforce payment terms—it's business, not personal.
