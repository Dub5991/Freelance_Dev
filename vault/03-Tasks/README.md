# ✅ Tasks

## Purpose
Individual tasks managed by the **work_server** MCP server.

## What Goes Here
All tasks are stored as YAML files: `task-YYYYMMDD-XXX.yaml`

These are **automatically managed** by the work MCP server - you should not edit them directly.

## Task Properties
- **Task ID**: `task-YYYYMMDD-XXX` (e.g., `task-20260115-001`)
- **Priority**: P0 (urgent), P1 (high), P2 (normal), P3 (low)
  - Maximum 3 P0 tasks at any time
- **Tags**: `[BILLABLE]` or `[INTERNAL]`
- **Client**: Associated client name (for billable tasks)
- **Hours**: Estimated and actual hours tracked

## Task Lifecycle
1. **Create** - Use `create_task` tool
2. **Work** - Use `log_hours` tool to track time
3. **Complete** - Use `complete_task` tool
4. **Bill** - Billable tasks feed into invoicing

## MCP Tools
- `create_task` - Create a new task
- `list_tasks` - List tasks with filters
- `complete_task` - Mark as done
- `log_hours` - Track time spent
- `get_billable_summary` - See billable hours by client

## Priority Guidelines
- **P0**: Must be done today, blocks other work, client escalation
- **P1**: Must be done this week, on the critical path
- **P2**: Important but not urgent, planned work
- **P3**: Nice to have, backlog items

## Example Task
```yaml
task_id: task-20260115-001
title: "Implement user authentication API"
description: "Add JWT-based auth to REST API"
priority: P1
status: in-progress
tags:
  - "[BILLABLE]"
client: "Acme Corp"
is_billable: true
estimated_hours: 8
actual_hours: 6.5
hours_log:
  - date: "2026-01-15T10:00:00"
    hours: 4
    notes: "Set up JWT library and basic structure"
  - date: "2026-01-15T15:00:00"
    hours: 2.5
    notes: "Implemented token generation and validation"
created_at: "2026-01-15T09:00:00"
updated_at: "2026-01-15T17:30:00"
```

## Best Practices
- Break large work into smaller tasks (<8 hours each)
- Log hours daily while work is fresh
- Always tag billable vs internal correctly
- Complete tasks promptly to enable invoicing
- Review task list at start of each day
