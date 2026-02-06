"""Claude Code agent – generates CLAUDE.md + .mcp.json."""

from __future__ import annotations

import json
from pathlib import Path

from odoo_boost.agents.base import Agent


class ClaudeCodeAgent(Agent):
    id = "claude_code"
    display_name = "Claude Code"

    @property
    def guidelines_path(self) -> Path:
        return self.project_path / "CLAUDE.md"

    @property
    def mcp_config_path(self) -> Path:
        return self.project_path / ".mcp.json"

    @property
    def skills_dir(self) -> Path:
        return self.project_path / ".ai" / "skills"

    def _mcp_config_content(self) -> str:
        return json.dumps(
            {
                "mcpServers": {
                    "odoo-boost": {
                        "command": "odoo-boost",
                        "args": ["mcp"],
                    }
                }
            },
            indent=2,
        ) + "\n"
