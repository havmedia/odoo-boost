"""MCP tool: execute_method – call any method on a model (like Tinker)."""

from __future__ import annotations

import json

from odoo_boost.mcp_server.context import get_connection


def execute_method(
    model: str,
    method: str,
    args: str = "[]",
    kwargs: str = "{}",
) -> str:
    """Execute an arbitrary ORM method on an Odoo model.

    This is similar to Laravel's Tinker – it lets you call any public method
    on any model. Use with care.

    Args:
        model: Technical model name, e.g. 'res.partner'.
        method: Method name, e.g. 'name_search', 'default_get', 'fields_get'.
        args: Positional arguments as JSON list, e.g. '[[1, 2, 3]]' for record IDs.
        kwargs: Keyword arguments as JSON object, e.g. '{"fields": ["name"]}'.
    """
    conn = get_connection()

    parsed_args = json.loads(args) if args else []
    parsed_kwargs = json.loads(kwargs) if kwargs else {}

    result = conn.execute(model, method, *parsed_args, **parsed_kwargs)

    return json.dumps({"model": model, "method": method, "result": result}, indent=2, default=str)
