# Contract Drafter Skill

## Description
Draft, review, and manage freelance contracts and legal agreements to protect your interests and establish clear working relationships.

## When to Use This Skill
- Creating service agreements for new clients
- Drafting NDAs and confidentiality agreements
- Generating statements of work
- Reviewing client-provided contracts
- Updating contract templates
- Managing contract lifecycle

## MCP Servers Used
- **onboarding_server**: For contract creation and tracking
- **client_server**: For client information
- **llc_ops_server**: For entity details and document storage

## Key Contract Types

### 1. Service Agreement / Independent Contractor Agreement
Standard agreement for freelance services.

**Must Include:**
- Parties and effective date
- Scope of services
- Payment terms and schedule
- Project timeline
- Intellectual property rights
- Confidentiality provisions
- Termination clauses
- Limitation of liability
- Governing law

### 2. Non-Disclosure Agreement (NDA)
Protects confidential information.

**Two Types:**
- **One-Way**: Client shares confidential info with you
- **Mutual**: Both parties share confidential info

**Must Include:**
- Definition of confidential information
- Obligations and restrictions
- Exclusions from confidentiality
- Term and termination
- Return of materials
- Remedies for breach

### 3. Master Service Agreement (MSA)
Framework agreement for ongoing relationship.

**Benefits:**
- One-time negotiation of terms
- Quick project starts
- Consistent terms across projects
- Individual SOWs for each project

**Must Include:**
- General terms and conditions
- Payment framework
- IP ownership default
- Process for adding SOWs
- Term and renewal

### 4. Statement of Work (SOW)
Project-specific details under MSA or standalone.

**Must Include:**
- Specific deliverables
- Acceptance criteria
- Timeline and milestones
- Project-specific pricing
- Dependencies and assumptions
- Change request process

## Contract Drafting Process

### Step 1: Information Gathering
```
- Client legal name and address
- Project scope and deliverables
- Timeline and milestones
- Payment amount and schedule
- Special requirements
- Existing client agreements
```

### Step 2: Template Selection
```
- Choose appropriate contract type
- Review template for completeness
- Check for outdated provisions
- Verify jurisdiction is correct
```

### Step 3: Customization
```
- Fill in all party information
- Customize scope of work
- Set specific payment terms
- Adjust timeline
- Add project-specific clauses
- Remove non-applicable sections
```

### Step 4: Review
```
- Read entire contract carefully
- Check for internal consistency
- Verify all placeholders replaced
- Ensure clear and unambiguous language
- Consider having attorney review
```

### Step 5: Execution
```
- Send to client for review
- Allow time for questions
- Negotiate terms if needed
- Execute via digital signature
- Store signed copy securely
```

## Essential Contract Clauses

### Scope of Work
```
"Contractor agrees to provide the following services:
[Detailed description of deliverables]

This agreement specifically excludes:
[List what's NOT included]"
```

### Payment Terms
```
"Client agrees to pay Contractor:
- Total Project Fee: $[Amount]
- Payment Schedule: [Details]
- Payment Method: [Wire/ACH/Check/Card]
- Late Fee: [X]% per month on overdue amounts
- Expenses: [Billable/Not billable]"
```

### Intellectual Property
**Option A - Work for Hire:**
```
"All work product created shall be considered
'work made for hire' and owned by Client upon
receipt of full payment."
```

**Option B - License:**
```
"Contractor retains ownership of work product
and grants Client an exclusive, royalty-free,
perpetual license to use the deliverables."
```

### Termination
```
"Either party may terminate this agreement with
[X] days written notice. Upon termination:
- Client pays for work completed to date
- Contractor delivers work in progress
- Confidentiality obligations survive
- IP rights vest per payment received"
```

### Limitation of Liability
```
"Contractor's total liability under this agreement
shall not exceed the fees paid by Client. Contractor
is not liable for indirect, consequential, or special
damages."
```

## Red Flags in Client Contracts

🚩 **Avoid These Terms:**

**Unlimited Liability**
- "Contractor is fully liable for all damages..."
- Negotiate cap on liability

**Unfavorable IP Terms**
- "All work product immediately owned by Client..."
- Add "upon full payment" condition

**Unreasonable Warranty**
- "Contractor warrants work will be error-free..."
- Limit to "professional standards"

**Spec Work Requirements**
- "Submit detailed proposal before contract..."
- Charge for substantial proposals

**Automatic Renewal**
- "Contract auto-renews unless canceled 90 days prior..."
- Prefer explicit renewal

**Non-Compete Overreach**
- "Cannot work with anyone in tech industry..."
- Narrow to direct competitors only

**Payment on Completion Only**
- "Full payment upon final approval..."
- Require deposits and milestone payments

## Contract Negotiation Tips

### When Client Pushes Back

**On Rates:**
- Explain value and expertise
- Show market research
- Offer payment plans, not rate cuts
- Stand firm on minimum rate

**On Timeline:**
- Explain realistic schedule
- Offer phased approach
- Identify dependencies
- Set clear milestones

**On Scope:**
- Clarify what's included
- Price additional requests
- Use change request process
- Document everything

**On Payment Terms:**
- Explain cash flow needs
- Offer small discount for advance payment
- Require deposit (25-50%)
- Hold firm on payment schedule

### Compromise Strategies

**When to Compromise:**
- Non-critical terms
- Standard industry practices
- Long-term relationship potential
- Fair client concerns

**When to Hold Firm:**
- Payment terms
- IP ownership before payment
- Unlimited liability
- Unreasonable scope
- Below-market rates

## Contract Management

### During Project
```
- Store signed contract securely
- Review terms before major decisions
- Track deliverables against contract
- Document scope changes
- Enforce payment terms
- Note any contract issues
```

### Contract Modifications
```
- Must be in writing
- Signed by both parties
- Reference original agreement
- Specify effective date
- Update stored copy
```

### Change Request Process
```
1. Client requests change
2. Assess impact on scope/timeline/cost
3. Provide written change estimate
4. Get approval before proceeding
5. Update project documentation
6. Invoice per change terms
```

### At Project End
```
- Verify all deliverables completed
- Ensure final payment received
- Exchange mutual releases (if applicable)
- Gather testimonial
- Store final contract version
- Note lessons learned
```

## Templates to Maintain

Create and maintain these templates:

1. **Standard Service Agreement** - Your standard terms
2. **NDA Template** - One-way and mutual versions
3. **MSA Template** - For ongoing clients
4. **SOW Template** - Project-specific details
5. **Change Request Form** - Scope modification process
6. **Project Completion Certificate** - Sign-off document

## Legal Resources

### When to Consult Attorney
- First contract draft
- Complex project terms
- Multi-party agreements
- International clients
- Significant project value
- Unusual requirements
- Dispute resolution

### DIY Resources
- State bar association
- SCORE mentors
- LegalZoom (basic templates)
- Rocket Lawyer
- Industry associations
- Fellow freelancers

## Document Storage

**Organize contracts:**
```
contracts/
├── templates/
├── active/
│   ├── [Client-Name]_[Type]_[Date].pdf
├── completed/
└── archived/
```

**Track in LLC Ops Server:**
- Upload using upload_document()
- Tag by client and year
- Set expiration reminders
- Link to client record

## Best Practices

✅ **Do:**
- Get everything in writing
- Read carefully before signing
- Keep signed copies
- Review templates annually
- Consult attorney when unsure
- Use clear, simple language

❌ **Don't:**
- Start work without contract
- Use outdated templates
- Sign without reading
- Accept unfavorable terms
- Forget to update client info
- Lose signed contracts

## Example Workflows

### New Client Contract
```
1. Gather project details
2. Select appropriate template
3. Customize for project
4. Generate via onboarding_server
5. Send to client
6. Answer questions
7. Negotiate if needed
8. Execute digitally
9. Store securely
10. Create project in work_server
```

### Contract Review Checklist
```
- [ ] Parties correctly identified
- [ ] Scope clearly defined
- [ ] Deliverables specific
- [ ] Payment terms acceptable
- [ ] Timeline realistic
- [ ] IP ownership clear
- [ ] Termination fair
- [ ] Liability limited
- [ ] Confidentiality included
- [ ] Governing law appropriate
```

---

**Remember:** A good contract protects both parties and prevents misunderstandings. Invest time in getting contracts right, and you'll save headaches later.
