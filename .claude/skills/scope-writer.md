# Scope Writer Skill

## Description
Write clear, comprehensive scopes of work that protect your interests, set proper expectations, and prevent scope creep.

## When to Use This Skill
- Creating proposals for new projects
- Defining project deliverables
- Responding to RFPs
- Documenting client agreements
- Preventing scope creep
- Clarifying ambiguous requirements

## MCP Servers Used
- **onboarding_server**: For scope of work generation
- **client_server**: For client context
- **work_server**: For breaking down into tasks

## Scope of Work Structure

### 1. Project Overview
**Purpose:** High-level context

```
Project Name: [Descriptive name]
Client: [Client name]
Date: [Today's date]
Prepared by: [Your name/LLC]

Executive Summary:
[2-3 sentences describing the project's purpose and value]
```

**Example:**
```
This scope of work outlines the development of a 
customer portal for AcmeCorp to enable self-service
account management, reducing support costs by an 
estimated 40%.
```

### 2. Project Objectives
**Purpose:** Define success criteria

```
Primary Objectives:
1. [Measurable goal 1]
2. [Measurable goal 2]
3. [Measurable goal 3]

Success Metrics:
- [How success will be measured]
- [Target outcomes]
```

**Example:**
```
Primary Objectives:
1. Reduce customer support tickets by 40%
2. Enable 80% of account changes without support
3. Launch to 1,000 beta users within 90 days

Success Metrics:
- User adoption rate >60% in first month
- Support ticket reduction of 35%+
- Customer satisfaction score >4.5/5
```

### 3. Detailed Deliverables
**Purpose:** Specific outputs you'll provide

```
For each deliverable, specify:
- Name and description
- Format/specifications
- Acceptance criteria
- Dependencies
- Timeline

Deliverable 1: [Name]
Description: [What it is]
Format: [File type, platform, etc.]
Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

**Example:**
```
Deliverable 1: User Authentication System
Description: Secure login/logout system with 
              password reset functionality
Format: React frontend + Node.js API
Acceptance Criteria:
- [ ] Users can register with email/password
- [ ] Email verification required
- [ ] Password reset via email link
- [ ] Session management working
- [ ] All security best practices implemented

Deliverable 2: Account Dashboard
Description: Main user interface showing account 
              status and actions
Format: Responsive web application
Acceptance Criteria:
- [ ] Shows current account status
- [ ] Displays recent activity
- [ ] Mobile-responsive design
- [ ] Matches provided design mockups
- [ ] Loads in <2 seconds
```

### 4. Timeline & Milestones
**Purpose:** Project schedule

```
Phase 1: [Phase name] - [Duration]
Week 1-2: [Activities]
- Deliverable A

Phase 2: [Phase name] - [Duration]
Week 3-4: [Activities]
- Deliverable B

Key Milestones:
- [Date]: Milestone 1
- [Date]: Milestone 2
- [Date]: Final Delivery
```

### 5. Budget & Payment
**Purpose:** Financial terms

```
Total Investment: $[Amount]
Payment Schedule:
- [X]% ($[Amount]) - Upon signing (Deposit)
- [X]% ($[Amount]) - [Milestone]
- [X]% ($[Amount]) - Final delivery

Hourly Rate: $[Rate]/hour (if applicable)
Estimated Hours: [Range] hours
Not-to-Exceed: $[Cap] (if applicable)

Payment Terms: Net [X] days
Payment Methods: [Wire/ACH/Card]
```

### 6. Assumptions
**Purpose:** What you're assuming to be true

```
This scope assumes:
1. [Assumption about client providing X]
2. [Assumption about existing infrastructure]
3. [Assumption about availability]
4. [Assumption about third-party services]
```

**Example:**
```
This scope assumes:
1. Client will provide access to existing database
2. Design mockups will be provided by [Date]
3. Client availability for weekly review meetings
4. Existing AWS infrastructure can be leveraged
5. Client will handle hosting and domain setup
6. Third-party APIs are documented and accessible
```

### 7. Exclusions (Critical!)
**Purpose:** What's NOT included

```
The following are explicitly excluded:
1. [What you won't do]
2. [What you won't provide]
3. [What's outside scope]

Additional work beyond this scope will require:
- Written change request
- Updated timeline
- Revised budget
- Signed amendment
```

**Example:**
```
The following are explicitly excluded:
1. Database migration from legacy system
2. Mobile native applications (iOS/Android)
3. Integration with payment processing
4. Training materials and documentation
5. Post-launch technical support beyond 30 days
6. Content creation or copywriting
7. SEO optimization
8. Marketing or user acquisition

Any of these can be added via change request.
```

### 8. Client Responsibilities
**Purpose:** What client must provide

```
Client agrees to:
1. [Provide X by date]
2. [Make decision-makers available]
3. [Provide timely feedback]
4. [Grant necessary access]
5. [Maintain communication]
```

**Example:**
```
Client agrees to:
1. Provide design mockups by Week 1
2. Grant API access within 3 business days
3. Respond to questions within 48 hours
4. Provide feedback within 5 business days
5. Make technical stakeholder available weekly
6. Provide test data and accounts
7. Review and approve deliverables promptly
```

### 9. Revisions & Feedback
**Purpose:** How changes are handled

```
Included Revisions:
- [X] rounds of revisions per deliverable
- Revisions requested within [Y] days of delivery
- Based on original scope and requirements

Additional Revisions:
- Billed at $[Rate]/hour
- Require written approval
- May impact timeline
```

### 10. Change Request Process
**Purpose:** Managing scope changes

```
All scope changes require:
1. Written change request submitted
2. Impact assessment (timeline/cost)
3. Written approval from both parties
4. Updated SOW signed
5. Payment adjustment if applicable

Change requests will be assessed within 2 business days.
```

### 11. Acceptance & Sign-off
**Purpose:** How completion is determined

```
Each deliverable will be:
1. Delivered to client for review
2. Reviewed against acceptance criteria
3. Feedback provided within [X] business days
4. Revisions made if needed
5. Formal acceptance documented

Final sign-off indicates:
- All deliverables meet acceptance criteria
- Project is complete per this scope
- Final payment is due
```

### 12. Post-Project Support
**Purpose:** What happens after delivery

```
Included Support:
- [X] days of bug fixes for defects
- Email support for implementation questions
- Documentation and handoff session

Ongoing Support (Optional):
- Monthly retainer: $[Amount]/month
- Hourly support: $[Rate]/hour
- Emergency support: $[Rate]/hour
```

## Scope Writing Best Practices

### Be Specific
✅ "Design and implement 5 RESTful API endpoints with full CRUD operations"
❌ "Build an API"

✅ "Create 3 responsive web pages (Home, About, Contact) matching provided mockups"
❌ "Build a website"

### Use Measurable Criteria
✅ "Page load time <2 seconds on 4G connection"
❌ "Fast loading website"

✅ "Mobile responsive on devices 375px width and up"
❌ "Works on mobile"

### Define Quantities
✅ "Up to 10 web pages"
❌ "A website"

✅ "2 rounds of revisions per deliverable"
❌ "Reasonable revisions"

### Set Boundaries
✅ "Excludes: Mobile app development, API integrations, ongoing maintenance"
❌ No exclusions listed

### Manage Risk
✅ "Assumes client provides API documentation. If not available, additional research time at $X/hour"
❌ No assumptions documented

## Common Scope Pitfalls

### Vague Language
❌ "User-friendly interface"
✅ "Interface follows WCAG 2.1 AA accessibility guidelines"

❌ "High-quality code"
✅ "Code passes ESLint, has 80%+ test coverage, includes inline documentation"

❌ "Modern design"
✅ "Design follows Material Design principles, responsive on devices 375px+"

### Unlimited Commitments
❌ "Unlimited revisions"
✅ "3 rounds of revisions included, additional at $X/hour"

❌ "Ongoing support included"
✅ "30 days bug fix support included, ongoing support available at $X/month"

❌ "Will work until client is satisfied"
✅ "Deliverable accepted when acceptance criteria met"

### Missing Exclusions
❌ Scope: "Build e-commerce website"
✅ "Build e-commerce website (excludes: payment processing integration, product photography, shipping configuration, tax calculations)"

## Scope Creep Prevention

### During Kickoff
```
1. Review scope in detail
2. Get explicit agreement on what's included/excluded
3. Establish change request process
4. Set expectations for revisions
5. Clarify communication channels
```

### During Project
```
When client requests something new:
1. "That's a great idea! Let me check if it's in scope."
2. Review SOW together
3. If not included: "This would be a change request. Let me provide an estimate."
4. Document everything in writing
5. Get approval before proceeding
```

### Handling Scope Creep
```
Client: "Can you also add [new feature]?"

You: "I'd be happy to! That wasn't in the original scope. Let me put together a change request with:
- Impact on timeline
- Additional cost
- Updated deliverables

Should take me a day to assess. Sound good?"
```

## Creating Scope with Onboarding Server

```python
# Example usage
generate_scope_of_work(
    client_name="AcmeCorp",
    project_name="Customer Portal",
    objectives=[
        "Reduce support tickets by 40%",
        "Enable self-service account management",
        "Launch to 1,000 beta users in 90 days"
    ],
    deliverables=[
        {
            "name": "User Authentication",
            "description": "Secure login system",
            "acceptance_criteria": [
                "Email/password registration",
                "Password reset functionality",
                "Session management"
            ]
        },
        {
            "name": "Account Dashboard",
            "description": "Main user interface",
            "acceptance_criteria": [
                "Shows account status",
                "Mobile responsive",
                "Loads in <2 seconds"
            ]
        }
    ],
    timeline="8 weeks",
    budget=15000,
    assumptions=[
        "Client provides database access",
        "Design mockups provided by Week 1",
        "Weekly review meetings"
    ],
    exclusions=[
        "Mobile native apps",
        "Payment processing",
        "Content creation"
    ]
)
```

## Example Workflows

### Creating New SOW
```
1. Conduct discovery meeting
2. Gather all requirements
3. Break down into deliverables
4. Define acceptance criteria
5. Estimate timeline and cost
6. List assumptions and exclusions
7. Generate SOW using onboarding_server
8. Review internally
9. Send to client
10. Discuss and refine
11. Get signed approval
```

### Handling Change Requests
```
1. Client requests change
2. Review against current scope
3. Assess impact:
   - Timeline: +X days
   - Cost: +$Y
   - Dependencies affected
4. Document in change request
5. Send to client for approval
6. Get written approval
7. Update SOW
8. Proceed with work
```

---

**Remember:** A clear scope protects both you and your client. Invest time upfront to define scope precisely, and you'll avoid conflicts and scope creep later.
