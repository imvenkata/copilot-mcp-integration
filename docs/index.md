# Copilot MCP Documentation Hub

Use this as the landing page for a Zensical/MkDocs-style site. Jump to quick references, workflows, and setup notes for GitLab and Confluence MCP usage.

## Jump links
- [Quick start](#quick-start)
- [Setup Copilot MCP](#setup-copilot-mcp)
- [Editor setup](#editor-setup)
- [Content map](#content-map)
- [Suggested navigation](#suggested-navigation-zensicalmkdocs)

## Quick start
1. Read the safety and scoping notes in [`docs/copilot-mcp-notes.md`](copilot-mcp-notes.md).
2. Skim the cheat sheet in [`docs/quick-reference.md`](quick-reference.md) for commands, env vars, and config snippets.
3. Follow the detailed flows in [`docs/workflow/example-workflows.md`](workflow/example-workflows.md) when you need step-by-step guidance.

## Setup Copilot MCP
- Enable Copilot with MCP support in your editor.
- Configure GitLab/Confluence MCP servers and tokens using the snippets in [`docs/quick-reference.md`](quick-reference.md).
- Place MCP settings in the appropriate config file for your editor (see file-path table in `docs/quick-reference.md` under “File Locations”).
- Keep secrets out of the repo; use env vars or your editor’s secure storage.

## Editor setup
- VS Code (Copilot Chat + MCP): see [`docs/editor-setup.md`](editor-setup.md) for paths and MCP server examples.
- Other editors (Cursor/Windsurf/etc.): follow their MCP config paths using the same snippets in the quick reference.

## Content map
- Overview and safety: [`docs/copilot-mcp-notes.md`](copilot-mcp-notes.md)
- Cheat sheet: [`docs/quick-reference.md`](quick-reference.md)
- Workflows: [`docs/workflow/example-workflows.md`](workflow/example-workflows.md)
- Editor setup: [`docs/editor-setup.md`](editor-setup.md)

## Suggested navigation (Zensical/MkDocs)
```yaml
nav:
  - Home: index.md
  - Overview & Safety: copilot-mcp-notes.md
  - Quick Reference: quick-reference.md
  - Workflows:
      - Example Workflows: workflow/example-workflows.md
  - Editor Setup: editor-setup.md
```
