"""Connection factory."""

from __future__ import annotations

from odoo_boost.config.schema import OdooConnection as OdooConnectionConfig
from odoo_boost.connection.base import OdooConnection
from odoo_boost.connection.xmlrpc import XmlRpcConnection


def create_connection(config: OdooConnectionConfig) -> OdooConnection:
    """Create an Odoo connection from configuration."""
    if config.protocol == "xmlrpc":
        return XmlRpcConnection(
            url=config.url,
            database=config.database,
            username=config.username,
            password=config.password,
        )
    raise ValueError(f"Unsupported protocol: {config.protocol}")
