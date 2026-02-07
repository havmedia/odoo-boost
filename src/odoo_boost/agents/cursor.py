"""Cursor agent – generates .cursor/rules/odoo-boost.mdc + .cursor/mcp.json."""

from __future__ import annotations

import json
from pathlib import Path

from odoo_boost.agents.base import Agent
from odoo_boost.guidelines.composer import compose_guidelines


class CursorAgent(Agent):
    id = "cursor"
    display_name = "Cursor"

    @property
    def guidelines_path(self) -> Path:
        return self.project_path / ".cursor" / "rules" / "odoo-boost.mdc"

    @property
    def mcp_config_path(self) -> Path:
        return self.project_path / ".cursor" / "mcp.json"

    @property
    def skills_dir(self) -> Path:
        return self.project_path / ".cursor" / "skills"

    def _write_guidelines(self) -> Path:
        """Cursor uses .mdc format with YAML frontmatter."""
        content = compose_guidelines(self.config.odoo_version)
        mdc = (
            "---\n"
            "description: Odoo development guidelines from Odoo Boost\n"
            "globs:\n"
            "alwaysApply: true\n"
            "---\n\n" + content
        )
        self.guidelines_path.parent.mkdir(parents=True, exist_ok=True)
        self.guidelines_path.write_text(mdc, encoding="utf-8")
        return self.guidelines_path

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
