# Invoice Prep Skill

## Description
Generate invoices from completed billable tasks, grouped by client.

## When to Use
- End of bi-weekly billing cycle
- When user says "create invoice for [client]"
- Friday afternoon review
- When user completes major billable work

## MCP Tools Used
- `work_server.get_billable_summary` - Get unbilled hours
- `billing_server.create_invoice` - Generate invoice
- `billing_server.send_invoice` - Send via Stripe (if configured)
- `client_server.get_client` - Get client details

## Process

1. **Check for unbilled work**
   ```
   get_billable_summary(client=null) - All clients
   get_billable_summary(client="Acme Corp") - Specific client
   ```

2. **Review completed tasks**
   - Show task IDs, descriptions, hours
   - Confirm with user before invoicing

3. **Create invoice**
   ```
   create_invoice(
     client_name="Acme Corp",
     task_ids=["task-20260115-001", "task-20260116-003"],
     due_days=30,
     notes="Thank you for your business"
   )
   ```

4. **Send invoice**
   ```
   send_invoice(
     invoice_id="INV-0042",
     customer_email="jane@acmecorp.com"
   )
   ```

## Output Format

**Step 1: Show unbilled work**
```markdown
📊 UNBILLED WORK

## Acme Corp (20.5 hours @ $175/hr = $3,587.50)
- task-20260115-001: Implement authentication API (8.5 hrs)
- task-20260116-003: Database optimization (12.0 hrs)

## Tech Startup (15.0 hours @ $150/hr = $2,250)
- task-20260114-002: Fix deployment issues (6.0 hrs)
- task-20260117-001: Feature consultation (9.0 hrs)

Total unbilled: 35.5 hours = $5,837.50

Which client should I invoice?
```

**Step 2: Create invoice**
```markdown
✅ Invoice Created

**INV-0043**
- Client: Acme Corp
- Amount: $3,587.50
- Hours: 20.5
- Due: Feb 14, 2026 (Net 30)

Ready to send via Stripe? (requires API key configured)
```

**Step 3: Send confirmation**
```markdown
✅ Invoice Sent

INV-0043 sent to jane@acmecorp.com via Stripe
- Hosted URL: https://invoice.stripe.com/...
- Payment methods: Card, ACH, Wire
- Reminders: Automatic from Stripe

Next: Update financial dashboard with this invoice
```

## Example Usage

**User:** "Let's invoice Acme Corp for this week's work"

**Claude:**
```
📊 UNBILLED WORK FOR ACME CORP

## Completed Billable Tasks (Jan 15-19)
- task-20260115-001: Implement user authentication API (8.5 hrs)
  Completed: Jan 15, marked [BILLABLE]
  
- task-20260116-003: Database query optimization (12.0 hrs)
  Completed: Jan 17, marked [BILLABLE]

**Total:** 20.5 hours @ $175/hr = **$3,587.50**

Create invoice INV-0043?
```

**User:** "Yes, and send it"

**Claude:**
```
✅ Invoice INV-0043 Created & Sent

**Details:**
- Client: Acme Corp (jane@acmecorp.com)
- Amount: $3,587.50
- Line items: 2 tasks, 20.5 hours
- Due date: Feb 14, 2026 (Net 30)
- Status: Sent via Stripe

**Payment link:** https://invoice.stripe.com/i/acct_xxx/invst_xxx

Jane will receive an email with the invoice and can pay via:
- Credit/Debit card
- ACH bank transfer
- Wire transfer

Stripe will send automatic payment reminders.

Your updated stats:
- Total invoiced this month: $12,400
- Outstanding AR: $11,700
- Average payment time: 18 days
```

## Pre-Flight Checks

Before creating invoice:
1. ✅ All tasks marked [BILLABLE]
2. ✅ All tasks marked "completed"
3. ✅ Hours logged for each task
4. ✅ Client exists in system
5. ✅ Hourly rate confirmed

If any check fails, alert user.

## Stripe Integration

If Stripe configured:
- ✅ Send professional invoice
- ✅ Automatic payment reminders
- ✅ Multiple payment methods
- ✅ Real-time payment notifications

If Stripe NOT configured:
- ⚠️ Manual invoice (YAML only)
- Suggest: "Want to set up Stripe? Add keys to .env"

## Follow-Up Actions

After invoicing:
- Update financial dashboard
- Log invoice in notes
- Schedule follow-up (7 days after due date)
- Mark tasks as "invoiced"

## Tips
- Invoice bi-weekly by default
- Group tasks by project/milestone
- Include clear descriptions (not just task IDs)
- Send within 3 days of work completion
- Always confirm before sending
