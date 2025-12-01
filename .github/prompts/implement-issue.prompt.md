---
name: "implement-issue"
description: "Deliver a small, testable change for a GitLab issue using MCP context."
---

# Implement GitLab Issue

Use MCP GitLab tools to stay in sync with the issue before coding. Default to read-only unless the user approves writes.

- Confirm GitLab host/namespace/project; use the configured default host/group if none is provided and decline cross-project requests.

## Required
- Project ID/path
- Issue ID
- Target branch (prefer a new feature branch; avoid committing directly to the protected/default branch unless explicitly requested) and desired delivery branch name

## Flow
1. Confirm host/namespace/project, then fetch the issue via MCP GitLab (project, issue ID) and restate title, description, labels, milestone, owner, acceptance criteria, and constraints.
2. Present a quick status table for prioritization (ID, title, state, assignee, labels, milestone, last updated).
3. Propose a short plan: scope, branch name, key changes, test/validation steps, and risks.
4. Outline MR draft metadata (title, description sections: Context, Changes, Tests, Risks/Rollback, Links) and labels/reviewers.

## Output
- Reconfirmed requirements and decisions.
- Status table (state, assignee, labels, milestone, updated).
- Implementation plan with a checklist for coding/tests/docs (include Definition of Done items if implied by labels/severity).
- Optional: MR draft text and the MCP parameters to create/update issue/MR after user consent.
