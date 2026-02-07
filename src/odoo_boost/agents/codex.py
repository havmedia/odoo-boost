"""Codex agent – generates AGENTS.md + .codex/config.toml."""

from __future__ import annotations

from pathlib import Path

from odoo_boost.agents.base import Agent


class CodexAgent(Agent):
    id = "codex"
    display_name = "OpenAI Codex"

    @property
    def guidelines_path(self) -> Path:
        return self.project_path / "AGENTS.md"

    @property
    def mcp_config_path(self) -> Path:
        return self.project_path / ".codex" / "config.toml"

    @property
    def skills_dir(self) -> Path:
        return self.project_path / ".agents" / "skills"

    def _mcp_config_content(self) -> str:
        cmd = self._mcp_command()
        args_toml = ", ".join(f'"{a}"' for a in cmd[1:])
        return (
            "# Odoo Boost MCP configuration for Codex\n"
            "[mcp_servers.odoo-boost]\n"
            f'command = "{cmd[0]}"\n'
            f"args = [{args_toml}]\n"
        )
