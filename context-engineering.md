Below is an updated, **Copilot-in-VS-Code** tutorial that ties together:

* `.github/skills/` (Agent Skills)
* `.github/instructions/` (path-specific custom instructions)
* `.github/agents/` (custom agents)
* `.github/prompts/` (prompt files)
* **Subagents** (`#runSubagent`) and where they fit

Everything is shown with **Python-project** examples.

---

## The mental model (how these pieces fit)

Think in **layers**, from “always-on rules” → “on-demand workflows” → “specialized capabilities” → “runtime orchestration”.

1. **Always-on guidance**

* `.github/copilot-instructions.md` (repo-wide rules)
* `.github/instructions/*.instructions.md` (path-specific rules with `applyTo` globs) ([GitHub Docs][1])

2. **On-demand workflows**

* `.github/prompts/*.prompt.md` (run with `/…` in chat; can pick agent/model/tools) ([Visual Studio Code][2])

3. **Personas / modes**

* `.github/agents/*.agent.md` (custom agents with their own instructions + tool/model limits + handoffs) ([Visual Studio Code][3])

4. **Reusable “capabilities”**

* `.github/skills/<skill>/SKILL.md` (+ scripts/templates/resources next to it). Copilot loads a skill when its description matches your task. ([Visual Studio Code][4])

5. **Subagents**

* Not a file/folder. It’s a **tool** you invoke (`#runSubagent`) to delegate a task into an isolated context and keep the main chat clean. ([Visual Studio Code][5])

---

## Step 0 — Create an opinionated Python baseline

Here’s a solid default structure you can drop into most Python repos:

```text
.github/
  copilot-instructions.md
  instructions/
    python-style.instructions.md
    tests.instructions.md
  prompts/
    add-fastapi-endpoint.prompt.md
    write-pytests.prompt.md
    triage-failing-tests.prompt.md
  agents/
    planner.agent.md
    implementer.agent.md
    reviewer.agent.md
  skills/
    pytest-triage/
      SKILL.md
      run_pytest.sh
    packaging-release/
      SKILL.md
      release_checklist.md
```

---

## 1) Repo-wide custom instructions: `.github/copilot-instructions.md`

This file applies broadly across the repo. ([GitHub Docs][1])

**Example (`.github/copilot-instructions.md`)**

```md
# Copilot instructions for this repository (Python)

## Project basics
- This is a Python 3.12+ project.
- Packaging is via `pyproject.toml`.
- Prefer `ruff` for lint/format and `pytest` for tests.

## Code standards
- Write type hints for all public functions and methods.
- Keep functions small and cohesive; avoid hidden side effects.
- Prefer dataclasses or pydantic models for structured data.

## Testing
- Use `pytest`.
- New code must include unit tests.
- Tests should be deterministic (no network/time randomness unless mocked).

## Workflow
- Before proposing changes, scan the closest existing patterns in the repo.
- If you add a dependency, justify why and keep it minimal.
```

**Tip (VS Code):** you can have VS Code generate a starter `.github/copilot-instructions.md` from the Chat view menu (“Generate Chat Instructions”). ([Visual Studio Code][6])

---

## 2) Path-specific instructions: `.github/instructions/*.instructions.md`

These let you apply rules only to specific files/paths via `applyTo` globs. ([GitHub Docs][1])
If both repo-wide and path-specific apply, **both are used**; avoid conflicts because resolution can be non-deterministic. ([GitHub Docs][1])

### Example A — Python style rules

```md
---
applyTo: "**/*.py"
---

## Python style rules
- Use ruff-compatible formatting.
- Prefer explicit imports; avoid wildcard imports.
- Public functions/classes must have docstrings (Google style or concise).
- Use pathlib over os.path where practical.
- Prefer returning typed domain objects over raw dicts.
```

### Example B — Tests-only rules

```md
---
applyTo: "tests/**/*.py"
---

## Test rules
- Use Arrange–Act–Assert structure.
- Prefer parametrize for variations.
- Use `pytest-mock` or unittest.mock for mocking.
- Do not hit network; use fixtures/mocks.
```

### Optional: “not for code review” instructions (agent-specific)

GitHub added `excludeAgent` so an instructions file can apply to some Copilot agents but not others (example: hide from “code-review” or “coding-agent”). ([The GitHub Blog][7])

```md
---
applyTo: "**/*.py"
excludeAgent: "code-review"
---

# Implementation-only hints
- When implementing, prefer the existing project patterns even if alternatives exist.
```

---

## 3) Prompt files: `.github/prompts/*.prompt.md`

Prompt files are reusable workflows you run on demand:

* In VS Code chat, type `/` + prompt name ([Visual Studio Code][2])
* They support YAML frontmatter like `agent`, `model`, and `tools` ([Visual Studio Code][2])
* Tool priority: prompt tools > referenced agent tools > selected agent defaults ([Visual Studio Code][2])

### Example 1 — Add a FastAPI endpoint (implementation workflow)

```md
---
name: add-fastapi-endpoint
description: Add a FastAPI endpoint with schema, tests, and docs update.
agent: agent
tools: ["search", "readFile", "edit", "runTests", "runInTerminal"]
argument-hint: "path=/v1/widgets method=GET"
---

You are adding a FastAPI endpoint.

Inputs:
- Endpoint path and method from the user
- Brief behavior description if provided

Steps:
1) Find existing router patterns and how dependencies/auth are done.
2) Implement the endpoint following repo conventions.
3) Add/extend pydantic models if needed.
4) Add pytest tests covering success + one failure case.
5) Run tests and fix failures.
6) Summarize changes and list files edited.
```

### Example 2 — Generate pytest tests for selected code

```md
---
name: write-pytests
description: Write pytest unit tests for the selected code.
agent: agent
tools: ["readFile", "search", "edit"]
argument-hint: "target=<module or file> focus=<edge cases?>"
---

Write unit tests using pytest for the selected code.

Rules:
- Use Arrange–Act–Assert.
- Prefer parametrize for variations.
- Mock external effects (I/O, time, network).
- Keep tests readable; avoid over-mocking.

Output:
- Provide the test file path and the complete test contents.
```

### Example 3 — Triage failing tests (uses subagent)

This is where you start weaving **subagents** into your “library”.

```md
---
name: triage-failing-tests
description: Diagnose failing pytest runs and propose minimal fixes.
agent: agent
tools: ["runTests", "runInTerminal", "readFile", "search", "runSubagent"]
argument-hint: "scope=tests or scope=full"
---

Run tests and triage failures.

Process:
1) Run the relevant pytest command.
2) Use #runSubagent to analyze the failure output and likely root causes.
3) Apply the smallest fix that matches repo patterns.
4) Re-run tests until green.
5) Summarize root cause + fix.
```

Why include `runSubagent` in `tools`? Because if you run prompt files or custom agents, VS Code recommends explicitly listing `runSubagent` in the frontmatter tools list. ([Visual Studio Code][5])

---

## 4) Custom agents: `.github/agents/*.agent.md`

Custom agents are “modes” you select in the Agents dropdown. VS Code detects `.md` files in `.github/agents/`. ([Visual Studio Code][3])
They support:

* `tools`, `model`, etc.
* `handoffs` to guide a multi-step flow (plan → implement → review) ([Visual Studio Code][3])
* `infer` to allow/disallow being used as a subagent (default true) ([Visual Studio Code][3])

### Agent A — Planner

```md
---
name: Planner
description: Plan changes without editing code.
tools: ["search", "readFile", "runSubagent"]
infer: true
handoffs:
  - label: Start Implementation
    agent: Implementer
    prompt: Implement the plan above. Keep changes minimal and add tests.
    send: false
---

You are in planning mode for a Python codebase.

Rules:
- Do not edit code.
- If you need deeper investigation, delegate it to #runSubagent and only bring back the conclusions.
- Output a plan with:
  - Overview
  - File-by-file changes
  - Test plan
  - Risks/edge cases
```

### Agent B — Implementer

```md
---
name: Implementer
description: Implement planned changes and keep tests green.
tools: ["search", "readFile", "edit", "runTests", "runInTerminal", "runSubagent"]
infer: true
handoffs:
  - label: Run Review
    agent: Reviewer
    prompt: Review the diff for correctness, security, and maintainability.
    send: false
---

You implement changes in a Python repo.

Rules:
- Follow `.github/copilot-instructions.md` and relevant `.github/instructions/*.instructions.md`.
- Make the smallest change that satisfies requirements.
- Add/adjust pytest tests.
- Keep commits/diffs focused.
```

### Agent C — Reviewer (and keep it out of subagents if you want)

```md
---
name: Reviewer
description: Review for correctness, security, and maintainability.
tools: ["readFile", "search"]
infer: false
---

You are a strict code reviewer.

Checklist:
- Correctness and edge cases
- Security concerns (auth, injection, secrets, unsafe deserialization)
- Maintainability (naming, structure, duplication)
- Tests: missing cases, flaky risks
Output:
- Findings grouped by severity (blocker/major/minor)
- Concrete suggestions
```

---

## 5) Agent Skills: `.github/skills/<skill>/SKILL.md`

Skills are portable “capabilities” that Copilot can auto-load when relevant. ([Visual Studio Code][4])
VS Code supports skills in:

* `.github/skills/` (recommended)
* `.claude/skills/` (legacy compatibility; useful if you previously used Claude Code skills) ([Visual Studio Code][4])

### Skill 1 — Pytest triage skill

`.github/skills/pytest-triage/SKILL.md`

```md
---
name: pytest-triage
description: Diagnose failing pytest runs, classify root causes, and propose minimal fixes with verification steps.
---

# Pytest triage skill

## When to use
Use when tests are failing locally or in CI and you need a structured diagnosis + fix.

## Procedure
1) Run tests:
   - Prefer targeted runs first: `pytest -q path/to/failing_test.py::test_name`
2) Classify failure:
   - Assertion mismatch (logic)
   - Fixture/setup issue
   - Mocking mistake
   - Time/order/flakiness
   - Environment/config mismatch
3) Identify minimal fix:
   - Prefer fixing production code over loosening assertions
   - Keep behavior stable; update tests only if spec changed
4) Verify:
   - Re-run targeted tests
   - Re-run full test suite if reasonable

## Scripts
- If available, use `./run_pytest.sh` for consistent flags.
```

Add a helper script next to it:

`.github/skills/pytest-triage/run_pytest.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
pytest -q --disable-warnings --maxfail=1 "$@"
```

### Skill 2 — Packaging + release checklist

`.github/skills/packaging-release/SKILL.md`

```md
---
name: packaging-release
description: Prepare a Python project release: version bump, changelog notes, build validation, and publishing checks.
---

# Packaging & release skill

## Procedure
1) Confirm version strategy (semver) and bump version in `pyproject.toml`.
2) Update CHANGELOG (or release notes).
3) Build and validate:
   - `python -m build`
   - `twine check dist/*` (if used)
4) Run full test suite.
5) Ensure tags/branch strategy matches repo norms.

See [release checklist](./release_checklist.md).
```

Skills use a “load only when needed” approach: Copilot can discover skills via `name`/`description`, then load instructions when relevant, then access extra files/scripts as needed. ([Visual Studio Code][4])

**Important: Skills are NOT redundant with `.github/instructions`.**

* Instructions = broad, path-based “rules of the road”.
* Skills = task-based playbooks + resources/scripts that get pulled in when relevant. ([Visual Studio Code][4])

---

## 6) Subagents in Copilot (the “Claude subagents” concept, in VS Code terms)

In VS Code Copilot Chat, **subagents** are “context-isolated” autonomous workers you spin up *inside* a chat session. They have their own context window and return only the final result, helping prevent the main chat from getting bloated/confused. ([Visual Studio Code][5])

Key behaviors:

* Not asynchronous/background; they run autonomously but inline. ([Visual Studio Code][5])
* By default they use the same agent/tools/model as the main chat, and can’t create more subagents. ([Visual Studio Code][5])
* You invoke them via the **`runSubagent` tool** (often referenced as `#runSubagent`). ([Visual Studio Code][8])

### How to enable/use subagents

1. Enable `runSubagent` in VS Code’s tool picker. ([Visual Studio Code][5])
2. In your prompt: ask Copilot to run a subagent for a clearly scoped task.

Example prompts:

* “Use a subagent to analyze why CI pytest is failing and return the most likely root cause and fix.” ([Visual Studio Code][5])
* “Analyze `pyproject.toml` and recommend the minimal dependency changes needed for feature X, using `#runSubagent`.” (pattern from VS Code guidance) ([Visual Studio Code][9])

### Using a *custom agent* as a subagent (Experimental)

VS Code can (experimentally) run a subagent using a different built-in/custom agent:

* enable `chat.customAgentInSubagent.enabled` ([Visual Studio Code][10])
* ensure your custom agent doesn’t set `infer: false` ([Visual Studio Code][5])
* then prompt: “Run the Planner agent as a subagent to produce a plan…” ([Visual Studio Code][5])

---

## Recommended “best practice” workflow for Python projects

**Feature work (clean + repeatable):**

1. Use **Planner agent** to create a plan (delegate research to subagent if needed)
2. Handoff to **Implementer**
3. Handoff to **Reviewer**
4. If tests fail: run `/triage-failing-tests`

**Bugfix (fast triage):**

* `/triage-failing-tests scope=targeted`
* If it smells like repo-specific procedure, rely on a **skill** (e.g., `pytest-triage`)

**When to choose skills vs prompts vs agents**

* “Do this task the same way every time” → **Prompt file**
* “I want a different persona/mode for a while” → **Custom agent**
* “This is a specialized playbook with scripts/templates” → **Skill**
* “This requires deep investigation but I don’t want to pollute main chat” → **Subagent**

---

## Comparison table

| Item                                      | Where it lives                                  | Trigger                                                   | Scope              | Best for                                                                       | Notes / gotchas                                                                                                                                      |
| ----------------------------------------- | ----------------------------------------------- | --------------------------------------------------------- | ------------------ | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repo-wide custom instructions             | `.github/copilot-instructions.md`               | Automatic                                                 | Whole repo         | Global conventions (Python version, tooling, testing expectations)             | Can be generated in VS Code (“Generate Chat Instructions”). ([Visual Studio Code][6])                                                                |
| Path-specific custom instructions         | `.github/instructions/*.instructions.md`        | Automatic when working on matching files                  | Per `applyTo` glob | Different rules for `src/` vs `tests/` vs `scripts/`                           | If repo-wide + path-specific both apply, both are used; avoid conflicts. ([GitHub Docs][1])                                                          |
| Agent-specific filtering for instructions | frontmatter `excludeAgent`                      | Automatic                                                 | Per agent          | Keep review guidance separate from implementation guidance                     | `excludeAgent` supports targeting (e.g., hide from code review). ([The GitHub Blog][7])                                                              |
| Prompt files                              | `.github/prompts/*.prompt.md`                   | Run via `/prompt-name` (or play button / command palette) | One run            | Repeatable workflows: add endpoint, write tests, triage CI                     | Can set `agent`, `model`, `tools`; tool priority is prompt > agent > defaults. ([Visual Studio Code][2])                                             |
| Custom agents                             | `.github/agents/*.agent.md`                     | Select in Agents dropdown                                 | While selected     | “Modes”: Planner, Implementer, Reviewer                                        | Support `handoffs` and `infer` (subagent eligibility). ([Visual Studio Code][3])                                                                     |
| Agent Skills                              | `.github/skills/<skill>/SKILL.md` (+ resources) | Auto-loaded when relevant                                 | Per task           | Specialized playbooks with scripts/templates (pytest triage, releases, deploy) | Also supports legacy `.claude/skills`; skills load progressively (metadata → instructions → resources). ([Visual Studio Code][4])                    |
| **Subagents**                             | (no folder) `#runSubagent` tool                 | Explicit in prompt (and tool enabled)                     | One delegated task | Deep research/analysis without bloating main chat context                      | Context-isolated; returns only final result; default uses same agent/tools/model; custom-agent subagents are experimental. ([Visual Studio Code][5]) |

---

If you want, I can also provide a **ready-to-copy “starter pack”** of these files tuned to your stack (FastAPI vs Django vs CLI lib, Poetry vs uv vs pip-tools, etc.)—but the examples above already work well as a strong default for most Python repos.

[1]: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot "Adding repository custom instructions for GitHub Copilot - GitHub Docs"
[2]: https://code.visualstudio.com/docs/copilot/customization/prompt-files "Use prompt files in VS Code"
[3]: https://code.visualstudio.com/docs/copilot/customization/custom-agents "Custom agents in VS Code"
[4]: https://code.visualstudio.com/docs/copilot/customization/agent-skills "Use Agent Skills in VS Code"
[5]: https://code.visualstudio.com/docs/copilot/chat/chat-sessions "Manage chat sessions in VS Code"
[6]: https://code.visualstudio.com/docs/copilot/customization/custom-instructions "Use custom instructions in VS Code"
[7]: https://github.blog/changelog/2025-11-12-copilot-code-review-and-coding-agent-now-support-agent-specific-instructions/ "Copilot code review and coding agent now support agent-specific instructions - GitHub Changelog"
[8]: https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features "GitHub Copilot in VS Code cheat sheet"
[9]: https://code.visualstudio.com/blogs/2025/11/03/unified-agent-experience "A Unified Experience for all Coding Agents"
[10]: https://code.visualstudio.com/docs/copilot/reference/copilot-settings "GitHub Copilot in VS Code settings reference"
