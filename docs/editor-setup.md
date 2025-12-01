# Editor Setup for Copilot MCP

## VS Code (Copilot Chat + MCP)
1. Enable GitHub Copilot Chat and MCP features.
2. Locate the MCP settings file (examples):
   - macOS: `~/Library/Application Support/Code/User/cline_mcp_settings.json`
   - Windows: `%APPDATA%/Code/User/cline_mcp_settings.json`
   - Linux: `~/.config/Code/User/cline_mcp_settings.json`
   - See the full table in [`docs/quick-reference.md`](quick-reference.md) under “File Locations”.
3. Add MCP servers, for example:
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
           "GITLAB_GROUP_ID": "my-group"
         }
       },
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
4. Restart VS Code; verify MCP tools are available in Copilot Chat.
5. Enable optional features via env vars as needed (`USE_PIPELINE`, `USE_GITLAB_WIKI`, `USE_MILESTONE`).

## Other editors (Cursor, Windsurf, etc.)
- Use the same MCP server snippets from [`docs/quick-reference.md`](quick-reference.md) and place them in the editor’s MCP settings file (see file-path table in the quick reference).
- Keep secrets in env vars or the editor’s secure storage; do not commit tokens. 
