# Claude Hooks

## What Are Hooks?

Hooks are automatic behaviors that Claude runs at specific times without being asked.

## Available Hooks

### session-start.md
**Runs:** At the beginning of every Claude session  
**Purpose:** Surface urgent items and daily priorities  
**What it does:**
- Checks for P0 tasks (max 3 limit)
- Alerts on overdue invoices
- Shows contract renewals
- Displays today's priorities

**Example:**
```
🌅 GOOD MORNING
🚨 2 urgent items need attention
📋 3 tasks for today
💰 Outstanding AR: $11,850
```

## How Hooks Work

1. You open Claude
2. Hook runs automatically
3. You see urgent items immediately
4. You can start working on priorities

## Customizing Hooks

Edit the hook file to:
- Change what's checked
- Adjust thresholds
- Modify output format
- Add custom checks

Or add to CLAUDE.md USER_EXTENSIONS:
```
<!-- Custom hook preferences -->
- session-start: Only show P0s, skip financial summary
- session-start: Alert if client health <5 (not 6)
```

## Creating New Hooks

Want a new hook? Create:
- `session-end.md` - Runs when ending session
- `weekly-review.md` - Runs every Friday
- `monthly-close.md` - Runs last day of month

Format:
```markdown
# Hook Name

**Trigger:** When it runs
**Purpose:** What it does
**Actions:** List of MCP tool calls
**Output:** Example of what user sees
```

## Disabling Hooks

To disable a hook:
1. Rename file (e.g., `session-start.md.disabled`)
2. Or tell Claude: "Don't run session-start hook"

## Best Practices

**Good Hooks:**
- ✅ Short and actionable
- ✅ Run quickly (<5 seconds)
- ✅ Show only what matters
- ✅ Help user make decisions

**Bad Hooks:**
- ❌ Verbose explanations
- ❌ Slow (>10 seconds)
- ❌ Show everything
- ❌ Just report status without action

## Troubleshooting

**Hook not running?**
- Check file name matches exactly
- Verify MCP servers are loaded
- Check CLAUDE.md for overrides

**Hook too slow?**
- Reduce number of MCP calls
- Cache frequently accessed data
- Use summary tools instead of list tools

**Hook too noisy?**
- Increase alert thresholds
- Hide non-urgent sections
- Customize in CLAUDE.md

## Ideas for Custom Hooks

**morning-motivation.md**
- Random productivity quote
- Yesterday's wins
- Today's potential

**client-birthday.md**
- Check for client milestones
- Suggest reaching out
- Build relationship

**tax-deadline.md**
- Runs 30/15/7/1 days before quarterly deadline
- Shows tax estimate
- Payment instructions

**portfolio-reminder.md**
- Runs monthly
- Prompts to update skills
- Log evidence from recent work
- Build showcase

---

*Hooks are a powerful way to automate routine checks and surface important information proactively.*
