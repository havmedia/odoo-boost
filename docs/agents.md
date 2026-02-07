# Agent Configuration

Odoo Boost supports 6 AI coding agents. Each agent gets three types of generated files:

1. **Guidelines** — Odoo development best practices in the agent's native format
2. **MCP Config** — Configuration so the agent can call Odoo Boost MCP tools
3. **Skills** — Step-by-step guides for common Odoo development tasks

## Supported Agents

### Claude Code

| File | Path |
|------|------|
| Guidelines | `CLAUDE.md` |
| MCP Config | `.mcp.json` |
| Skills | `.ai/skills/` |

**MCP Config format (`.mcp.json`):**
```json
{
  "mcpServers": {
    "odoo-boost": {
      "command": "/path/to/python",
      "args": ["-m", "odoo_boost", "mcp"]
    }
  }
}
```

> The `command` is set to the full path of the Python interpreter that has Odoo Boost installed. This ensures the MCP server starts in the correct environment regardless of `PATH`.

Claude Code auto-detects both `CLAUDE.md` and `.mcp.json` in the project root. No additional setup needed.

You can also manually add the MCP server:
```bash
claude mcp add odoo-boost -- python -m odoo_boost mcp
```

---

### Cursor

| File | Path |
|------|------|
| Guidelines | `.cursor/rules/odoo-boost.mdc` |
| MCP Config | `.cursor/mcp.json` |
| Skills | `.cursor/skills/` |

**Guidelines format:** Cursor uses `.mdc` files with YAML frontmatter:
```markdown
---
description: Odoo development guidelines from Odoo Boost
globs:
alwaysApply: true
---

# Odoo Development Guidelines
...
```

**MCP Config format (`.cursor/mcp.json`):**
```json
{
  "mcpServers": {
    "odoo-boost": {
      "command": "/path/to/python",
      "args": ["-m", "odoo_boost", "mcp"]
    }
  }
}
```

Cursor auto-detects both files. Open the project in Cursor and the guidelines and tools are immediately available.

---

### GitHub Copilot

| File | Path |
|------|------|
| Guidelines | `.github/copilot-instructions.md` |
| MCP Config | `.vscode/mcp.json` |
| Skills | `.github/skills/` |

**MCP Config format (`.vscode/mcp.json`):**
```json
{
  "servers": {
    "odoo-boost": {
      "command": "/path/to/python",
      "args": ["-m", "odoo_boost", "mcp"]
    }
  }
}
```

Open the project in VS Code with GitHub Copilot. The instructions file and MCP config are auto-detected.

---

### OpenAI Codex

| File | Path |
|------|------|
| Guidelines | `AGENTS.md` |
| MCP Config | `.codex/config.toml` |
| Skills | `.agents/skills/` |

**MCP Config format (`.codex/config.toml`):**
```toml
# Odoo Boost MCP configuration for Codex
[mcp_servers.odoo-boost]
command = "/path/to/python"
args = ["-m", "odoo_boost", "mcp"]
```

Codex reads `AGENTS.md` automatically and connects to MCP servers defined in `.codex/config.toml`.

---

### Gemini CLI

| File | Path |
|------|------|
| Guidelines | `GEMINI.md` |
| MCP Config | `.gemini/settings.json` |
| Skills | `.agents/skills/` |

**MCP Config format (`.gemini/settings.json`):**
```json
{
  "mcpServers": {
    "odoo-boost": {
      "command": "/path/to/python",
      "args": ["-m", "odoo_boost", "mcp"]
    }
  }
}
```

Gemini CLI reads `GEMINI.md` and `.gemini/settings.json` from the project root.

> **Note:** Gemini CLI and Codex share the `.agents/skills/` directory to avoid duplication.

---

### Junie

| File | Path |
|------|------|
| Guidelines | `.junie/guidelines.md` |
| MCP Config | `.junie/mcp/mcp.json` |
| Skills | `.junie/skills/` |

**MCP Config format (`.junie/mcp/mcp.json`):**
```json
{
  "mcpServers": {
    "odoo-boost": {
      "command": "/path/to/python",
      "args": ["-m", "odoo_boost", "mcp"]
    }
  }
}
```

---

## Selecting Agents

### During Install

The `odoo-boost install` wizard lets you pick agents interactively:

```
Enter agent numbers (comma-separated) or 'all' [all]: 1,2,3
```

### In Config

You can also edit `odoo-boost.json` directly:

```json
{
  "agents": ["claude_code", "cursor", "copilot"]
}
```

Valid agent IDs: `claude_code`, `cursor`, `copilot`, `codex`, `gemini_cli`, `junie`

Then run `odoo-boost update` to regenerate files.

## Adding / Removing Agents

1. Edit the `agents` list in `odoo-boost.json`
2. Run `odoo-boost update`

Files for removed agents are **not** automatically deleted. To clean up, remove them manually or use `odoo-boost install` to start fresh.

## How the MCP Server Starts

When your AI agent uses an MCP tool, it runs `python -m odoo_boost mcp` as a subprocess (using the full path to the Python interpreter). This:

1. Reads `odoo-boost.json` from the current directory (or walks up to find it)
2. Connects to Odoo via XML-RPC
3. Authenticates
4. Starts the MCP server on stdio

The agent communicates with the MCP server via stdin/stdout using the [MCP protocol](https://modelcontextprotocol.io/).

### Why full Python paths?

The generated MCP configs embed the absolute path to the Python interpreter (e.g. `/home/user/.venv/bin/python`) instead of a bare `odoo-boost` command. This is because AI agents typically spawn MCP servers as subprocesses without inheriting your shell's `PATH` or virtualenv activation. Using the full path guarantees the correct Python environment is used every time.

If you move or recreate your virtualenv, run `odoo-boost update` to regenerate the MCP configs with the new path.
