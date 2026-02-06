# Odoo Boost

AI coding agents with deep introspection into running Odoo instances via MCP tools.

Inspired by [Laravel Boost](https://github.com/nicepkg/laravel-boost), Odoo Boost gives your AI coding assistant deep knowledge of your Odoo project — models, views, records, access rights, configuration, and more — plus Odoo-specific development guidelines and step-by-step skills.

## Features

- **15 MCP Tools** — Introspect models, views, records, access rights, config, routes, workflows, and more from a live Odoo instance
- **6 AI Agents** — Claude Code, Cursor, Copilot, Codex, Gemini CLI, Junie
- **Odoo Guidelines** — Version-aware development best practices injected into your agent's context
- **8 Skills** — Step-by-step guides for common Odoo development tasks (creating models, views, security, OWL components, etc.)
- **Multi-version** — Supports Odoo 17, 18, and 19
- **Zero config on Odoo side** — Connects via XML-RPC, no Odoo module installation needed

## Installation

```bash
pip install odoo-boost
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install odoo-boost
```

## Quick Start

### 1. Run the install wizard

```bash
cd /path/to/your/odoo-project
odoo-boost install
```

The wizard will:
- Ask for your Odoo connection details (URL, database, username, password)
- Test the connection and detect the Odoo version
- Let you select which AI agents to configure
- Generate all necessary files (guidelines, MCP config, skills)

### 2. Verify the connection

```bash
odoo-boost check
```

Or with explicit credentials:

```bash
odoo-boost check --url http://localhost:8069 --database mydb --username admin --password admin
```

### 3. Start coding

Your AI agent is now configured. The MCP server starts automatically when your agent needs it. Try asking your agent:

> "What models are available in this Odoo instance?"
> "Show me the fields on the res.partner model"
> "Search for all installed modules related to accounting"

## Commands

| Command | Description |
|---------|-------------|
| `odoo-boost install` | Interactive setup wizard |
| `odoo-boost check` | Test connection to Odoo |
| `odoo-boost update` | Re-generate files from saved config |
| `odoo-boost mcp` | Start the MCP server (stdio) |
| `odoo-boost --version` | Show version |

## How It Works

```
┌─────────────────┐     stdio      ┌─────────────────┐    XML-RPC     ┌──────────────┐
│   AI Agent      │◄──────────────►│  Odoo Boost     │◄─────────────►│    Odoo      │
│ (Claude, etc.)  │                │  MCP Server     │               │   Instance   │
└─────────────────┘                └─────────────────┘               └──────────────┘
        │                                  │
        ▼                                  │
  Guidelines +                        15 MCP Tools
  Skills (md)                    (models, views, records,
                                  config, access rights…)
```

Odoo Boost sits between your AI agent and your Odoo instance. It provides:

1. **MCP Tools** — Your agent calls tools like `list_models`, `search_records`, `database_schema` to understand your Odoo instance in real-time
2. **Guidelines** — Odoo development best practices are injected into your agent's context so it writes idiomatic code
3. **Skills** — Step-by-step guides for common tasks (creating models, views, security rules, etc.)

## Documentation

- [Getting Started](docs/getting-started.md) — Full setup walkthrough
- [MCP Tools Reference](docs/mcp-tools.md) — All 15 tools with parameters and examples
- [Agent Configuration](docs/agents.md) — Supported agents and their generated files
- [Configuration](docs/configuration.md) — `odoo-boost.json` schema and CLI options
- [Guidelines](docs/guidelines.md) — Bundled Odoo development guidelines
- [Skills](docs/skills.md) — Step-by-step development skills
- [Contributing](CONTRIBUTING.md) — How to add tools, agents, and skills

## Supported Agents

| Agent | Guidelines | MCP Config | Skills |
|-------|-----------|------------|--------|
| Claude Code | `CLAUDE.md` | `.mcp.json` | `.ai/skills/` |
| Cursor | `.cursor/rules/odoo-boost.mdc` | `.cursor/mcp.json` | `.cursor/skills/` |
| GitHub Copilot | `.github/copilot-instructions.md` | `.vscode/mcp.json` | `.github/skills/` |
| OpenAI Codex | `AGENTS.md` | `.codex/config.toml` | `.agents/skills/` |
| Gemini CLI | `GEMINI.md` | `.gemini/settings.json` | `.agents/skills/` |
| Junie | `.junie/guidelines.md` | `.junie/mcp/mcp.json` | `.junie/skills/` |

## License

MIT
