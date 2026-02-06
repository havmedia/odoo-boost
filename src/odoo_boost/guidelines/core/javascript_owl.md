## JavaScript and OWL

### OWL Framework
- Odoo uses **OWL** (Odoo Web Library) as its frontend component framework (v14+).
- OWL is a modern reactive framework similar to Vue/React with XML templates.
- Components are ES6 classes extending `Component` from `@odoo/owl`.
- Templates use QWeb syntax with `t-` directives.

### Component Structure
```javascript
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MyComponent extends Component {
    static template = "my_module.MyComponent";
    static props = {
        recordId: { type: Number, optional: true },
    };

    setup() {
        this.state = useState({ count: 0 });
    }

    increment() {
        this.state.count++;
    }
}
```

### Template (QWeb XML)
- Place in `static/src/xml/my_component.xml`.
- Register via assets in `__manifest__.py`.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="my_module.MyComponent">
        <div class="my-component">
            <span t-esc="state.count"/>
            <button t-on-click="increment">+1</button>
        </div>
    </t>
</templates>
```

### Key Concepts
- **Hooks**: `useState`, `useRef`, `useEffect`, `useService`, `useEnv` — similar to React hooks.
- **Services**: Use `useService("rpc")` for RPC calls, `useService("orm")` for ORM operations, `useService("notification")` for toasts.
- **Registry**: `registry.category("actions")`, `registry.category("fields")`, `registry.category("services")`.
- **Props validation**: Define `static props` for type checking in dev mode.
- **Lifecycle**: `setup()` (constructor-like), `willStart()`, `mounted()`, `willUnmount()`.

### Assets Declaration
```python
'assets': {
    'web.assets_backend': [
        'my_module/static/src/js/**/*',
        'my_module/static/src/xml/**/*',
        'my_module/static/src/scss/**/*',
    ],
},
```

### Best Practices
- Use the `@odoo-module` pragma at the top of every JS file.
- Use Odoo's built-in services (`rpc`, `orm`, `action`) instead of raw `fetch`.
- Keep components small and focused — compose from smaller components.
- Use `t-key` on `t-foreach` loops for proper reconciliation.
- Don't directly manipulate the DOM — use OWL's reactive state instead.
