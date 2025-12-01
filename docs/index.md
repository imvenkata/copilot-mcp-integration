# Copilot MCP Documentation Hub

Use this as the landing page for a Zensical/MkDocs-style site. Jump to quick references, workflows, and setup notes for GitLab and Confluence MCP usage.

## Quick start
1. Read the safety and scoping notes in `docs/copilot-mcp-notes.md`.
2. Skim the cheat sheet in `docs/quick-reference.md` for commands, env vars, and config snippets.
3. Follow the detailed flows in `docs/workflow/example-workflows.md` when you need step-by-step guidance.

## Content map
- Overview and safety: `docs/copilot-mcp-notes.md`
- Cheat sheet: `docs/quick-reference.md`
- Workflows: `docs/workflow/example-workflows.md`

## Suggested navigation (Zensical/MkDocs)
```yaml
nav:
  - Home: index.md
  - Overview & Safety: copilot-mcp-notes.md
  - Quick Reference: quick-reference.md
  - Workflows:
      - Example Workflows: workflow/example-workflows.md
```

## Notes for Zensical
- Keep files in `docs/` as the content root; the suggested nav above can be adapted to Zensical’s config format.
- Preserve relative links between docs (`quick-reference.md` ↔ `workflow/example-workflows.md`).
- Add a theme or styling via your Zensical config; content is Markdown-only. 
