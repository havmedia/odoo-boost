"""Shared server context holding the Odoo connection and config."""

from __future__ import annotations

from dataclasses import dataclass

from odoo_boost.config.schema import OdooBoostConfig
from odoo_boost.connection.base import OdooConnection


@dataclass
class ServerContext:
    """Holds connection + config for MCP tool handlers."""

    connection: OdooConnection
    config: OdooBoostConfig


# Module-level singleton set at server start.
_ctx: ServerContext | None = None


def set_context(ctx: ServerContext) -> None:
    global _ctx
    _ctx = ctx


def get_context() -> ServerContext:
    if _ctx is None:
        raise RuntimeError("Server context not initialised.")
    return _ctx


def get_connection() -> OdooConnection:
    return get_context().connection
