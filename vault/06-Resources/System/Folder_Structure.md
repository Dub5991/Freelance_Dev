# 📁 Folder Structure Guide

## Complete Directory Tree

```
Freelance_Dev/
├── core/
│   └── mcp/                    # MCP servers (Python)
│       ├── __init__.py
│       ├── work_server.py      # Task management
│       ├── client_server.py    # CRM
│       ├── billing_server.py   # Invoicing & Stripe
│       ├── llc_ops_server.py   # Financial operations
│       ├── onboarding_server.py # Setup wizard
│       └── career_server.py    # Career development
│
├── vault/                       # Your PARA workspace
│   ├── 00-Inbox/               # Quick capture
│   │   └── README.md
│   │
│   ├── 01-Quarter_Goals/       # Strategic OKRs
│   │   ├── README.md
│   │   ├── Q1-2026.md
│   │   └── Q2-2026.md
│   │
│   ├── 02-Week_Priorities/     # Weekly planning
│   │   ├── README.md
│   │   ├── Week-2026-01.md
│   │   └── Week-2026-02.md
│   │
│   ├── 03-Tasks/               # MCP-managed tasks
│   │   ├── README.md
│   │   ├── task-20260115-001.yaml  # Auto-created
│   │   └── task-20260115-002.yaml
│   │
│   ├── 04-Projects/            # Multi-week engagements
│   │   ├── README.md
│   │   ├── Project-AcmeCorp-Migration.md
│   │   └── Project-Internal-Website.md
│   │
│   ├── 05-Areas/               # Ongoing responsibilities
│   │   ├── People/             # Internal contacts
│   │   │   ├── README.md
│   │   │   └── john-smith.yaml  # MCP-managed
│   │   │
│   │   ├── Companies/          # External clients
│   │   │   ├── README.md
│   │   │   ├── acme-corp.yaml  # MCP-managed
│   │   │   └── tech-startup.yaml
│   │   │
│   │   ├── Finance/            # Money matters
│   │   │   ├── README.md
│   │   │   ├── invoices/
│   │   │   │   ├── INV-0001.yaml  # MCP-managed
│   │   │   │   └── INV-0002.yaml
│   │   │   ├── expenses/
│   │   │   │   ├── EXP-20260115103045.yaml  # MCP-managed
│   │   │   │   └── EXP-20260116140523.yaml
│   │   │   └── tax/
│   │   │       ├── Q1-2026-Estimate.md
│   │   │       └── 2025-Annual-Tax.md
│   │   │
│   │   ├── Business_Dev/       # Pipeline & growth
│   │   │   ├── README.md
│   │   │   ├── prospect-techstartup.md
│   │   │   └── wins-losses-2026.md
│   │   │
│   │   └── Career/             # Professional development
│   │       ├── skills/
│   │       │   ├── python.yaml  # MCP-managed
│   │       │   └── aws.yaml
│   │       └── portfolio/
│   │           └── portfolio-20260115103045.yaml
│   │
│   ├── 06-Resources/           # Reference materials
│   │   ├── System/             # System documentation
│   │   │   ├── System_Guide.md
│   │   │   ├── Technical_Guide.md
│   │   │   ├── Folder_Structure.md  # This file
│   │   │   └── AI_Model_Options.md
│   │   │
│   │   └── Templates/          # Reusable templates
│   │       ├── SOW_Template.md
│   │       ├── Invoice_Template.md
│   │       ├── Contract_Template.md
│   │       └── Proposal_Template.md
│   │
│   └── 07-Archives/            # Completed work
│       ├── README.md
│       ├── 2025/
│       │   ├── Projects/
│       │   ├── Clients/
│       │   └── Goals/
│       └── 2026/
│
├── .claude/                    # Claude Desktop integration
│   ├── skills/                 # Pre-built skills
│   │   ├── daily-plan/
│   │   │   └── SKILL.md
│   │   ├── invoice-prep/
│   │   │   └── SKILL.md
│   │   ├── client-health/
│   │   │   └── SKILL.md
│   │   ├── proposal-draft/
│   │   │   └── SKILL.md
│   │   ├── week-revenue/
│   │   │   └── SKILL.md
│   │   ├── tax-prep/
│   │   │   └── SKILL.md
│   │   ├── meeting-prep/
│   │   │   └── SKILL.md
│   │   ├── week-review/
│   │   │   └── SKILL.md
│   │   └── setup/
│   │       └── SKILL.md
│   │
│   ├── hooks/                  # Auto-run hooks
│   │   ├── session-start.md
│   │   └── README.md
│   │
│   └── reference/              # MCP documentation
│       └── mcp-servers.md
│
├── System/                     # System configuration
│   └── .mcp.json.example       # MCP config template
│
├── CLAUDE.md                   # Main system prompt
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
├── .gitignore                  # Protect secrets & data
├── .env                        # Your secrets (not committed!)
├── env.example                 # Environment template
├── requirements.txt            # Python dependencies
├── package.json                # Node dependencies
└── install.sh                  # Automated installer
```

## Folder Purposes

### Root Level
- **core/** - MCP server implementations (don't edit unless customizing)
- **vault/** - YOUR workspace (edit freely, use MCP tools)
- **.claude/** - Claude Desktop integration (pre-built skills)
- **System/** - Configuration templates
- **CLAUDE.md** - AI assistant personality and rules
- **README.md** - Getting started guide
- **.env** - Your secrets (created from env.example)

### Vault Organization (PARA)

#### P - Projects (Goal-oriented)
- **00-Inbox**: Capture zone, process weekly
- **01-Quarter_Goals**: 3-month objectives
- **02-Week_Priorities**: 7-day focus
- **03-Tasks**: Individual work items (MCP creates these)
- **04-Projects**: Multi-week engagements with clients

#### A - Areas (Ongoing Responsibilities)
- **05-Areas/People**: Individual contacts
- **05-Areas/Companies**: Corporate clients
- **05-Areas/Finance**: Money tracking
- **05-Areas/Business_Dev**: Sales pipeline
- **05-Areas/Career**: Skills & portfolio

#### R - Resources (Reference)
- **06-Resources/System**: How this system works
- **06-Resources/Templates**: Reusable documents

#### A - Archives (Inactive)
- **07-Archives**: Completed projects, old clients

## File Naming Conventions

### MCP-Managed Files (YAML)
```
task-YYYYMMDD-XXX.yaml          # Tasks
INV-XXXX.yaml                   # Invoices
EXP-YYYYMMDDHHMMSS.yaml         # Expenses
client-name.yaml                # Clients/prospects
skill-name.yaml                 # Skills
portfolio-YYYYMMDDHHMMSS.yaml   # Portfolio items
```

### User-Created Files (Markdown)
```
QX-YYYY.md                      # Quarter goals
Week-YYYY-WW.md                 # Week priorities
Project-ClientName-Title.md     # Projects
prospect-companyname.md         # Prospects
```

## Data Flow

```
User → Claude → MCP Server → YAML File → vault/
                    ↓
            Stripe API (for billing)
```

### Example: Create Task Flow
1. User: "Create a P1 task for Acme Corp API work"
2. Claude calls `work_server.create_task()`
3. Server generates `task-20260115-001.yaml`
4. Server saves to `vault/03-Tasks/`
5. Server returns task ID to Claude
6. Claude confirms to user

### Example: Invoice Flow
1. User: "Create invoice for Acme Corp"
2. Claude calls `billing_server.create_invoice()`
3. Server loads tasks from `vault/03-Tasks/`
4. Server loads client from `vault/05-Areas/Companies/`
5. Server generates `INV-0001.yaml`
6. Server saves to `vault/05-Areas/Finance/invoices/`
7. Server optionally sends via Stripe
8. Claude shows invoice summary

## Storage Size Estimates

Typical usage after 1 year:
```
03-Tasks/           ~500 files   × 1 KB  = 500 KB
05-Areas/Companies/ ~20 files    × 2 KB  = 40 KB
05-Areas/Finance/   ~200 files   × 1 KB  = 200 KB
Total YAML:                              ~1 MB

Markdown notes:                          ~5 MB
Total:                                   ~6 MB
```

**Verdict**: Extremely lightweight, years of data fits in megabytes.

## Git Integration (Optional)

### Recommended .gitignore
```
.env                    # Never commit secrets
.mcp.json              # Local config
vault/**/*.yaml        # User data (or use private repo)
vault/**/*.yml
!vault/**/README.md    # Allow documentation
```

### What to Commit
- ✅ Code (core/)
- ✅ Documentation (README, guides)
- ✅ Templates
- ✅ Claude skills
- ❌ User data (vault YAML files)
- ❌ Secrets (.env)

## Customization

### Adding a Folder
```bash
mkdir -p vault/05-Areas/MyCustomArea
echo "# My Custom Area" > vault/05-Areas/MyCustomArea/README.md
```

### Custom MCP Storage
Edit MCP servers to save elsewhere:
```python
CUSTOM_PATH = Path(VAULT_PATH) / "05-Areas" / "MyCustomArea"
```

### Alternate Organization
Don't like PARA? Restructure:
```
vault/
├── clients/
├── projects/
├── finance/
└── personal/
```
Just update MCP server paths accordingly.

## Migration Paths

### From Other Systems

**Notion/Obsidian → Freelance LLC OS**
1. Export to Markdown
2. Map to PARA folders
3. Convert structured data to YAML
4. Import via MCP tools

**Spreadsheets → Freelance LLC OS**
1. Export clients to CSV
2. Write Python script to convert CSV → YAML
3. Import to `05-Areas/Companies/`
4. Verify with `list_clients`

**Harvest/Toggl → Freelance LLC OS**
1. Export time entries
2. Convert to task YAML format
3. Import to `03-Tasks/`
4. Generate retroactive invoices

## Backup Structure

Recommended backup preserves structure:
```
backup-20260115/
├── vault/              # Full vault copy
├── .env               # Encrypted secrets
└── .mcp.json          # MCP config
```

## Performance

**Scalability Limits**:
- ✅ Up to 10,000 files per folder (smooth)
- ⚠️ 10,000 - 50,000 files (slower, still works)
- ❌ 50,000+ files (consider database)

**Optimization**:
- Archive old data yearly
- Index frequently searched fields
- Cache loaded YAML in memory

## Security

**Sensitive Files**:
- `.env` - API keys, secrets
- `vault/**/*.yaml` - Client data, financials
- `.mcp.json` - May contain paths

**Protection**:
- Use `.gitignore`
- Encrypt backups
- Secure file permissions (chmod 600)
- Never share .env

## Next Steps

1. ✅ Understand this structure
2. ✅ Run `/setup` in Claude to create folders
3. ✅ Start using the system
4. ✅ Customize as needed

**Remember**: This is YOUR system. Modify freely to fit your workflow!
