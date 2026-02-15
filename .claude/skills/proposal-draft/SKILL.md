# Proposal Draft Skill

## Description
Draft professional proposals/SOWs using the template and client context.

## When to Use
- New prospect needs a proposal
- Expanding scope with existing client
- Converting discovery call to formal engagement

## MCP Tools Used
- `client_server.get_client` - Client details and history
- `career_server.list_skills` - Your expertise
- `career_server.get_portfolio` - Relevant case studies

## Process

1. **Gather context**
   - Client needs (ask user)
   - Project scope (ask user)
   - Timeline and budget (ask user)

2. **Pull client data**
   ```
   get_client(name="Prospect Inc")
   ```

3. **Get relevant portfolio**
   ```
   get_portfolio(skill="React", top_n=3)
   ```

4. **Use SOW_Template.md** and customize

## Template Customization

**From template:**
- Project overview
- Scope of work
- Deliverables timeline
- Investment structure
- Your experience

**Add from system:**
- Client name and contact (from CRM)
- Your LLC details (from .env)
- Relevant case studies (from portfolio)
- Current skills/expertise (from career tracker)

## Example Usage

**User:** "Draft a proposal for Tech Startup's API project"

**Claude:**
```
I'll create a proposal using our template. Let me gather some information:

1. What's the project scope? (e.g., "Build REST API with authentication")
2. Estimated hours? (e.g., 120 hours)
3. Timeline? (e.g., 8 weeks)
4. Any specific deliverables? (e.g., API, docs, testing)

[User provides details]

Great! Let me check your portfolio for relevant experience...

Found:
- 3 similar API projects
- React/Node.js expertise (5 years)
- AWS deployment experience

Drafting proposal...

---

# PROFESSIONAL SERVICES PROPOSAL

**Prepared for:** Tech Startup Inc.  
**Prepared by:** [Your LLC Name]  
**Date:** January 15, 2026  
**Valid through:** February 14, 2026

## Executive Summary

Thank you for the opportunity to propose our services for your API development project. Based on our conversation on January 10, we understand that Tech Startup needs a scalable REST API with authentication to support your new mobile application.

We propose an 8-week engagement to design, build, and deploy a production-ready API. This approach will deliver a secure, well-documented API that can scale with your user growth and integrate seamlessly with your mobile app.

## Understanding Your Needs

### Current Situation
- New mobile app launching Q1 2026
- Need backend API for user management and core features
- Current setup is prototype-only, not production-ready
- Timeline: Must launch by March 31

### Desired Outcomes
- Production-grade REST API
- JWT-based authentication
- Scalable architecture on AWS
- Comprehensive documentation
- Knowledge transfer to your team

## Proposed Solution

### Our Approach
We'll use an iterative, milestone-based approach:
- ✅ Quick wins with working API in Week 2
- ✅ Weekly demos to ensure alignment
- ✅ Security-first design
- ✅ Automated testing and CI/CD

### Technology Stack
- **Backend:** Node.js with Express (proven, fast, your team knows JS)
- **Database:** PostgreSQL (ACID compliance, excellent for user data)
- **Auth:** JWT with refresh tokens (industry standard, secure)
- **Cloud:** AWS (Lambda + RDS for scalability)
- **CI/CD:** GitHub Actions (free, easy to maintain)

[... continues with full proposal using template ...]

## Investment

**Estimated Timeline:** 8 weeks  
**Estimated Effort:** 120 hours  
**Hourly Rate:** $150/hour  
**Estimated Total:** **$18,000**

## Why Work With Us

### Relevant Experience

**Similar Project: Fintech API Platform**
- Client: Financial services startup
- Challenge: Build secure API for mobile banking app
- Solution: Node.js REST API with OAuth2, deployed on AWS
- Outcome: Handled 50K daily users, zero security incidents

**Similar Project: SaaS Backend Migration**
- Client: B2B SaaS company
- Challenge: Replace legacy monolith with modern API
- Solution: Microservices architecture with comprehensive docs
- Outcome: 10x faster response times, 95% test coverage

---

Draft ready! Want me to:
1. Save to vault/05-Areas/Business_Dev/
2. Adjust any sections?
3. Add more case studies?
4. Change pricing structure?
```

## Pricing Strategies

**Time & Materials** (Recommended for uncertain scope)
```
Invoiced bi-weekly for actual hours worked
Flexible, you only pay for what's done
Good for: Evolving requirements
```

**Fixed Price** (For well-defined scope)
```
Single project price
Paid in milestones: 30/40/30
Good for: Clear deliverables, fixed budget
```

**Retainer** (For ongoing work)
```
X hours per month at locked rate
Unused hours roll over (up to 20%)
Good for: Long-term partnerships
```

## Competitive Positioning

**Your Advantages:**
- Solo practitioner = direct access, no account managers
- Dev-built = understand technical tradeoffs
- Modern stack = maintainable, not legacy
- Transparent pricing = no hidden fees

**Address Concerns:**
- Solo = might seem risky
  → Show portfolio, testimonials, track record
- Higher rate than offshore
  → Emphasize quality, communication, timezone
- Time & materials = open-ended cost
  → Provide estimate, weekly updates, cap if needed

## Follow-Up

After sending proposal:
1. Log in CRM as commitment
2. Set follow-up reminder (3-5 days)
3. Track in business dev pipeline
4. Prepare for negotiation

**Follow-up email template:**
```
Hi [Name],

Just wanted to confirm you received the proposal for [Project]. 

Happy to discuss any questions or adjust the approach based on your feedback.

Best time to chat this week?

Best,
[You]
```

## Tips
- Use template, don't write from scratch
- Pull in real portfolio examples
- Be specific about deliverables
- Show understanding of their business
- Make it easy to say yes (clear next steps)
