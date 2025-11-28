---
name: "prepare-release-notes"
description: "Compile GitLab release notes from milestones/tags with MCP tooling."
---

# Prepare Release Notes

Use MCP GitLab tools to gather MRs/issues for a milestone or tag. Keep actions read-only unless the user authorizes publishing.

## Required
- Project ID/path
- Release scope: milestone, tag(s), or commit range
- Audience (internal/external) and format (Markdown, changelog section)

## Optional
- Highlight categories (features, fixes, breaking changes, security, infrastructure)
- Links for deployment notes, rollback/runbooks, and known issues

## Flow
1. List merged MRs/issues in scope; note missing labels or approvals.
2. Group changes by category and surface risks, migrations, and deployment steps.
3. Provide follow-ups: open tracking issue, create release entry, or tag creation—only after confirmation.

## Output
- Draft release notes with sections (Headline, Highlights, Detailed Changes, Risks/Breaking, Deployment/Validation, Links).
- Checklist of verifications (pipeline status, approvals, artifacts) and MCP parameters for any publish/tag actions.
