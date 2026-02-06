# MCP Tools Reference

Odoo Boost provides 15 MCP tools that give your AI agent deep introspection into a running Odoo instance. All tools connect via XML-RPC and respect Odoo's access rights.

All tools return JSON strings.

---

## application_info

Get Odoo application info: server version, installed modules, database details.

**Parameters:** None

**Returns:**
```json
{
  "server_version": "18.0",
  "server_serie": "18.0",
  "protocol_version": 1,
  "installed_modules_count": 147,
  "installed_modules": [
    { "name": "account", "description": "Invoicing", "version": "18.0.2.0.0" },
    ...
  ]
}
```

**Example prompt:** "What version of Odoo is running and what modules are installed?"

---

## database_schema

Get the field definitions (schema) of an Odoo model.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_name` | str | yes | — | Technical model name, e.g. `res.partner` |

**Returns:**
```json
{
  "model": "res.partner",
  "name": "Contact",
  "field_count": 212,
  "fields": [
    {
      "name": "name",
      "label": "Name",
      "type": "char",
      "relation": null,
      "required": true,
      "readonly": false,
      "stored": true,
      "indexed": true,
      "help": null
    },
    ...
  ]
}
```

**Example prompt:** "Show me the schema of the sale.order model"

---

## database_query

Execute an ORM `search_read` on any Odoo model. Safe — goes through access rights.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | str | yes | — | Technical model name |
| `domain` | str | no | `"[]"` | Odoo domain as JSON string |
| `fields` | str | no | `"[]"` | JSON list of field names. Empty for all |
| `limit` | int | no | `80` | Max records to return |
| `offset` | int | no | `0` | Records to skip |
| `order` | str | no | `""` | Sort order, e.g. `"name asc"` |

**Returns:**
```json
{
  "model": "res.partner",
  "total_count": 523,
  "returned_count": 5,
  "offset": 0,
  "limit": 5,
  "records": [
    { "id": 1, "name": "My Company", "email": "info@example.com" },
    ...
  ]
}
```

**Example prompt:** "Find all partners that are companies, show name and email, limit to 10"

---

## list_models

List available Odoo models with field counts.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter_name` | str | no | `""` | Substring filter on model name |
| `filter_module` | str | no | `""` | Filter by source module name |
| `limit` | int | no | `200` | Max models to return |

**Returns:**
```json
{
  "total": 12,
  "models": [
    { "model": "sale.order", "name": "Sales Order", "field_count": 89 },
    { "model": "sale.order.line", "name": "Sales Order Line", "field_count": 67 },
    ...
  ]
}
```

**Example prompt:** "List all models related to 'sale'"

---

## list_views

List Odoo views (`ir.ui.view`), optionally filtered by model or type. Returns the full XML architecture.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_name` | str | no | `""` | Filter by model name |
| `view_type` | str | no | `""` | Filter by type: `form`, `list`, `kanban`, `search`, etc. |
| `limit` | int | no | `50` | Max views to return |

**Returns:**
```json
{
  "total": 3,
  "views": [
    {
      "id": 123,
      "name": "res.partner.view.form",
      "model": "res.partner",
      "type": "form",
      "priority": 16,
      "inherit_id": null,
      "active": true,
      "arch": "<form>...</form>"
    },
    ...
  ]
}
```

**Example prompt:** "Show me the form views for res.partner"

---

## list_menus

List Odoo menu items (`ir.ui.menu`).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `parent_id` | int | no | `0` | `0` = root menus only, `-1` = all menus, or a specific parent ID |
| `limit` | int | no | `200` | Max menus to return |

**Returns:**
```json
{
  "total": 12,
  "menus": [
    {
      "id": 1,
      "name": "Discuss",
      "complete_name": "Discuss",
      "parent_id": null,
      "action": "ir.actions.client,123",
      "sequence": 1,
      "child_count": 3
    },
    ...
  ]
}
```

**Example prompt:** "Show me the top-level menu structure"

---

## list_routes

List website pages and known controller routes.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `filter_url` | str | no | `""` | Substring filter on URL |
| `limit` | int | no | `100` | Max routes to return |

**Returns:**
```json
{
  "total": 15,
  "routes": [
    { "type": "page", "url": "/about-us", "name": "About Us", "published": true },
    { "type": "rewrite", "url": "/old-page", "target": "/new-page", "name": "Redirect" },
    ...
  ]
}
```

> **Note:** Requires the `website` module to be installed for page listings.

**Example prompt:** "What website pages are published?"

---

## list_access_rights

List access rights (`ir.model.access`) and record rules (`ir.rule`) for a model.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_name` | str | no | `""` | Filter by model name. Empty for all. |
| `limit` | int | no | `100` | Max entries per type |

**Returns:**
```json
{
  "model_filter": "res.partner",
  "access_rights": [
    {
      "name": "res_partner_user",
      "model": "Contact",
      "group": "User",
      "read": true, "write": true, "create": true, "unlink": false
    },
    ...
  ],
  "record_rules": [
    {
      "name": "res_partner_rule",
      "model": "Contact",
      "domain": "['|',('id','child_of',user.commercial_partner_id.id),...]",
      "global": false,
      "read": true, "write": true, "create": true, "unlink": true
    },
    ...
  ]
}
```

**Example prompt:** "What are the access rights and record rules for sale.order?"

---

## get_config

Get Odoo system configuration parameters (`ir.config_parameter`).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `key` | str | no | `""` | Exact key or substring filter. Empty returns all. |
| `limit` | int | no | `100` | Max parameters to return |

**Returns:**
```json
{
  "total": 3,
  "parameters": [
    { "key": "web.base.url", "value": "http://localhost:8069" },
    ...
  ]
}
```

**Example prompt:** "What is the web.base.url configuration?"

---

## get_module_info

Get detailed information about an Odoo module including dependencies and models it defines.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `module_name` | str | yes | — | Technical module name, e.g. `sale` |

**Returns:**
```json
{
  "name": "sale",
  "title": "Sales",
  "summary": "From quotations to invoices",
  "author": "Odoo SA",
  "version": "18.0.2.0.0",
  "state": "installed",
  "category": "Sales/Sales",
  "license": "LGPL-3",
  "application": true,
  "dependencies": [
    { "name": "account", "auto_install_required": false },
    ...
  ],
  "models": [
    { "model": "sale.order", "name": "Sales Order" },
    { "model": "sale.order.line", "name": "Sales Order Line" },
    ...
  ]
}
```

**Example prompt:** "Tell me about the sale module — what does it depend on and what models does it define?"

---

## search_records

Search and read records from any Odoo model with domain filtering and pagination.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | str | yes | — | Technical model name |
| `domain` | str | no | `"[]"` | Odoo domain as JSON string |
| `fields` | str | no | `"[]"` | JSON list of field names |
| `limit` | int | no | `20` | Max records to return |
| `offset` | int | no | `0` | Records to skip |
| `order` | str | no | `""` | Sort order |

This is similar to `database_query` but with a smaller default limit (20 vs 80), designed for browsing records.

**Example prompt:** "Search for all users, show name and login, sorted by name"

---

## execute_method

Execute an arbitrary ORM method on an Odoo model. This is similar to Laravel's Tinker — use with care.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | str | yes | — | Technical model name |
| `method` | str | yes | — | Method name, e.g. `default_get`, `fields_get`, `name_search` |
| `args` | str | no | `"[]"` | Positional arguments as JSON list |
| `kwargs` | str | no | `"{}"` | Keyword arguments as JSON object |

**Returns:**
```json
{
  "model": "res.partner",
  "method": "default_get",
  "result": { "name": false, "company_type": "company", ... }
}
```

**Example prompt:** "Call default_get on res.partner to see what default values are set"

---

## read_log_entries

Read Odoo log entries from `ir.logging`. Requires `log_db` to be configured in `odoo.conf`.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `level` | str | no | `""` | Filter by level: `WARNING`, `ERROR`, `CRITICAL` |
| `func` | str | no | `""` | Filter by function name substring |
| `limit` | int | no | `50` | Max entries to return |

**Returns:**
```json
{
  "total": 5,
  "entries": [
    {
      "timestamp": "2025-01-15 10:30:00",
      "level": "WARNING",
      "name": "odoo.addons.sale",
      "function": "_check_order",
      "path": "/path/to/file.py",
      "line": "142",
      "message": "Order validation failed"
    },
    ...
  ]
}
```

> **Note:** Returns an error message if `log_db` is not configured.

**Example prompt:** "Show me the latest error log entries"

---

## search_docs

Search Odoo documentation and return relevant links. Does not require a connection — works from a built-in topic index.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `topic` | str | no | `""` | Topic keyword (e.g. `orm`, `views`, `security`). Empty lists all topics. |
| `version` | str | no | `""` | Odoo version, e.g. `18.0`. Defaults to `18`. |

**Available topics:** `orm`, `fields`, `views`, `actions`, `security`, `controllers`, `qweb`, `owl`, `assets`, `testing`, `data`, `reports`, `module`, `web_services`, `mixins`

**Returns:**
```json
{
  "results": [
    {
      "topic": "orm",
      "title": "ORM API",
      "url": "https://www.odoo.com/documentation/18/developer/reference/backend/orm.html",
      "description": "Model definitions, fields, CRUD, domains, recordsets."
    }
  ]
}
```

**Example prompt:** "Find me the Odoo documentation for OWL components"

---

## list_workflows

List automated actions (`base.automation`) and server actions (`ir.actions.server`).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model_name` | str | no | `""` | Filter by model name |
| `limit` | int | no | `50` | Max entries per type |

**Returns:**
```json
{
  "model_filter": "sale.order",
  "automated_actions": [
    {
      "id": 5,
      "name": "Auto-confirm quotation",
      "model": "sale.order",
      "trigger": "on_write",
      "active": true,
      "server_action_count": 1
    }
  ],
  "server_actions": [
    {
      "id": 12,
      "name": "Send confirmation email",
      "model": "sale.order",
      "type": "email",
      "code_preview": "",
      "sequence": 5
    }
  ]
}
```

**Example prompt:** "What automated actions and server actions exist for sale.order?"
