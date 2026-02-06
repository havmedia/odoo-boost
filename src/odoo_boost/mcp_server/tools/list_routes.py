"""MCP tool: list_routes – website pages and known controller routes."""

from __future__ import annotations

import json

from odoo_boost.mcp_server.context import get_connection


def list_routes(
    filter_url: str = "",
    limit: int = 100,
) -> str:
    """List website pages and known controller routes.

    Args:
        filter_url: Optional substring filter on URL path.
        limit: Maximum number of routes to return (default 100).
    """
    conn = get_connection()

    routes: list[dict] = []

    # 1. Try website.page (if website module is installed)
    try:
        domain: list = []
        if filter_url:
            domain.append(("url", "ilike", filter_url))

        pages = conn.search_read(
            "website.page",
            domain=domain,
            fields=["name", "url", "is_published", "website_id"],
            limit=limit,
            order="url",
        )
        for p in pages:
            routes.append({
                "type": "page",
                "url": p.get("url", ""),
                "name": p.get("name", ""),
                "published": p.get("is_published", False),
            })
    except Exception:
        pass  # website module not installed

    # 2. Try ir.http routing rules (available on all versions)
    try:
        domain = []
        if filter_url:
            domain.append(("url", "ilike", filter_url))

        url_rewrites = conn.search_read(
            "website.rewrite",
            domain=domain,
            fields=["name", "url_from", "url_to"],
            limit=limit,
        )
        for r in url_rewrites:
            routes.append({
                "type": "rewrite",
                "url": r.get("url_from", ""),
                "target": r.get("url_to", ""),
                "name": r.get("name", ""),
            })
    except Exception:
        pass  # model may not exist

    result = {
        "total": len(routes),
        "routes": routes,
    }
    return json.dumps(result, indent=2, default=str)
