# Copilot MCP Integration (Deep Architecture)

This repository uses the **Context-Aware** architecture for GitHub Copilot. It automatically switches context between GitLab coding and Confluence documentation tasks.

## 📂 Structure
* **Global Rules:** `.github/copilot-instructions.md` (always active)
* **GitLab Context:** `.github/instructions/gitlab_api.instructions.md` (auto-applies on `*.py`, `*.yml`, CI files)
* **Confluence Context:** `.github/instructions/confluence_docs.instructions.md` (auto-applies on `docs/*.md`)
* **Actions (Prompts):** `.github/prompts/*.prompt.md` (available via context menu)

## 🚀 Quick Start
1. **Environment:** `cp .env.example .env` and fill in your tokens.
2. **Install:** Open in VS Code and click **"Reopen in Container"** (recommended) or run `pip install -r requirements.txt`.
3. **Check prompts:** Browse available actions in `.github/prompts/*.prompt.md` or see `docs/quick-reference.md` for usage examples.

## 🤖 How to use Actions
In Copilot Chat, click the **Attach Context (+)** button or type `#` to select a prompt:
* `#create-issue` — draft a GitLab issue with labels/milestone.
* `#create-merge-request` — scaffold an MR description.
* `#review-merge-request` — run a structured MR review.
* `#trigger-pipeline` or `#manage-milestones` — CI/CD and milestone helpers.
* `#migrate-confluence-space` — migrate Confluence content to markdown.
* `#query-issues`, `#prepare-release-notes`, `#implement-issue` — additional workflows.
