# Project Manager Skill

## Description
Manage freelance projects end-to-end using the Work Server, tracking tasks, billable hours, and project status to ensure successful delivery and client satisfaction.

## When to Use This Skill
- Starting a new client project
- Tracking project progress and tasks
- Managing multiple concurrent projects
- Logging billable hours
- Generating project status reports
- Identifying project risks and blockers

## MCP Servers Used
- **work_server**: Primary server for project and task management
- **client_server**: For client context and communication
- **billing_server**: For tracking project financials

## Step-by-Step Instructions

### 1. Project Initiation
When starting a new project:

```
1. Review project scope and requirements
2. Break down project into tasks using create_task()
3. Set appropriate priorities (P0-P3) based on deadlines
4. Assign billable status to client tasks
5. Set estimated hours for each task
6. Link tasks to client in the system
```

**Example Prompts:**
- "Create a new project task for building the API integration for AcmeCorp"
- "Set up project tasks for the website redesign project with TechCorp"

### 2. Task Management
For ongoing project work:

```
1. List tasks by status, client, or priority using list_tasks()
2. Update task status as work progresses using update_task()
3. Log hours worked using log_hours()
4. Monitor P0 task limits (max 3 active)
5. Complete tasks using complete_task() when done
```

**Example Prompts:**
- "Show me all active P0 tasks"
- "List all billable tasks for AcmeCorp"
- "Log 3.5 hours on the API integration task"
- "Mark the database setup task as completed"

### 3. Time Tracking
For accurate billable hour tracking:

```
1. Log hours immediately after work sessions
2. Include descriptive notes of work done
3. Specify the work date if not today
4. Track both billable and internal tasks
5. Review total hours vs. estimates regularly
```

**Example Prompts:**
- "Log 2 hours on client meeting preparation for today"
- "How many hours have I logged this week on the TechCorp project?"

### 4. Project Reporting
Generate status reports:

```
1. Get billable summary by client using get_billable_summary()
2. Review task completion rates
3. Check budget burn rate (hours used vs. estimated)
4. Identify blockers and at-risk tasks
5. Prepare status updates for clients
```

**Example Prompts:**
- "Generate a billable hours summary for this month"
- "Show me the current status of all AcmeCorp tasks"
- "What's my billable hours breakdown by client for Q2?"

### 5. Project Closure
When wrapping up a project:

```
1. Complete all remaining tasks
2. Generate final billable hours report
3. Review actual vs. estimated hours
4. Document lessons learned
5. Archive project files
6. Update client's project count in client_server
```

**Example Prompts:**
- "Generate a final report for the AcmeCorp project"
- "Show total hours logged and remaining budget for TechCorp project"

## Best Practices

### Task Creation
- ✅ Use descriptive, action-oriented task titles
- ✅ Set realistic estimated hours
- ✅ Mark billable status correctly
- ✅ Assign appropriate priorities
- ❌ Don't create duplicate tasks
- ❌ Don't exceed 3 active P0 tasks

### Time Tracking
- ✅ Log hours daily for accuracy
- ✅ Include meaningful descriptions
- ✅ Track both billable and internal time
- ✅ Review estimates vs. actuals regularly
- ❌ Don't forget to log small tasks
- ❌ Don't batch log without details

### Communication
- ✅ Provide weekly status updates to clients
- ✅ Flag blockers immediately
- ✅ Celebrate milestone completions
- ✅ Document project decisions
- ❌ Don't surprise clients with delays
- ❌ Don't hide problems until critical

## Error Handling

### Common Errors

**"Cannot create P0 task. Maximum 3 active P0 tasks allowed"**
- Review current P0 tasks
- Complete or deprioritize less critical P0s
- Reassess if new task truly needs P0 priority

**"Duplicate task"**
- Check if similar task already exists
- Update existing task instead of creating new one
- Use different client or title if legitimately different

**"Task not found"**
- Verify task ID is correct
- List tasks to find the correct ID
- Task may have been completed or deleted

## Integration with Other Skills

- **Client Advisor**: Coordinate task updates with client communication
- **Invoice Handler**: Sync billable hours with invoicing
- **Weekly Reviewer**: Include project status in weekly reviews
- **Scope Writer**: Ensure tasks align with agreed scope

## Success Metrics

Track these metrics for project success:
- Tasks completed on time (target: >90%)
- Actual vs. estimated hours (target: ±10%)
- P0 task velocity (average days to complete)
- Client satisfaction scores
- Billable utilization rate (target: >75%)

## Example Workflows

### Weekly Project Review
```
1. List all active tasks by priority
2. Review hours logged vs. estimated
3. Update task statuses
4. Identify any blockers
5. Plan next week's priorities
6. Generate status update for client
```

### Monthly Project Health Check
```
1. Get billable summary for the month
2. Review all project tasks by client
3. Check for overdue tasks
4. Assess budget vs. actuals
5. Update project timeline if needed
6. Schedule client check-in if concerns
```

---

**Remember:** Good project management is about communication, transparency, and proactive problem-solving. Use the MCP servers to maintain accurate records and provide visibility to both yourself and your clients.
