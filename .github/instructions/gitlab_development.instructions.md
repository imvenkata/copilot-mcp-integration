applyTo:
  - "**/*.py"
  - "**/*.yml"
  - "**/*.yaml"
  - ".gitlab-ci.yml"
  - ".github/workflows/**"

# GitLab Development Workflow

## Applies when
- Building or refactoring code tied to GitLab issues/epics or MCP GitLab automation.
- Planning implementation branches, tests, or release notes for GitLab projects.

## Instructions
- Pull context first: fetch the issue/epic/MR via MCP and restate the acceptance criteria, owners, labels, and milestone.
- Propose a minimal plan (branch, scope, tests) before coding; keep work in small increments with clear checkpoints.
- Align with project conventions: link issues in commit/MR text (`Closes #ID`), respect protected branches, and default to draft MRs.
- Include validation steps per change: unit/integration tests, pipeline expectations, and manual checks for critical paths; confirm required CI runners/variables exist before suggesting pipeline runs.
- Note dependencies on GitLab settings (runners, required approvals, CI variables) and avoid altering them without explicit approval.
- When suggesting code, keep secrets out, use env vars for tokens, and add brief comments only where behavior is non-obvious.
- When drafting MRs, provide the template sections (Context, Changes, Tests, Risks/Rollback, Links) to align with prompts.
