# Client Health Skill

## Description
Check relationship health scores and flag at-risk clients.

## When to Use
- Weekly client review
- Before major meetings
- Monthly relationship audit
- When user asks "how are my client relationships?"

## MCP Tools Used
- `client_server.get_client_health` - Health scores
- `client_server.check_renewals` - Upcoming contract renewals
- `client_server.list_clients` - All clients
- `billing_server.get_revenue_summary` - Revenue by client

## Process

1. **Get all client health scores**
   ```
   get_client_health(min_score=null) - All clients
   get_client_health(min_score=6) - At-risk only
   ```

2. **Check for warning signs**
   - Score < 6 (at risk)
   - Score dropped recently
   - No recent meetings (>30 days)
   - Open commitments overdue

3. **Check contract renewals**
   ```
   check_renewals(days_ahead=30)
   ```

4. **Provide actionable recommendations**

## Output Format

```markdown
💚 CLIENT HEALTH CHECK - [Date]

## 🟢 HEALTHY (Score 7-10)
**Acme Corp** - Score: 9 ⬆️
- Last meeting: 3 days ago
- Contract: Renews Sep 30, 2026 (225 days)
- Open commitments: 1 (on track)
- Action: None needed

**Tech Startup** - Score: 8
- Last meeting: 1 week ago
- Contract: Renews Dec 31, 2026 (350 days)
- Open commitments: 0
- Action: None needed

## 🟡 NEUTRAL (Score 5-6)
**Legacy Inc** - Score: 6 ⬇️
- Last meeting: 21 days ago
- Contract: Renews Mar 31, 2026 (75 days!)
- Open commitments: 3 (2 yours, 1 theirs)
- ⚠️ Action: Schedule check-in, start renewal talk

## 🔴 AT RISK (Score 1-4)
**Old Client** - Score: 4 ⬇️⬇️
- Last meeting: 45 days ago
- Contract: Renews Feb 15, 2026 (31 days!)
- Open commitments: 5 (4 yours overdue!)
- 🚨 Action: URGENT - Address commitments, save relationship

## 📊 SUMMARY
- Total clients: 4
- Healthy: 2 (50%)
- Neutral: 1 (25%)
- At risk: 1 (25%)
- Contracts expiring <60 days: 1

## 🎯 RECOMMENDED ACTIONS
1. **URGENT:** Call Old Client about overdue commitments
2. **Soon:** Schedule renewal talk with Legacy Inc (75 days out)
3. **Routine:** Continue regular check-ins with healthy clients
```

## Example Usage

**User:** "How are my client relationships?"

**Claude:**
```
💚 CLIENT HEALTH CHECK

I see 4 active clients. Here's the breakdown:

## 🟢 HEALTHY (2 clients)
Both Acme Corp (score: 9) and Tech Startup (score: 8) are doing great:
- Regular communication
- No overdue items
- Contracts secure for 6+ months

## 🟡 NEEDS ATTENTION (1 client)
**Legacy Inc** - Score dropped from 7 to 6
- Haven't met in 3 weeks (unusual for them)
- Contract renews in 75 days
- You have 2 open commitments for them

**Recommendation:** Schedule a check-in this week and start the renewal conversation.

## 🔴 AT RISK (1 client)
**Old Client** - Score: 4 (down from 6 last month)
- No contact in 45 days
- Contract expires in 31 days
- 4 of your commitments are overdue
- They haven't paid last invoice (28 days old)

**🚨 URGENT:** This relationship needs immediate attention. The combination of:
- Overdue commitments
- Pending renewal
- Late payment
- Radio silence

...suggests they may not renew. Recommend calling today.

## NEXT STEPS
1. Call Old Client today about commitments and renewal
2. Email Legacy Inc to schedule check-in
3. Keep weekly cadence with healthy clients

Want me to:
- Draft email to Legacy Inc?
- Pull up Old Client commitments?
- Check revenue impact if Old Client churns?
```

## Warning Triggers

Flag these situations:

### 🚨 Critical (Score 1-4)
- Score dropped 3+ points
- No meeting in >45 days
- Multiple overdue commitments
- Late payment + renewal soon

### ⚠️ Warning (Score 5-6)
- Score dropped 2 points
- No meeting in >30 days
- Renewal in <60 days
- Pattern of slow responses

### 💡 Opportunity (Score 9-10)
- Strong relationship
- Potential for expansion
- Good for referrals/testimonials

## Health Score Guidelines

Remind user of scoring:
- **9-10**: Excellent - advocate, referring others
- **7-8**: Good - professional, on track
- **5-6**: Neutral - professional but distant
- **3-4**: At risk - issues, poor communication
- **1-2**: Critical - likely to churn

## Follow-Up Actions

After health check:
- Schedule meetings for at-risk clients
- Draft renewal conversations
- Update health scores after interactions
- Track trends over time

## Revenue Impact Analysis

For at-risk clients, show:
- Annual revenue from this client
- % of total revenue
- Cost of losing them
- Effort needed to replace

Example:
```
💰 REVENUE IMPACT if Old Client churns:
- Annual value: $45,000 (23% of total revenue)
- Replacement cost: ~90 hours of business dev
- Impact on Q1 targets: Would miss by 20%
- Verdict: Worth significant effort to save
```

## Tips
- Check health weekly
- Update scores after every significant interaction
- Start renewal talks 60-90 days early
- Document health changes in meeting notes
- Use health scores to prioritize attention
