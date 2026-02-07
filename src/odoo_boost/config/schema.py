"""Pydantic models for odoo-boost.json configuration."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class OdooConnection(BaseModel):
    """Odoo server connection settings."""

    url: str = Field(description="Odoo server URL, e.g. http://localhost:8069")
    database: str = Field(description="Database name")
    username: str = Field(default="admin", description="Login username")
    password: str = Field(default="admin", description="Login password or API key")
    protocol: Literal["xmlrpc"] = Field(default="xmlrpc", description="Connection protocol")


class OdooBoostConfig(BaseModel):
    """Root configuration model for odoo-boost.json."""

    connection: OdooConnection
    odoo_version: str | None = Field(
        default=None, description="Detected Odoo version (e.g. '17.0', '18.0', '19.0')"
    )
    agents: list[str] = Field(
        default_factory=list,
        description="Enabled agent identifiers (e.g. ['claude_code', 'cursor'])",
    )
    project_path: str = Field(default=".", description="Path to the Odoo project root")
