"""MCP tool: read_log_entries – ir.logging entries (if log_db configured)."""

from __future__ import annotations

import json

from odoo_boost.mcp_server.context import get_connection


def read_log_entries(
    level: str = "",
    func: str = "",
    limit: int = 50,
) -> str:
    """Read Odoo log entries from ir.logging (requires log_db to be configured).

    Args:
        level: Filter by log level (e.g. 'WARNING', 'ERROR', 'CRITICAL').
        func: Filter by function name substring.
        limit: Maximum entries to return (default 50).
    """
    conn = get_connection()

    domain: list = []
    if level:
        domain.append(("level", "=", level.upper()))
    if func:
        domain.append(("func", "ilike", func))

    try:
        logs = conn.search_read(
            "ir.logging",
            domain=domain,
            fields=["create_date", "name", "level", "dbname", "func", "path", "line", "message"],
            limit=limit,
            order="create_date desc",
        )
    except Exception as exc:
        return json.dumps({
            "error": f"Cannot read ir.logging: {exc}. "
            "Ensure log_db is configured in odoo.conf.",
        })

    result = {
        "total": len(logs),
        "entries": [
            {
                "timestamp": l.get("create_date", ""),
                "level": l.get("level", ""),
                "name": l.get("name", ""),
                "function": l.get("func", ""),
                "path": l.get("path", ""),
                "line": l.get("line", ""),
                "message": l.get("message", ""),
            }
            for l in logs
        ],
    }
    return json.dumps(result, indent=2, default=str)
