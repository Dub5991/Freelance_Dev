# 🚀 Freelance Dev OS - Project Intelligence File

## Project Overview

**Freelance Dev OS** is a comprehensive operating system for managing a freelance development business as an LLC. It provides a suite of Model Context Protocol (MCP) servers that enable AI assistants (like Claude) to help with task management, client relations, billing, tax planning, onboarding, and career development.

### Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude AI Assistant                     │
│         (Enhanced with Claude Skills in .claude/skills/)    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ MCP Protocol
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                    MCP Server Layer                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │Work Server  │  │Client Server│  │Billing      │         │
│  │- Tasks      │  │- CRM        │  │- Invoices   │         │
│  │- Hours      │  │- Meetings   │  │- Stripe API │         │
│  │- Projects   │  │- Health     │  │- Revenue    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │LLC Ops      │  │Onboarding   │  │Career       │         │
│  │- Expenses   │  │- Workflows  │  │- Skills     │         │
│  │- Taxes      │  │- SOW        │  │- Portfolio  │         │
│  │- Compliance │  │- Checklists │  │- Rates      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Data Persistence
                      │
┌─────────────────────┴───────────────────────────────────────┐
│                    Storage Layer                             │
│  - JSON files in data/ directory                            │
│  - PARA vault structure in vault/                           │
│  - YAML for work server (tasks, hours)                      │
└─────────────────────────────────────────────────────────────┘
```

## Repository Structure

```
Freelance_Dev/
├── .claude/
│   └── skills/           # 9 Claude skill definitions
│       ├── project-manager.md
│       ├── client-advisor.md
│       ├── invoice-handler.md
│       ├── tax-strategist.md
│       ├── onboarding-specialist.md
│       ├── career-coach.md
│       ├── contract-drafter.md
│       ├── weekly-reviewer.md
│       └── scope-writer.md
├── core/
│   ├── config.py         # Central configuration management
│   ├── utils.py          # Shared utility functions
│   └── mcp/              # MCP server implementations
│       ├── base_server.py
│       ├── work_server.py
│       ├── client_server.py
│       ├── billing_server.py
│       ├── llc_ops_server.py
│       ├── onboarding_server.py
│       └── career_server.py
├── vault/                # PARA organization system
│   ├── 1-Projects/       # Active client projects
│   ├── 2-Areas/          # Business areas of responsibility
│   ├── 3-Resources/      # Reference materials
│   └── 4-Archive/        # Completed/inactive items
├── tests/                # Pytest test suite
├── data/                 # Runtime data storage (gitignored)
├── .env                  # Environment configuration (gitignored)
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
├── install.sh            # Installation script
└── README.md             # User-facing documentation
```

## Navigating the Codebase

### Core Components

**`core/config.py`** - Configuration management
- Loads environment variables from .env file
- Provides Config class with all settings
- Includes validation and default values
- Use `Config.ensure_directories()` to create needed paths

**`core/utils.py`** - Shared utilities
- Date/time formatting functions
- Currency formatting and calculations
- JSON file I/O with error handling
- Validation functions (email, phone)
- ID generation utilities

**`core/mcp/base_server.py`** - Base class for all MCP servers
- Provides CRUD operations for collections
- JSON-based data persistence
- Logging configuration
- Error handling patterns
- All servers inherit from BaseMCPServer

### MCP Servers

Each MCP server follows this pattern:

1. **Inherits from BaseMCPServer**
2. **Initializes collections** in `__init__()`
3. **Implements `get_info()`** to describe available tools
4. **Provides tool methods** that return dicts with results
5. **Uses `_create_record()`, `_update_record()`, etc.** from base class

**Work Server** (`work_server.py`) - Exception: Uses YAML storage
- Unique task IDs: `task-YYYYMMDD-XXX`
- Priority enforcement (max 3 P0 tasks)
- Billable hours tracking per client
- Tools: `create_task`, `list_tasks`, `log_hours`, `get_billable_summary`

**Client Server** (`client_server.py`) - CRM functionality
- Client health scoring (0-100 scale)
- Meeting logs with action items
- Renewal tracking and risk assessment
- Tools: `create_client`, `log_meeting`, `get_health_score`, `list_renewals`

**Billing Server** (`billing_server.py`) - Financial operations
- Invoice generation with line items
- Stripe API integration (optional)
- Payment tracking and reminders
- Revenue and profit reporting
- Tools: `create_invoice`, `record_payment`, `get_revenue_report`

**LLC Ops Server** (`llc_ops_server.py`) - Business operations
- Expense tracking and categorization
- Quarterly tax estimation
- Profit/loss calculations
- Compliance checklists
- Tools: `create_expense`, `get_tax_estimate`, `get_profit_loss`

**Onboarding Server** (`onboarding_server.py`) - Client onboarding
- Multi-step workflow management
- SOW (Statement of Work) generation
- Checklist tracking
- Tools: `start_onboarding`, `complete_step`, `generate_sow`

**Career Server** (`career_server.py`) - Professional development
- Skill tracking with evidence
- Portfolio management
- Rate recommendations based on skills
- Tools: `add_skill`, `log_skill_evidence`, `get_rate_suggestion`

## How MCP Servers Work Together

### Data Flow Example: Complete Project Flow

1. **Onboarding**: New client starts with `onboarding_server.start_onboarding()`
2. **Client Setup**: Create client profile with `client_server.create_client()`
3. **Project Planning**: Create tasks with `work_server.create_task()`
4. **Execution**: Log hours with `work_server.log_hours()`
5. **Client Management**: Log meetings with `client_server.log_meeting()`
6. **Billing**: Create invoice with `billing_server.create_invoice()` using hours from work_server
7. **Payment**: Track payment with `billing_server.record_payment()`
8. **Operations**: Log expenses with `llc_ops_server.create_expense()`
9. **Taxes**: Calculate quarterly taxes with `llc_ops_server.get_tax_estimate()`
10. **Review**: Generate business review with data from all servers

### Cross-Server Integration Points

- **Work → Billing**: Billable hours feed into invoice generation
- **Client → Work**: Client health affects task priority
- **Billing → LLC Ops**: Revenue flows into profit/loss calculations
- **LLC Ops → Billing**: Expenses reduce taxable income
- **Career → Billing**: Skill levels inform rate recommendations
- **Onboarding → All**: New clients trigger workflows across servers

## Coding Conventions and Standards

### Python Style
- Follow PEP 8 style guide
- Use type hints for function signatures
- Docstrings in Google style format
- Maximum line length: 100 characters
- Use descriptive variable names

### Error Handling
- Return dicts with `{"error": "message"}` for errors
- Return dicts with `{"success": True, "data": ...}` for success
- Log errors with `self.logger.error()`
- Never raise exceptions that would crash the server

### Data Persistence
- All data stored in `data/` directory
- Most servers use JSON via BaseMCPServer methods
- Work server uses YAML for human-readable task storage
- Always use `Config.ensure_directories()` before file I/O
- Use utility functions from `core/utils.py` for JSON operations

### ID Generation
- Use descriptive prefixes: `inv-`, `client-`, `task-`, `exp-`
- Include date components: `prefix-YYYYMMDD-HHMMSS`
- Use `generate_id()` from utils for consistency
- Work server has custom ID format: `task-YYYYMMDD-XXX`

### Testing
- Use pytest for all tests
- Mock external services (Stripe, email, etc.)
- Use temporary directories for test data
- Fixtures for setup/teardown
- Test both success and error cases

## Common Tasks

### Adding a New MCP Server

1. Create new file in `core/mcp/your_server.py`
2. Import BaseMCPServer: `from .base_server import BaseMCPServer`
3. Create class inheriting from BaseMCPServer
4. Initialize collections in `__init__()`
5. Implement `get_info()` method
6. Add tool methods that return dicts
7. Update `core/mcp/__init__.py` to export new server
8. Create tests in `tests/test_your_server.py`
9. Document in README.md

### Adding a New Tool to Existing Server

1. Define method in server class
2. Add docstring with Args and Returns
3. Implement logic using base class methods
4. Update `get_info()` to list new tool
5. Add tests for the new tool
6. Update relevant Claude skill if applicable

### Running the System

**Local development:**
```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values

# Run individual server
python -m core.mcp.work_server

# Run tests
pytest tests/ -v
```

**Using with Claude:**
1. Configure Claude to use MCP servers
2. Reference Claude skills in `.claude/skills/`
3. Ask Claude to perform tasks using natural language
4. Claude will call appropriate MCP server tools

### Debugging

**Enable debug logging:**
```bash
export LOG_LEVEL=DEBUG
```

**Check data files:**
```bash
# View current data
cat data/work_data.json | python -m json.tool
cat data/client_data.json | python -m json.tool

# Check logs
tail -f data/app.log
```

**Test individual server:**
```python
from core.mcp.work_server import create_task, list_tasks

# Create a test task
result = create_task("Test task", priority="P2")
print(result)

# List all tasks
tasks = list_tasks()
print(tasks)
```

## Configuration

### Required Environment Variables
- `LLC_NAME`: Your business name
- `OWNER_NAME`: Your name

### Optional but Recommended
- `STRIPE_API_KEY`: For payment processing
- `LLC_EIN`, `LLC_STATE`: For tax reporting
- `DEFAULT_HOURLY_RATE`: Default billing rate

### Optional Features
- `SMTP_*`: Email notifications
- `CLAUDE_API_KEY`: AI features
- `VAULT_PATH`: Custom PARA vault location

See `.env.example` for full configuration options.

## PARA Vault System

The `vault/` directory uses PARA methodology:

- **Projects** (1-): Active client projects with deadlines
- **Areas** (2-): Ongoing responsibilities (business ops, finance, etc.)
- **Resources** (3-): Reference materials (templates, contracts)
- **Archive** (4-): Completed projects and inactive items

Each MCP server can read/write to appropriate vault locations.

## Performance Considerations

- JSON files are loaded on server init and kept in memory
- Use `_save_data()` sparingly to minimize disk I/O
- For large datasets, consider pagination in list operations
- Work server YAML files are loaded on each operation (acceptable for task volume)

## Security Notes

- Never commit `.env` file (it's gitignored)
- Store Stripe keys securely
- Validate all user inputs
- Sanitize file paths to prevent directory traversal
- Use environment variables for sensitive data

## Getting Help

1. Check README.md for user-facing documentation
2. Review Claude skills in `.claude/skills/` for usage patterns
3. Read server docstrings for API documentation
4. Check tests for usage examples
5. Review logs in `data/app.log` for errors

## Future Enhancements

Potential areas for expansion:
- Database backend (SQLite or PostgreSQL)
- Web dashboard for visualization
- Mobile app integration
- Advanced analytics and forecasting
- Integrations with more services (QuickBooks, Calendly, etc.)
- Multi-user support for team management
