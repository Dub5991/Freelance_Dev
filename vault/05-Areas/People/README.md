# 👥 People

## Purpose
Individual contacts and relationships (internal team, partners, prospects).

## What Goes Here
People files are stored as YAML by the **client_server** MCP when:
- Email domain matches your LLC domain (internal)
- Individual contacts vs. companies

## File Structure
Each person gets a YAML file: `firstname-lastname.yaml`

## Managed by MCP
The **client_server** automatically:
- Routes internal email domains here
- Tracks relationship health scores (1-10)
- Logs meetings and commitments
- Tracks contract renewal dates

## Example Person File
```yaml
client_id: john-smith
name: "John Smith"
contact_name: "John Smith"
email: "john@partnerfirm.com"
phone: "+1-555-123-4567"
type: prospect
is_internal: false
health_score: 8
hourly_rate: 150
contract_start: null
contract_end: null
meetings:
  - date: "2026-01-10T14:00:00"
    notes: "Initial consultation about cloud migration project"
    attendees: ["John Smith", "Me"]
    logged_at: "2026-01-10T15:30:00"
commitments:
  - description: "Send proposal by Friday"
    owner: me
    due_date: "2026-01-15"
    status: open
    created_at: "2026-01-10T14:30:00"
health_history:
  - date: "2026-01-10"
    score: 8
    notes: "Great initial meeting, strong interest"
created_at: "2026-01-10T15:30:00"
updated_at: "2026-01-10T15:30:00"
```

## MCP Tools
- `create_client` - Add new person
- `get_client` - View details
- `log_meeting` - Record interactions
- `add_commitment` - Track action items
- `update_health_score` - Maintain relationship health

## Best Practices
- Log every significant interaction
- Update health scores monthly
- Track commitments carefully (yours and theirs)
- Review before every meeting
- Note personal details for relationship building

## Health Score Guidelines
- **9-10**: Excellent - Strong advocate, referring others
- **7-8**: Good - Responsive, professional, on track
- **5-6**: Neutral - Professional but distant
- **3-4**: At Risk - Issues, poor communication
- **1-2**: Critical - Likely to churn, escalate
