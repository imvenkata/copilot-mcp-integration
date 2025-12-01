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

## 📚 Documentation site (Zensical)
We ship a Zensical config (`zensical.toml`) that turns the Markdown in `docs/` into a static site.

### Serve locally
1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install zensical`
3. `zensical serve` then open http://localhost:8000

### Build static site
1. Ensure `zensical` is installed (see above).
2. `zensical build` (output goes to `site/`, which is git-ignored).

Navigation is defined in `zensical.toml` and covers:
- Home (`docs/index.md`)
- Overview & Safety (`docs/copilot-mcp-notes.md`)
- Quick Reference (`docs/quick-reference.md`)
- Workflows (`docs/workflow/example-workflows.md`)

### Publish to GitHub Pages
- CI: `.github/workflows/publish-docs.yml` builds the site on `main` and deploys to GitHub Pages.
- Config: update `site_url` in `zensical.toml` to your Pages URL (e.g., `https://<user>.github.io/copilot-mcp-integration`).
- Enable Pages: in repo settings, set Pages source to “GitHub Actions”.
