# Guidelines

Odoo Boost bundles comprehensive Odoo development guidelines that are injected into your AI agent's context. This ensures your agent writes idiomatic Odoo code following official best practices.

## What's Included

The guidelines are composed from 9 core files plus a version-specific addendum:

### Core Guidelines

| File | Topic | Covers |
|------|-------|--------|
| `odoo_general.md` | General Principles | Architecture, conventions, module dependencies |
| `module_structure.md` | Module Structure | Directory layout, `__manifest__.py`, file naming |
| `orm_best_practices.md` | ORM Best Practices | Models, fields, CRUD, domains, performance |
| `security.md` | Security | ACLs, record rules, groups, common pitfalls |
| `views_and_ui.md` | Views & UI | Form, list, kanban, search, inheritance, actions |
| `controllers.md` | Controllers | HTTP routes, JSON-RPC, best practices |
| `javascript_owl.md` | JavaScript & OWL | Components, templates, hooks, services, assets |
| `testing.md` | Testing | Python tests, HTTP tests, test patterns |
| `coding_style.md` | Coding Style | Python, XML, JS conventions, naming, commits |

### Version-Specific Files

| File | Version | Key Topics |
|------|---------|------------|
| `v17.md` | Odoo 17 | `<list>` tag, `attrs` removal, OWL 2, `Command` API |
| `v18.md` | Odoo 18 | Inline expressions mandatory, portal redesign |
| `v19.md` | Odoo 19 | `<tree>` removed, Python 3.12+ required |

## How Version Selection Works

During `odoo-boost install`, the detected Odoo version is saved to `odoo-boost.json`:

```json
{
  "odoo_version": "18.0"
}
```

When generating guidelines, the composer:

1. Assembles all 9 core files
2. Appends the matching version file (e.g. `v18.md` for version `18.0`)
3. Writes the result to the agent's guidelines file

This means your agent gets version-correct advice. For example:
- On Odoo 17: "Use `<list>` instead of `<tree>` (both work but `<list>` is preferred)"
- On Odoo 19: "Only `<list>` is supported — `<tree>` will cause errors"

## Where Guidelines Are Written

Each agent has its own guidelines file in the format it expects:

| Agent | File | Format |
|-------|------|--------|
| Claude Code | `CLAUDE.md` | Markdown |
| Cursor | `.cursor/rules/odoo-boost.mdc` | Markdown with YAML frontmatter |
| GitHub Copilot | `.github/copilot-instructions.md` | Markdown |
| OpenAI Codex | `AGENTS.md` | Markdown |
| Gemini CLI | `GEMINI.md` | Markdown |
| Junie | `.junie/guidelines.md` | Markdown |

## Refreshing Guidelines

To regenerate guidelines (e.g. after an Odoo Boost update with improved content):

```bash
odoo-boost update
```

## Programmatic Access

You can use the guidelines composer directly in Python:

```python
from odoo_boost.guidelines import compose_guidelines

# All core guidelines + v18-specific notes
content = compose_guidelines("18.0")

# Core guidelines only (no version-specific notes)
content = compose_guidelines()
```
