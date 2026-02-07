"""Junie agent – generates .junie/guidelines.md + .junie/mcp/mcp.json."""

from __future__ import annotations

import json
from pathlib import Path

from odoo_boost.agents.base import Agent


class JunieAgent(Agent):
    id = "junie"
    display_name = "Junie"

    @property
    def guidelines_path(self) -> Path:
        return self.project_path / ".junie" / "guidelines.md"

    @property
    def mcp_config_path(self) -> Path:
        return self.project_path / ".junie" / "mcp" / "mcp.json"

    @property
    def skills_dir(self) -> Path:
        return self.project_path / ".junie" / "skills"

    def _mcp_config_content(self) -> str:
        cmd = self._mcp_command()
        return (
            json.dumps(
                {
                    "mcpServers": {
                        "odoo-boost": {
                            "command": cmd[0],
                            "args": cmd[1:],
                        }
                    }
                },
                indent=2,
            )
            + "\n"
        )
