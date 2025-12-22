# Context Engineering

* `.github/instructions` (path-specific instructions)
* `.github/skills` (Agent Skills)
* `.github/agents` (custom agent profiles)
* `.github/prompts` (prompt files)



## The mental model (when each one gets applied)

Think of these as **four different knobs**:

1. **Instructions** = *always-on guidance* (repo-wide + path-specific)
2. **Prompt files** = *on-demand “macros” you run* (usually with `/something`)
3. **Custom agents** = *preconfigured “teammates”* (tools + behavior)
4. **Skills** = *on-demand deep playbooks* Copilot can load when relevant

GitHub explicitly recommends using **custom instructions for simple guidance relevant to almost every task**, and **skills for more detailed instructions that should be accessed only when relevant**. ([GitHub Docs][1])

---

## Suggested repo layout

```text
.github/
  copilot-instructions.md
  instructions/
    backend.instructions.md
    frontend.instructions.md
    docs.instructions.md
    python.instructions.md
  prompts/
    review-code.prompt.md
    explain-code.prompt.md
    debug-ci.prompt.md
  agents/
    planner.agent.md
    test-specialist.agent.md
  skills/
    pytest-failure-triage/
      SKILL.md
      scripts/
        parse_pytest_output.py
    dependency-upgrade/
      SKILL.md
    release-cut/
      SKILL.md

```

---

Here’s a **copy-pasteable example set** for a typical Python repo using **pytest + ruff + mypy** (swap tools if you use different ones). I’m giving you:

* `.github/copilot-instructions.md`
* `.github/instructions/*.instructions.md`
* `.github/prompts/*.prompt.md`
* `.github/agents/*.agent.md`
* `.github/skills/*/SKILL.md` (+ optional helper scripts)

---

## Suggested layout

```text
.github/
  copilot-instructions.md
  instructions/
    python.instructions.md
    tests.instructions.md
    docs.instructions.md
  prompts/
    review-python.prompt.md
    add-pytest-tests.prompt.md
    fix-typing.prompt.md
    debug-ci.prompt.md
  agents/
    planner.agent.md
    test-specialist.agent.md
    maintainer.agent.md
  skills/
    pytest-failure-triage/
      SKILL.md
      scripts/
        parse_pytest_output.py
    dependency-upgrade/
      SKILL.md
    release-cut/
      SKILL.md
```

---

# 1) Repo-wide instructions

## `.github/copilot-instructions.md`

```md
# Copilot instructions (Python project)

## Project goals
- Write clear, maintainable Python.
- Prefer small, composable functions.
- Keep side effects at the edges (I/O, network, filesystem).

## Supported Python + tooling (edit to match this repo)
- Python: 3.11+
- Tests: pytest
- Lint/format: ruff
- Type-check: mypy

## Commands (keep these up to date)
- Install: `python -m pip install -r requirements-dev.txt`
- Tests: `pytest -q`
- Lint: `ruff check .`
- Format: `ruff format .`
- Types: `mypy src`

## Definition of done for changes
- All tests pass locally.
- Lint + formatting are clean.
- Types are clean (or clearly justified with narrow ignores).
- Add/update tests for behavior changes.
- Update docs/README when behavior or public APIs change.

## Coding conventions
- Prefer `pathlib.Path` over `os.path`.
- Prefer `dataclasses` for simple data containers.
- Prefer explicit errors with helpful messages.
- Avoid overly clever one-liners; readability > brevity.
- When editing existing code, match existing style and patterns.

## Performance & safety
- Avoid quadratic loops on large collections.
- Validate external inputs early; fail fast with good messages.
- Never log secrets (tokens, passwords, keys).
```

---

# 2) Path-specific instructions

## `.github/instructions/python.instructions.md` (applies to all Python files)

```md
---
applyTo: "**/*.py"
---

## Python file guidance
- Use type hints for public functions and non-trivial internals.
- Keep functions < ~50 lines when practical; split helpers.
- Prefer `logging` over prints; no debug prints in commits.
- Raise specific exceptions (`ValueError`, `KeyError`, custom) with actionable messages.
- If you add a dependency, justify it briefly in the PR description and update dependency files.

## Structure
- Keep domain logic in `src/` (or equivalent).
- Keep CLI / entrypoints minimal and delegate to library code.
```

## `.github/instructions/tests.instructions.md` (only tests)

```md
---
applyTo: "tests/**/*.py"
---

## Pytest conventions
- Use Arrange–Act–Assert pattern.
- Prefer fixtures over repeated setup.
- Avoid sleeping/time-based flakiness; use freezegun or monkeypatch time.
- Name tests for behavior: `test_<what>__<condition>__<expected>()`

## Assertions
- Assert the most important behavior first.
- For exceptions: use `with pytest.raises(ExpectedError, match="...")`.
```

## `.github/instructions/docs.instructions.md` (docs + Markdown)

```md
---
applyTo: "**/*.md"
---

## Documentation conventions
- Use short paragraphs and runnable code blocks.
- Prefer examples over prose.
- Keep README instructions current with actual commands.
```

---

# 3) Prompt files (reusable “macros”)

## `.github/prompts/review-python.prompt.md`

```md
---
description: "Review Python changes with a checklist (correctness, tests, types, security)."
---

Review the selected changes (or currently open files).

Output sections:
1) Summary (1-3 bullets)
2) Correctness risks (with file:line references if possible)
3) Test coverage gaps (what to add)
4) Type-hinting / API clarity issues
5) Security or secrets risks
6) Suggested patch (only if small and safe)
```

## `.github/prompts/add-pytest-tests.prompt.md`

```md
---
description: "Generate pytest tests for the selected code."
argument-hint: "Target module/function and key behaviors"
---

Write pytest tests for: {{args}}

Rules:
- Do not modify production code unless absolutely necessary; if necessary, explain why.
- Use existing fixtures/patterns from the repo.
- Include at least:
  - happy path
  - one edge case
  - one failure case (exception or invalid input)

Return:
- New/updated test files with code blocks
- Short note explaining what each test protects
```

## `.github/prompts/fix-typing.prompt.md`

```md
---
description: "Fix mypy errors with minimal API changes."
---

Given the current mypy errors (paste them if not visible), propose fixes that:
- minimize public API changes
- avoid broad `Any`
- use narrow casts and `TypedDict`/`Protocol` when appropriate
- keep runtime behavior unchanged

Provide:
- explanation of root cause
- patch-style edits
```

## `.github/prompts/debug-ci.prompt.md`

```md
---
description: "Debug failing CI run and propose fixes."
---

Use this workflow:
1) Identify which job/step failed and why.
2) Classify failure: test, lint, typing, packaging, env, network/flaky.
3) Provide 1-3 likely root causes.
4) Propose a minimal fix.
5) Propose a regression test or guardrail to prevent recurrence.
```

---

# 4) Custom agents (specialized “teammates”)

## `.github/agents/planner.agent.md`

```md
---
name: planner
description: "Plans changes: breaks work into steps, highlights risks, defines tests."
infer: true
---

You are a senior Python engineer focused on planning.

When asked to implement something:
- First produce a plan with steps, risks, and acceptance criteria.
- Identify what tests should be added/updated.
- Identify what files are likely to change.
- Keep the plan short and actionable.
```

## `.github/agents/test-specialist.agent.md`

```md
---
name: test-specialist
description: "Writes high-quality pytest tests and improves coverage with minimal production edits."
infer: true
---

You are a testing specialist.

Rules:
- Only change production code if tests cannot be written otherwise.
- Prefer deterministic tests; avoid sleeps and randomness.
- Use fixtures and parametrization.
- Explain test intent briefly.

Deliver:
- test code
- rationale for coverage
- any follow-ups (e.g., missing seams)
```

## `.github/agents/maintainer.agent.md`

```md
---
name: maintainer
description: "Maintains repo hygiene: dependencies, packaging, CI, release readiness."
infer: true
---

You are the repository maintainer.

Focus:
- dependency upgrades (minimal breakage)
- packaging metadata correctness
- CI stability
- changelog/release notes discipline

When suggesting changes:
- prefer small PRs
- include commands to verify locally
- call out backwards compatibility
```

---

# 5) Skills (deep playbooks Copilot can load on-demand)

## `.github/skills/pytest-failure-triage/SKILL.md`

```md
---
name: pytest-failure-triage
description: Use when tests fail or CI shows pytest failures. Diagnose failures quickly and propose minimal fixes.
---

# Pytest failure triage workflow

## 1) Reproduce
- Run the smallest failing set first:
  - `pytest -q`
  - then narrow: `pytest -q path/to/test_file.py::test_name -vv`

## 2) Classify
- Assertion mismatch (logic)
- Exception mismatch (unexpected error type/message)
- Flaky/time-related
- Environment-dependent (paths, locale, timezone)
- Test isolation issue (shared state)

## 3) Debug efficiently
- Print/log only in local debugging; do not commit prints.
- Inspect fixtures and shared state.
- Look for order dependence: `pytest -q --random-order` (if available).

## 4) Fix strategy
- Prefer fixing production bug if real.
- Otherwise fix the test if assumptions are wrong.
- Ensure the test checks behavior, not implementation details.

## 5) Add regression coverage
- Add a focused test for the root cause.
- Ensure failure mode is explicit (exception + message match where useful).

## Optional helper scripts
- If pytest output is large, use `scripts/parse_pytest_output.py` to summarize.
```

### Optional helper script

`/.github/skills/pytest-failure-triage/scripts/parse_pytest_output.py`

```python
#!/usr/bin/env python3
"""
Parse pytest output from stdin and summarize failures by test nodeid.

Usage:
  pytest -q | python .github/skills/pytest-failure-triage/scripts/parse_pytest_output.py
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict

FAIL_RE = re.compile(r"^FAILED\s+(?P<nodeid>\S+)\s+-\s+(?P<reason>.+)$")

def main() -> int:
    reasons: dict[str, list[str]] = defaultdict(list)
    for line in sys.stdin:
        m = FAIL_RE.match(line.strip())
        if m:
            reasons[m.group("nodeid")].append(m.group("reason"))

    if not reasons:
        print("No FAILED lines detected.")
        return 0

    print("Failure summary:")
    for nodeid, rs in reasons.items():
        print(f"- {nodeid}")
        for r in rs[:3]:
            print(f"  - {r}")
        if len(rs) > 3:
            print(f"  - (+{len(rs)-3} more)")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
```

---

## `.github/skills/dependency-upgrade/SKILL.md`

```md
---
name: dependency-upgrade
description: Use when upgrading Python dependencies (requirements, poetry, uv, pip-tools). Minimizes breakage and validates changes.
---

# Dependency upgrade playbook

## 1) Decide scope
- Single package bump vs full refresh
- Security-only upgrades vs feature upgrades

## 2) Upgrade safely
- Prefer upgrading one dependency group at a time.
- Record versions and why the bump is needed.

## 3) Validate
Run:
- `ruff check .`
- `ruff format .` (if applicable)
- `mypy src`
- `pytest -q`

## 4) If breakage occurs
- Identify API changes in upstream release notes.
- Add/adjust compatibility shims only if needed.
- Update tests to reflect intended behavior.

## 5) Deliverable
- Updated lock/requirements files
- Short changelog entry (if repo uses one)
- Notes about any behavior changes
```

---

## `.github/skills/release-cut/SKILL.md`

```md
---
name: release-cut
description: Use when preparing a Python release (PyPI package). Checks versioning, changelog, tags, and CI.
---

# Release cut checklist (Python)

## 1) Ensure main is green
- CI passing
- `pytest -q`, `ruff check .`, `mypy src`

## 2) Versioning
- Update version in the canonical place:
  - `pyproject.toml` (preferred) or `src/<pkg>/__init__.py`
- Confirm semver intent:
  - PATCH: bugfix
  - MINOR: backward-compatible features
  - MAJOR: breaking changes

## 3) Changelog / release notes
- Summarize user-visible changes.
- Include upgrade notes if behavior changed.

## 4) Packaging sanity checks
- `python -m build`
- `twine check dist/*` (if used)
- Verify included files (MANIFEST / package_data).

## 5) Tagging + publishing (adjust to your process)
- Tag: `vX.Y.Z`
- Publish via CI or maintainers’ process.
```

---

## Quick “what goes where” for Python repos

* Put **commands and “definition of done”** in `copilot-instructions.md`
* Put **language-specific rules** in `.github/instructions/python.instructions.md`
* Put **testing style rules** in `.github/instructions/tests.instructions.md`
* Put your **team’s repeatable workflows** into `.github/prompts/*.prompt.md`
* Create **role agents** (planner/tester/maintainer) in `.github/agents`
* Put **deep runbooks** (CI triage, release process, dependency upgrades) in `.github/skills`

