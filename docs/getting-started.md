# Getting Started

This guide walks you through installing Odoo Boost and connecting it to your Odoo instance.

## Prerequisites

- **Python 3.10+** (3.12+ recommended)
- **A running Odoo instance** (17, 18, or 19) accessible via HTTP
- **Admin credentials** (or an API key) for the Odoo instance

## Step 1: Install Odoo Boost

```bash
pip install odoo-boost
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install odoo-boost
```

Or as a global CLI tool (available outside any virtualenv):

```bash
uv tool install odoo-boost
```

Verify the installation:

```bash
odoo-boost --version
# or equivalently:
python -m odoo_boost --version
```

## Step 2: Run the Install Wizard

Navigate to your Odoo project directory and run:

```bash
cd /path/to/your/odoo-project
odoo-boost install
```

The wizard will guide you through:

### Connection Details

```
Step 1: Odoo connection details

  Odoo URL [http://localhost:8069]:
  Database name: mydb
  Username [admin]:
  Password / API key [admin]:
```

### Connection Test

The wizard automatically tests your connection and detects the Odoo version:

```
Step 2: Testing connection…

  Server version: 18.0
  Authenticated as UID: 2
  Detected Odoo version: 18.0
```

### Agent Selection

Choose which AI agents you want to configure:

```
Step 3: Select AI agents to configure

  1. Claude Code (claude_code)
  2. Cursor (cursor)
  3. GitHub Copilot (copilot)
  4. OpenAI Codex (codex)
  5. Gemini CLI (gemini_cli)
  6. Junie (junie)

  Enter agent numbers (comma-separated) or 'all' [all]:
```

Enter specific numbers (e.g. `1,2,3`) or just press Enter for all agents.

### File Generation

The wizard generates all necessary files:

```
Step 4: Generating files…

  Created odoo-boost.json
  Created CLAUDE.md
  Created .mcp.json
  Created .ai/skills/creating_models/SKILL.md
  ...
```

## Step 3: Verify the Connection

```bash
odoo-boost check
```

This reads credentials from `odoo-boost.json` and tests the connection:

```
Checking Odoo connection...

  Server version: 18.0
  Authenticated as UID: 2
  Installed modules: 147

            Connection Summary
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property       ┃ Value                 ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ URL            │ http://localhost:8069 │
│ Database       │ mydb                  │
│ Username       │ admin                 │
│ Server Version │ 18.0                  │
│ Protocol       │ xmlrpc                │
└────────────────┴───────────────────────┘

Connection successful!
```

You can also test with explicit credentials (useful before running `install`):

```bash
odoo-boost check --url http://localhost:8069 --database mydb --username admin --password admin
```

## Step 4: Start Using It

Your AI agent is now configured. How you use it depends on which agent you chose.

### Claude Code

The `.mcp.json` file is auto-detected. Just start Claude Code in your project:

```bash
claude
```

Or manually add the MCP server:

```bash
claude mcp add odoo-boost -- python -m odoo_boost mcp
```

Then try:

```
> Use the list_models tool to show me all models related to "sale"
> What fields does the sale.order model have?
> Search for all confirmed sale orders from the last 30 days
```

### Cursor

Open the project in Cursor. It auto-detects `.cursor/mcp.json` and `.cursor/rules/odoo-boost.mdc`.

### GitHub Copilot (VS Code)

Open the project in VS Code. Copilot reads `.vscode/mcp.json` and `.github/copilot-instructions.md`.

### Other Agents

Each agent has its own configuration files — see [Agent Configuration](agents.md) for details.

## Updating Generated Files

If you change your Odoo connection, add agents, or want to refresh the guidelines:

1. Edit `odoo-boost.json` (or re-run `odoo-boost install`)
2. Run:

```bash
odoo-boost update
```

This regenerates all agent files from your saved config.

## Next Steps

- [MCP Tools Reference](mcp-tools.md) — Learn what each of the 15 tools does
- [Agent Configuration](agents.md) — Details on each agent's file layout
- [Skills](skills.md) — Browse the step-by-step development guides
- [Configuration](configuration.md) — Full config reference
