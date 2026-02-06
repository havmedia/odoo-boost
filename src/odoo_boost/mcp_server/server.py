"""FastMCP server definition – registers all 15 Odoo tools."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from odoo_boost.config.schema import OdooBoostConfig
from odoo_boost.connection.factory import create_connection
from odoo_boost.mcp_server.context import ServerContext, set_context

# Tool implementations
from odoo_boost.mcp_server.tools.application_info import application_info
from odoo_boost.mcp_server.tools.database_schema import database_schema
from odoo_boost.mcp_server.tools.database_query import database_query
from odoo_boost.mcp_server.tools.list_models import list_models
from odoo_boost.mcp_server.tools.list_views import list_views
from odoo_boost.mcp_server.tools.list_menus import list_menus
from odoo_boost.mcp_server.tools.list_routes import list_routes
from odoo_boost.mcp_server.tools.list_access_rights import list_access_rights
from odoo_boost.mcp_server.tools.get_config import get_config
from odoo_boost.mcp_server.tools.get_module_info import get_module_info
from odoo_boost.mcp_server.tools.search_records import search_records
from odoo_boost.mcp_server.tools.execute_method import execute_method
from odoo_boost.mcp_server.tools.read_log_entries import read_log_entries
from odoo_boost.mcp_server.tools.search_docs import search_docs
from odoo_boost.mcp_server.tools.list_workflows import list_workflows


def create_mcp_server(config: OdooBoostConfig) -> FastMCP:
    """Build a FastMCP server wired to a live Odoo connection."""

    # Establish connection
    conn = create_connection(config.connection)
    conn.authenticate()

    set_context(ServerContext(connection=conn, config=config))

    mcp = FastMCP(
        "odoo-boost",
        instructions=(
            "Odoo Boost MCP server – provides deep introspection into a "
            "running Odoo instance. Use these tools to explore models, views, "
            "records, configuration, access rights, and more."
        ),
    )

    # Register all tools with the FastMCP server
    mcp.tool()(application_info)
    mcp.tool()(database_schema)
    mcp.tool()(database_query)
    mcp.tool()(list_models)
    mcp.tool()(list_views)
    mcp.tool()(list_menus)
    mcp.tool()(list_routes)
    mcp.tool()(list_access_rights)
    mcp.tool()(get_config)
    mcp.tool()(get_module_info)
    mcp.tool()(search_records)
    mcp.tool()(execute_method)
    mcp.tool()(read_log_entries)
    mcp.tool()(search_docs)
    mcp.tool()(list_workflows)

    return mcp
