## Odoo General Principles

### Architecture Overview
- Odoo follows a **Model-View-Controller** pattern built on its own ORM framework.
- Business logic lives in **models** (Python classes inheriting `models.Model`).
- Presentation is handled by **views** (XML-defined UI) and **templates** (QWeb).
- HTTP endpoints are handled by **controllers** (Python classes inheriting `http.Controller`).
- Odoo uses a **module system** — every feature is packaged as a module with a `__manifest__.py`.

### Key Conventions
- Always use the ORM instead of raw SQL — the ORM handles access rights, computed fields, and audit trails.
- Prefer extending existing models (`_inherit`) over creating new ones when adding fields to standard models.
- Use XML IDs (`xml_id`) for all data records to ensure proper upgradability.
- Follow Odoo's naming conventions: model names use dots (`sale.order`), Python files use underscores (`sale_order.py`).
- Keep business logic in models, not in controllers or views.

### Module Dependencies
- Declare all dependencies in `__manifest__.py` under the `depends` key.
- Never import from a module you don't depend on.
- Use `base` as the minimum dependency — all modules implicitly depend on it.
- Avoid circular dependencies between modules.
