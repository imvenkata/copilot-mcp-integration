Below is a practical “best setup” tutorial for **Python projects** using these Copilot customization building blocks:

* `.github/copilot-instructions.md` (repo-wide instructions)
* `.github/instructions/*.instructions.md` (path/file-type scoped instructions)
* `.github/prompts/*.prompt.md` (on-demand reusable prompts)
* `.github/agents/*.agent.md` (switchable personas with tool limits)
* `.github/skills/<skill-name>/SKILL.md` (auto-loaded playbooks + resources)

It’s worth doing all of these because they’re **not redundant**: GitHub’s guidance is to use **custom instructions for simple, always-relevant rules** and **skills for deeper, task-specific playbooks** that load only when needed. ([GitHub Docs][1])

---

## 1) The mental model: what loads when

### Always-on guidance (great defaults)

1. **Repo-wide** instructions: `.github/copilot-instructions.md` applies broadly. ([GitHub Docs][2])
2. **Scoped** instructions: `.github/instructions/*.instructions.md` apply via `applyTo` globs, and can stack with repo-wide instructions. Avoid conflicts because Copilot’s choice between conflicting instructions can be non-deterministic. ([GitHub Docs][2])
3. In IDEs like VS Code, instructions files are combined and ordering isn’t guaranteed; they mainly influence **create/modify** operations (and **not** inline completions). ([Visual Studio Code][3])

### On-demand workflows (you explicitly invoke)

* **Prompt files**: run via `/your-prompt` in chat; they’re reusable templates with YAML frontmatter (agent/tools/model/etc.). ([Visual Studio Code][4])
  *Note:* prompt files are in public preview and currently limited to certain IDEs (VS Code / Visual Studio / JetBrains). ([GitHub Docs][5])

### Persona switching (you pick an agent)

* **Custom agents**: `.github/agents/*.agent.md` lets you define a “Testing Specialist”, “Security Reviewer”, etc., including tool access and whether it can be auto-selected (`infer`). ([GitHub Docs][6])

### Auto-loaded playbooks (Copilot decides)

* **Agent Skills**: folders under `.github/skills/<name>/SKILL.md` (or `.claude/skills` too) that Copilot injects when relevant to your prompt. ([GitHub Docs][1])

---

## 2) Recommended Python repo layout (copy this)

```text
.github/
  copilot-instructions.md
  instructions/
    python.instructions.md
    tests.instructions.md
    docs.instructions.md
  prompts/
    add-feature.prompt.md
    write-tests.prompt.md
    triage-ci.prompt.md
  agents/
    test-specialist.agent.md
    security-reviewer.agent.md
  skills/
    pytest-failure-debugging/
      SKILL.md
      notes.md
      scripts/
        reproduce.sh
```

---

## 3) Repo-wide instructions: `.github/copilot-instructions.md`

Use this for **project facts + conventions** you want applied to almost everything (commands, structure, style, “how we do things here”). ([GitHub Docs][2])

**Example (Python package using `src/` layout + pytest):**

```md
# Copilot instructions for this repository (Python)

## Project layout
- Source code lives in `src/<package_name>/`
- Tests live in `tests/`
- Prefer small, focused modules; avoid circular imports.

## Tooling & commands (use these defaults)
- Run tests: `pytest -q`
- Lint/format (if present): `ruff check .` and `ruff format .`
- Type check (if present): `mypy src`

## Coding standards
- Prefer type hints on public functions.
- Write docstrings for public modules/classes/functions.
- Raise specific exceptions; avoid bare `except:`.
- Keep functions cohesive; avoid “god” classes.

## When making changes
- Update/extend tests for behavior changes.
- Keep changes minimal and consistent with existing patterns.
- If you need config details, look for `pyproject.toml`.
```

---

## 4) Scoped instructions: `.github/instructions/*.instructions.md`

Use these when **different parts of your repo need different rules**. Each file starts with YAML frontmatter containing `applyTo` (glob). ([GitHub Docs][2])

### `python.instructions.md` (applies to all Python files)

```md
---
applyTo: "**/*.py"
---
# Python rules

- Prefer `pathlib.Path` over `os.path`.
- Avoid global state; pass dependencies explicitly.
- Use `logging` (no `print`) for non-test code.
- Add type hints; prefer `typing` stdlib types.
- Keep public APIs stable; don’t rename exported symbols without reason.
```

### `tests.instructions.md` (test-only rules)

```md
---
applyTo: "tests/**/*.py"
---
# Pytest rules

- Use Arrange/Act/Assert structure.
- Prefer `pytest.mark.parametrize` for coverage.
- Prefer fixtures over repeated setup code.
- Tests should be deterministic; avoid network/time dependencies unless explicitly mocked.
```

### `docs.instructions.md` (markdown-only rules)

```md
---
applyTo: "**/*.md"
---
# Documentation rules

- Show runnable examples (copy/paste friendly).
- Prefer short sections + bullets; avoid huge walls of text.
- Mention the exact command(s) to verify changes locally.
```

**Important:** If both repo-wide + path-specific instructions match, Copilot can use **both**; avoid contradictions. ([GitHub Docs][2])

---

## 5) Prompt files: `.github/prompts/*.prompt.md`

Prompt files are **reusable, on-demand** workflows. In VS Code you run them by typing `/prompt-name` in chat. ([Visual Studio Code][4])
They support YAML header fields like `description`, `name`, `argument-hint`, `agent`, `model`, `tools`. ([Visual Studio Code][4])

### A) “Add feature” prompt (scaffold code + tests)

`.github/prompts/add-feature.prompt.md`

```md
---
name: add-feature
description: Add a small feature with tests (Python)
argument-hint: "feature='...' files='...'"
agent: agent
---
You are working in a Python repository.

Goal:
- Implement: ${input:feature:Describe the feature}
- Touch these areas/files (if provided): ${input:files:Optional list of files/modules}

Rules:
- Follow repo conventions in `.github/copilot-instructions.md` and matching `.github/instructions/*.instructions.md`.
- Make the smallest coherent change.
- Add/extend pytest tests in `tests/` to cover the change.
- Provide:
  1) What you changed (bullets)
  2) Why
  3) Commands to verify locally (pytest, lint/typecheck if relevant)
```

### B) “Write tests” prompt (great for existing functions)

`.github/prompts/write-tests.prompt.md`

```md
---
name: write-tests
description: Generate pytest tests for the selected code/file
argument-hint: "focus='edge cases' or 'happy path'"
agent: agent
---
Write pytest tests for: ${file}

Focus: ${input:focus:What should the tests emphasize?}

Constraints:
- Do not change production code unless absolutely required; if required, explain why.
- Prefer parametrization and clear test names.
- Include at least:
  - happy path
  - edge case(s)
  - error handling case
```

### C) “Triage CI” prompt (when GitHub Actions/CI fails)

`.github/prompts/triage-ci.prompt.md`

```md
---
name: triage-ci
description: Diagnose CI/test failures and propose minimal fixes
argument-hint: "paste logs or link failing step"
agent: ask
---
You are diagnosing a CI failure in a Python repo.

Input (logs/error):
${input:logs:Paste the failing output}

Deliver:
1) Likely root cause(s) with confidence
2) Minimal fix options (ordered)
3) What to run locally to confirm
```

---

## 6) Custom agents: `.github/agents/*.agent.md`

Custom agents are **personas you switch to**, with explicit tool access and behavior. You can create them in `.github/agents` and they show up in agent dropdowns / Copilot agent UI depending on platform. ([GitHub Docs][6])
Key frontmatter fields include `description` (required), plus `tools`, `infer`, `target`, and optional `mcp-servers`. ([GitHub Docs][7])

### A) Testing specialist (only cares about tests)

`.github/agents/test-specialist.agent.md`

```md
---
name: test-specialist
description: Improves pytest coverage/quality without changing production code unless requested
tools: ["read", "search", "edit"]
infer: true
---
You are a testing specialist for a Python repo.

Rules:
- Prefer adding tests over changing prod code.
- If prod code must change to enable testability, propose the smallest refactor and explain.
- Use pytest idioms (fixtures, parametrization).
- Keep tests deterministic (no network/time unless mocked).

Output format:
- Summary
- Tests added/changed
- How to run (commands)
```

### B) Security reviewer (read-only posture)

`.github/agents/security-reviewer.agent.md`

```md
---
name: security-reviewer
description: Reviews Python code for common security issues and suggests fixes
tools: ["read", "search"]
infer: false
---
You are a security reviewer.

Focus areas:
- injection risks (shell/sql/template)
- unsafe deserialization
- authz/authn mistakes
- secrets handling
- dependency risks (if visible in config)

Deliver:
- Findings (severity + rationale)
- Concrete remediation suggestions
- Minimal patch guidance (but do not edit files directly)
```

*(Tip: `infer: false` is useful for “special” agents you only want when you explicitly pick them.)* ([GitHub Docs][7])

---

## 7) Agent Skills: `.github/skills/<skill>/SKILL.md`

Skills are **auto-loaded** when Copilot decides your prompt matches the skill’s description. A skill is a folder; the required file is `SKILL.md` with YAML frontmatter (`name`, `description`). ([GitHub Docs][1])

Copilot injects the skill instructions into context when it chooses to use it, and it can also use scripts/resources bundled in the skill directory. ([GitHub Docs][1])

### Example skill: Pytest failure debugging

`.github/skills/pytest-failure-debugging/SKILL.md`

```md
---
name: pytest-failure-debugging
description: Step-by-step playbook to reproduce and fix pytest failures locally and in CI.
---
When asked to debug a failing pytest run, follow this checklist:

1) Reproduce
- Run `pytest -q` (or the command shown in CI logs).
- If it’s order-dependent, retry with `pytest -q --maxfail=1 -x`.

2) Classify the failure
- Assertion mismatch
- Fixture/setup error
- Import/path issue
- Platform-specific behavior
- Flake (timing/randomness)

3) Narrow scope
- Run only failing tests: `pytest -q path/to/test.py::test_name`
- Use `-k` to filter, and `-vv` for detail.

4) Typical fixes
- Stabilize time/randomness via dependency injection/mocking
- Fix fixture scope misuse
- Ensure package import paths match `src/` layout
- Remove reliance on test execution order

5) Output
- Root cause summary
- Minimal patch suggestion
- Verification commands
```

Optional extra resources in the same folder (ex: `scripts/reproduce.sh`, notes, known CI quirks) become available to the agent when the skill is loaded.

**Compatibility note:** GitHub explicitly supports skills in `.github/skills`, and also recognizes `.claude/skills` (handy if you already have Claude Code skills). ([GitHub Docs][1])

---

## 8) A simple “best practice” layering that works

1. Put **global repo truths** in `copilot-instructions.md` (structure, commands, standards). ([GitHub Docs][2])
2. Put **file-specific rules** in `.github/instructions/` with tight `applyTo` globs. ([GitHub Docs][2])
3. Put **repeatable workflows** in `.github/prompts/` (add feature, write tests, triage CI). ([Visual Studio Code][4])
4. Put **role/persona behavior** in `.github/agents/` (test specialist, security reviewer). ([GitHub Docs][6])
5. Put **deep playbooks + scripts** in `.github/skills/` (auto-loaded). ([GitHub Docs][1])

---

## Comparison table

| Feature                    | Path / filename                                          | Activated how?                                                                | Scope                  | Best for                                                          | Notes / gotchas                                                                                                                                                                                 |
| -------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repo-wide instructions     | `.github/copilot-instructions.md`                        | Automatically included in repo context                                        | Whole repo             | Always-relevant conventions (structure, commands, coding style)   | Stacks with path-specific instructions. ([GitHub Docs][2])                                                                                                                                      |
| Path-specific instructions | `.github/instructions/*.instructions.md` with `applyTo:` | Automatically when edited file matches glob; can be manually attached in IDEs | Specific files/folders | Different rules for `src/`, `tests/`, `docs/`                     | Avoid contradictions; conflicts can behave non-deterministically; IDEs may combine in no guaranteed order. ([GitHub Docs][2])                                                                   |
| Prompt files               | `.github/prompts/*.prompt.md`                            | You run it (e.g., `/write-tests`)                                             | Task-specific          | Repeatable workflows (scaffold feature, write tests, review code) | Frontmatter supports `agent/tools/model`; currently preview + IDE-limited. ([Visual Studio Code][4])                                                                                            |
| Custom agents              | `.github/agents/*.agent.md`                              | You select agent; can also be auto-used if `infer:true`                       | Persona-level          | “Testing specialist”, “Security reviewer”, “Planner”              | Configurable tools (`tools`), auto-selection (`infer`), target env (`target`). Some VS Code-only fields may be ignored on GitHub.com. ([GitHub Docs][7])                                        |
| Agent Skills               | `.github/skills/<skill>/SKILL.md`                        | Copilot auto-loads when skill description matches your request                | Skill folder           | Deep playbooks + scripts/resources for specialized tasks          | `SKILL.md` required; injected when used; `.claude/skills` also supported; works across Copilot coding agent/CLI/VS Code Insiders (stable support coming soon per changelog). ([GitHub Docs][1]) |

If you tell me your current Python stack (FastAPI/Django/CLI/lib, pytest/unittest, ruff/black/mypy, src/ layout or not), I can tailor the exact file contents (especially the `applyTo` globs and the prompts) to match your repo.

[1]: https://docs.github.com/copilot/concepts/agents/about-agent-skills "About Agent Skills - GitHub Docs"
[2]: https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot "Adding repository custom instructions for GitHub Copilot - GitHub Docs"
[3]: https://code.visualstudio.com/docs/copilot/customization/custom-instructions "Use custom instructions in VS Code"
[4]: https://code.visualstudio.com/docs/copilot/customization/prompt-files "Use prompt files in VS Code"
[5]: https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/your-first-prompt-file "Your first prompt file - GitHub Docs"
[6]: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents "Creating custom agents - GitHub Docs"
[7]: https://docs.github.com/en/copilot/reference/custom-agents-configuration "Custom agents configuration - GitHub Docs"
