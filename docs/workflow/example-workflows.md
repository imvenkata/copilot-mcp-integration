# Copilot MCP Workflow Examples

Quick reference for using the repo's Copilot prompts (`.github/prompts/*.prompt.md`) and agents (`.github/agents/*.agent.md`). Prompts are task-specific templates you invoke on demand; agents are personas with behaviors/goals you keep active for a session. See also: `docs/copilot-mcp-notes.md` for when instructions vs prompts vs agents apply.

Cheat sheet: `docs/quick-reference.md` for command snippets, env vars, and config examples.

## Quick nav
- [Baseline instructions](#baseline-instructions-auto-applied)
- [How to run + safety](#how-to-run--safety-checklist)
- [Prompt workflows](#prompt-workflows-githubpromptsgithubprompts)
- [Agent workflows](#agent-workflows-githubagentsgithubagents)
- [Scenarios](#combining-prompts-and-agents-scenarios)

## Baseline instructions (auto-applied)
- Repo instructions (`.github/copilot-instructions.md`) always apply: read-only bias, use MCP first, surface permissions/branch protections.
- Scoped instructions live in `.github/instructions/*.instructions.md` (GitLab dev/API: `**/*.py`, `**/*.yml`, `**/*.yaml`, `.gitlab-ci.yml`, `.github/workflows/**`; Confluence docs: `docs/**/*.md`).
- Instructions stack: global + any matching scoped instructions, alongside whichever prompt/agent you pick.

## How to run + safety checklist
- Stay within the configured GitLab host/group and `GITLAB_ALLOWED_PROJECT_IDS`; decline cross-project requests and confirm scope before any action.
- Confirm MCP parameters before acting: project/group path, issue/MR ID, branch/tag, action, and desired read-only vs write behavior.
- Call out permissions early: required tokens/env vars (`GITLAB_PERSONAL_ACCESS_TOKEN`, `GITLAB_API_URL`), protected branches, approvals, environments.
- Stay read-only unless you explicitly confirm a write/trigger; show MCP call parameters first.
- Include project IDs/paths and scopes in the ask (issue/MR IDs, branches/tags, space keys); set pagination/sample sizes when fetching history.
- Surface pipeline/test impacts if editing CI/YAML or automation; prefer MCP data over assumptions.

## Prompt workflows (`.github/prompts`)

### Implement Issue — `implement-issue`
- When: Deliver a small, testable change for a GitLab issue.
- Required: project ID/path, issue ID, target branch, delivery branch name.
- Best practices: confirm host/group/project scope, prefer a feature branch (avoid committing directly to protected/default), fetch and restate issue via MCP, plan scope/tests/risks, outline MR draft metadata (title, description sections, labels/reviewers).

### Review Merge Request — `review-merge-request`
- When: Structured MR review with actionable findings.
- Required: project ID/path, MR ID, review scope (full/targeted/follow-up).
- Best practices: confirm host/group/project scope, use the latest MR version and flag stale/outdated branches, fetch MR state/pipelines/approvals, order findings by severity, flag missing tests/docs/branch blockers, draft comments with file/line refs (draft-only unless approved to post).

### MR Health Check — `mr-health-check`
- When: Quick readiness snapshot before merge.
- Required: project ID/path, MR ID. Optional: target branch, priority labels.
- Best practices: confirm host/group/project scope, use the latest MR version and flag if branch is behind target, collect approvals/discussions/pipelines, list failing jobs with URLs, score readiness, highlight missing docs/tests and risky signals.

### Flaky Test Triage — `flaky-test-triage`
- When: Investigating an intermittent test on a branch/tag.
- Required: project ID/path, branch/tag, test name or pattern.
- Best practices: set sample size/pagination, compute failure rate, link failing jobs/log snippets, call out patterns (runner/stage/commit/time), propose repro/mitigations.

### Summarize Issues — `summarize-issues`
- When: Roll up one or more issues with recent comments.
- Required: project ID/path, issue ID or list.
- Best practices: set comment window/pagination, include author/timestamps in digests, flag missing metadata (assignee/severity), provide rollup by state/priority.

### Query Issues — `query-issues`
- When: List issues by filters for triage/reporting.
- Required: project/group ID or path; filters (state, labels/milestone, ordering).
- Best practices: confirm pagination, show key fields (ID, title, state, labels, assignee, milestone, updated), highlight blockers/missing metadata, propose follow-ups only with approval.

### Create Issue — `create-issue`
- When: Draft a well-scoped GitLab issue.
- Required: project/group, title, type/labels and severity/priority, summary and acceptance criteria.
- Best practices: capture milestones/due dates/assignees/links if relevant; show MCP create parameters before sending.

### Create Merge Request — `create-merge-request`
- When: Scaffold an MR draft and metadata.
- Required: project ID/path, source and target branches, title and brief summary.
- Best practices: include issue links, labels, reviewers, milestone, pipeline needs; present MCP call for confirmation before creation.

### Manage Milestones — `manage-milestones`
- When: List/create/update/report on milestones.
- Required: project/group ID/path and action (list/create/update/report).
- Best practices: include title/description/dates/state, link issues/MRs if summarizing; show MCP parameters before modifying.

### Trigger Pipeline — `trigger-pipeline`
- When: Trigger new pipeline, retry failed pipeline, or play a manual job.
- Required: project ID/path; branch or pipeline ID; action (trigger/retry/play).
- Best practices: confirm host/group/project scope and that pipelines are enabled (`USE_PIPELINE=true`), confirm protected branches/env impacts, needed variables, and any dry-run/skip rules; show exact MCP trigger/retry call and how to monitor; proceed only with explicit approval.

### Prepare Release Notes — `prepare-release-notes`
- When: Compile release notes for a milestone, tag, or range.
- Required: project ID/path; scope (milestone, tag(s), or commit range); audience/format.
- Best practices: group changes by category, call out risks/migrations/deployment steps, list verifications (pipelines/approvals/artifacts), include links for rollback/runbooks/known issues.

### Migrate Confluence Space — `migrate-confluence-space`
- When: Plan a Confluence space migration to `docs/`.
- Required: source space key/name, target output path/repo folder, scope (all vs subset).
- Best practices: define attachment/link rewriting and hierarchy mapping, note rate/size limits and credentials, outline export/transform/validate steps; draft MCP commands for approval.

## Agent workflows (`.github/agents`)

All GitLab agents confirm host/group/project scope and stay within `GITLAB_ALLOWED_PROJECT_IDS`; they operate read-only until you approve writes or triggers.

### GitLab Code Reviewer
- Purpose: Structured MR reviews with severity-ordered findings.
- Example ask: "Use GitLab Code Reviewer on project `group/app` MR 456; focus on auth changes and do not post notes."
- Best practices: stay read-only unless approved, show MCP parameters before actions, run reflection to ensure findings match current MR state.

### GitLab Developer Assistant
- Purpose: Build/test GitLab automation and CI safely.
- Example ask: "As GitLab Developer Assistant, propose a safe CI change to add a nightly job in `.gitlab-ci.yml` for project `group/api`."
- Best practices: explain stage impacts, keep secrets out, no pipeline triggers/merges without approval, reflect on assumptions.

### GitLab Issue Specialist
- Purpose: Draft/curate issues and lists with rollups.
- Example ask: "As GitLab Issue Specialist, summarize open `sev2` issues in `group/app`, paginating if needed."
- Best practices: use pagination/backoff, flag missing labels/severity, keep actions read-only unless confirmed.

### GitLab Release Manager
- Purpose: Release notes/tags with safety checks.
- Example ask: "Act as GitLab Release Manager for milestone `v1.4` in `group/app`; draft notes and gate on failing pipelines."
- Best practices: require explicit confirmation before tags/releases or triggers; reflect on scope/approvals/pipeline data.

### GitLab Workflow Automation
- Purpose: Coordinate pipelines/milestones/wiki tasks.
- Example ask: "As GitLab Workflow Automation, plan a dry-run pipeline trigger on `main` for project `group/data` and list impacts."
- Best practices: prefer previews/dry-runs, surface protected branch/env constraints, reflect on scope and unknowns.

### Confluence Migration Agent
- Purpose: Migrate Confluence content to `docs/` Markdown for MkDocs.
- Example ask: "Use Confluence Migration Agent to migrate space `OPS`, pages under `Runbooks/`, to `docs/ops/runbooks`; attachments in `docs/assets/ops`."
- Best practices: confirm link/attachment rewrite rules, sanitize slugs, rewrite links to relative paths, run link checks, flag lossy conversions; reflect on mappings before writing.

## Combining prompts and agents (scenarios)
- Issue triage/creation: run `query-issues` to list by state/label/milestone, use `summarize-issues` for comment digests, then `create-issue` or GitLab Issue Specialist for follow-ups.
- Implement a fix/feature: use `implement-issue` to restate requirements/plan/branch, then GitLab Developer Assistant to iterate on CI/automation; hand off to `create-merge-request` for scaffolding.
- MR review: start with `mr-health-check` for readiness, then `review-merge-request` or GitLab Code Reviewer for detailed findings without posting notes.
- Release work: `prepare-release-notes` to draft notes, `trigger-pipeline` for guarded runs, and GitLab Release Manager to gate on pipelines/approvals before tagging.
- Confluence migration: `migrate-confluence-space` for plan/commands, then Confluence Migration Agent to execute with link/attachment rewrites.
