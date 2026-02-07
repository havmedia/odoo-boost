"""Copilot agent – generates .github/copilot-instructions.md + .vscode/mcp.json."""

from __future__ import annotations

import json
from pathlib import Path

from odoo_boost.agents.base import Agent


class CopilotAgent(Agent):
    id = "copilot"
    display_name = "GitHub Copilot"

    @property
    def guidelines_path(self) -> Path:
        return self.project_path / ".github" / "copilot-instructions.md"

    @property
    def mcp_config_path(self) -> Path:
        return self.project_path / ".vscode" / "mcp.json"

    @property
    def skills_dir(self) -> Path:
        return self.project_path / ".github" / "skills"

    def _mcp_config_content(self) -> str:
        cmd = self._mcp_command()
        return (
            json.dumps(
                {
                    "servers": {
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
