# Skills

Odoo Boost includes 8 step-by-step skill guides that help AI agents perform common Odoo development tasks. Each skill is a `SKILL.md` file with YAML frontmatter and a detailed walkthrough.

## Available Skills

| Skill | Directory | Description |
|-------|-----------|-------------|
| Creating Models | `creating_models/` | Create a new Odoo model with fields, constraints, and methods |
| XML Views | `xml_views/` | Create and customize form, list, kanban, and search views |
| Security Rules | `security_rules/` | Set up ACLs (`ir.model.access`) and record rules (`ir.rule`) |
| OWL Components | `owl_components/` | Create custom OWL frontend components with templates |
| Controllers & Routes | `controllers_routes/` | Create HTTP controllers and API endpoints |
| Report Development | `report_development/` | Create QWeb PDF reports and report actions |
| Automated Actions | `automated_actions/` | Create `base.automation` and server actions |
| Testing | `testing/` | Write Python and JavaScript tests for Odoo modules |

## Skill Format

Each skill is a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: Creating Models
description: Step-by-step guide to create a new Odoo model with fields, constraints, and methods.
globs: ["models/**/*.py", "__manifest__.py"]
---

# Creating Odoo Models

## Steps

1. **Create the Python file** ...
2. **Define the model class** ...
...

## Checklist
- [ ] `_name` and `_description` set
- [ ] Fields defined with proper types
...
```

### Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Human-readable skill name |
| `description` | Brief description of what the skill covers |
| `globs` | File patterns the skill applies to (used by agents that support glob-based context) |

## Where Skills Are Installed

Each agent writes skills to its own directory:

| Agent | Skills Directory |
|-------|-----------------|
| Claude Code | `.ai/skills/` |
| Cursor | `.cursor/skills/` |
| GitHub Copilot | `.github/skills/` |
| Codex | `.agents/skills/` |
| Gemini CLI | `.agents/skills/` |
| Junie | `.junie/skills/` |

> Codex and Gemini CLI share `.agents/skills/` to avoid duplication.

Each skill gets its own subdirectory:

```
.ai/skills/
├── creating_models/
│   └── SKILL.md
├── xml_views/
│   └── SKILL.md
├── security_rules/
│   └── SKILL.md
├── owl_components/
│   └── SKILL.md
├── controllers_routes/
│   └── SKILL.md
├── report_development/
│   └── SKILL.md
├── automated_actions/
│   └── SKILL.md
└── testing/
    └── SKILL.md
```

## Programmatic Access

```python
from odoo_boost.skills import list_skills, load_skill, install_skills
from pathlib import Path

# List available skill names
skills = list_skills()
# ['creating_models', 'xml_views', 'security_rules', ...]

# Read a single skill's content
content = load_skill("creating_models")

# Install all skills to a directory
install_skills(Path("./my-skills"))
```
