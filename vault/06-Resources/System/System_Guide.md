# 📘 Freelance LLC Operating System - System Guide

## Welcome to Your AI-Powered LLC OS

This system is purpose-built for freelance software engineers running an LLC. It combines the PARA organizational method with AI-powered automation via MCP (Model Context Protocol) servers.

## Core Philosophy

**Built by devs, for devs** - This isn't another bloated SaaS platform. It's a clean, local-first system that you own and control.

### Design Principles
1. **Local-first**: Your data lives on your machine
2. **AI-augmented**: Claude handles repetitive ops via MCP
3. **YAML-based**: Human-readable, git-friendly data storage
4. **Modular**: Use what you need, ignore the rest
5. **Extensible**: Add your own MCP servers and workflows

## System Architecture

```
┌─────────────────────────────────────────────────┐
│              Claude AI Assistant                │
│         (via MCP protocol)                      │
└────────────┬───────────────────────────┬────────┘
             │                           │
    ┌────────▼────────┐         ┌───────▼────────┐
    │  MCP Servers    │         │   Your Vault   │
    │  (Python async) │◄────────►│   (YAML data)  │
    └────────┬────────┘         └───────┬────────┘
             │                           │
    ┌────────▼────────┐         ┌───────▼────────┐
    │  Stripe API     │         │  Git tracking  │
    │  (payments)     │         │  (optional)    │
    └─────────────────┘         └────────────────┘
```

## Six MCP Servers

### 1. Work Server (`work_server.py`)
**Purpose**: Task and time tracking
- Task IDs: `task-YYYYMMDD-XXX`
- Priority enforcement (max 3 P0s)
- [BILLABLE] vs [INTERNAL] tagging
- Hour logging per task
- Billable hours summary by client

### 2. Client Server (`client_server.py`)
**Purpose**: CRM and relationship management
- Internal vs External routing by email
- Relationship health tracking (1-10 score)
- Meeting history and notes
- Commitment tracking (yours & theirs)
- Contract renewal alerts (30 days before)

### 3. Billing Server (`billing_server.py`)
**Purpose**: Invoicing and payment tracking
- Generate invoices from billable tasks
- Stripe integration for professional invoices
- Payment status tracking
- Outstanding invoice aging
- Revenue analytics

### 4. LLC Ops Server (`llc_ops_server.py`)
**Purpose**: Business finance and operations
- Financial dashboard (revenue, expenses, profit)
- Expense logging with categories
- Quarterly tax estimates
- Profit & loss statements
- Revenue by client analysis

### 5. Onboarding Server (`onboarding_server.py`)
**Purpose**: First-time setup wizard
- Guided LLC information collection
- Strategic pillar definition
- Vault folder creation
- .env file generation
- Validation and resume capability

### 6. Career Server (`career_server.py`)
**Purpose**: Professional development
- Skill tracking with proficiency levels
- Evidence and portfolio building
- Rate optimization suggestions
- Skill gap analysis vs. strategic pillars

## PARA Organization

Your vault follows the PARA method:

- **00-Inbox**: Quick capture, process weekly
- **01-Quarter_Goals**: OKRs, strategic planning
- **02-Week_Priorities**: Weekly planning
- **03-Tasks**: Individual work items (MCP managed)
- **04-Projects**: Multi-week engagements
- **05-Areas**: Ongoing responsibilities
  - People (internal contacts)
  - Companies (clients)
  - Finance (invoices, expenses, tax)
  - Business Dev (pipeline, proposals)
- **06-Resources**: Reference materials
- **07-Archives**: Completed work

## Daily Workflow

### Morning (15 min)
1. Open Claude with MCP servers loaded
2. Review priorities: `/daily-plan` skill
3. Check urgent items:
   - P0 tasks (max 3!)
   - Overdue invoices
   - Client commitments due today
4. Time-block your day

### During Work
1. Create tasks as needed: `create_task`
2. Log hours as you work: `log_hours`
3. Take quick notes in `00-Inbox/`
4. Log client meetings immediately: `log_meeting`

### End of Day (10 min)
1. Complete finished tasks: `complete_task`
2. Log any remaining hours
3. Move inbox items to proper folders
4. Review tomorrow's priorities

## Weekly Workflow

### Friday Afternoon (1 hour)
1. Week review: `/week-review` skill
2. Complete all tasks for the week
3. Generate invoices: `/invoice-prep` skill
4. Check client health: `/client-health` skill
5. Plan next week: `/daily-plan` skill
6. Process inbox to zero

## Monthly Workflow

### First Friday (2 hours)
1. Review outstanding invoices
2. Log all business expenses
3. Check contract renewals: `check_renewals`
4. Update client health scores
5. Review revenue: `/week-revenue` skill
6. Update portfolio with recent wins
7. Business development review

## Quarterly Workflow

### First Week of Quarter (4 hours)
1. Review previous quarter goals
2. Run financial dashboard
3. Calculate quarterly taxes: `/tax-prep` skill
4. Update strategic pillars
5. Set next quarter OKRs
6. Archive completed projects
7. Rate review and optimization

## Getting Help

### MCP Server Documentation
See `.claude/reference/mcp-servers.md` for:
- All available tools
- Parameter requirements
- Example calls
- Return formats

### Claude Skills
Pre-built skills in `.claude/skills/`:
- `/setup` - First-time onboarding
- `/daily-plan` - Daily priorities
- `/invoice-prep` - Generate invoices
- `/client-health` - Check relationships
- `/proposal-draft` - Create proposals
- `/week-revenue` - Revenue summary
- `/tax-prep` - Tax estimates
- `/meeting-prep` - Pre-meeting prep
- `/week-review` - Weekly retrospective

### Technical Docs
- `Technical_Guide.md` - Setup, troubleshooting, advanced usage
- `Folder_Structure.md` - Detailed PARA layout
- `AI_Model_Options.md` - Claude model selection

## Best Practices

### Data Management
- **Backup regularly**: Your vault is precious
- **Use git**: Optional but recommended for history
- **Don't edit YAML directly**: Use MCP tools
- **Review weekly**: Keep data current

### Financial Hygiene
- **Invoice promptly**: Within 3 days of completion
- **Track expenses daily**: Don't let receipts pile up
- **Check AR weekly**: Follow up on late payments
- **Quarterly tax prep**: Don't wait until deadline

### Client Management
- **Log meetings immediately**: Capture context while fresh
- **Update health scores**: After major milestones
- **Track commitments**: Both yours and theirs
- **Renewal conversations**: Start 60 days early

### Personal Development
- **Log evidence**: Capture wins and impact
- **Update skills**: As you learn and use
- **Build portfolio**: Showcasable work
- **Review rates**: Quarterly optimization

## Customization

This system is **yours to modify**:
- Add custom MCP servers
- Extend Claude skills
- Modify templates
- Adjust workflows
- Change folder structure

See `Technical_Guide.md` for development guidance.

## Support & Community

- **Issues**: GitHub Issues for bugs
- **Discussions**: GitHub Discussions for questions
- **Contributions**: PRs welcome!
- **License**: MIT - use commercially, modify freely

## Next Steps

1. **Complete onboarding**: Use `/setup` skill
2. **Create first client**: `create_client` tool
3. **Add a task**: `create_task` tool
4. **Start working**: Log hours as you go
5. **Weekly review**: End of first week
6. **First invoice**: End of first billing cycle

Welcome to organized, AI-augmented freelance life! 🚀
