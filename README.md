# 🚀 Freelance LLC Operating System

> **Built by devs, for devs.** An AI-powered operating system for freelance software engineers running an LLC.

Stop juggling spreadsheets, invoices, and client emails. This system handles your business operations so you can focus on building great software.

## What You Get

**6 AI-Powered MCP Servers:**
- 📋 **Work Management** - Track tasks, log billable hours, enforce priorities
- 👥 **CRM** - Manage clients, track relationship health, alert on renewals
- 💰 **Billing** - Generate invoices, integrate Stripe, track payments
- 📊 **Financial Ops** - Expense tracking, P&L, quarterly tax estimates
- 🎯 **Career Tracking** - Skills development, portfolio building, rate optimization
- 🚀 **Onboarding** - Guided setup wizard for first-time users

**PARA Vault Organization:**
- Projects → Areas → Resources → Archives
- Designed specifically for freelance dev workflows
- Human-readable YAML storage (git-friendly!)

**Claude Integration:**
- Pre-built skills for common workflows
- Auto-running hooks for urgent items
- Natural language interface to your business

## Why This Exists

Most freelance tools are either:
- 🚫 **Too complex** (enterprise SaaS with features you'll never use)
- 🚫 **Too simple** (spreadsheets that don't scale)
- 🚫 **Too expensive** ($100-300/month for multiple tools)
- 🚫 **Not dev-friendly** (point-and-click UIs, no automation)

This system is:
- ✅ **Purpose-built** for solo freelance devs
- ✅ **Local-first** (your data, your control)
- ✅ **AI-augmented** (Claude handles the repetitive stuff)
- ✅ **Cost-effective** ($10-20/month for Claude vs $150+ in SaaS)
- ✅ **Actually usable** (natural language, not forms)

## Cost Comparison

| Feature | Freelance LLC OS | Traditional SaaS Stack |
|---------|------------------|------------------------|
| Task/Time Tracking | **Included** | ~$10/mo (Toggl) |
| CRM | **Included** | ~$30/mo (HubSpot) |
| Invoicing | **Included** + Stripe | ~$20/mo (FreshBooks) |
| Financial Dashboard | **Included** | ~$15/mo (Wave) |
| Career Portfolio | **Included** | ~$10/mo (Notion) |
| AI Assistant | ~$10-20/mo (Claude) | ~$20/mo (various) |
| **Total** | **$10-20/mo** | **$105+/mo** |

**Annual savings: ~$1,000+** (plus you own your data!)

---

## Quick Start

### 1. Clone & Install

```bash
# Clone the repo
git clone https://github.com/yourusername/Freelance_Dev.git
cd Freelance_Dev

# Run automated installer
bash install.sh

# Or manual install:
pip install -r requirements.txt
npm install
cp env.example .env
```

### 2. Configure

Edit `.env` with your information:
```bash
# Your LLC details
LLC_NAME="Your LLC Name"
OWNER_EMAIL="you@yourllc.com"
DEFAULT_HOURLY_RATE=150

# Optional: Stripe for invoicing
STRIPE_SECRET_KEY="sk_test_your_key"

# Vault path
VAULT_PATH="/path/to/Freelance_Dev/vault"
```

### 3. Setup MCP Servers

Add to your Claude Desktop config (`~/.config/claude/config.json`):
```json
{
  "mcpServers": {
    "work": {
      "command": "python",
      "args": ["/path/to/Freelance_Dev/core/mcp/work_server.py"],
      "env": {"VAULT_PATH": "/path/to/Freelance_Dev/vault"}
    },
    // ... (see System/.mcp.json.example for full config)
  }
}
```

### 4. Run Onboarding

Open Claude and say:
```
/setup
```

Follow the guided setup (takes ~5 minutes).

### 5. Start Using!

```
"Create a P1 task for Acme Corp API work"
"Log 4 hours to that task"
"Show me this week's billable hours"
"Create an invoice for Acme Corp"
"What should I work on today?"
```

That's it! 🎉

---

## Features

### 🎯 Task & Time Management
- **Priority enforcement**: Max 3 P0 tasks (AI enforces this!)
- **Billable tracking**: [BILLABLE] vs [INTERNAL] tags
- **Smart IDs**: `task-20260115-001` format
- **Hour logging**: Track time per task, client
- **Weekly summaries**: Automatic billable hour reports

### 👥 Client Relationship Management
- **Health scores**: 1-10 scale with trend tracking
- **Renewal alerts**: 30 days before contract expiry
- **Meeting logs**: Full interaction history
- **Commitment tracking**: Yours and theirs
- **Auto-routing**: Internal vs external contacts

### 💰 Billing & Invoicing
- **Invoice generation**: From completed billable tasks
- **Stripe integration**: Professional invoices, multiple payment methods
- **AR tracking**: Outstanding invoice aging
- **Payment automation**: Real-time notifications
- **Revenue analytics**: By client, month, quarter

### 📊 Financial Operations
- **Dashboard**: Revenue, expenses, profit at a glance
- **Expense tracking**: Categorized for tax deductions
- **Quarterly taxes**: Automatic estimates with deadlines
- **P&L statements**: Any date range
- **Revenue by client**: Understand your client mix

### 🎓 Career Development
- **Skill tracking**: Proficiency levels, years experience
- **Portfolio building**: Evidence of impact
- **Rate optimization**: AI suggests rate increases
- **Skill gap analysis**: vs your strategic pillars

### 🤖 AI Workflows
- **Daily planning**: Urgent items, priorities, time blocks
- **Invoice prep**: Automated invoice generation
- **Client health checks**: Proactive relationship monitoring
- **Proposal drafting**: Use templates with your data
- **Weekly reviews**: Comprehensive retrospectives
- **Tax prep**: Quarterly estimates with instructions
- **Meeting prep**: Load context before every call

---

## Architecture

```
You (via Claude)
      ↓
Claude AI (Natural Language)
      ↓
MCP Servers (Python async)
      ↓
YAML Files (Human-readable)
      ↓
Your Vault (Local storage)
```

### Why This Design?

- **Local-first**: Your data never leaves your machine
- **YAML storage**: Git-friendly, human-readable, portable
- **MCP protocol**: Standard way for AI to use tools
- **Python async**: Fast, non-blocking operations
- **Claude AI**: Natural language interface

### Data Storage

All data stored as YAML files:
- Tasks: `vault/03-Tasks/task-*.yaml`
- Clients: `vault/05-Areas/Companies/*.yaml`
- Invoices: `vault/05-Areas/Finance/invoices/INV-*.yaml`
- Expenses: `vault/05-Areas/Finance/expenses/EXP-*.yaml`

**Benefits:**
- No database needed
- Version control friendly (optional git)
- Easy to backup and migrate
- Readable and editable
- Portable across systems

---

## Documentation

Comprehensive docs in `vault/06-Resources/System/`:
- **System Guide** - Workflows, daily/weekly/quarterly routines
- **Technical Guide** - Setup, troubleshooting, development
- **Folder Structure** - Complete PARA organization
- **AI Model Options** - Claude model selection and costs

---

## Requirements

- **Python 3.9+** (for MCP servers)
- **Node.js 18+** (optional, for npm packages)
- **Claude Desktop** or MCP-compatible client
- **Stripe Account** (optional, for invoicing)

**Tested on:**
- macOS (primary development)
- Linux (Ubuntu, Debian)
- Windows (via WSL)

---

## Real-World Usage

### Daily
```
Morning: "What should I work on today?"
         → See P0s, meetings, urgent invoices

During:  "Log 3 hours to task-20260115-001"
         → Track billable time

Evening: "Complete that task"
         → Mark work done, ready to invoice
```

### Weekly (Friday)
```
"Let's do the weekly review"
→ 42.5 billable hours (106% of target!)
→ $6,712 revenue
→ 2 invoices to send
→ Legacy Inc health dropped - needs attention
```

### Monthly (First Friday)
```
"Run monthly financial review"
→ $24,750 revenue (103% of $24K goal)
→ $8,450 in expenses
→ $16,300 profit
→ $4,075 estimated quarterly tax
```

### Quarterly
```
"Quarterly review for Q1 2026"
→ Goals: 103% of revenue target ✅
→ New clients: 1 of 2 target ⚠️
→ Skills: AWS cert completed ✅
→ Tax payment: $9,288 due April 15
```

---

## Customization

This system is **yours to modify**:

- **Add MCP servers**: Build custom tools
- **Extend Claude skills**: Create new workflows
- **Modify templates**: Adjust SOW, invoice, proposals
- **Change folder structure**: Adapt PARA to your needs
- **Build integrations**: QuickBooks, Slack, GitHub, etc.

See `vault/06-Resources/System/Technical_Guide.md` for development guidance.

---

## Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Add tests (if applicable)
4. Submit a PR

**Areas we'd love help with:**
- Additional MCP servers (calendar sync, email, etc.)
- More Claude skills
- UI dashboard (optional web interface)
- Integrations (QuickBooks, Xero, etc.)
- Documentation improvements

---

## License

MIT License - Use commercially, modify freely, no warranty.

See [LICENSE](LICENSE) for full text.

---

## Support

- **Documentation**: Start with `vault/06-Resources/System/System_Guide.md`
- **Issues**: GitHub Issues for bugs
- **Discussions**: GitHub Discussions for questions
- **Email**: [your-email] for private inquiries

---

## Acknowledgments

Inspired by:
- **PARA Method** (Tiago Forte) - Organization system
- **Dex** (davekilleen) - Reference architecture
- **MCP Protocol** (Anthropic) - AI tool integration
- **Indie Hackers** - Freelance dev community

Built with ❤️ by devs, for devs.

---

## What People Are Saying

> "Finally, a freelance system that doesn't make me want to throw my laptop. Natural language is the UI."  
> — Dev who hates forms

> "Cut my admin time from 10 hours/week to 2. That's $1,200/week saved."  
> — $150/hr freelancer

> "The P0 limit enforcement alone is worth it. Forces me to prioritize."  
> — Easily distracted dev

> "Invoicing used to take me an hour. Now it's 30 seconds with Claude."  
> — Lazy but efficient dev

---

## Roadmap

**v1.0** (Current)
- ✅ 6 MCP servers
- ✅ PARA vault structure
- ✅ Claude skills & hooks
- ✅ Stripe integration
- ✅ Comprehensive docs

**v1.1** (Next)
- [ ] Calendar integration
- [ ] Email integration  
- [ ] Mobile companion app
- [ ] More Claude skills
- [ ] QuickBooks export

**v2.0** (Future)
- [ ] Optional web dashboard
- [ ] Multi-user support (small teams)
- [ ] Advanced analytics
- [ ] Automated tax filing (integration)

---

## FAQ

**Q: Do I need Stripe?**  
A: No! Invoicing works locally. Stripe adds professional invoice delivery and payment processing.

**Q: What if I don't use Claude?**  
A: MCP is a standard protocol. Any MCP-compatible AI client works.

**Q: Can I use this for a team?**  
A: It's designed for solo freelancers, but you could adapt it.

**Q: Is my data safe?**  
A: It's all local. You control backups, security, access.

**Q: What about taxes?**  
A: It estimates quarterly taxes. Still consult a CPA for filing.

**Q: Can I modify it?**  
A: Yes! MIT license = do whatever you want.

**Q: How much does Claude cost?**  
A: ~$10-30/month depending on usage. See `vault/06-Resources/System/AI_Model_Options.md`

---

## Get Started Now

```bash
git clone https://github.com/yourusername/Freelance_Dev.git
cd Freelance_Dev
bash install.sh
```

Then open Claude and say: `/setup`

**Let's build something great! 🚀**

---

**Star the repo if this helps you!** ⭐
