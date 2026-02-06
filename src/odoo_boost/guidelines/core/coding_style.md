## Coding Style

### Python
- Follow PEP 8 with Odoo-specific conventions.
- Line length: 120 characters max (Odoo's standard).
- Imports order: stdlib, third-party, odoo (`from odoo import ...`), local.
- Use `from odoo import models, fields, api, _` for common imports.
- Use `_()` for all user-facing strings (translation).
- Method order in models: default fields, ORM overrides (`create`, `write`), compute methods, action methods, business logic.
- Private methods start with underscore: `_compute_total()`, `_check_constraints()`.
- Use `@api.constrains` for Python-level validation, SQL constraints for DB-level.

### XML
- Indent with 4 spaces (consistent with Python).
- Use meaningful XML IDs: `module_name.model_name_view_type`.
- One XML record per logical unit — don't cram unrelated records in one file.
- Use `noupdate="1"` for data that shouldn't be overwritten on module upgrade.

### JavaScript
- Use ES6+ syntax with `@odoo-module` pragma.
- PascalCase for component classes, camelCase for methods and variables.
- Template names match the module + component: `my_module.MyComponent`.
- Use Odoo's service layer, not direct API calls.

### Naming Conventions Summary
| Entity | Convention | Example |
|--------|-----------|---------|
| Model name | Dot-separated | `sale.order.line` |
| Python file | Underscored | `sale_order_line.py` |
| XML ID | Dot-separated | `sale.order_line_view_form` |
| Field name | snake_case | `partner_shipping_id` |
| Method name | snake_case | `action_confirm` |
| JS Component | PascalCase | `SaleOrderLine` |
| CSS class | kebab-case | `o-sale-order-line` |

### Git Commit Messages
- Start with `[TAG]` indicating type: `[FIX]`, `[IMP]`, `[ADD]`, `[REM]`, `[REF]`, `[MOV]`.
- Include module name: `[FIX] sale: correct tax computation on refund`.
- Keep the first line under 80 characters.
