# Configuration

Odoo Boost stores its configuration in `odoo-boost.json` in your project root. This file is created by `odoo-boost install` and read by all other commands.

## odoo-boost.json Schema

```json
{
  "connection": {
    "url": "http://localhost:8069",
    "database": "mydb",
    "username": "admin",
    "password": "admin",
    "protocol": "xmlrpc"
  },
  "odoo_version": "18.0",
  "agents": ["claude_code", "cursor", "copilot"],
  "project_path": "."
}
```

### `connection` (required)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `url` | string | yes | — | Odoo server URL, e.g. `http://localhost:8069` |
| `database` | string | yes | — | Database name |
| `username` | string | no | `"admin"` | Login username |
| `password` | string | no | `"admin"` | Login password or API key |
| `protocol` | string | no | `"xmlrpc"` | Connection protocol. Currently only `xmlrpc`. |

### `odoo_version` (optional)

Detected Odoo version string (e.g. `"17.0"`, `"18.0"`, `"19.0"`). Auto-detected during `odoo-boost install`. Used to select version-specific guidelines.

### `agents` (optional)

List of enabled agent identifiers. Valid values:

- `"claude_code"` — Claude Code
- `"cursor"` — Cursor
- `"copilot"` — GitHub Copilot
- `"codex"` — OpenAI Codex
- `"gemini_cli"` — Gemini CLI
- `"junie"` — Junie

Default: `[]` (no agents configured).

### `project_path` (optional)

Path to the project root. Default: `"."` (current directory). Used by `odoo-boost update` to determine where to write files.

## Config File Discovery

All commands that need config (`check`, `mcp`, `update`) search for `odoo-boost.json` by walking up the directory tree from the current working directory. This means you can run commands from any subdirectory of your project.

You can also specify an explicit path:

```bash
odoo-boost check --config /path/to/odoo-boost.json
odoo-boost mcp --config /path/to/odoo-boost.json
odoo-boost update --config /path/to/odoo-boost.json
```

## CLI Options

### Global

| Option | Description |
|--------|-------------|
| `--version`, `-v` | Show version and exit |
| `--help` | Show help |

### `odoo-boost check`

| Option | Description |
|--------|-------------|
| `--url` | Odoo server URL (overrides config) |
| `--database` | Database name (overrides config) |
| `--username` | Username (overrides config) |
| `--password` | Password or API key (overrides config) |
| `--config`, `-c` | Explicit path to odoo-boost.json |

When `--url` and `--database` are provided, config file is not needed.

### `odoo-boost mcp`

| Option | Description |
|--------|-------------|
| `--config`, `-c` | Explicit path to odoo-boost.json |

### `odoo-boost update`

| Option | Description |
|--------|-------------|
| `--config`, `-c` | Explicit path to odoo-boost.json |

### `odoo-boost install`

No options — fully interactive.

## Security Notes

`odoo-boost.json` contains your Odoo credentials in plain text. You should:

- Add `odoo-boost.json` to your `.gitignore` to avoid committing credentials
- Use an API key instead of a password when possible (Odoo 14+)
- Use a dedicated Odoo user with minimal permissions for the MCP connection

The `odoo-boost install` wizard does **not** automatically add entries to `.gitignore`. You should do this manually:

```bash
echo "odoo-boost.json" >> .gitignore
```
