# Onboarding Specialist Skill

## Description
Run structured client onboarding workflows to ensure smooth project starts and set clear expectations using the Onboarding Server.

## When to Use This Skill
- Starting work with a new client
- Kicking off a new project with existing client
- Creating and managing contracts
- Generating scopes of work
- Tracking onboarding progress
- Sending welcome packets

## MCP Servers Used
- **onboarding_server**: Primary server for workflow management
- **client_server**: For client information
- **billing_server**: For payment setup
- **work_server**: For project task creation

## Step-by-Step Instructions

### 1. Start Onboarding Workflow
```
1. Use start_onboarding() with client details
2. Select appropriate template (standard or custom)
3. Review onboarding steps
4. Set project name and notes
5. Track workflow ID for updates
```

**Example Prompts:**
- "Start onboarding workflow for AcmeCorp website redesign project"
- "Begin new client onboarding for TechStart Inc"

### 2. Track Progress
```
1. Use get_onboarding_status() regularly
2. Review completed vs. remaining steps
3. Check progress percentage
4. Identify next pending step
5. Plan actions accordingly
```

**Example Prompts:**
- "Show onboarding progress for AcmeCorp"
- "What's the next step in the TechStart onboarding?"

### 3. Update Steps
```
1. Complete steps using update_onboarding_step()
2. Mark as: pending, in_progress, completed, or skipped
3. Add notes about completion
4. Move to next step automatically
```

**Example Prompts:**
- "Mark discovery meeting step as completed for AcmeCorp"
- "Update contract signed step with signature date"

### 4. Create Contracts
```
1. Use create_contract() for agreements
2. Choose type: service_agreement, nda, msa, sow
3. Include all terms and conditions
4. Track contract status
5. Record signatures using sign_contract()
```

**Example Prompts:**
- "Create service agreement for AcmeCorp project"
- "Generate NDA for TechStart"
- "Mark contract as signed by client"

### 5. Generate Scope of Work
```
1. Use generate_scope_of_work()
2. Include:
   - Project objectives
   - Detailed deliverables
   - Timeline and milestones
   - Budget
   - Assumptions and exclusions
3. Get client approval
4. Convert to contract
```

**Example Prompts:**
- "Generate scope of work for website redesign"
- "Create SOW with API integration deliverables"

### 6. Send Welcome Packet
```
1. Use send_welcome_packet()
2. Include project overview
3. Add communication guidelines
4. Provide resource links
5. Set expectations clearly
```

**Example Prompts:**
- "Send welcome packet to AcmeCorp"
- "Generate onboarding materials for new client"

## Standard Onboarding Steps

1. **Initial Discovery Meeting** - Understand needs
2. **Create Scope of Work** - Define project
3. **Send Proposal** - Present solution and pricing
4. **Generate Contract** - Create agreement
5. **Contract Signed** - Obtain signatures
6. **Payment Setup** - Configure billing
7. **Send Welcome Packet** - Provide resources
8. **Project Kickoff** - Launch work

## Best Practices

### Discovery Phase
- ✅ Ask detailed questions
- ✅ Understand true goals
- ✅ Identify constraints
- ✅ Assess technical requirements
- ✅ Discuss timeline and budget

### Contract Phase
- ✅ Use clear, simple language
- ✅ Define scope explicitly
- ✅ Include change request process
- ✅ Specify payment terms
- ✅ Address IP ownership

### Kickoff Phase
- ✅ Set communication expectations
- ✅ Introduce team members
- ✅ Review timeline together
- ✅ Establish collaboration tools
- ✅ Schedule regular check-ins

## Scope of Work Template

### Must Include:
1. **Project Overview** - What and why
2. **Objectives** - Measurable goals
3. **Deliverables** - Specific outputs
4. **Timeline** - Milestones and dates
5. **Budget** - Total cost breakdown
6. **Assumptions** - What you're assuming
7. **Exclusions** - What's NOT included
8. **Acceptance Criteria** - Definition of done

### Red Flags to Avoid:
- ❌ Vague deliverables
- ❌ Unlimited revisions
- ❌ Unclear timeline
- ❌ Missing acceptance criteria
- ❌ No change request process

## Contract Essentials

### Key Clauses:
- **Services** - What you'll deliver
- **Timeline** - When you'll deliver it
- **Payment** - How much and when
- **IP Rights** - Who owns the work
- **Confidentiality** - Information protection
- **Termination** - How to end agreement
- **Liability** - Limitation of damages
- **Dispute Resolution** - How to handle conflicts

### Payment Terms Options:
- 50% upfront, 50% on completion
- Monthly retainer
- Milestone-based payments
- Net 30 after delivery
- Per-hour with cap

## Welcome Packet Contents

Include:
- Welcome letter
- Project overview document
- Communication guidelines
- Timeline and milestones
- Team contact information
- Access credentials (if needed)
- Collaboration tool links
- FAQ document
- Next steps checklist

## Error Handling

**"Template not found"**
- Use default template-standard
- Create custom template if needed

**"Required steps incomplete"**
- Complete all required steps before finalizing
- Or skip non-critical steps explicitly

**"Contract already exists"**
- Update existing contract
- Create new version if major changes

## Integration with Other Skills

- **Client Advisor**: Create client profile first
- **Project Manager**: Create initial tasks after kickoff
- **Invoice Handler**: Set up billing after contract
- **Contract Drafter**: Generate proper agreements

## Success Metrics

- Onboarding completion time: Target <7 days
- Client satisfaction after onboarding: Target >4.5/5
- Contract clarity score: No misunderstandings
- Time to first invoice: Target <30 days
- Referrals from well-onboarded clients: Track

## Example Workflows

### New Client Onboarding
```
1. Start onboarding workflow
2. Conduct discovery meeting
3. Generate scope of work
4. Send proposal
5. Create service agreement
6. Get contract signed
7. Set up payment method
8. Send welcome packet
9. Schedule kickoff meeting
10. Complete onboarding
```

### Project Kickoff Meeting Agenda
```
1. Introductions
2. Project goals review
3. Timeline walkthrough
4. Communication plan
5. Tool demonstration
6. Q&A session
7. Next steps agreement
```

---

**Remember:** Good onboarding sets the tone for the entire project. Take time to do it right, and you'll avoid misunderstandings later.
