# Contributing to Odoo Boost

## Development Setup

```bash
git clone https://github.com/odoo-boost/odoo-boost.git
cd odoo-boost

# Create a venv with Python 3.13
uv venv --python 3.13

# Install in editable mode
source .venv/bin/activate
uv pip install -e .

# Verify
odoo-boost --version
```

## Project Layout

```
src/odoo_boost/
├── cli/                    # Typer CLI commands
├── config/                 # Pydantic config schema + load/save
├── connection/             # Abstract base + XML-RPC client
├── mcp_server/
│   ├── server.py           # FastMCP server, registers all tools
│   ├── context.py          # Singleton holding connection + config
│   └── tools/              # One file per MCP tool (15 total)
├── agents/                 # One file per agent (6 total) + base class
├── guidelines/
│   ├── composer.py          # Assembles markdown into a single document
│   └── core/               # 9 markdown files + versions/
└── skills/                 # 8 skill directories with SKILL.md + loader
```

## Adding a New MCP Tool

1. **Create the tool file** at `src/odoo_boost/mcp_server/tools/my_tool.py`:

```python
"""MCP tool: my_tool – short description."""

from __future__ import annotations

import json

from odoo_boost.mcp_server.context import get_connection


def my_tool(param1: str, param2: int = 10) -> str:
    """One-line description shown to the AI agent.

    Args:
        param1: Description of param1.
        param2: Description of param2.
    """
    conn = get_connection()

    # Use conn.search_read(), conn.execute(), conn.search_count(), etc.
    records = conn.search_read("ir.model", [], fields=["model", "name"], limit=param2)

    result = {"data": records}
    return json.dumps(result, indent=2, default=str)
```

Key conventions:
- The function name becomes the MCP tool name
- The docstring's first line becomes the tool description
- All parameters must have type annotations
- Always return a JSON string
- Use `get_connection()` from `context.py` to get the Odoo connection
- Use `default=str` in `json.dumps()` to handle datetime and other non-serializable types

2. **Register the tool** in `src/odoo_boost/mcp_server/server.py`:

```python
# Add import
from odoo_boost.mcp_server.tools.my_tool import my_tool

# Add registration (inside create_mcp_server)
mcp.tool()(my_tool)
```

3. **Test it** against a live Odoo instance:

```python
from odoo_boost.mcp_server.tools.my_tool import my_tool
# (after setting up context)
result = my_tool("test", 5)
print(result)
```

## Adding a New Agent

1. **Create the agent file** at `src/odoo_boost/agents/my_agent.py`:

```python
"""My Agent – generates guidelines + MCP config."""

from __future__ import annotations

import json
from pathlib import Path

from odoo_boost.agents.base import Agent


class MyAgent(Agent):
    id = "my_agent"
    display_name = "My Agent"

    @property
    def guidelines_path(self) -> Path:
        return self.project_path / "MY_AGENT.md"

    @property
    def mcp_config_path(self) -> Path:
        return self.project_path / ".my-agent" / "mcp.json"

    @property
    def skills_dir(self) -> Path:
        return self.project_path / ".my-agent" / "skills"

    def _mcp_config_content(self) -> str:
        # Return the MCP config in whatever format your agent expects
        return json.dumps({
            "mcpServers": {
                "odoo-boost": {
                    "command": "odoo-boost",
                    "args": ["mcp"],
                }
            }
        }, indent=2) + "\n"
```

Override `_write_guidelines()` if your agent needs a special format (like Cursor's `.mdc` with frontmatter).

2. **Register the agent** in `src/odoo_boost/agents/__init__.py`:

```python
from odoo_boost.agents.my_agent import MyAgent

AGENTS: dict[str, type[Agent]] = {
    # ... existing agents ...
    "my_agent": MyAgent,
}
```

3. **Test it**:

```python
from pathlib import Path
from odoo_boost.config.schema import OdooBoostConfig, OdooConnection
from odoo_boost.agents.my_agent import MyAgent

config = OdooBoostConfig(
    connection=OdooConnection(url="http://localhost:8069", database="mydb", username="admin", password="admin"),
    odoo_version="18.0",
    agents=["my_agent"],
)

agent = MyAgent(config=config, project_path=Path("/tmp/test"))
created = agent.install()
for p in created:
    print(p)
```

## Adding a New Skill

1. **Create the directory**: `src/odoo_boost/skills/my_skill/`

2. **Write `SKILL.md`** with YAML frontmatter:

```markdown
---
name: My Skill
description: What this skill teaches.
globs: ["relevant/**/*.py"]
---

# My Skill

## Steps

1. **First step** ...
2. **Second step** ...

## Checklist
- [ ] Item one
- [ ] Item two
```

3. **Register the skill** in `src/odoo_boost/skills/loader.py`:

```python
_SKILL_DIRS = [
    # ... existing skills ...
    "my_skill",
]
```

## Adding a Guideline File

1. **Create the markdown file** in `src/odoo_boost/guidelines/core/`:

```markdown
## My Topic

### Key Points
- Point one
- Point two
```

2. **Add it to the composer** in `src/odoo_boost/guidelines/composer.py`:

```python
_CORE_FILES = [
    # ... existing files ...
    "my_topic.md",
]
```

For version-specific files, add to `src/odoo_boost/guidelines/core/versions/`.

## Testing

To test MCP tools against a live Odoo instance:

```bash
source .venv/bin/activate
python3 -c "
from odoo_boost.config.schema import OdooBoostConfig, OdooConnection
from odoo_boost.connection.factory import create_connection
from odoo_boost.mcp_server.context import ServerContext, set_context

conn_cfg = OdooConnection(url='http://localhost:8069', database='mydb', username='admin', password='admin')
config = OdooBoostConfig(connection=conn_cfg, odoo_version='18.0', agents=[])
conn = create_connection(conn_cfg)
conn.authenticate()
set_context(ServerContext(connection=conn, config=config))

# Now test your tool
from odoo_boost.mcp_server.tools.my_tool import my_tool
print(my_tool('test'))
"
```

## Code Style

- Use `from __future__ import annotations` at the top of every module
- Type hints on all public function signatures
- Docstrings on all public functions (used as MCP tool descriptions)
- Return JSON strings from MCP tools (not dicts)
- Use `json.dumps(..., default=str)` to handle non-serializable types
