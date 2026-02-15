# 📦 Projects

## Purpose
Multi-week initiatives and client engagements.

## What Goes Here
- **Client Projects** - Ongoing engagements with deliverables
- **Internal Projects** - Business improvements, marketing campaigns
- **Research Projects** - Exploration of new technologies or markets

## Structure
One file per project: `ProjectName-ClientName.md`

## Template Structure
```markdown
# Project: [Project Name] - [Client Name]

## Overview
**Client**: Acme Corp  
**Start Date**: 2026-01-01  
**Target Completion**: 2026-03-31  
**Budget**: 200 hours @ $150/hr = $30,000  
**Status**: 🟢 On Track

## Objectives
- Migrate legacy system to cloud infrastructure
- Implement CI/CD pipeline
- Train client team on new system

## Deliverables
- [ ] Architecture design doc (Week 1-2)
- [ ] Cloud infrastructure setup (Week 3-4)
- [ ] Application migration (Week 5-8)
- [ ] CI/CD pipeline (Week 9-10)
- [ ] Documentation and training (Week 11-12)

## Tasks
_Link to specific task IDs_
- task-20260115-001 ✅
- task-20260116-003 🔄
- task-20260120-007 ⏳

## Hours Tracked
_Use work_server to get actual hours_
- Weeks 1-2: 32 hours
- Weeks 3-4: 28 hours
- **Total**: 60 / 200 hours (30%)

## Risks & Issues
- **RISK**: Client infrastructure access delayed
  - Mitigation: Working on design docs while waiting
- **ISSUE**: Legacy code more complex than estimated
  - Impact: May need 10-20 additional hours

## Notes
- Client is very responsive and engaged
- Weekly check-ins on Fridays at 2pm
- Key stakeholder: Jane Smith (CTO)
```

## Project Status Indicators
- 🟢 **On Track** - Progressing as planned
- 🟡 **At Risk** - Issues that need attention
- 🔴 **Blocked** - Cannot proceed, escalation needed
- ✅ **Complete** - Done and delivered

## Best Practices
- Update status weekly
- Link to related tasks for traceability
- Track actual vs. estimated hours
- Document decisions and context
- Maintain risk register

## MCP Integration
- Use **work_server** to track project tasks
- Use **billing_server** to invoice milestones
- Use **client_server** to log project meetings
