# Meeting Prep Skill

## Description
Prepare for client meetings by loading context, history, and action items.

## When to Use
- Before every client meeting (15 min prep)
- When calendar shows upcoming meeting
- When user says "I have a meeting with [client] in [time]"

## MCP Tools Used
- `client_server.get_client` - Full client history
- `work_server.list_tasks` - Active tasks for client
- `work_server.get_billable_summary` - Recent hours
- `billing_server.list_outstanding_invoices` - Payment status

## Process

1. **Load client data**
   ```
   get_client(name="Acme Corp")
   ```

2. **Get active work**
   ```
   list_tasks(client="Acme Corp", status="all")
   ```

3. **Check financial status**
   ```
   get_billable_summary(client="Acme Corp")
   list_outstanding_invoices(client_name="Acme Corp")
   ```

4. **Prepare talking points**

## Output Format

```markdown
🤝 MEETING PREP: Acme Corp

**Meeting:** Weekly Check-in
**Date/Time:** Friday, Jan 17, 2pm
**Attendees:** Jane Smith (CTO), Bob Johnson (PM)
**Duration:** 30 minutes

## 📋 QUICK CONTEXT

**Relationship Health:** 9/10 ⬆️ (up from 8 last month)
**Contract:** Renews Sep 30, 2026 (257 days - secure)
**Last Meeting:** 7 days ago (Jan 10)

**This Week's Interaction:**
- Deployed authentication API (task-20260115-001)
- 25 hours logged on their projects
- They responded within 4 hours to all communications

## 💼 ACTIVE WORK

**In Progress:**
- task-20260116-003: Database optimization (P1)
  - 12 hours logged, estimated 15 total
  - On track for completion next week
  
- task-20260117-004: New feature scoping (P2)
  - Just started, planning phase

**Recently Completed:**
- ✅ task-20260115-001: Authentication API (8.5 hrs)
  - Deployed Tuesday, working perfectly
  - Positive feedback from their mobile team

## 💰 FINANCIAL STATUS

**This Week:**
- Hours worked: 25.0
- Billable value: $4,375 (@ $175/hr)
- Invoice sent: INV-0043 for previous work ($3,587.50)

**Outstanding:**
- INV-0043: $3,587.50 (sent Jan 15, due Feb 14)
- No overdue invoices ✅

**Historical:**
- Average payment time: 12 days (excellent)
- Total revenue YTD: $18,400
- Largest client (41% of revenue)

## 🎯 AGENDA ITEMS

**Your Updates:**
1. ✅ Auth API deployed and stable
2. 🔄 DB optimization on track for next week
3. 📋 New feature ready for scope discussion

**Ask Them:**
1. Feedback on auth API performance?
2. Ready to kick off Q1 2026 roadmap planning?
3. Any concerns or blockers?

**Follow-Up Items (from last meeting):**
- ✅ You: Send API documentation (sent Jan 11)
- ⏳ Them: Provide Q1 resource allocation (due today)
- ⏳ Them: Schedule training session with team (pending)

## ⚠️ POTENTIAL TOPICS

**Things to Mention:**
- Project is running smoothly, on budget
- Upcoming milestones for Q1
- Capacity for additional work if needed

**Things to Address (if they bring up):**
- INV-0043 is current, due Feb 14 (don't need to mention unless they ask)

**Things to Avoid:**
- Bringing up rate increases (relationship is great, but not the time)
- Scope creep (new feature needs proper scoping)

## 🚨 ISSUES TO ESCALATE

**None currently** - all work on track, relationship healthy.

## 📝 MEETING CHECKLIST

Before meeting:
- [ ] Review this prep (done!)
- [ ] Pull up task list
- [ ] Have invoice ready (if they ask)
- [ ] Notepad for action items

During meeting:
- [ ] Take notes on commitments
- [ ] Log any new work requests
- [ ] Confirm next meeting time

After meeting:
- [ ] Log meeting notes immediately
- [ ] Create tasks for new commitments
- [ ] Update health score if needed
- [ ] Send follow-up email with action items

## 💡 CONVERSATION STARTERS

**Build Rapport:**
- "How's the mobile app launch coming?"
- "How did the team like the auth implementation?"

**Business Context:**
- "What's top priority for you this quarter?"
- "Any new features cooking for Q2?"

**Relationship Building:**
- "Who else on your team should I connect with?"
- "Any feedback on how our collaboration is going?"

---

**Remember:**
- Listen more than you talk
- Take notes on all commitments
- Confirm next steps before ending
- Follow up within 24 hours
```

## Example Usage

**User:** "I have a call with Acme in 10 minutes"

**Claude:**
```
🤝 QUICK MEETING PREP: Acme Corp

**3 Things to Know:**
1. **Relationship: Excellent** (9/10, your top client, 41% of revenue)
2. **Work Status: On Track** (auth API deployed this week, DB optimization in progress)
3. **Financials: Clean** (no overdue invoices, they pay in 12 days average)

**From Last Meeting (7 days ago):**
- ✅ You delivered: API documentation
- ⏳ They owe: Q1 resource allocation (due today)

**Talk About:**
- Auth API feedback (deployed Tuesday)
- DB optimization timeline (next week)
- Q1 roadmap discussion

**Don't Forget:**
- Log meeting notes right after
- Create tasks for any new work
- Send follow-up email with action items

Want full prep details?
```

## Context to Load

**Relationship Context:**
- Health score and trend
- Contract status
- Communication patterns
- Recent interactions

**Work Context:**
- Active tasks and status
- Recently completed work
- Upcoming deliverables
- Blockers or risks

**Financial Context:**
- Recent billings
- Outstanding invoices
- Payment patterns
- Revenue contribution

**History Context:**
- Last meeting notes
- Outstanding commitments
- Unresolved issues
- Wins to celebrate

## After Meeting

**Immediate (within 1 hour):**
```
log_meeting(
  client_name="Acme Corp",
  date="2026-01-17T14:00:00",
  notes="[Summary of discussion]",
  attendees="Jane Smith, Bob Johnson"
)
```

**Same Day:**
- Create tasks for new commitments
- Update health score if needed
- Send follow-up email

**Template Follow-Up Email:**
```
Hi Jane & Bob,

Great catching up today! Quick summary:

Action Items:
- [Me] Complete DB optimization by Jan 24
- [Me] Send Q1 capacity forecast by Friday
- [You] Schedule training with mobile team

Next Steps:
- Continue with current priorities
- Check in next Friday 2pm

Let me know if I missed anything!

Best,
[You]
```

## Tips
- Prep 15 minutes before meeting
- Review last meeting notes
- Know your numbers (hours, invoices)
- Prepare questions to ask
- Take notes during call
- Log meeting immediately after
- Follow up within 24 hours
