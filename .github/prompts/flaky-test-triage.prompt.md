---
name: "flaky-test-triage"
description: "Investigate flaky tests using MCP pipeline history and logs."
---

# Flaky Test Triage

Use MCP GitLab tools in read-only mode to analyze flaky tests. Confirm before triggering or rerunning jobs.

## Required
- Project ID/path
- Branch or tag
- Test name/pattern

## Optional
- Time/window or number of recent pipelines to inspect
- Relevant job/stage filters

## Flow
1. Confirm GitLab host/namespace/project and scope (branch/tag, test pattern); use the configured default host/group if unspecified and decline cross-project requests. Set pagination for recent pipelines/jobs.
2. Fetch recent runs via MCP; collect pass/fail counts, durations, and log snippets for the test.
3. Compute failure rate and note patterns (by runner, stage, commit, time of day, retry).
4. Identify likely causes: recent code changes, slow setup, external calls, data races, or flaky fixtures.
5. Propose repro steps and mitigations (quarantine/skip, retry/backoff, fixture fixes, isolation); show MCP parameters before any action.

## Output
- Failure rate summary and sample failing job links/log snippets.
- Pattern observations (per runner/stage/commit) and suspected causes.
- Repro steps and targeted fixes.
- Optional: MCP parameters for retries/notes if the user asks to execute.
