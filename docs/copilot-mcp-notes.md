# Copilot + GitLab MCP: How to pick instructions, prompts, and agents

## How instructions apply
- Repo-wide (always on): `.github/copilot-instructions.md` sets the baseline (read-only bias, use MCP first, call out permissions/branch protections).
- Scoped (path-aware): `.github/instructions/*.instructions.md` only apply when your conversation touches matching paths.
  - GitLab dev/API: `**/*.py`, `**/*.yml`, `**/*.yaml`, `.gitlab-ci.yml`, `.github/workflows/**`.
  - Confluence docs: `docs/**/*.md`.
- Stacking: global instructions always apply; any scoped instructions whose `applyTo` matches also apply. If no path match, scoped instructions stay idle.

## Prompts vs. agents (when to pick)
- Prompts (`.github/prompts/*.prompt.md`): single-run guided flows you manually start in Copilot (e.g., `implement-issue`, `review-merge-request`, `query-issues`, `trigger-pipeline`, `prepare-release-notes`). Good when you want a checklist or structured output for one task.
- Agents (`.github/agents/*.agent.md`): personas you select in the Agents menu (e.g., GitLab Code Reviewer, Developer Assistant, Issue Specialist, Release Manager, Workflow Automation). They persist across the conversation and keep their goals/behavior active.

- Use a **prompt** when you want a structured, one-off workflow. You explicitly start it, it runs through its checklist, and then it’s done. Good for: “Draft an MR,” “Query issues with filters,” “Trigger a pipeline with guardrails,” “Prepare release notes for milestone X.”
  
- Use an **agent** when you want a persona to stay with you across the conversation. You pick it once, and it keeps its goals/behavior active as you move between tasks. Good for: ongoing MR review with context, iterative dev/CI guidance, continuous issue triage/curation, coordinating pipelines and milestones over multiple steps.



## Practical GitLab MCP flows and what to use
- Issue triage or creation: start with `query-issues` to list by state/label/milestone; switch to `create-issue` to draft; use the GitLab Issue Specialist agent for ongoing curation.
- Implement a fix/feature: use `implement-issue` prompt to restate the issue, plan, and draft MR metadata; add the GitLab Developer Assistant agent for continued coding/CI guidance.
- MR review: run `review-merge-request` prompt for a structured pass or pick the GitLab Code Reviewer agent for ongoing review context; keep comments draft unless approved to post via MCP.
- Release prep: use `prepare-release-notes` prompt for milestone/tag rollups; the GitLab Release Manager agent helps keep safety checks and approvals in view.
- Pipeline action: use `trigger-pipeline` prompt to trigger/retry/play with guardrails; the GitLab Workflow Automation agent coordinates pipelines/milestones/wiki tasks.

## Quick safety checklist (any GitLab MCP task)
- Confirm MCP params before acting: project/group ID or path; issue/MR ID; branch; action; desired read-only vs write.
- Call out permissions upfront: PAT/OAuth env vars (`GITLAB_PERSONAL_ACCESS_TOKEN`, `GITLAB_API_URL`), branch protections, approvals, environments.
- Prefer MCP for data; if proposing writes, show the tool name and parameters and get consent first.
- Surface tests/validation and pipeline impacts when editing CI/YAML or automation code.

## Putting it together (examples)
- **List open P1 bugs this week and draft an issue for a new regression**
  - Global instructions apply.
  - Use `query-issues` prompt to fetch issues; if you’re editing YAML/Python while automating, GitLab scoped instructions apply.
  - Draft the new regression with `create-issue` prompt; if you edit a CI file, GitLab dev/API scoped instructions kick in.
- **Review MR 42 and suggest fixes, don’t post comments yet**
  - Global instructions apply.
  - Choose the “GitLab Code Reviewer” agent or the `review-merge-request` prompt.
  - If you open CI files in the MR, the GitLab scoped instructions also influence guidance (pipeline impacts, permissions).
- **Trigger the release pipeline on main and prep notes for milestone 15.1**
  - Global instructions apply (warn about approvals/protections).
  - Use `trigger-pipeline` prompt for the pipeline action; `prepare-release-notes` prompt for notes.
  - If you touch `.gitlab-ci.yml`, the GitLab scoped instructions apply too.

