# 🏢 Companies

## Purpose
Corporate clients and prospects (external organizations).

## What Goes Here
Company files are stored as YAML by the **client_server** MCP when:
- Email domain does NOT match your LLC domain (external)
- Company/organization vs. individual person

## File Structure
Each company gets a YAML file: `company-name.yaml`

## Managed by MCP
The **client_server** automatically:
- Routes external email domains here
- Tracks relationship health scores (1-10)
- Monitors contract renewal dates with alerts
- Logs meetings and commitments
- Calculates revenue per client

## Example Company File
```yaml
client_id: acme-corp
name: "Acme Corp"
contact_name: "Jane Smith"
email: "jane@acmecorp.com"
phone: "+1-555-987-6543"
type: client
is_internal: false
health_score: 9
hourly_rate: 175
contract_start: "2025-10-01"
contract_end: "2026-09-30"
meetings:
  - date: "2026-01-05T10:00:00"
    notes: "Q4 retrospective and Q1 planning"
    attendees: ["Jane Smith", "Bob Johnson", "Me"]
    logged_at: "2026-01-05T11:30:00"
  - date: "2025-12-15T14:00:00"
    notes: "Weekly check-in, discussed priorities"
    attendees: ["Jane Smith", "Me"]
    logged_at: "2025-12-15T15:00:00"
commitments:
  - description: "Deliver API documentation"
    owner: me
    due_date: "2026-01-20"
    status: open
    created_at: "2026-01-05T10:30:00"
  - description: "Provide Q1 resource allocation"
    owner: client
    due_date: "2026-01-10"
    status: open
    created_at: "2026-01-05T10:30:00"
health_history:
  - date: "2026-01-05"
    score: 9
    notes: "Excellent Q4 retrospective, expanding engagement"
  - date: "2025-10-01"
    score: 7
    notes: "New client onboarding"
created_at: "2025-10-01T09:00:00"
updated_at: "2026-01-05T11:30:00"
```

## MCP Tools
- `create_client` - Add new company
- `get_client` - View details and renewal warnings
- `list_clients` - See all clients/prospects
- `log_meeting` - Record interactions
- `add_commitment` - Track action items
- `update_health_score` - Maintain relationship health
- `check_renewals` - See upcoming contract expirations

## Best Practices
- Log every client meeting within 24 hours
- Update health scores after major milestones
- Set contract_end dates to enable renewal alerts
- Track both your commitments AND client commitments
- Review client health monthly
- Check renewals dashboard weekly

## Renewal Alerts
System automatically alerts **30 days before** contract expiry:
```
⚠️ WARNING: Acme Corp contract expires in 27 days!
Start renewal conversation now.
```

## Health Score Guidelines
- **9-10**: Excellent - Growing engagement, referring others
- **7-8**: Good - Consistent work, responsive communication
- **5-6**: Neutral - Basic professionalism, minimal engagement
- **3-4**: At Risk - Reduced communication, scope creep, payment delays
- **1-2**: Critical - Major issues, likely to terminate

## Revenue Tracking
Use **billing_server** and **llc_ops_server** to track:
- Total revenue per client
- Hourly rate effectiveness
- Payment patterns
- Client profitability
