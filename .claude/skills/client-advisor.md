# Client Advisor Skill

## Description
Manage client relationships, track communication, monitor client health, and build long-term partnerships using the Client Server.

## When to Use This Skill
- Onboarding new clients
- Tracking client communications
- Monitoring client satisfaction
- Scheduling and documenting meetings
- Identifying at-risk client relationships
- Planning client outreach and follow-ups

## MCP Servers Used
- **client_server**: Primary server for CRM functionality
- **work_server**: For tracking client project work
- **billing_server**: For client payment history
- **onboarding_server**: For new client setup

## Step-by-Step Instructions

### 1. Client Onboarding
When bringing on a new client:

```
1. Create client profile using create_client()
2. Validate email and phone information
3. Document client preferences and communication style
4. Set initial health score
5. Log first communication
6. Schedule kickoff meeting
```

**Example Prompts:**
- "Create a new client profile for Sarah Johnson at TechCorp"
- "Add client AcmeCorp with email info@acmecorp.com"

### 2. Communication Tracking
For every client interaction:

```
1. Log communication using log_communication()
2. Include type (email, call, meeting, message)
3. Add meaningful subject and notes
4. Tag sentiment if notable (positive, neutral, negative)
5. Update last_contact date automatically
6. Plan next follow-up if needed
```

**Example Prompts:**
- "Log an email with AcmeCorp about project timeline"
- "Record a phone call with TechCorp discussing budget concerns"
- "Show me all communications with Sarah Johnson from this month"

### 3. Meeting Management
Before and after client meetings:

```
Before Meeting:
1. Schedule meeting using schedule_meeting()
2. Set agenda and duration
3. Send calendar invite
4. Prepare discussion points

After Meeting:
1. Log meeting notes using log_meeting_notes()
2. Document action items
3. Identify next steps
4. Follow up on commitments
```

**Example Prompts:**
- "Schedule a kickoff meeting with AcmeCorp for next Tuesday at 2pm"
- "Log notes from today's status meeting with TechCorp"
- "Show me upcoming meetings this week"

### 4. Client Health Monitoring
Regularly assess client relationship health:

```
1. Calculate health score using calculate_health_score()
2. Review scoring breakdown:
   - Recent communication (30 points)
   - Payment history (25 points)
   - Project activity (25 points)
   - Satisfaction rating (20 points)
3. Identify at-risk clients (score < 40)
4. Take action to improve health
5. Document improvement plans
```

**Example Prompts:**
- "Calculate health score for all active clients"
- "Show me clients with health scores below 60"
- "What's the current health status of AcmeCorp?"

**Health Score Interpretation:**
- 80-100: Excellent (maintain and grow)
- 60-79: Good (standard maintenance)
- 40-59: Fair (needs attention)
- 20-39: At Risk (immediate action needed)
- 0-19: Critical (intervention required)

### 5. Client Intelligence
Get comprehensive client overview:

```
1. Use get_client_summary() for full picture
2. Review recent communications
3. Check upcoming meetings
4. Assess financial relationship
5. Identify opportunities for growth
```

**Example Prompts:**
- "Give me a complete summary of TechCorp"
- "What's the status of my relationship with AcmeCorp?"

### 6. Relationship Building
Proactive client relationship management:

```
1. List clients by health score or industry
2. Identify clients needing check-ins
3. Plan value-add touchpoints
4. Schedule quarterly business reviews
5. Request testimonials from happy clients
6. Seek referrals from excellent relationships
```

**Example Prompts:**
- "Which clients haven't I contacted in over 30 days?"
- "List all clients in the technology industry"
- "Show me clients who might provide referrals"

## Best Practices

### Communication
- ✅ Log all significant interactions
- ✅ Respond within established SLAs
- ✅ Be proactive with updates
- ✅ Document important decisions
- ✅ Follow up on commitments
- ❌ Don't let small issues become big problems
- ❌ Don't go dark during difficult situations

### Relationship Health
- ✅ Monitor health scores monthly
- ✅ Act on declining scores immediately
- ✅ Celebrate wins with clients
- ✅ Seek feedback regularly
- ✅ Provide value beyond projects
- ❌ Don't ignore warning signs
- ❌ Don't assume everything is fine

### Professionalism
- ✅ Maintain clear boundaries
- ✅ Set and meet expectations
- ✅ Communicate honestly
- ✅ Admit mistakes promptly
- ✅ Focus on solutions, not excuses
- ❌ Don't overpromise and underdeliver
- ❌ Don't blame clients for misunderstandings

## Response Time SLAs

Establish and follow these standards:

| Priority | Response Time | Example |
|----------|---------------|---------|
| Urgent | 2 hours | Production issue, critical bug |
| High | 4 hours | Project deadline question, important decision |
| Normal | 24 hours | Status update, general question |
| Low | 48 hours | Non-urgent information request |

## Client Health Warning Signs

Watch for these red flags:

🚩 **Communication Issues**
- Delayed responses
- Short, curt replies
- Canceling meetings
- CC'ing managers/lawyers

🚩 **Financial Issues**
- Late payments
- Disputing invoices
- Requesting discounts frequently
- Budget cuts

🚩 **Satisfaction Issues**
- Negative feedback
- Complaints increasing
- Quality concerns
- Comparing to competitors

🚩 **Engagement Issues**
- No future projects discussed
- Reduced communication
- Minimal meeting participation
- Exploring other vendors

## Client Recovery Strategies

When health score drops:

**For Communication Issues (60-79):**
- Schedule check-in call
- Increase update frequency
- Address concerns proactively

**For At-Risk Clients (40-59):**
- Immediate 1:1 meeting
- Identify root causes
- Create improvement plan
- Weekly check-ins

**For Critical Clients (<40):**
- Emergency meeting
- Escalate to decision-makers
- Offer remediation
- Document everything
- Consider relationship viability

## Error Handling

### Common Errors

**"Invalid email address"**
- Check format has @ symbol and domain
- Verify no typos
- Confirm with client if uncertain

**"Client already exists"**
- Check for duplicate by email
- Update existing client instead
- Verify it's not a different contact at same company

**"Client not found"**
- Verify client ID is correct
- List clients to find correct ID
- May need to create client profile first

## Integration with Other Skills

- **Project Manager**: Link tasks to client context
- **Invoice Handler**: Ensure billing aligns with relationship status
- **Onboarding Specialist**: Smooth handoff from sales to delivery
- **Weekly Reviewer**: Include client health in reviews

## Success Metrics

Track these relationship metrics:

- **Client Retention Rate**: Target >90%
- **Net Promoter Score**: Target >8/10
- **Response Time Compliance**: Target >95%
- **Average Health Score**: Target >75
- **Referrals per Year**: Target 3-5
- **Client Lifetime Value**: Track and grow

## Example Workflows

### New Client Setup
```
1. Create client profile with all details
2. Log initial discovery call
3. Schedule kickoff meeting
4. Start onboarding workflow
5. Set 30-day check-in reminder
```

### Monthly Relationship Review
```
1. Calculate health scores for all clients
2. Review communications from past month
3. Identify clients needing check-ins
4. Schedule follow-up meetings
5. Plan value-add touchpoints
6. Update client notes
```

### Quarterly Business Review
```
1. Get complete client summary
2. Review projects completed
3. Analyze financial relationship
4. Discuss future opportunities
5. Gather satisfaction feedback
6. Plan next quarter collaboration
```

---

**Remember:** Strong client relationships are built on trust, communication, and consistent delivery. Use the Client Server to maintain organized, professional relationships that lead to long-term success.
