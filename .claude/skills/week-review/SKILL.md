# Week Review Skill

## Description
Comprehensive weekly retrospective covering work, finances, and planning.

## When to Use
- Every Friday afternoon (last thing before weekend)
- When user asks "let's do the weekly review"
- End of pay period

## MCP Tools Used
- `work_server.list_tasks` - Tasks completed/created this week
- `work_server.get_billable_summary` - Hours breakdown
- `client_server.get_client_health` - Relationship check
- `billing_server.get_revenue_summary` - Financial summary
- `billing_server.list_outstanding_invoices` - AR status

## Process

1. **Review work completed**
2. **Check billable hours**
3. **Review financial status**
4. **Check client health**
5. **Plan next week**
6. **Identify improvements**

## Output Format

```markdown
📊 WEEKLY REVIEW - Week of Jan 13-17, 2026

## ✅ WORK COMPLETED

**Tasks Finished:** 5
- ✅ task-20260115-001: Auth API (Acme Corp, 8.5 hrs)
- ✅ task-20260116-002: Bug fixes (Tech Startup, 4.0 hrs)
- ✅ task-20260116-003: DB optimization (Acme Corp, 12.0 hrs)
- ✅ task-20260117-004: Code review (Legacy Inc, 3.0 hrs)
- ✅ task-20260117-005: Documentation (Acme Corp, 5.0 hrs)

**Tasks Created:** 3
- task-20260119-001: New feature scoping (P2)
- task-20260119-002: Performance testing (P1)
- task-20260119-003: Client meeting prep (P3)

**Tasks In Progress:** 2
- task-20260118-001: API integration (P1, 60% done)
- task-20260118-002: Security audit (P2, 30% done)

## 💰 FINANCIAL SUMMARY

**Billable Hours:** 42.5 hours
- Target: 40 hours ✅ (+6%)
- Breakdown:
  - Acme Corp: 25.0 hrs ($4,375)
  - Tech Startup: 12.5 hrs ($1,875)
  - Legacy Inc: 5.0 hrs ($462.50)

**Revenue Generated:** $6,712.50
**Invoices Created:** 2 ($5,837.50)
**Cash Collected:** $4,200

**AR Status:**
- Total outstanding: $11,850
- Overdue (>30 days): $3,500 ⚠️
- Action needed: Follow up on INV-0041

## 🤝 CLIENT RELATIONSHIPS

**Meetings This Week:** 3
- Acme Corp: Weekly check-in (excellent discussion)
- Tech Startup: Planning session (scope new work)
- Legacy Inc: Quick sync (minor issues)

**Health Scores:**
- Acme Corp: 9 (stable, excellent)
- Tech Startup: 8 (stable, good)
- Legacy Inc: 6 ⚠️ (dropped from 7, needs attention)

**Action Needed:**
- Legacy Inc health dropped - schedule deeper check-in

## 📈 METRICS & TRENDS

**vs Last Week:**
- Hours: 42.5 vs 38.0 (+11.8%) ⬆️
- Revenue: $6,712 vs $5,700 (+17.8%) ⬆️
- Tasks done: 5 vs 4 (+25%) ⬆️

**Month Progress:**
- Hours: 118.5 / 160 target (74%)
- Revenue: $18,562 / $24,000 target (77%)
- On pace: $24,750 (103% of target) ✅

## 🎉 WINS THIS WEEK

1. **Exceeded hours target** - 42.5 hrs (106% of 40)
2. **Major deployment** - Auth API for Acme Corp (biggest deliverable this month)
3. **Strong collections** - $4.2K collected (double last week)
4. **New work scoped** - Tech Startup expansion opportunity
5. **Zero P0s** - All urgent work handled

## ⚠️ CONCERNS & ISSUES

1. **Legacy Inc health drop** (6/10)
   - Cause: Some communication issues noted
   - Plan: Schedule 1:1 to address

2. **Aging AR** ($3,500 at 30-60 days)
   - Invoice: INV-0041 (Legacy Inc)
   - Plan: Follow up Monday morning

3. **No internal work** (0 hours this week)
   - Risk: Falling behind on skills/marketing
   - Plan: Block 5 hours next week for portfolio update

## 📋 NEXT WEEK PRIORITIES

**Top 3:**
1. Complete API integration (task-20260118-001) for Acme Corp
2. Follow up on overdue invoice (INV-0041)
3. Legacy Inc relationship repair - deeper check-in

**Client Work (target 40 hours):**
- Acme Corp: 20 hours (API integration, security)
- Tech Startup: 15 hours (new feature kick-off)
- Legacy Inc: 5 hours (fix issues, rebuild relationship)

**Internal Work (target 5 hours):**
- Portfolio update with recent projects
- Update skills (log new tech used this quarter)
- Review Q1 goals progress

**Meetings Scheduled:**
- Mon: Legacy Inc check-in (9am)
- Wed: Tech Startup kickoff (2pm)
- Fri: Acme Corp weekly (2pm)

## 🔄 PROCESS IMPROVEMENTS

**What Worked Well:**
- ✅ Daily hour logging kept billing accurate
- ✅ Friday invoice prep avoided weekend work
- ✅ Meeting prep skill saved time and improved quality

**What Didn't Work:**
- ❌ No internal work time (all client hours)
- ❌ Missed check-in with Legacy Inc earlier in week
- ❌ One invoice still in draft (should've sent)

**Changes for Next Week:**
- Block Monday 8-10am for internal work
- Set reminder for client health checks (Wednesdays)
- Send all invoices by Thursday EOD

## 📊 INBOX STATUS

**Current items in 00-Inbox:** 7
- 3 client emails (need responses)
- 2 article links (to read)
- 1 conference opportunity (to evaluate)
- 1 receipt (to log as expense)

**Plan:** Process to zero during next week's internal time

## 🎯 PROGRESS ON GOALS

**Q1 2026 Goals Check:**

1. **Revenue: $60K target**
   - Current: $18,562 (31% - on track)
   - Pace: $74K projected ✅

2. **2 New Clients**
   - Current: 1 prospect in pipeline (Tech Startup expansion counts)
   - Need: 1 more prospect

3. **AWS Certification**
   - Progress: Started studying
   - Behind: Need to book exam

**Action:** Block time for certification study

## 📅 UPCOMING EVENTS

**Next Week:**
- Mon: Follow up on overdue invoice
- Tue: Nothing scheduled
- Wed: Tech Startup kickoff
- Thu: Send invoices for week
- Fri: Weekly reviews with all clients

**Upcoming Deadlines:**
- Jan 31: Send monthly summary to all clients
- Feb 15: Q1 2026 check-in (6 weeks to Q1 end)
- Apr 15: Q1 tax payment due

---

## 🚀 READY FOR NEXT WEEK?

Summary:
- ✅ Strong week (42.5 hrs, 103% of target)
- ✅ Major deliverable shipped
- ✅ Good cash collection
- ⚠️ 2 issues to address (Legacy Inc, INV-0041)
- ⚠️ Need more internal time

**Monday Morning Checklist:**
- [ ] Follow up on INV-0041
- [ ] Prepare for Legacy Inc meeting
- [ ] Review top 3 priorities
- [ ] Time block the week
- [ ] Process inbox

Have a great weekend! 🎉
```

## Example Usage

**User:** "Let's do the weekly review"

**Claude:**
```
📊 WEEKLY REVIEW - Week of Jan 13-17

Let me pull together your week...

## THE HIGHLIGHTS
- ✅ Crushed it: 42.5 hours (106% of target)
- ✅ Shipped: Auth API for Acme Corp (huge!)
- ✅ Collected: $4.2K in payments
- ⚠️ Watch: Legacy Inc health dropped to 6
- ⚠️ Action: $3.5K invoice now 35 days old

## THE NUMBERS
- Revenue: $6,712 (week) | $18,562 (month, on pace for 103%)
- Tasks done: 5 | Tasks created: 3
- Meetings: 3 | All productive

## NEXT WEEK
Top 3:
1. Complete API integration (biggest deliverable)
2. Fix Legacy Inc relationship
3. Chase that 35-day invoice

You're on track for $24,750 this month (above your $24K target).

Main concerns:
- No internal work this week (0 hours)
- Legacy Inc needs attention
- One overdue invoice to collect

Want to:
- Dive deeper into any section?
- Set specific Monday priorities?
- Plan the time blocks for next week?
```

## Components

**Essential Sections:**
- Work completed (wins!)
- Financial summary
- Client relationships
- Next week plan

**Optional Sections (if relevant):**
- Inbox status
- Process improvements
- Goal progress
- Upcoming events

## Review Cadence

- **Weekly:** This full review
- **Monthly:** + Financial deep dive
- **Quarterly:** + Goal assessment + Tax prep

## Follow-Up Actions

After review:
1. Process inbox to zero
2. Create Monday's top 3 tasks
3. Block next week's calendar
4. Send any pending invoices
5. Archive completed work
6. Update goal tracking

## Tips
- Do this every Friday, same time
- Be honest about what didn't work
- Celebrate wins (you earned them!)
- Plan next week while context is fresh
- Keep review <30 minutes
- Make it a habit, not a chore
