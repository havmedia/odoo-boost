"""MCP tool: search_records – search_read on any model with domain/fields/pagination."""

from __future__ import annotations

import json

from odoo_boost.mcp_server.context import get_connection


def search_records(
    model: str,
    domain: str = "[]",
    fields: str = "[]",
    limit: int = 20,
    offset: int = 0,
    order: str = "",
) -> str:
    """Search and read records from any Odoo model with domain filtering and pagination.

    Args:
        model: Technical model name, e.g. 'res.partner'.
        domain: Odoo domain filter as JSON string, e.g. '[["is_company","=",true]]'.
        fields: JSON list of field names, e.g. '["name","email"]'. Empty for default fields.
        limit: Maximum records to return (default 20).
        offset: Number of records to skip (default 0).
        order: Sort order, e.g. 'name asc, id desc'.
    """
    conn = get_connection()

    parsed_domain = json.loads(domain) if domain else []
    parsed_fields = json.loads(fields) if fields else []

    records = conn.search_read(
        model,
        domain=parsed_domain,
        fields=parsed_fields or None,
        limit=limit,
        offset=offset,
        order=order or None,
    )

    total = conn.search_count(model, domain=parsed_domain)

    result = {
        "model": model,
        "total_count": total,
        "returned_count": len(records),
        "offset": offset,
        "limit": limit,
        "records": records,
    }
    return json.dumps(result, indent=2, default=str)
