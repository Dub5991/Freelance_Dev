# 💰 Finance

## Purpose
All financial data managed by **llc_ops_server** and **billing_server**.

## Subdirectories

### `/invoices`
Managed by **billing_server**:
- Invoice YAML files: `INV-0001.yaml`, `INV-0002.yaml`, etc.
- Generated from completed [BILLABLE] tasks
- Tracks payment status and history
- Integrates with Stripe for payment processing

### `/expenses`
Managed by **llc_ops_server**:
- Expense YAML files: `EXP-YYYYMMDDHHMMSS.yaml`
- Categorized business expenses
- Used for profit/loss calculations
- Fed into quarterly tax estimates

### `/tax`
Tax planning and records:
- Quarterly tax estimates
- Annual tax preparation
- Deduction tracking
- Mileage logs (if applicable)

## MCP Tools

### Billing Server
- `create_invoice` - Generate invoice from tasks
- `send_invoice` - Send via Stripe
- `check_payment_status` - Check if paid
- `list_outstanding_invoices` - AR aging
- `record_payment` - Manual payment entry
- `get_revenue_summary` - Revenue analytics

### LLC Ops Server
- `get_dashboard` - Financial overview
- `log_expense` - Record business expense
- `get_tax_estimate` - Quarterly tax calculation
- `get_profit_loss` - P&L statement
- `get_revenue_by_client` - Client revenue analysis

## Example Invoice
```yaml
invoice_id: INV-0001
invoice_number: 1
client_name: "Acme Corp"
client_email: "jane@acmecorp.com"
line_items:
  - task_id: task-20260110-001
    description: "Implement user authentication"
    hours: 8.5
  - task_id: task-20260112-002
    description: "API integration work"
    hours: 12.0
total_hours: 20.5
hourly_rate: 175
subtotal: 3587.50
tax: 0
total: 3587.50
status: sent
created_at: "2026-01-15T09:00:00"
due_date: "2026-02-14"
sent_at: "2026-01-15T09:30:00"
notes: "Payment due within 30 days"
payments: []
stripe_invoice_id: "in_1AbC2dEf3GhI4j"
```

## Example Expense
```yaml
expense_id: EXP-20260115103045
amount: 49.99
category: Software
description: "GitHub Copilot monthly subscription"
vendor: "GitHub"
date: "2026-01-15"
created_at: "2026-01-15T10:30:45"
```

## Financial Workflows

### Monthly Invoicing
1. Review completed [BILLABLE] tasks
2. Group by client
3. Create invoices with `create_invoice`
4. Send via Stripe with `send_invoice`
5. Track payment status weekly

### Expense Tracking
1. Log expenses immediately with `log_expense`
2. Categorize properly for tax deductions
3. Keep receipts (scan to PDF)
4. Review expense report monthly

### Quarterly Tax Preparation
1. Run `get_tax_estimate` for quarter
2. Review profit/loss statement
3. Calculate estimated tax payment
4. Pay by deadline (see LLC Ops README)
5. Document payment in `/tax`

## Tax Categories
- **Software**: Development tools, SaaS subscriptions
- **Hardware**: Computers, monitors, peripherals
- **Office**: Supplies, furniture, coworking space
- **Travel**: Client visits, conferences, mileage
- **Education**: Courses, certifications, books
- **Marketing**: Website, advertising, business cards
- **Legal**: Contracts, incorporation, compliance
- **Accounting**: Bookkeeping, tax prep, CPA
- **Insurance**: Liability, health (if applicable)
- **Meals**: Client meals (50% deductible)
- **Other**: Miscellaneous business expenses

## Best Practices
- **Invoice promptly** - Send within 3 days of work completion
- **Track expenses daily** - Don't let receipts pile up
- **Review AR weekly** - Follow up on overdue invoices
- **Check tax estimates quarterly** - Avoid surprises
- **Reconcile monthly** - Compare to bank statements
- **Backup regularly** - Keep financial data secure

## Stripe Integration
🔴 **YOUR ACTION NEEDED**: Configure Stripe in `.env`:
```
STRIPE_SECRET_KEY=sk_live_YOUR_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET_HERE
```

Benefits of Stripe:
- Professional invoice delivery
- Automatic payment reminders
- Multiple payment methods
- Real-time payment notifications
- Detailed payment history
