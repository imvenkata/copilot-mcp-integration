---
name: "query-issues"
description: "List and summarize GitLab issues with MCP GitLab tools."
---

# Query GitLab Issues

Use MCP GitLab tools in read-only mode to fetch issues, then provide a concise summary.

- Confirm GitLab host/namespace/project; use the configured default host/group if none is provided and decline cross-project requests.

## Required
- Project/group ID or path
- Filters: state (opened/closed), label(s) and/or milestone, and ordering (updated_at/created_at)

## Optional
- Assignee(s)/author, search text, severity/priority labels, pagination size

## Flow
1. Confirm host/namespace/project and filters; set `per_page` and pagination strategy.
2. List issues via MCP GitLab; include ID, title, state, labels, assignee, milestone, updated time, and blocking flags.
3. Summarize patterns: counts by state/label/milestone, oldest blocking items, and missing metadata (assignee/priority/severity).
4. Offer follow-ups (assign, label, close, create MR link) only after explicit approval.

## Output
- Brief table or bullet summary with key fields per issue and totals by state/label.
- Call out blockers/risk (no assignee, overdue milestone) and propose next actions.
- If writes are approved, list the MCP parameters before executing any change.
