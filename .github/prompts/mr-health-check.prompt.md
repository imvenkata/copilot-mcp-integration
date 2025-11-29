---
name: "mr-health-check"
description: "Assess GitLab MR readiness with MCP: pipelines, approvals, blockers, and risk."
---

# Merge Request Health Check

Use this to evaluate an MR before merge. Default to read-only; do not trigger pipelines or post notes without user approval.

## Required
- Project ID/path
- MR ID

## Optional
- Target branch (if different from default)
- Priority/labels to highlight

## Flow
1. Fetch MR via MCP: title, state, labels, approvals, blocking discussions, pipeline status/log links.
2. List failing jobs (name, stage, URL) and note required approvals/tests missing.
3. Check for risky signals: breaking change labels, missing docs/tests, large diff, outdated branch.
4. Produce a ready-to-merge score (0–100) with rationale (pipelines, approvals, blockers, docs/tests).
5. Offer follow-ups (post review notes, trigger/retry pipeline) only after confirmation; show MCP parameters first.

## Output
- MR summary (state, approvals, pipeline result/links, blockers).
- Ready-to-merge score with brief rationale.
- Blockers list and missing tests/docs.
- Failing jobs table with URLs and suggested fixes.
- Optional next steps plus MCP call parameters if requested.
