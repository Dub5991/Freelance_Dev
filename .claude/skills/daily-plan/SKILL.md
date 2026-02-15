# Daily Plan Skill

## Description
Generate daily priorities by checking P0/P1 tasks, upcoming meetings, and commitments.

## When to Use
- Every morning to start the day
- When user asks "what should I work on today?"
- After completing major tasks to reassess priorities

## MCP Tools Used
- `work_server.list_tasks` - Get P0 and P1 tasks
- `client_server.list_clients` - Check for meetings today
- `billing_server.list_outstanding_invoices` - AR status

## Process

1. **Get urgent tasks**
   ```
   list_tasks(priority="P0")
   list_tasks(priority="P1")
   ```

2. **Check for meetings/commitments**
   ```
   list_clients() - review for today's meetings
   ```

3. **Check financial urgency**
   ```
   list_outstanding_invoices() - any >30 days overdue?
   ```

4. **Present prioritized plan**
   - P0 tasks first (enforce max 3!)
   - Client meetings second
   - Overdue financial items third
   - P1 tasks fourth
   - Time blocks for focus work

## Output Format

```markdown
🌅 DAILY PLAN - [Date]

## 🚨 URGENT (Do First)
- [ ] [P0 task 1]
- [ ] [P0 task 2]
- [ ] [Client Meeting at TIME]

## 💼 HIGH PRIORITY (Today)
- [ ] [P1 task 1]
- [ ] [P1 task 2]
- [ ] Follow up on overdue invoice INV-XXXX

## 📅 COMMITMENTS DUE
- [ ] [Commitment 1 for Client X]

## ⏰ TIME BLOCKS
- 9am-12pm: Deep work on [P0 task]
- 1pm-2pm: [Client meeting]
- 2pm-5pm: [P1 tasks]

## 📊 CONTEXT
- Billable hours this week: X
- Outstanding invoices: $X,XXX
- P0s at limit: [Yes/No]
```

## Example Usage

**User:** "What should I focus on today?"

**Claude:**
```
🌅 DAILY PLAN - January 15, 2026

## 🚨 URGENT (Do First)
- [ ] task-20260115-001: Deploy API hotfix for Acme Corp (P0)
- [ ] 2pm: Weekly check-in with Tech Startup

## 💼 HIGH PRIORITY (Today)
- [ ] task-20260114-003: Code review for Project X (P1)
- [ ] Follow up on INV-0042 (35 days overdue, $3,500)

## 📅 COMMITMENTS DUE
- [ ] Send proposal to Prospect Inc (promised by EOD)

## ⏰ TIME BLOCKS
- 9am-11am: Deep work on hotfix (task-20260115-001)
- 11am-12pm: Code review batch
- 1pm-2pm: Lunch + admin
- 2pm-3pm: Tech Startup meeting
- 3pm-5pm: Finish code reviews, send proposal

## 📊 CONTEXT
- Billable hours this week: 28 of target 40
- Outstanding invoices: $8,200
- P0s: 1 active (safe)
- Next meeting after today: Friday 10am with Acme
```

## Tips
- Always show P0 count vs limit (3)
- Flag if any invoice is >30 days old
- Include "billable hours this week" for pacing
- Suggest time blocks for deep work
- Remind of commitments due today

## Follow-Up Actions
After presenting plan, offer:
- "Want me to create any new tasks?"
- "Need to update any priorities?"
- "Ready to log yesterday's hours?"
