# 🔧 Technical Guide

## Installation & Setup

### Prerequisites
- **Python 3.9+**
- **Node.js 18+**
- **Git** (optional, recommended)
- **Claude Desktop** or MCP-compatible client

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/Freelance_Dev.git
cd Freelance_Dev

# Run automated installer (detects OS, installs deps)
bash install.sh

# Or manual install:
pip install -r requirements.txt
npm install

# Copy environment template
cp env.example .env

# Edit .env with your information
nano .env  # or your preferred editor

# Run onboarding
# (Use Claude with MCP servers configured)
# In Claude: /setup
```

### MCP Configuration

Create or update your MCP client configuration (e.g., `~/.config/claude/config.json`):

```json
{
  "mcpServers": {
    "work": {
      "command": "python",
      "args": ["/absolute/path/to/Freelance_Dev/core/mcp/work_server.py"],
      "env": {
        "VAULT_PATH": "/absolute/path/to/Freelance_Dev/vault"
      }
    },
    "client": {
      "command": "python",
      "args": ["/absolute/path/to/Freelance_Dev/core/mcp/client_server.py"],
      "env": {
        "VAULT_PATH": "/absolute/path/to/Freelance_Dev/vault"
      }
    },
    "billing": {
      "command": "python",
      "args": ["/absolute/path/to/Freelance_Dev/core/mcp/billing_server.py"],
      "env": {
        "VAULT_PATH": "/absolute/path/to/Freelance_Dev/vault",
        "STRIPE_SECRET_KEY": "sk_test_YOUR_KEY"
      }
    },
    "llc-ops": {
      "command": "python",
      "args": ["/absolute/path/to/Freelance_Dev/core/mcp/llc_ops_server.py"],
      "env": {
        "VAULT_PATH": "/absolute/path/to/Freelance_Dev/vault"
      }
    },
    "onboarding": {
      "command": "python",
      "args": ["/absolute/path/to/Freelance_Dev/core/mcp/onboarding_server.py"],
      "env": {
        "VAULT_PATH": "/absolute/path/to/Freelance_Dev/vault"
      }
    },
    "career": {
      "command": "python",
      "args": ["/absolute/path/to/Freelance_Dev/core/mcp/career_server.py"],
      "env": {
        "VAULT_PATH": "/absolute/path/to/Freelance_Dev/vault"
      }
    }
  }
}
```

### Stripe Setup (Optional but Recommended)

1. Create account at [stripe.com](https://stripe.com)
2. Get API keys from [dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys)
3. Add to `.env`:
```env
STRIPE_SECRET_KEY=sk_live_YOUR_KEY
STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_KEY
STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET
```

4. Set up webhook (optional, for payment notifications):
   - URL: Your server endpoint (if self-hosting)
   - Events: `invoice.paid`, `invoice.payment_failed`

## Architecture Details

### MCP Server Pattern

Each server follows this async pattern:

```python
class ServerName:
    def __init__(self):
        self.server = Server("server-name")
        self._setup_handlers()
    
    def _setup_handlers(self):
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            # Return available tools
            
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any):
            # Route to handlers
            
    async def _tool_handler(self, **kwargs):
        # Implement tool logic
        # Read/write YAML files
        # Return structured results
```

### Data Storage

All data is stored as YAML for:
- **Human readability**: Easy to inspect and debug
- **Git-friendly**: Clean diffs, merge-friendly
- **No database**: Zero infrastructure
- **Portable**: Move anywhere, no export needed

Example task storage:
```yaml
task_id: task-20260115-001
title: "Implement feature X"
priority: P1
status: in-progress
client: "Acme Corp"
is_billable: true
actual_hours: 6.5
created_at: "2026-01-15T09:00:00"
```

### Tool Execution Flow

```
Claude → MCP Client → MCP Server → Python Handler → YAML I/O → Response → Claude
```

1. User asks Claude something
2. Claude decides which MCP tool to call
3. MCP client sends request to server
4. Server routes to appropriate handler
5. Handler reads/writes YAML files
6. Handler returns structured response
7. Claude interprets and responds to user

## Troubleshooting

### MCP Server Not Found
```
Error: Server 'work' not found
```
**Solution**: Check MCP config file path and server command paths are absolute.

### Import Errors
```
ModuleNotFoundError: No module named 'mcp'
```
**Solution**: 
```bash
pip install -r requirements.txt
# or
pip install mcp pyyaml stripe python-dotenv
```

### YAML Parse Errors
```
yaml.scanner.ScannerError: mapping values are not allowed here
```
**Solution**: YAML syntax error. Check for:
- Proper indentation (spaces, not tabs)
- Quoted strings with special characters
- Valid YAML structure

### Stripe Errors
```
Stripe error: Invalid API Key
```
**Solution**: 
1. Check `.env` has correct `STRIPE_SECRET_KEY`
2. Ensure key starts with `sk_test_` or `sk_live_`
3. Verify key is active in Stripe dashboard

### Permission Errors
```
PermissionError: [Errno 13] Permission denied: '/vault/03-Tasks/task-20260115-001.yaml'
```
**Solution**: Check file/folder permissions:
```bash
chmod -R u+rw vault/
```

## Development

### Adding a New MCP Server

1. Create server file: `core/mcp/my_server.py`
2. Follow the async pattern (see existing servers)
3. Define tools with proper schemas
4. Implement handlers with YAML I/O
5. Add to `core/mcp/__init__.py`
6. Update MCP config to load server
7. Document in `.claude/reference/`

### Adding a Claude Skill

1. Create skill directory: `.claude/skills/my-skill/`
2. Create `SKILL.md` with:
   - Skill name and description
   - When to use it
   - MCP tools it calls
   - Example usage
3. Test with Claude

### Custom Workflows

Extend the system by:
- Adding new vault folders
- Creating custom templates
- Building automation scripts
- Integrating other APIs

## Performance

### Optimization Tips
- **Cache in memory**: Servers cache loaded YAML
- **Batch operations**: Group related tool calls
- **Index for search**: Add search indexes if needed
- **Async throughout**: All I/O is non-blocking

### Scaling Considerations
- System handles **thousands of tasks/clients/invoices**
- YAML is fine up to ~10K files per folder
- Beyond that, consider:
  - Archiving old data
  - Database migration (PostgreSQL + keep YAML for portability)
  - Sharding by year/quarter

## Security

### Best Practices
1. **Never commit .env** - Keep secrets out of git
2. **Use .gitignore** - Protect vault data
3. **Backup regularly** - Your data is valuable
4. **Stripe test mode** - Use test keys during dev
5. **API key rotation** - Change keys periodically

### Data Privacy
- All data is **local-first**
- No telemetry or tracking
- You own 100% of your data
- Claude only sees what you share via MCP

## Backup & Recovery

### Recommended Backup Strategy

```bash
# Daily automated backup
tar -czf "backup-$(date +%Y%m%d).tar.gz" vault/ .env

# Weekly full backup
rsync -av Freelance_Dev/ /path/to/backup/
```

### Git-based Backup (Optional)

```bash
# Initialize git in vault (careful with secrets!)
cd vault
git init
git add *.md  # Only add documentation, not data
git commit -m "Vault structure"

# Or: Backup to private Git repo
# Make sure .gitignore protects sensitive data!
```

### Cloud Backup Options
- **Dropbox/Google Drive**: Sync vault folder
- **iCloud**: Mac users
- **Backblaze**: Automated cloud backup
- **Private Git repo**: GitHub private repo (be careful!)

## Testing

### Manual Testing
```bash
# Test work server
cd core/mcp
python work_server.py
# In another terminal:
# Send test MCP requests (use mcp CLI or test client)

# Test YAML I/O
python
>>> import yaml
>>> with open('test.yaml', 'w') as f:
...     yaml.dump({'test': 'data'}, f)
```

### Integration Testing
Use Claude Desktop or compatible MCP client to test full workflows:
1. Create a test client
2. Create a test task
3. Log hours
4. Generate invoice
5. Verify all YAML files created correctly

## Updating

### Pulling Updates
```bash
cd Freelance_Dev
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
npm update
```

### Migration Notes
When updating, check `CHANGELOG.md` for:
- Breaking changes
- New required env vars
- YAML schema changes
- Migration scripts

## Advanced Usage

### Custom Claude System Prompt
Edit `CLAUDE.md` to:
- Adjust AI personality
- Add custom rules
- Define your workflow preferences
- Add user-specific extensions

### Scripting & Automation
Write Python scripts using the MCP servers:

```python
import asyncio
from core.mcp.work_server import WorkServer

async def main():
    work = WorkServer()
    result = await work._list_tasks(status="todo", priority="P0")
    print(f"P0 tasks: {result['count']}")

asyncio.run(main())
```

### API Integration
Add more integrations:
- **QuickBooks**: For accounting
- **Slack**: For notifications
- **GitHub**: For issue tracking
- **Calendar**: For meeting sync

## Support

### Getting Help
1. Check this guide first
2. Review `System_Guide.md` for workflows
3. Search GitHub Issues
4. Ask in GitHub Discussions
5. Open a new Issue with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version)

### Contributing
See `CONTRIBUTING.md` (create if you want contributions!)

## Maintenance

### Weekly
- Review logs for errors
- Check disk space
- Verify backups completed

### Monthly
- Update dependencies
- Archive old data
- Review security settings

### Quarterly
- Full system audit
- Performance review
- Backup verification

---

**Built with ❤️ by devs, for devs.**
