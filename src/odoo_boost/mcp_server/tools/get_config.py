"""MCP tool: get_config – ir.config_parameter values."""

from __future__ import annotations

import json

from odoo_boost.mcp_server.context import get_connection


def get_config(
    key: str = "",
    limit: int = 100,
) -> str:
    """Get Odoo system configuration parameters (ir.config_parameter).

    Args:
        key: Exact key or substring filter. Empty returns all.
        limit: Maximum number of parameters to return (default 100).
    """
    conn = get_connection()

    domain: list = []
    if key:
        domain.append(("key", "ilike", key))

    params = conn.search_read(
        "ir.config_parameter",
        domain=domain,
        fields=["key", "value"],
        limit=limit,
        order="key",
    )

    result = {
        "total": len(params),
        "parameters": [{"key": p["key"], "value": p.get("value", "")} for p in params],
    }
    return json.dumps(result, indent=2, default=str)
