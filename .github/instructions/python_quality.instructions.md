---
applyTo: "**/*.py"
---

# Python Code Quality & Linting

## Applies when
- Editing Python code or tests.

## Instructions
- Follow existing repo linters/formatters (ruff/flake8/black) and type checkers (mypy/pyright) if present; use existing config files (pyproject/cfg/toml).
- Keep functions focused and typed; add type hints and docstrings for non-trivial functions or public APIs.
- Avoid broad exception handling; prefer explicit errors/logging and handle retries/backoff when calling external services.
- Update or add tests when changing behavior and list how to run them.
- Minimize new dependencies; if adding one, state why and where it’s used.
- Keep secrets out of code—use environment variables for tokens/keys.
