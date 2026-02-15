# 🚀 Freelance Dev OS

**A comprehensive operating system for running your freelance development business as an LLC**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-102%20passing-success.svg)](#testing)

Freelance Dev OS is an AI-powered business management system built on Model Context Protocol (MCP) servers. It provides intelligent automation for task management, client relationships, billing, tax planning, onboarding workflows, and career development—all designed specifically for freelance developers operating as LLCs.

---

## 🎯 What is Freelance Dev OS?

Freelance Dev OS transforms your business management from scattered tools and spreadsheets into a unified, AI-assisted operating system. Using Claude (or other AI assistants) with specialized MCP servers, you can manage your entire freelance business through natural language conversations.

**Key Benefits:**
- 🤖 **AI-First**: Talk to Claude to manage your business, no complex UIs
- 📊 **Complete Visibility**: Track projects, clients, finances in one place
- 💰 **Revenue-Focused**: Built-in billing, invoicing, and Stripe integration
- 📝 **Tax-Ready**: Automated expense tracking and quarterly tax estimates
- 🎓 **Career Growth**: Skill tracking and portfolio management built-in
- 🏢 **LLC-Optimized**: Compliance checklists and business entity management

---

## 🏗️ Architecture Overview

```
                     ┌─────────────────────────────────┐
                     │   Claude AI Assistant           │
                     │   Enhanced with 9 Skills        │
                     └────────────┬────────────────────┘
                                  │
                         MCP Protocol
                                  │
        ┌─────────────────────────┴─────────────────────────┐
        │                                                     │
        │              MCP Server Ecosystem                  │
        │                                                     │
┌───────┴────────┐  ┌─────────────┐  ┌─────────────────────┴──────┐
│  Work Server   │  │Client Server│  │    Billing Server           │
│  • Projects    │  │  • CRM      │  │    • Invoices               │
│  • Tasks       │  │  • Meetings │  │    • Stripe Integration     │
│  • Time Track  │  │  • Health   │  │    • Revenue Reports        │
└───────┬────────┘  └──────┬──────┘  └────────┬────────────────────┘
        │                   │                   │
┌───────┴────────┐  ┌──────┴──────┐  ┌────────┴────────────────────┐
│ LLC Ops Server │  │ Onboarding  │  │    Career Server            │
│ • Expenses     │  │ • Workflows │  │    • Skills Tracking        │
│ • Taxes        │  │ • SOWs      │  │    • Portfolio              │
│ • Compliance   │  │ • Checklists│  │    • Rate Suggestions       │
└────────────────┘  └─────────────┘  └─────────────────────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                    JSON/YAML Storage
                            │
                   ┌────────┴─────────┐
                   │  data/ directory │
                   │  vault/ (PARA)   │
                   └──────────────────┘
```

---

## ✨ Features

### 📋 Work Server - Project & Task Management
- **Smart Task Tracking**: Unique IDs, priority enforcement (max 3 P0 tasks)
- **Billable Hours**: Track time with client attribution
- **Project Analytics**: Billable summaries, budget burn tracking
- **Status Management**: Active, blocked, completed workflows

### 👥 Client Server - Relationship Management
- **Client Profiles**: Contact info, company details, preferences
- **Health Scoring**: 0-100 scale based on engagement, payments, satisfaction
- **Meeting Logs**: Notes, action items, attendee tracking
- **Communication History**: Email, calls, meetings timeline
- **Renewal Tracking**: Identify at-risk relationships

### 💳 Billing Server - Financial Operations
- **Invoice Generation**: Line items, tax, discounts
- **Stripe Integration**: Payment processing (optional)
- **Payment Tracking**: Partial payments, overdue alerts
- **Revenue Reports**: By period, by client, profit margins
- **Expense Management**: Categorization for tax purposes

### 🏢 LLC Ops Server - Business Operations
- **Entity Management**: EIN, state registration, addresses
- **Tax Deadlines**: Quarterly estimates, annual return reminders
- **Expense Tracking**: Categorized business expenses
- **Compliance Checklist**: State filings, licenses, renewals
- **Document Storage**: Operating agreements, registrations

### 🎯 Onboarding Server - Client Onboarding
- **Workflow Templates**: Web dev, consulting, mobile app
- **Multi-Step Process**: From consultation to contract signing
- **SOW Generation**: Statement of Work with scope, deliverables, pricing
- **Checklist Tracking**: Ensure nothing is missed
- **Progress Monitoring**: Know where each client stands

### 🎓 Career Server - Professional Development
- **Skill Library**: Track proficiency levels, years of experience
- **Evidence Logging**: Projects, courses, certifications
- **Portfolio Management**: Showcase completed work
- **Rate Suggestions**: AI-powered pricing based on skills
- **Skill Gap Analysis**: Identify areas for growth
- **Learning Plans**: Structured skill development roadmaps

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dub5991/Freelance_Dev.git
   cd Freelance_Dev
   ```

2. **Run the installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   The script will:
   - Check Python version
   - Create a virtual environment
   - Install dependencies
   - Set up directories
   - Create `.env` from template

3. **Configure your environment**
   ```bash
   nano .env  # or vim, or your favorite editor
   ```

   Update these key values:
   ```env
   LLC_NAME="Your Freelance LLC"
   OWNER_NAME="Your Name"
   DEFAULT_HOURLY_RATE=150.0
   STRIPE_API_KEY=sk_test_your_key  # Optional
   LLC_EIN="12-3456789"
   ```

4. **Verify installation**
   ```bash
   source venv/bin/activate
   python -m core.mcp.work_server
   pytest tests/ -v
   ```

---

## 📖 Usage Examples

### Managing Tasks

```python
from core.mcp.work_server import create_task, log_hours, get_billable_summary

# Create a billable task
task = create_task(
    title="Build user authentication API",
    priority="P0",
    billable=True,
    client="AcmeCorp",
    estimated_hours=20.0
)

# Log hours worked
log_hours(
    task_id=task["task_id"],
    hours=5.5,
    description="Implemented OAuth2 flow and JWT tokens"
)

# Get billable summary
summary = get_billable_summary(
    client="AcmeCorp",
    period="current_month"
)
print(f"Total billable: {summary['total_billable_hours']}h")
```

### Client Management

```python
from core.mcp.client_server import ClientServer

server = ClientServer()

# Create a new client
client = server.create_client(
    name="John Doe",
    email="john@acmecorp.com",
    company="Acme Corp",
    phone="+1-555-123-4567"
)

# Log a meeting
meeting = server.schedule_meeting(
    client_id=client["client_id"],
    title="Project Kickoff",
    scheduled_time="2024-07-01T10:00:00",
    agenda="Discuss requirements and timeline"
)

# Check client health
health = server.calculate_health_score(client["client_id"])
print(f"Client health: {health['health_score']}/100")
```

### Creating Invoices

```python
from core.mcp.billing_server import BillingServer

billing = BillingServer()

# Create an invoice
invoice = billing.create_invoice(
    client_id="client-123",
    client_name="Acme Corp",
    items=[
        {
            "description": "Web Development (40 hrs @ $150/hr)",
            "quantity": 40,
            "rate": 150.0
        },
        {
            "description": "Consulting (10 hrs @ $200/hr)",
            "quantity": 10,
            "rate": 200.0
        }
    ],
    tax_rate=0.08,  # 8% tax
    notes="Payment due within 30 days"
)

# Total: $6000 + $2000 = $8000 + $640 tax = $8640
```

### With Claude (Natural Language)

Once configured with Claude's MCP support:

```
You: "Create a P0 task for the API integration project with AcmeCorp, estimate 25 hours"

Claude: [calls work_server.create_task]
"I've created task-20240615-001 for the API integration project. It's marked as P0 
priority, billable to AcmeCorp, with 25 estimated hours."

You: "Log 6 hours on that task. I finished the authentication endpoints today."

Claude: [calls work_server.log_hours]
"Logged 6 hours on task-20240615-001. You have 19 hours remaining on the estimate."

You: "How are my billable hours looking this month?"

Claude: [calls work_server.get_billable_summary]
"This month you've logged 87.5 billable hours:
- AcmeCorp: 45.5 hours
- TechCorp: 32 hours  
- StartupCo: 10 hours"
```

---

## 📂 PARA Vault Structure

The `vault/` directory uses the PARA methodology for organizing business information:

```
vault/
├── 1-Projects/              # Active client projects
│   ├── _templates/          # Project templates
│   └── [project-folders]/   # Individual projects
├── 2-Areas/                 # Areas of responsibility
│   ├── business-ops/        # Business operations
│   ├── client-relations/    # Client relationship docs
│   ├── finance/             # Financial records
│   └── professional-development/
├── 3-Resources/             # Reference materials
│   ├── contracts/           # Contract templates
│   ├── templates/           # Document templates
│   └── tools/               # Tool configurations
└── 4-Archive/               # Completed/inactive items
```

**PARA stands for:**
- **P**rojects: Time-bound efforts with deadlines
- **A**reas: Ongoing responsibilities
- **R**esources: Reference materials
- **A**rchive: Completed items

---

## 🎭 Claude Skills Overview

Located in `.claude/skills/`, these skills enhance Claude's ability to help you:

| Skill | Purpose | Primary Server |
|-------|---------|----------------|
| **project-manager** | End-to-end project management | work_server |
| **client-advisor** | Client relationship management | client_server |
| **invoice-handler** | Invoicing and payment tracking | billing_server |
| **tax-strategist** | Tax planning and estimates | llc_ops_server |
| **onboarding-specialist** | Client onboarding workflows | onboarding_server |
| **career-coach** | Career development planning | career_server |
| **contract-drafter** | Contract drafting and review | Multiple servers |
| **weekly-reviewer** | Business reviews and reports | All servers |
| **scope-writer** | Scope of work creation | onboarding_server |

Each skill contains:
- Detailed step-by-step instructions
- Example prompts and expected outputs
- Integration points with other skills
- Error handling guidance
- Best practices

---

## ⚙️ Configuration

### Environment Variables

Key configuration options in `.env`:

**Business Information**
```env
LLC_NAME="Your Freelance LLC"
LLC_EIN="12-3456789"
LLC_STATE="CA"
OWNER_NAME="Your Name"
```

**Billing**
```env
DEFAULT_HOURLY_RATE=150.0
DEFAULT_CURRENCY=USD
PAYMENT_TERMS_DAYS=30
```

**Stripe Integration** (Optional)
```env
STRIPE_API_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret
```

**Taxes**
```env
TAX_YEAR=2024
QUARTERLY_TAX_RATE=0.30
```

**Email Notifications** (Optional)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

See `.env.example` for complete configuration options.

---

## 🧪 Testing

The project includes comprehensive test coverage for all MCP servers.

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_work_server.py -v

# Run with coverage
pytest tests/ --cov=core --cov-report=html

# Run specific test
pytest tests/test_billing_server.py::test_create_invoice_basic -v
```

### Test Structure

- `tests/test_work_server.py` - 18 tests for task management
- `tests/test_client_server.py` - 15 tests for CRM
- `tests/test_billing_server.py` - 20 tests for billing/invoicing
- `tests/test_llc_ops_server.py` - 14 tests for LLC operations
- `tests/test_onboarding_server.py` - 16 tests for onboarding
- `tests/test_career_server.py` - 19 tests for career development

**Total: 102 tests** covering all core functionality.

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. Fork the repository
2. Clone your fork
3. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes
5. Run tests to ensure everything works
   ```bash
   pytest tests/ -v
   ```
6. Commit with descriptive messages
   ```bash
   git commit -m "Add: New feature description"
   ```
7. Push to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
8. Create a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings in Google style format
- Add tests for new features
- Keep functions focused and small
- Use descriptive variable names

### Adding a New MCP Server

1. Create `core/mcp/your_server.py`
2. Inherit from `BaseMCPServer`
3. Implement required methods
4. Add tests in `tests/test_your_server.py`
5. Update documentation
6. Create corresponding Claude skill

See `CLAUDE.md` for detailed development guidelines.

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Freelance Dev OS Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full license text in LICENSE file]
```

---

## 🙏 Credits & Acknowledgments

**Inspired by [davekilleen/Dex](https://github.com/davekilleen/Dex)**  
The Dex project pioneered the concept of AI-powered developer tools using MCP. Freelance Dev OS builds on these ideas specifically for freelance business management.

**Built with:**
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) by Anthropic
- [Claude](https://www.anthropic.com/claude) AI assistant
- [Stripe](https://stripe.com/) for payment processing
- Python ecosystem: pytest, pydantic, pyyaml, rich

**Community:**
- Issue tracking: [GitHub Issues](https://github.com/Dub5991/Freelance_Dev/issues)
- Discussions: [GitHub Discussions](https://github.com/Dub5991/Freelance_Dev/discussions)

---

## 📞 Support & Resources

### Documentation
- **User Guide**: See this README
- **Developer Guide**: See [CLAUDE.md](CLAUDE.md)
- **API Documentation**: Docstrings in each server file
- **Skills Guide**: See `.claude/skills/` directory

### Getting Help
1. Check the [FAQ section](https://github.com/Dub5991/Freelance_Dev/wiki/FAQ) (coming soon)
2. Search [existing issues](https://github.com/Dub5991/Freelance_Dev/issues)
3. Ask in [Discussions](https://github.com/Dub5991/Freelance_Dev/discussions)
4. Create a new issue with detailed description

### Roadmap

**Current Features (v0.1.0)**
- ✅ 6 MCP servers with full functionality
- ✅ PARA vault organization
- ✅ 9 Claude skills
- ✅ Comprehensive test suite
- ✅ Stripe integration

**Planned Features (v0.2.0)**
- 📊 Web dashboard for visualization
- 📱 Mobile app integration
- 🔄 Database backend (SQLite/PostgreSQL)
- 📈 Advanced analytics and forecasting
- 🔗 More integrations (QuickBooks, Calendly, etc.)
- 👥 Multi-user/team support

---

## 🚀 Start Your Journey

Ready to transform your freelance business?

```bash
git clone https://github.com/Dub5991/Freelance_Dev.git
cd Freelance_Dev
./install.sh
```

Then configure your `.env` and start building your business OS!

---

**Made with ❤️ for freelance developers who want to focus on code, not spreadsheets.**

⭐ Star this repo if you find it useful!
