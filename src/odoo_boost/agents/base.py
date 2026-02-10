"""Abstract Agent base class."""

from __future__ import annotations

import shutil
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from odoo_boost.config.schema import OdooBoostConfig
from odoo_boost.guidelines.composer import compose_guidelines
from odoo_boost.skills.loader import install_skills


class Agent(ABC):
    """Base class for AI coding agent integrations.

    Each subclass knows how to generate:
    1. Guidelines file (markdown with dev instructions)
    2. MCP config file (so the agent can use odoo-boost MCP tools)
    3. Skills directory (step-by-step guides for common tasks)
    """

    id: str  # e.g. "claude_code"
    display_name: str  # e.g. "Claude Code"

    def __init__(self, config: OdooBoostConfig, project_path: Path) -> None:
        self.config = config
        self.project_path = project_path

    # -- public API ----------------------------------------------------------

    def install(self) -> list[Path]:
        """Generate all files for this agent. Returns paths created."""
        created: list[Path] = []
        if self.config.generate_ai_files:
            created.append(self._write_guidelines())
            created.extend(self._write_skills())
        if self.config.generate_mcp:
            created.append(self._write_mcp_config())
        return created

    def uninstall(self) -> None:
        """Remove generated files (best-effort)."""
        for path in [self.guidelines_path, self.mcp_config_path]:
            if path.is_file():
                path.unlink()
        if self.skills_dir.is_dir():
            shutil.rmtree(self.skills_dir)

    # -- abstract properties each agent must define --------------------------

    @property
    @abstractmethod
    def guidelines_path(self) -> Path:
        """Absolute path to the generated guidelines file."""

    @property
    @abstractmethod
    def mcp_config_path(self) -> Path:
        """Absolute path to the generated MCP config file."""

    @property
    @abstractmethod
    def skills_dir(self) -> Path:
        """Absolute path to the skills directory."""

    @abstractmethod
    def _mcp_config_content(self) -> str:
        """Return the MCP configuration file content as a string."""

    # -- helpers -------------------------------------------------------------

    def _mcp_command(self) -> list[str]:
        """Return the command to start the MCP server.

        Uses the full path to the current Python interpreter so the MCP
        server starts in the correct environment regardless of ``PATH``.
        """
        return [sys.executable, "-m", "odoo_boost", "mcp"]

    def _write_guidelines(self) -> Path:
        """Compose and write the guidelines file."""
        content = compose_guidelines(self.config.odoo_version)
        self.guidelines_path.parent.mkdir(parents=True, exist_ok=True)
        self.guidelines_path.write_text(content, encoding="utf-8")
        return self.guidelines_path

    def _write_mcp_config(self) -> Path:
        """Write the MCP config file."""
        self.mcp_config_path.parent.mkdir(parents=True, exist_ok=True)
        self.mcp_config_path.write_text(self._mcp_config_content(), encoding="utf-8")
        return self.mcp_config_path

    def _write_skills(self) -> list[Path]:
        """Install skill files into the skills directory."""
        return install_skills(self.skills_dir)
