"""Tests for all 15 MCP tools using MockOdooConnection."""

from __future__ import annotations

import json

import pytest

from odoo_boost.mcp_server.tools.application_info import application_info
from odoo_boost.mcp_server.tools.database_query import database_query
from odoo_boost.mcp_server.tools.database_schema import database_schema
from odoo_boost.mcp_server.tools.execute_method import execute_method
from odoo_boost.mcp_server.tools.get_config import get_config
from odoo_boost.mcp_server.tools.get_module_info import get_module_info
from odoo_boost.mcp_server.tools.list_access_rights import list_access_rights
from odoo_boost.mcp_server.tools.list_menus import list_menus
from odoo_boost.mcp_server.tools.list_models import list_models
from odoo_boost.mcp_server.tools.list_routes import list_routes
from odoo_boost.mcp_server.tools.list_views import list_views
from odoo_boost.mcp_server.tools.list_workflows import list_workflows
from odoo_boost.mcp_server.tools.read_log_entries import read_log_entries
from odoo_boost.mcp_server.tools.search_docs import search_docs
from odoo_boost.mcp_server.tools.search_records import search_records

pytestmark = pytest.mark.usefixtures("server_context")


# ---------------------------------------------------------------------------
# application_info
# ---------------------------------------------------------------------------


class TestApplicationInfo:
    def test_returns_json(self):
        result = json.loads(application_info())
        assert "server_version" in result
        assert result["server_version"] == "18.0"

    def test_installed_modules(self):
        result = json.loads(application_info())
        assert result["installed_modules_count"] == 2  # base + sale (installed)
        names = [m["name"] for m in result["installed_modules"]]
        assert "base" in names
        assert "sale" in names


# ---------------------------------------------------------------------------
# database_schema
# ---------------------------------------------------------------------------


class TestDatabaseSchema:
    def test_known_model(self):
        result = json.loads(database_schema("res.partner"))
        assert result["model"] == "res.partner"
        assert result["field_count"] == 3

    def test_unknown_model(self):
        result = json.loads(database_schema("nonexistent.model"))
        assert "error" in result

    def test_fields_have_type(self):
        result = json.loads(database_schema("res.partner"))
        types = {f["name"]: f["type"] for f in result["fields"]}
        assert types["name"] == "char"
        assert types["company_id"] == "many2one"


# ---------------------------------------------------------------------------
# database_query
# ---------------------------------------------------------------------------


class TestDatabaseQuery:
    def test_basic_query(self):
        result = json.loads(database_query("res.partner"))
        assert result["model"] == "res.partner"
        assert result["total_count"] == 2
        assert result["returned_count"] == 2

    def test_domain_filter(self):
        result = json.loads(database_query("res.partner", domain='[["is_company", "=", true]]'))
        assert result["total_count"] == 1

    def test_fields_filter(self):
        result = json.loads(database_query("res.partner", fields='["name"]'))
        for rec in result["records"]:
            assert "name" in rec

    def test_limit(self):
        result = json.loads(database_query("res.partner", limit=1))
        assert result["returned_count"] == 1


# ---------------------------------------------------------------------------
# list_models
# ---------------------------------------------------------------------------


class TestListModels:
    def test_returns_models(self):
        result = json.loads(list_models())
        assert result["total"] == 2

    def test_filter_by_name(self):
        result = json.loads(list_models(filter_name="partner"))
        assert result["total"] == 1
        assert result["models"][0]["model"] == "res.partner"

    def test_field_count(self):
        result = json.loads(list_models())
        partner = [m for m in result["models"] if m["model"] == "res.partner"][0]
        assert partner["field_count"] == 3


# ---------------------------------------------------------------------------
# list_views
# ---------------------------------------------------------------------------


class TestListViews:
    def test_all_views(self):
        result = json.loads(list_views())
        assert result["total"] == 2

    def test_filter_by_model(self):
        result = json.loads(list_views(model_name="res.partner"))
        assert result["total"] == 2

    def test_filter_by_type(self):
        result = json.loads(list_views(view_type="form"))
        assert result["total"] == 1
        assert result["views"][0]["type"] == "form"


# ---------------------------------------------------------------------------
# list_menus
# ---------------------------------------------------------------------------


class TestListMenus:
    def test_root_menus(self):
        result = json.loads(list_menus(parent_id=0))
        assert result["total"] == 1
        assert result["menus"][0]["name"] == "Sales"

    def test_all_menus(self):
        result = json.loads(list_menus(parent_id=-1))
        assert result["total"] == 2


# ---------------------------------------------------------------------------
# list_routes
# ---------------------------------------------------------------------------


class TestListRoutes:
    def test_returns_result(self):
        # No website.page / website.rewrite seeded, so routes should be empty
        # (the tool catches exceptions silently)
        result = json.loads(list_routes())
        assert "total" in result
        assert "routes" in result


# ---------------------------------------------------------------------------
# list_access_rights
# ---------------------------------------------------------------------------


class TestListAccessRights:
    def test_returns_acls_and_rules(self):
        result = json.loads(list_access_rights())
        assert "access_rights" in result
        assert "record_rules" in result

    def test_has_entries(self):
        result = json.loads(list_access_rights())
        assert len(result["access_rights"]) >= 1
        assert len(result["record_rules"]) >= 1


# ---------------------------------------------------------------------------
# get_config
# ---------------------------------------------------------------------------


class TestGetConfig:
    def test_all_params(self):
        result = json.loads(get_config())
        assert result["total"] == 2

    def test_filter_by_key(self):
        result = json.loads(get_config(key="web.base"))
        assert result["total"] == 1
        assert result["parameters"][0]["key"] == "web.base.url"


# ---------------------------------------------------------------------------
# get_module_info
# ---------------------------------------------------------------------------


class TestGetModuleInfo:
    def test_known_module(self):
        result = json.loads(get_module_info("base"))
        assert result["name"] == "base"
        assert result["state"] == "installed"

    def test_unknown_module(self):
        result = json.loads(get_module_info("nonexistent_mod"))
        assert "error" in result


# ---------------------------------------------------------------------------
# search_records
# ---------------------------------------------------------------------------


class TestSearchRecords:
    def test_basic_search(self):
        result = json.loads(search_records("res.partner"))
        assert result["model"] == "res.partner"
        assert result["total_count"] == 2

    def test_with_domain(self):
        result = json.loads(search_records("res.partner", domain='[["is_company", "=", true]]'))
        assert result["total_count"] == 1


# ---------------------------------------------------------------------------
# execute_method
# ---------------------------------------------------------------------------


class TestExecuteMethod:
    def test_execute(self):
        result = json.loads(execute_method("res.partner", "name_search"))
        assert result["model"] == "res.partner"
        assert result["method"] == "name_search"
        assert "result" in result


# ---------------------------------------------------------------------------
# read_log_entries
# ---------------------------------------------------------------------------


class TestReadLogEntries:
    def test_no_logs(self):
        # ir.logging not seeded, so should return empty or error
        result = json.loads(read_log_entries())
        # Could be {"total": 0, "entries": []} or {"error": ...}
        assert "total" in result or "error" in result


# ---------------------------------------------------------------------------
# search_docs
# ---------------------------------------------------------------------------


class TestSearchDocs:
    def test_list_all_topics(self):
        result = json.loads(search_docs())
        assert "available_topics" in result
        assert len(result["available_topics"]) > 10

    def test_search_orm(self):
        result = json.loads(search_docs(topic="orm"))
        assert "results" in result
        assert any("orm" in r["topic"].lower() for r in result["results"])

    def test_search_with_version(self):
        result = json.loads(search_docs(topic="views", version="17.0"))
        assert "results" in result
        assert any("/17/" in r["url"] for r in result["results"])

    def test_no_match(self):
        result = json.loads(search_docs(topic="xyznonexistent"))
        assert "message" in result
        assert "available_topics" in result


# ---------------------------------------------------------------------------
# list_workflows
# ---------------------------------------------------------------------------


class TestListWorkflows:
    def test_returns_both_types(self):
        result = json.loads(list_workflows())
        assert "automated_actions" in result
        assert "server_actions" in result

    def test_filter_by_model(self):
        result = json.loads(list_workflows(model_name="res.partner"))
        if result["automated_actions"]:
            assert result["automated_actions"][0]["model"] == "res.partner"
