import os

# ---------------------------------------------------------
# DEFINING THE FILE CONTENT
# ---------------------------------------------------------
files = {
    # ---------------------------------------------------------
    # 1. CONFIGURATION & ENVIRONMENT
    # ---------------------------------------------------------
    "README.md": """# Copilot MCP Integration (Deep Architecture)

This repository uses the **Context-Aware** architecture for GitHub Copilot. It automatically switches context between GitLab coding and Confluence documentation tasks.

## 📂 Structure
* **Global Rules:** `.github/copilot-instructions.md` (Always Active)
* **GitLab Context:** `.github/instructions/gitlab_api.instructions.md` (Active on `*.py`, `*.yml`)
* **Confluence Context:** `.github/instructions/confluence_docs.instructions.md` (Active on `docs/*.md`)
* **Actions (Prompts):** `.github/prompts/*.prompt.md` (Available via Context Menu)

## 🚀 Quick Start
1. **Environment:** `cp .env.example .env` and fill in your tokens.
2. **Install:** Open in VS Code and click **"Reopen in Container"** (Recommended) or install `requirements.txt`.
3. **Validate:** Run `python scripts/validate_mcp_config.py`.

## 🤖 How to use Actions
In Copilot Chat, click the **Attach Context (+)** button or type `#` to select a prompt:
* Select `#create-mr` to draft a Merge Request.
* Select `#migrate-page` to fetch Wiki content.
* Select `#debug-connection` to test tools.
""",

    ".env.example": """# GITLAB
GITLAB_API_URL=https://gitlab.com
GITLAB_ACCESS_TOKEN=glpat-xxxxxxxxxxxxxxxxx

# CONFLUENCE
CONFLUENCE_URL=https://your-domain.atlassian.net/wiki
CONFLUENCE_USERNAME=your.email@company.com
CONFLUENCE_API_TOKEN=ATATT3xxxxxxxxxxxxxxxxx
""",

    ".vscode/settings.json": """{
    "github.copilot.chat.search.codeReferencing": true,
    "github.copilot.advanced.useProjectContext": true,
    
    // ENABLE PROMPT FILES (The new standard)
    "chat.promptFiles": true,

    // Syntax Highlighting for Instructions
    "files.associations": {
        "*.instructions.md": "markdown",
        "*.prompt.md": "markdown"
    }
}""",

    ".devcontainer/devcontainer.json": """{
  "name": "Copilot MCP Workspace",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/git:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "github.copilot",
        "github.copilot-chat",
        "ms-python.python"
      ],
      "settings": {
        "chat.promptFiles": true
      }
    }
  },
  "postCreateCommand": "pip install -r requirements.txt && echo '✅ Ready. Configure your .env file now.'"
}""",

    "requirements.txt": """mcp
python-dotenv
requests
python-gitlab
atlassian-python-api
""",

    # ---------------------------------------------------------
    # 2. GLOBAL LAYER (Always Active)
    # ---------------------------------------------------------
    ".github/copilot-instructions.md": """# Global Operational Protocols

You are an AI Assistant integrated with GitLab and Confluence MCP servers.

## 🛡️ Critical Security Rules (ALWAYS ACTIVE)
1.  **No Token Leaks:** Never output raw `GITLAB_ACCESS_TOKEN` or `CONFLUENCE_API_TOKEN` values.
2.  **Destructive Actions:** If a user asks to delete a branch, drop a database, or overwrite a wiki page, **ask for explicit confirmation** first.
3.  **Tool Availability:** * If the user asks for GitLab data, verify the `python-gitlab` tool is reachable.
    * If the user asks for Confluence data, verify the Atlassian tool is reachable.

## 🧠 How to use this repo
* If I am editing a **Python file**, assume I am working on MCP Tooling or GitLab Automation.
* If I am editing a **Markdown file** in `docs/`, assume I am migrating content from Confluence.
""",

    # ---------------------------------------------------------
    # 3. CONTEXT LAYER (Auto-loaded based on file type)
    # ---------------------------------------------------------
    
    # GITLAB CONTEXT: Applies to Python and CI/CD files
    ".github/instructions/gitlab_api.instructions.md": """---
applyTo: "**/*.py,**/.gitlab-ci.yml,**/scripts/*"
---

# GitLab Development Context

You are assisting with GitLab Automation logic. The user is likely writing a script or configuring a pipeline.

## 1. Python-GitLab Patterns
When writing scripts using `python-gitlab`:
* Always authenticate using `os.getenv('GITLAB_ACCESS_TOKEN')`.
* **Pagination:** Always assume lists (projects, issues) are paginated. Use `iterator=True` or `all=True` to prevent partial data bugs.

## 2. MCP Tool Schemas
When the user asks to "Call the GitLab Tool" (via Chat), use these JSON structures:

### Issue Creation
```json
{
  "title": "str",
  "description": "markdown",
  "labels": "comma,separated",
  "confidential": false
}
```
""",

    # CONFLUENCE CONTEXT: Applies to documentation files
    ".github/instructions/confluence_docs.instructions.md": """---
applyTo: "docs/**/*.md"
---

# Confluence Documentation Context

You are assisting with migrating or creating documentation from Confluence.

## 1. Content Migration Patterns
When fetching content from Confluence:
* Use the Confluence MCP tool to retrieve page content.
* Preserve markdown formatting when converting from Confluence's storage format.
* Maintain page hierarchy and links when possible.

## 2. Documentation Structure
* Store migrated pages in `docs/` directory.
* Use descriptive filenames matching the Confluence page titles.
* Include metadata (original URL, last updated) in frontmatter if needed.
""",

    # ---------------------------------------------------------
    # 4. PROMPT FILES (Actions available via Context Menu)
    # ---------------------------------------------------------
    
    ".github/prompts/create-mr.prompt.md": """# Create Merge Request

Help me create a GitLab Merge Request for the current branch.

Steps:
1. Identify the current branch name.
2. Check for uncommitted changes.
3. Draft a merge request description with:
   - What changed
   - Why it changed
   - Testing notes
4. Use the GitLab MCP tool to create the MR.
""",

    ".github/prompts/migrate-page.prompt.md": """# Migrate Confluence Page

Help me fetch and migrate a Confluence wiki page to markdown.

Steps:
1. Ask for the Confluence page URL or page ID.
2. Use the Confluence MCP tool to fetch the page content.
3. Convert to markdown format.
4. Save to `docs/` directory with appropriate filename.
5. Preserve formatting, links, and structure.
""",

    ".github/prompts/debug-connection.prompt.md": """# Debug MCP Connection

Help me test the MCP server connections.

Steps:
1. Check if `.env` file exists and has required variables.
2. Test GitLab connection by listing a project.
3. Test Confluence connection by fetching a test page.
4. Report any errors or missing configuration.
"""
}

# ---------------------------------------------------------
# FILE CREATION LOGIC
# ---------------------------------------------------------

def create_files():
    """Create all files defined in the files dictionary."""
    for file_path, content in files.items():
        # Create directory if it doesn't exist
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ Created directory: {dir_path}")
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created file: {file_path}")

if __name__ == "__main__":
    print("🚀 Setting up Deep Architecture for Copilot MCP Integration...\n")
    create_files()
    print("\n✨ Setup complete! Configure your .env file and start using Copilot.")