# MCP Servers Reference

Complete documentation for all 6 MCP servers in Freelance LLC OS.

---

## 1. Work Server (`work_server.py`)

**Purpose:** Task and time tracking with billable hour management

### Tools

#### `create_task`
Create a new task with priority and billing information.

**Parameters:**
- `title` (required): Task title
- `priority` (required): P0, P1, P2, or P3
- `description`: Task details
- `client`: Client name (for billable work)
- `is_billable`: true/false
- `estimated_hours`: Estimated time

**Returns:** Task ID (e.g., `task-20260115-001`)

**Example:**
```
create_task(
  title="Implement user authentication",
  priority="P1",
  client="Acme Corp",
  is_billable=true,
  estimated_hours=8
)
```

**Rules:**
- Max 3 P0 tasks allowed (enforced!)
- Task IDs auto-generated: `task-YYYYMMDD-XXX`
- Tags auto-added: [BILLABLE] or [INTERNAL]

#### `list_tasks`
List tasks with optional filters.

**Parameters:**
- `status`: "todo", "in-progress", "completed", "all"
- `priority`: "P0", "P1", "P2", "P3"
- `client`: Filter by client name
- `billable_only`: true/false

**Returns:** Array of tasks

#### `complete_task`
Mark task as completed.

**Parameters:**
- `task_id` (required): Task to complete

**Returns:** Completion confirmation with billable hours

#### `log_hours`
Log time worked on a task.

**Parameters:**
- `task_id` (required): Task ID
- `hours` (required): Hours worked
- `notes`: Work description

**Returns:** Updated total hours

**Best Practice:** Log hours daily while work is fresh

#### `get_billable_summary`
Get billable hours summary by client.

**Parameters:**
- `client`: Filter by client (optional)
- `start_date`: YYYY-MM-DD format
- `end_date`: YYYY-MM-DD format

**Returns:** Hours and breakdown by client

**Use for:** Invoice preparation, weekly reviews

---

## 2. Client Server (`client_server.py`)

**Purpose:** CRM for managing client relationships

### Tools

#### `create_client`
Add new client or prospect.

**Parameters:**
- `name` (required): Client/company name
- `email` (required): Contact email
- `type` (required): "client" or "prospect"
- `contact_name`: Primary contact
- `phone`: Phone number
- `contract_start`: YYYY-MM-DD
- `contract_end`: YYYY-MM-DD
- `hourly_rate`: Rate for this client

**Returns:** Client ID

**Auto-routing:**
- Email domain matches yours → saved to People/
- Email domain external → saved to Companies/

#### `get_client`
Get full client details.

**Parameters:**
- `name` (required): Client name

**Returns:** Client object with history, warnings

**Includes:** Renewal warnings if contract expires <30 days

#### `list_clients`
List all clients with filters.

**Parameters:**
- `type`: "client", "prospect", "all"
- `health_threshold`: Show clients below this score

**Returns:** Array of clients with key info

#### `log_meeting`
Record client interaction.

**Parameters:**
- `client_name` (required): Client name
- `notes` (required): Meeting summary
- `date`: YYYY-MM-DD (defaults to today)
- `attendees`: Comma-separated names

**Returns:** Confirmation

**Best Practice:** Log within 1 hour while memory is fresh

#### `add_commitment`
Track action items and commitments.

**Parameters:**
- `client_name` (required): Client name
- `commitment` (required): Description
- `owner` (required): "me" or "client"
- `due_date`: YYYY-MM-DD

**Returns:** Confirmation

#### `check_renewals`
Check for expiring contracts.

**Parameters:**
- `days_ahead`: Look ahead N days (default 30)

**Returns:** List of contracts expiring soon

**Use weekly** to stay ahead of renewals

#### `get_client_health`
Get relationship health scores.

**Parameters:**
- `min_score`: Filter by score threshold

**Returns:** Clients with health scores and metrics

**Scoring:**
- 9-10: Excellent
- 7-8: Good
- 5-6: Neutral
- 3-4: At risk
- 1-2: Critical

#### `update_health_score`
Update relationship health.

**Parameters:**
- `client_name` (required): Client name
- `score` (required): 1-10
- `notes`: Reason for score

**Returns:** Updated score

**Update after:** Major milestones, issues, renewals

---

## 3. Billing Server (`billing_server.py`)

**Purpose:** Invoicing and payment tracking with Stripe

### Tools

#### `create_invoice`
Generate invoice from billable tasks.

**Parameters:**
- `client_name` (required): Client to invoice
- `task_ids` (required): Array of task IDs
- `due_days`: Payment due in N days (default 30)
- `notes`: Invoice notes

**Returns:** Invoice ID and amount

**Process:**
1. Loads tasks and validates [BILLABLE]
2. Gets client hourly rate
3. Generates invoice with line items
4. Saves to Finance/invoices/

#### `send_invoice`
Send invoice via Stripe.

**Parameters:**
- `invoice_id` (required): Invoice to send
- `customer_email` (required): Client email

**Returns:** Stripe hosted URL

**Requires:** Stripe API key in .env

**Benefits:**
- Professional invoice delivery
- Multiple payment methods
- Automatic reminders
- Real-time notifications

#### `check_payment_status`
Check if invoice is paid.

**Parameters:**
- `invoice_id` (required): Invoice ID

**Returns:** Payment status and amounts

**Checks:** Local status and Stripe status (if linked)

#### `list_outstanding_invoices`
List unpaid invoices.

**Parameters:**
- `client_name`: Filter by client (optional)

**Returns:** Outstanding invoices with aging

**Use for:** AR aging, collection priorities

#### `record_payment`
Manually record payment.

**Parameters:**
- `invoice_id` (required): Invoice ID
- `amount` (required): Amount paid
- `payment_method` (required): "stripe", "check", "wire", "other"
- `transaction_id`: Reference number

**Returns:** Updated payment status

**Use when:** Payment received outside Stripe

#### `get_revenue_summary`
Revenue analytics.

**Parameters:**
- `start_date`: YYYY-MM-DD
- `end_date`: YYYY-MM-DD
- `group_by`: "client", "month", "quarter"

**Returns:** Revenue breakdown

**Use for:** Financial reviews, client value analysis

---

## 4. LLC Ops Server (`llc_ops_server.py`)

**Purpose:** Financial operations and business metrics

### Tools

#### `get_dashboard`
Financial overview.

**Parameters:**
- `year`: Year (default current)
- `quarter`: Quarter 1-4 (optional)

**Returns:** Revenue, expenses, profit, taxes

**Includes:**
- Total revenue (from billing)
- Total expenses (logged)
- Net profit
- Profit margin %
- Outstanding invoices
- Estimated quarterly tax
- Net after tax

#### `log_expense`
Record business expense.

**Parameters:**
- `amount` (required): Expense amount
- `category` (required): Software, Hardware, Office, Travel, Education, Marketing, Legal, Accounting, Insurance, Meals, Other
- `description` (required): What it's for
- `date`: YYYY-MM-DD (default today)
- `vendor`: Who you paid

**Returns:** Expense ID

**Categories for tax deductions:**
- Software: SaaS, tools, subscriptions
- Hardware: Computer, monitor, equipment
- Office: Supplies, furniture, coworking
- Travel: Client visits, conferences
- Education: Courses, certifications
- Marketing: Website, ads, business cards
- Legal: Contracts, incorporation
- Accounting: Bookkeeping, tax prep
- Insurance: Liability, health
- Meals: Client meals (50% deductible)
- Other: Miscellaneous

#### `get_tax_estimate`
Quarterly tax calculation.

**Parameters:**
- `year` (required): Tax year
- `quarter` (required): 1-4

**Returns:** Tax estimate and deadline

**Deadlines:**
- Q1: April 15 (Jan-Mar)
- Q2: June 15 (Apr-May)
- Q3: September 15 (Jun-Aug)
- Q4: January 15 (Sep-Dec of previous year)

**Calculation:**
- Gets profit for quarter
- Applies tax rate (from .env, default 25%)
- Shows deadline and days until

#### `get_profit_loss`
P&L statement.

**Parameters:**
- `start_date` (required): YYYY-MM-DD
- `end_date` (required): YYYY-MM-DD

**Returns:** Revenue, expenses, net income

**Breakdown:**
- Total revenue (from paid invoices)
- Expenses by category
- Net income (profit)
- Profit margin %

#### `get_revenue_by_client`
Revenue breakdown by client.

**Parameters:**
- `year`: Year (default current)

**Returns:** Revenue per client with percentages

**Use for:**
- Client concentration risk
- Revenue diversification
- Client value analysis

---

## 5. Onboarding Server (`onboarding_server.py`)

**Purpose:** First-time setup wizard

### Tools

#### `start_onboarding`
Begin or resume onboarding.

**Returns:** Current step and progress

**Steps:**
1. LLC info (name, EIN)
2. Owner info (name, email)
3. Billing rates
4. Stripe setup
5. Strategic pillars

#### `submit_step`
Submit data for a step.

**Parameters:**
- `step` (required): Step name
- `data` (required): Step data object

**Returns:** Next step

**Validation:**
- Checks required fields
- Validates formats (EIN, email)
- Confirms data before saving

#### `get_onboarding_status`
Check progress.

**Returns:** Completion status and remaining steps

#### `complete_onboarding`
Finalize setup.

**Returns:** Confirmation and next steps

**Creates:**
- Vault folder structure
- .env file from collected data
- Onboarding state file

**Use once:** During initial setup

---

## 6. Career Server (`career_server.py`)

**Purpose:** Professional development tracking

### Tools

#### `add_skill`
Add or update a skill.

**Parameters:**
- `name` (required): Skill name
- `category` (required): Programming Language, Framework, Tool, Cloud Platform, Database, Methodology, Soft Skill, Domain Knowledge
- `proficiency` (required): Beginner, Intermediate, Advanced, Expert
- `years_experience`: Years using
- `last_used`: YYYY-MM-DD

**Returns:** Skill ID

#### `log_evidence`
Record skill application.

**Parameters:**
- `skill_name` (required): Related skill
- `project` (required): Project/client name
- `description` (required): What you did
- `impact`: Business results
- `date`: YYYY-MM-DD

**Returns:** Confirmation

**Also:** Adds to portfolio automatically

#### `get_portfolio`
Get portfolio items.

**Parameters:**
- `skill`: Filter by skill
- `category`: Filter by category
- `top_n`: Limit results

**Returns:** Portfolio items

**Use for:** Proposals, resume, case studies

#### `suggest_rate`
Rate optimization analysis.

**Parameters:**
- `current_rate` (required): Current hourly rate

**Returns:** Suggested rate with justification

**Based on:**
- Number of expert-level skills
- Total years of experience
- Portfolio depth

#### `list_skills`
List all skills.

**Parameters:**
- `category`: Filter by category
- `min_proficiency`: Minimum level

**Returns:** Skills with metadata

#### `get_skill_gaps`
Identify learning needs.

**Returns:** Missing skills vs strategic pillars

**Use for:** Professional development planning

---

## Common Patterns

### Error Handling
All tools return:
```
{
  "success": true/false,
  "message": "...",
  ...data...
}
```

Check `success` before using data.

### Date Formats
Always use: `YYYY-MM-DD` (e.g., "2026-01-15")

### File Storage
- Tasks: `vault/03-Tasks/task-*.yaml`
- Clients: `vault/05-Areas/{People,Companies}/*.yaml`
- Invoices: `vault/05-Areas/Finance/invoices/INV-*.yaml`
- Expenses: `vault/05-Areas/Finance/expenses/EXP-*.yaml`
- Skills: `vault/05-Areas/Career/skills/*.yaml`

### IDs
- Tasks: `task-YYYYMMDD-XXX` (auto)
- Invoices: `INV-XXXX` (sequential)
- Expenses: `EXP-YYYYMMDDHHMMSS` (timestamp)
- Clients: `name-slug` (derived from name)

---

**Built for devs, by devs. Use freely, modify as needed. MIT licensed.**
