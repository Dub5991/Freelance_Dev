# Setup Skill

## Description
Guide first-time users through system onboarding.

## When to Use
- First time running the system
- When user says "setup" or "onboarding"
- When vault structure doesn't exist
- When .env file is missing

## MCP Tools Used
- `onboarding_server.start_onboarding` - Begin setup
- `onboarding_server.submit_step` - Submit each step
- `onboarding_server.get_onboarding_status` - Check progress
- `onboarding_server.complete_onboarding` - Finalize setup

## Process

1. **Welcome & explain**
2. **Start onboarding**
3. **Guide through 5 steps**
4. **Create vault structure**
5. **Generate .env file**
6. **Verify setup**

## Steps

### Step 1: LLC Information
Collect:
- LLC name
- EIN (XX-XXXXXXX format)

### Step 2: Owner Information
Collect:
- Owner name
- Email address

### Step 3: Billing Rates
Collect:
- Default hourly rate

### Step 4: Stripe Setup
Ask:
- Ready to set up Stripe now? (yes/no)
- If yes: Get API keys
- If no: Can set up later

### Step 5: Strategic Pillars
Collect:
- 2-5 strategic focus areas (e.g., "Cloud Architecture", "AI/ML", "DevOps")

## Output Format

```markdown
👋 WELCOME TO FREELANCE LLC OS

I'm your AI-powered operating system for running a freelance LLC.

Think of me as your:
- Task manager (tracks billable hours)
- CRM (manages client relationships)
- CFO (handles invoicing and finances)
- Career coach (tracks skills and portfolio)

Let's get you set up! This takes about 5 minutes.

---

## SETUP STEP 1 OF 5: LLC INFORMATION

I need some basic info about your LLC.

**What's your LLC name?**
(e.g., "Smith Consulting LLC")

[User provides]

Great! **What's your EIN?**
(Format: XX-XXXXXXX, find it on your LLC formation docs)

[User provides]

✅ LLC Info saved

---

## SETUP STEP 2 OF 5: OWNER INFORMATION

**What's your full name?**

[User provides]

**What's your business email?**
(This helps me route internal vs external contacts)

[User provides]

✅ Owner Info saved

---

## SETUP STEP 3 OF 5: BILLING RATES

**What's your default hourly rate?**
(You can set different rates per client later)

💡 Typical freelance dev rates:
- Junior: $75-100/hr
- Mid-level: $100-150/hr
- Senior: $150-250/hr
- Architect/Specialist: $250-400/hr

[User provides: 150]

✅ Default rate: $150/hr

---

## SETUP STEP 4 OF 5: STRIPE INTEGRATION

Stripe enables professional invoicing with:
- One-click payment links
- Automatic reminders
- Multiple payment methods
- Real-time notifications

**Do you want to set up Stripe now?**
(You can skip and add it later)

[User chooses]

If YES:
```
Great! Here's how:
1. Create account at stripe.com (if you haven't)
2. Get API keys from: dashboard.stripe.com/apikeys
3. You'll add them to .env file after setup

I'll create a placeholder in your .env file.
```

If NO:
```
No problem! You can add Stripe keys to .env anytime.
Invoices will be tracked locally until you connect Stripe.
```

✅ Stripe noted

---

## SETUP STEP 5 OF 5: STRATEGIC PILLARS

Define 2-5 focus areas for your business.
These guide skill development and business development.

💡 Examples:
- "Cloud Architecture, DevOps, Security"
- "Full Stack Web, Mobile, AI Integration"
- "Enterprise Backend, Microservices, Kubernetes"

**What are your strategic pillars?**
(Comma-separated, e.g., "Cloud Architecture, DevOps, AI/ML")

[User provides]

✅ Strategic pillars set

---

## 🎉 SETUP COMPLETE!

Creating your workspace...

✅ Created vault folder structure
✅ Generated .env file
✅ Set up PARA organization
✅ Configured MCP servers

## NEXT STEPS

### 1. Configure Stripe (if you want invoicing)
```bash
# Edit .env file
nano .env

# Add your Stripe keys:
STRIPE_SECRET_KEY=sk_live_YOUR_KEY_HERE
STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_KEY_HERE
```

Get keys from: https://dashboard.stripe.com/apikeys

### 2. Install Dependencies
```bash
pip install -r requirements.txt
npm install
```

### 3. Configure MCP Client
Your MCP client (Claude Desktop) needs to know about the servers.

Example config: `~/.config/claude/config.json`
See: `System/.mcp.json.example` for template

### 4. Start Using!

Try these commands:
- "What should I work on today?" (daily plan)
- "Create a P1 task for [client]" (task creation)
- "Add client [name]" (CRM)
- "Show me this week's revenue" (finances)

## WHAT YOU GOT

**Vault Structure (PARA method):**
- 00-Inbox: Quick capture
- 01-Quarter_Goals: Strategic planning
- 02-Week_Priorities: Weekly focus
- 03-Tasks: Work tracking (MCP managed)
- 04-Projects: Multi-week engagements
- 05-Areas: Clients, finances, business dev
- 06-Resources: Templates and docs
- 07-Archives: Completed work

**6 MCP Servers:**
- work_server: Task and time tracking
- client_server: CRM and relationships
- billing_server: Invoicing with Stripe
- llc_ops_server: Financial operations
- career_server: Skills and portfolio
- onboarding_server: This setup (done!)

**Templates:**
- SOW (Statement of Work)
- Invoice
- Contract (MSA)
- Proposal

**Documentation:**
- System Guide (workflows)
- Technical Guide (setup, troubleshooting)
- Folder Structure (organization)
- AI Model Options (performance vs cost)

## READY TO ROCK! 🚀

You're all set. I'll help you:
- Track billable hours accurately
- Manage client relationships
- Generate and send invoices
- Handle LLC finances
- Develop your career

Let's build something great together!

**What do you want to do first?**
```

## Example Usage

**User:** "/setup"

**Claude:**
```
👋 WELCOME TO FREELANCE LLC OS

I'm your AI-powered business operating system!

This setup takes ~5 minutes. I'll ask you about:
1. Your LLC details
2. Billing rates
3. Stripe integration (optional)
4. Strategic focus areas

Then I'll create your vault structure and configuration files.

Ready to start?
```

[User confirms]

```
## STEP 1/5: LLC INFORMATION

What's your LLC name?
```

[Continues through all steps...]

```
🎉 SETUP COMPLETE!

I've created:
- ✅ Vault structure (PARA organization)
- ✅ .env configuration file
- ✅ MCP server setup

Next:
1. Add Stripe keys to .env (if you want invoicing)
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your MCP client

Try saying: "Create a task" or "Add a client"

Welcome aboard! 🚀
```

## Post-Setup Verification

After onboarding, check:
1. ✅ Vault folders created
2. ✅ .env file exists
3. ✅ README files in place
4. ✅ Templates available
5. ✅ MCP servers can be loaded

If any fail, guide user to fix.

## Troubleshooting

**Common Issues:**

1. **Vault permissions**
   ```bash
   chmod -R u+rw vault/
   ```

2. **MCP servers not loading**
   - Check Python install: `python --version`
   - Install deps: `pip install -r requirements.txt`
   - Verify paths in MCP config

3. **Stripe errors**
   - Keys in .env start with `sk_` and `pk_`
   - Check dashboard.stripe.com/apikeys
   - Test mode keys start with `_test_`

## Follow-Up

After setup:
- Create first client
- Create first task
- Do a quick tour of features
- Point to System Guide for workflows

## Tips
- Be patient and encouraging
- Explain why each step matters
- Offer examples for each input
- Verify data before saving
- Celebrate completion!
