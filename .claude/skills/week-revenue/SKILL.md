# Week Revenue Skill

## Description
Summarize weekly revenue, billable hours, and financial performance.

## When to Use
- Friday afternoon weekly review
- End of pay period
- Monthly financial review
- When user asks "how did this week go financially?"

## MCP Tools Used
- `work_server.get_billable_summary` - Hours worked
- `billing_server.get_revenue_summary` - Invoices created
- `billing_server.list_outstanding_invoices` - AR status
- `llc_ops_server.get_dashboard` - Overall financial snapshot

## Process

1. **Calculate week dates**
   ```
   This week: Mon-Fri dates
   ```

2. **Get billable hours**
   ```
   get_billable_summary(
     start_date="2026-01-13",
     end_date="2026-01-17"
   )
   ```

3. **Get invoices created**
   ```
   get_revenue_summary(
     start_date="2026-01-13",
     end_date="2026-01-17"
   )
   ```

4. **Check AR status**
   ```
   list_outstanding_invoices()
   ```

5. **Calculate metrics and trends**

## Output Format

```markdown
💰 WEEK REVENUE SUMMARY - Week of Jan 13-17, 2026

## 📊 KEY METRICS

**Billable Hours:** 42.5 hours
- Target: 40 hours ✅
- Utilization: 106% (over target!)
- Breakdown by client:
  - Acme Corp: 25.0 hrs
  - Tech Startup: 12.5 hrs
  - Legacy Inc: 5.0 hrs

**Revenue Generated:** $6,712.50
- Acme Corp: $4,375 (25 hrs @ $175)
- Tech Startup: $1,875 (12.5 hrs @ $150)
- Legacy Inc: $462.50 (5 hrs @ $92.50)

**Invoices Created:** 2
- INV-0043: Acme Corp - $3,587.50 (sent)
- INV-0044: Tech Startup - $2,250 (draft)

## 💳 ACCOUNTS RECEIVABLE

**Total Outstanding:** $11,850
- Current (<30 days): $8,350
- 30-60 days: $3,500
- >60 days: $0 ✅

**This Week's Collections:** $4,200
- INV-0038: Legacy Inc paid ($1,200)
- INV-0040: Tech Startup paid ($3,000)

## 📈 TRENDS

**vs Last Week:**
- Hours: 42.5 vs 38.0 (+11.8%) ⬆️
- Revenue: $6,712 vs $5,700 (+17.8%) ⬆️
- Collections: $4,200 vs $2,100 (+100%) ⬆️⬆️

**Month-to-Date (3 weeks):**
- Hours: 118.5 / target 160 (74%)
- Revenue: $18,562 / target $24,000 (77%)
- On pace for: $24,750 (103% of target) ✅

## 🎯 COMMENTARY

**Wins:**
- ✅ Over target hours (42.5 vs 40)
- ✅ Strong collections week ($4.2K)
- ✅ No overdue invoices >60 days
- ✅ On pace to exceed monthly target

**Concerns:**
- ⚠️ Still have $3,500 in 30-60 day aging
- ⚠️ INV-0044 still in draft (send!)

**Next Week:**
- Send INV-0044 to Tech Startup
- Follow up on INV-0041 (35 days old)
- Target: 40 billable hours
- Goal: Get AR below $10K

## 💵 CASH FLOW FORECAST

**This Week Collected:** $4,200
**Next Week Expected:** $2,250 (if INV-0044 sent today)
**Outstanding after next week:** $9,600

**Action Items:**
1. Send INV-0044 today (Friday)
2. Email reminder for INV-0041
3. Log all hours for next week by Friday
```

## Example Usage

**User:** "How was the week revenue-wise?"

**Claude:**
```
💰 Great week! Here's the breakdown:

## THE NUMBERS
- **Billable Hours:** 42.5 (target: 40) ✅
- **Revenue Generated:** $6,712
- **Invoices Sent:** 2 ($5,837)
- **Cash Collected:** $4,200

## WHAT THIS MEANS
You're running 6% ahead of target hours and on pace for $24,750 this month (103% of your $24K goal).

Strong collections this week ($4.2K) means cash flow is healthy. AR is at $11,850 which is about 1.5 weeks of billings - that's good.

## ACTIONS FOR NEXT WEEK
1. **Send INV-0044** - It's drafted but not sent ($2,250)
2. **Follow up on INV-0041** - Now 35 days old ($3,500)
3. **Keep pace** - Another 40 hour week puts you solidly above target

Want me to:
- Send that draft invoice now?
- Draft follow-up for the 35-day invoice?
- Look deeper at any specific client?
```

## Metrics to Track

**Volume Metrics:**
- Billable hours
- Invoices created
- Tasks completed

**Financial Metrics:**
- Revenue generated
- Cash collected
- AR aging
- Average hourly rate

**Efficiency Metrics:**
- Utilization % (hours / target)
- Collection time (days from invoice to payment)
- Invoice-to-cash cycle

**Trend Metrics:**
- Week-over-week growth
- Month-to-date progress
- Pace to target

## Targets

Help user set and track:
- **Weekly hours:** 30-40 for full-time
- **Monthly revenue:** Based on goals
- **AR aging:** <30 days ideal
- **Utilization:** 75-85% sustainable

## Visualization

If user wants charts (can't show actual charts, but describe):
```
Hours by Client (Week of Jan 13):
Acme Corp     ████████████████████████░ 58.8%
Tech Startup  ████████████░░░░░░░░░░░░░ 29.4%
Legacy Inc    ███░░░░░░░░░░░░░░░░░░░░░░ 11.8%

Revenue Trend (Last 4 Weeks):
Week 1: $5,200 ████████░░
Week 2: $5,700 █████████░
Week 3: $6,712 ██████████
Week 4: [TBD]
```

## Follow-Up Actions

After revenue review:
- Send any draft invoices
- Follow up on aging AR
- Adjust next week's targets
- Log expenses from this week
- Update financial projections

## Tips
- Run this every Friday
- Compare to targets and trends
- Celebrate wins (over target!)
- Address concerns proactively
- Keep AR under 30 days
- Invoice promptly (within 3 days)
