# Session Start Hook

**Auto-runs at the beginning of each Claude session**

## Purpose
Surface urgent items and provide context for the day ahead.

## Actions

### 1. Check P0 Tasks
```
list_tasks(priority="P0")
```
- Alert if >= 3 (at limit!)
- Flag if any P0 is >3 days old
- Suggest which to downgrade if over limit

### 2. Check Overdue Invoices
```
list_outstanding_invoices()
```
- Alert if any >30 days overdue
- Show total AR aging
- Suggest follow-up actions

### 3. Check Contract Renewals
```
check_renewals(days_ahead=30)
```
- Alert on any expiring <30 days
- Show renewal preparation checklist
- Suggest scheduling renewal conversation

### 4. Show Today's Priorities
```
list_tasks(status="todo")
```
- P0 and P1 tasks
- Today's meetings (from client notes)
- Commitments due today

## Example Output

```
🌅 GOOD MORNING - Wednesday, January 17, 2026

## 🚨 URGENT ITEMS
⚠️ 3 P0 tasks active (at limit!)
⚠️ INV-0041 is 35 days overdue ($3,500)
✅ No contracts expiring soon

## 📋 TODAY'S FOCUS
**P0 Tasks:**
1. task-20260117-001: Production hotfix for Acme Corp

**P1 Tasks:**
2. task-20260116-003: Complete DB optimization
3. task-20260117-002: Code review for Tech Startup

**Meetings:**
- 2pm: Tech Startup weekly check-in (30 min)

**Commitments Due:**
- Send Q1 proposal to Legacy Inc (promised today)

## 💰 FINANCIAL SNAPSHOT
- Outstanding invoices: $11,850
- This week's billable: 28 hours (of 40 target)
- QTD revenue: $18,562

## 🎯 QUICK WINS
- Complete that P0 hotfix
- Follow up on 35-day invoice
- Log hours from yesterday

Ready to dive in? What's first?
```

## Behavior Rules

**Always show:**
- P0 count and status
- Overdue invoices >30 days
- Contracts expiring <30 days

**Only show if relevant:**
- Low client health scores (<6)
- Uncommitted hours from yesterday
- Inbox items >7 days old

**Never show:**
- Empty sections (if no urgent items, say "✅ No urgent items")
- Historical data (focus on today/this week)
- Verbose explanations (keep it actionable)

## Customization

Users can customize in CLAUDE.md USER_EXTENSIONS section:
- Disable specific checks
- Change thresholds
- Add custom checks
- Modify output format

## Tips

This hook sets the tone for the day:
- Be concise (30 seconds to read)
- Be actionable (what to do, not just status)
- Be positive (celebrate when things are good!)
- Be urgent when needed (but don't cry wolf)

---

*This hook runs automatically. No user action needed.*
