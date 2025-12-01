# Quick Reference Guide

Fast lookup tables for common GitLab and Confluence MCP operations.

## GitLab Quick Commands

Use the configured GitLab host/group and allowed project IDs; decline cross-project requests. Writes (push, merge, pipeline triggers, wiki/milestone changes) require explicit user approval and enabled feature flags (`USE_PIPELINE`, `USE_GITLAB_WIKI`, `USE_MILESTONE`).

### Code Review

| Task              | Prompt Example                                         |
| ----------------- | ------------------------------------------------------ |
| Review MR         | `@workspace /review-merge-request 42 123`            |
| Get MR diffs      | `Get the diffs for merge request #15`                |
| Create draft note | `Create a draft note on MR #23 about error handling` |
| Publish review    | `Publish all draft notes on MR #23`                  |
| List open MRs     | `List all open merge requests in project 456`        |

### Issues

| Task           | Prompt Example                                                     |
| -------------- | ------------------------------------------------------------------ |
| Create bug     | `@workspace /create-issue "Login fails with OAuth" bug 123 high` |
| Create feature | `@workspace /create-issue "Add 2FA support" feature`             |
| List my issues | `Show me my assigned issues`                                     |
| Update issue   | `Update issue #42 to mark as in-progress`                        |
| Link issues    | `Link issue #42 to issue #38 as 'relates to'`                    |

### Merge Requests

| Task        | Prompt Example                                                             |
| ----------- | -------------------------------------------------------------------------- |
| Create MR   | `@workspace /create-merge-request feature/login main "Fix auth timeout"` |
| Update MR   | `Update MR #15 to add the security label`                                |
| Merge MR    | `Merge merge request #30`                                                |
| Add comment | `Add comment to MR #12 suggesting error handling improvement`            |

Note: MR merges or note publication should only proceed after explicit user confirmation.

### Branches & Files

| Task             | Prompt Example                                              |
| ---------------- | ----------------------------------------------------------- |
| Create branch    | `Create branch feature/oauth from main in project 123`    |
| Compare branches | `Compare main and feature/auth branches`                  |
| Get file         | `Get contents of config/database.yml from staging branch` |
| Push files       | `Push these three files to feature/api branch`            |

### CI/CD (requires `USE_PIPELINE=true`)

| Task             | Prompt Example                            |
| ---------------- | ----------------------------------------- |
| Trigger pipeline | `@workspace /trigger-pipeline main 123` |
| Check status     | `What's the status of pipeline #456?`   |
| Get job logs     | `Get the output of failed job #789`     |
| Retry pipeline   | `Retry pipeline #456`                   |
| Run manual job   | `Run manual job #789`                   |

Note: Pipeline triggers/retries/play actions require explicit approval and an enabled pipeline feature flag.

### Wiki (requires `USE_GITLAB_WIKI=true`)

| Task        | Prompt Example                                      |
| ----------- | --------------------------------------------------- |
| List pages  | `@workspace /manage-wiki list 123`                |
| Get page    | `@workspace /manage-wiki get getting-started`     |
| Create page | `@workspace /manage-wiki create "API Guide" 123`  |
| Update page | `@workspace /manage-wiki update installation 123` |

### Milestones (requires `USE_MILESTONE=true`)

| Task             | Prompt Example                                                                     |
| ---------------- | ---------------------------------------------------------------------------------- |
| List milestones  | `@workspace /manage-milestones list 123`                                         |
| Create milestone | `@workspace /manage-milestones create "Sprint 16" 123 "2024-02-16" "2024-02-29"` |
| Get details      | `@workspace /manage-milestones get 42 123`                                       |
| Track issues     | `Show me issues in milestone Sprint 16`                                          |

## Confluence Quick Commands

### Space Operations

| Task                | Prompt Example                                                         |
| ------------------- | ---------------------------------------------------------------------- |
| List spaces         | `List all Confluence spaces I have access to`                        |
| Get space structure | `Show me the page hierarchy for the Engineering space`               |
| Search pages        | `Search for pages about authentication in the Developer Guide space` |

### Page Operations

| Task               | Prompt Example                                                  |
| ------------------ | --------------------------------------------------------------- |
| Get page           | `Get the Getting Started page from the Developer Guide space` |
| Export as Markdown | `Export the API Reference page as Markdown`                   |
| List children      | `Show me all child pages under API Documentation`             |

### Migration

| Task              | Prompt Example                                                 |
| ----------------- | -------------------------------------------------------------- |
| Migrate space     | `@workspace /migrate-confluence-space ENGINEERING docs/`     |
| Get attachments   | `Download all images from the User Guide space`              |
| Analyze structure | `Analyze the Engineering Wiki space structure for migration` |

## Configuration Snippets

### GitLab - Basic Setup

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "npx",
      "args": ["-y", "@zereight/mcp-gitlab"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "glpat-xxxx",
        "GITLAB_API_URL": "https://gitlab.com/api/v4",
        "GITLAB_ALLOWED_PROJECT_IDS": "12345,67890",
        "GITLAB_GROUP_ID": "my-group",
        "GITLAB_READ_ONLY_MODE": "true"
      }
    }
  }
}
```

### GitLab - OAuth2

```json
{
  "env": {
    "GITLAB_USE_OAUTH": "true",
    "GITLAB_OAUTH_CLIENT_ID": "your_client_id",
    "GITLAB_OAUTH_CLIENT_SECRET": "your_client_secret",
    "GITLAB_OAUTH_REDIRECT_URI": "http://127.0.0.1:8888/callback",
    "GITLAB_API_URL": "https://gitlab.com/api/v4"
  }
}
```

Ensure the redirect URI matches the GitLab application configuration; keep the client secret out of version control.

### GitLab - Read-Only Mode

```json
{
  "env": {
    "GITLAB_PERSONAL_ACCESS_TOKEN": "glpat-xxxx",
    "GITLAB_API_URL": "https://gitlab.com/api/v4",
    "GITLAB_ALLOWED_PROJECT_IDS": "12345,67890",
    "GITLAB_READ_ONLY_MODE": "true"
  }
}
```

### GitLab - Full Features

```json
{
  "env": {
    "GITLAB_PERSONAL_ACCESS_TOKEN": "glpat-xxxx",
    "GITLAB_API_URL": "https://gitlab.com/api/v4",
    "GITLAB_PROJECT_ID": "12345",
    "GITLAB_ALLOWED_PROJECT_IDS": "12345,67890",
    "GITLAB_GROUP_ID": "my-group",
    "USE_PIPELINE": "true",
    "USE_GITLAB_WIKI": "true",
    "USE_MILESTONE": "true"
  }
}
```

### Confluence

```json
{
  "mcpServers": {
    "confluence": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-confluence"],
      "env": {
        "CONFLUENCE_URL": "https://your-domain.atlassian.net",
        "CONFLUENCE_USERNAME": "your-email@domain.com",
        "CONFLUENCE_API_TOKEN": "your_token"
      }
    }
  }
}
```

## Environment Variables

### GitLab

| Variable                         | Required | Default                       | Description                             |
| -------------------------------- | -------- | ----------------------------- | --------------------------------------- |
| `GITLAB_PERSONAL_ACCESS_TOKEN` | Yes*     | -                             | Personal access token (*not with OAuth) |
| `GITLAB_USE_OAUTH`             | No       | `false`                     | Enable OAuth2                           |
| `GITLAB_OAUTH_CLIENT_ID`       | If OAuth | -                             | OAuth client ID                         |
| `GITLAB_OAUTH_CLIENT_SECRET`   | If OAuth | -                             | OAuth client secret                     |
| `GITLAB_API_URL`               | No       | `https://gitlab.com/api/v4` | GitLab API endpoint                     |
| `GITLAB_PROJECT_ID`            | No       | -                             | Default project                         |
| `GITLAB_ALLOWED_PROJECT_IDS`   | No       | -                             | Allowed projects (comma-separated)      |
| `GITLAB_GROUP_ID`              | No       | -                             | Default group/namespace scope           |
| `GITLAB_READ_ONLY_MODE`        | No       | `false`                     | Read-only operations                    |
| `USE_GITLAB_WIKI`              | No       | `false`                     | Enable wiki tools                       |
| `USE_MILESTONE`                | No       | `false`                     | Enable milestone tools                  |
| `USE_PIPELINE`                 | No       | `false`                     | Enable pipeline tools                   |

### Confluence

| Variable                 | Required | Default | Description             |
| ------------------------ | -------- | ------- | ----------------------- |
| `CONFLUENCE_URL`       | Yes      | -       | Confluence instance URL |
| `CONFLUENCE_USERNAME`  | Yes      | -       | Username or email       |
| `CONFLUENCE_API_TOKEN` | Yes      | -       | API token               |

## Common Patterns

### Daily Code Review Workflow

```
1. "List all open MRs assigned to me"
2. "@workspace /review-merge-request 42"
3. "Create draft notes for improvements"
4. "Publish draft notes when ready"
```

### Feature Development Workflow

```
1. "Create branch feature/new-feature from main"
2. [Make changes locally]
3. "Push changes to feature/new-feature" (requires approval)
4. "@workspace /create-merge-request feature/new-feature main 'Add new feature'"
5. "@workspace /trigger-pipeline feature/new-feature" (requires `USE_PIPELINE=true` and approval)
```

### Sprint Planning Workflow

```
1. "@workspace /manage-milestones create 'Sprint 16' 123 '2024-02-16' '2024-02-29'"
2. "List all issues with label 'backlog'"
3. [Assign issues to Sprint 16]
4. "@workspace /manage-milestones get 42 123"
```

### Bug Fix Workflow

```
1. "@workspace /create-issue 'Fix login timeout' bug 123 high"
2. "Create branch bugfix/login-timeout from main"
3. [Fix the bug]
4. "@workspace /create-merge-request bugfix/login-timeout main 'Fix login timeout'" (confirm before posting)
5. "Link MR to issue #42"
```

### Documentation Update Workflow

```
1. "@workspace /manage-wiki list 123"
2. "@workspace /manage-wiki get api-guide 123"
3. "@workspace /manage-wiki update api-guide 123"
4. [Provide new content]
```

## Error Messages & Solutions

| Error                  | Likely Cause                   | Solution                             |
| ---------------------- | ------------------------------ | ------------------------------------ |
| `401 Unauthorized`   | Invalid or expired token       | Regenerate token, update config      |
| `403 Forbidden`      | Insufficient permissions       | Check token scopes, verify user role |
| `404 Not Found`      | Project/MR/Issue doesn't exist | Verify ID/path is correct            |
| `Tool not found`     | Feature not enabled            | Enable feature flag in config        |
| `Connection timeout` | Network issue                  | Check API URL, verify connectivity   |

## Keyboard Shortcuts (in supported editors)

| Action            | Shortcut                 |
| ----------------- | ------------------------ |
| Trigger Copilot   | `Cmd/Ctrl + I`         |
| Accept suggestion | `Tab`                  |
| Show inline chat  | `Cmd/Ctrl + K`         |
| Open chat panel   | `Cmd/Ctrl + Shift + I` |

## Token Scopes

### GitLab Personal Access Token

| Scope                | Access Level | Use Case             |
| -------------------- | ------------ | -------------------- |
| `api`              | Full access  | All operations       |
| `read_api`         | Read-only    | Code review, viewing |
| `read_repository`  | Repo read    | File access only     |
| `write_repository` | Repo write   | Create/update files  |

### Confluence API Token

- Full access to all spaces user can view
- No granular scopes available
- Use dedicated service accounts for production

## Rate Limits

### GitLab

- Authenticated: 2,000 requests/min (GitLab.com)
- Self-hosted: Configurable by admin
- MCP handles retries automatically

### Confluence

- Cloud: 10 requests/sec
- Data Center: Configurable
- Respect rate limits in batch operations

## File Locations

### Configuration Files

| Tool           | Path (macOS)                                 | Path (Windows)                               |
| -------------- | -------------------------------------------- | -------------------------------------------- |
| VS Code        | `~/Library/.../cline_mcp_settings.json`    | `%APPDATA%\...\cline_mcp_settings.json`    |
| Claude Desktop | `~/Library/.../claude_desktop_config.json` | `%APPDATA%\...\claude_desktop_config.json` |
| Cursor         | `.cursor/mcp-settings.json`                | `.cursor\mcp-settings.json`                |
| Windsurf       | `.windsurf/mcp-settings.json`              | `.windsurf\mcp-settings.json`              |

### OAuth Token Storage

- GitLab OAuth token: `~/.gitlab-mcp-token.json`

## Quick Troubleshooting

### Problem: MCP server not loading

**Check:**

1. Configuration file syntax (valid JSON)
2. File path is correct
3. Environment variables set
4. Restart AI assistant

### Problem: Authentication failing

**Check:**

1. Token is valid and not expired
2. Token has required scopes
3. API URL is correct
4. Test token with curl

### Problem: Slow performance

**Solutions:**

1. Set `GITLAB_PROJECT_ID` for default
2. Enable only needed features
3. Use project ID instead of path
4. Check network connectivity

### Problem: Tools not appearing

**Solutions:**

1. Enable feature flags (`USE_PIPELINE`, etc.)
2. Verify token permissions
3. Restart AI assistant
4. Check tool names in docs

## Resources

### Documentation

- [Setup Guide](./setup-guide.md) - Complete setup instructions
- [GitLab Guide](../instructions/gitlab.md) - Full GitLab documentation
- [Confluence Guide](../instructions/confluence.md) - Full Confluence documentation
- [Configuration Examples](../examples/README.md) - Ready-to-use configs

### External Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [@zereight/mcp-gitlab](https://github.com/zereight/gitlab-mcp)
- [GitLab API Docs](https://docs.gitlab.com/ee/api/)
- [Confluence API Docs](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/)

### Support

- Open issue in repository
- Check troubleshooting sections
- Review error messages carefully
- Test with minimal configuration first
