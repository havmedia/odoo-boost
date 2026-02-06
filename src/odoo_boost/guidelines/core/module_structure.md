## Module Structure

### Standard Directory Layout
```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   └── my_model_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml          # groups + record rules
├── data/
│   └── data.xml              # default data records
├── demo/
│   └── demo.xml              # demo data (loaded in demo mode)
├── controllers/
│   ├── __init__.py
│   └── main.py
├── wizard/
│   ├── __init__.py
│   └── my_wizard.py
├── report/
│   └── my_report.xml
├── static/
│   ├── description/
│   │   └── icon.png
│   └── src/
│       ├── js/
│       ├── xml/               # OWL component templates
│       └── scss/
└── i18n/
    └── fr.po
```

### __manifest__.py
- Required keys: `name`, `version`, `depends`, `data`.
- Version format: `<odoo_version>.<module_version>`, e.g. `18.0.1.0.0`.
- `data` lists XML/CSV files loaded in order — security files first, then views, then data.
- `demo` lists files loaded only when demo data is enabled.
- `assets` defines JavaScript/CSS bundles to include.
- `license` should be `LGPL-3` for community modules.
- `installable` defaults to `True`; set to `False` for deprecated modules.

### File Naming
- Model files: named after the model they define (`sale_order.py` for `sale.order`).
- View files: `<model_name>_views.xml` (e.g. `sale_order_views.xml`).
- Security files: always `ir.model.access.csv` and optional `security.xml`.
- Each Python package (`models/`, `controllers/`, `wizard/`) needs an `__init__.py`.
