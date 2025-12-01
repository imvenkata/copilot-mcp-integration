---
name: "summarize-issues"
description: "Summarize one or more GitLab issues with MCP, including recent comments."
---

# Summarize GitLab Issues

Use this to get a high-level understanding of one or many issues. Default to read-only; do not post notes without confirmation.

- Confirm GitLab host/namespace/project; use the configured default host/group if none is provided and decline cross-project requests.

## Required
- Project ID/path
- Issue ID or list of issue IDs

## Optional
- Comment window (e.g., last 7/14/30 days) or max comments to include
- Filters to flag (severity/priority/labels, assignee, milestone)

## Flow
1. Confirm host/namespace/project and scope (issue IDs, comment window); set pagination for notes.
2. Fetch each issue via MCP GitLab: title, state, labels, assignee(s), milestone, updated time.
3. Fetch recent comments/notes per issue (respect the window/limit); capture author, timestamp, and key points.
4. Produce a compact summary per issue and an overall rollup (states, priorities, owners, oldest updates).
5. Offer follow-ups (assign/label/comment/close) only after confirmation; show MCP parameters before any action.

## Output
- Per-issue summary: ID, title, state, labels, assignee, milestone, updated, and brief comment digest with links.
- Rollup: counts by state/priority/label, oldest unupdated items, and obvious gaps (no assignee, missing severity).
- Optional next steps plus MCP call parameters if the user wants updates posted.
