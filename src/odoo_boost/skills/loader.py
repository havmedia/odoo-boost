"""Skill loading and installation utilities."""

from __future__ import annotations

import importlib.resources
from pathlib import Path

_SKILL_DIRS = [
    "creating_models",
    "xml_views",
    "security_rules",
    "owl_components",
    "controllers_routes",
    "report_development",
    "automated_actions",
    "testing",
]


def list_skills() -> list[str]:
    """Return the list of available skill names."""
    return list(_SKILL_DIRS)


def load_skill(skill_name: str) -> str:
    """Read and return the SKILL.md content for a skill."""
    ref = importlib.resources.files("odoo_boost.skills") / skill_name / "SKILL.md"
    return ref.read_text(encoding="utf-8")


def install_skills(target_dir: Path) -> list[Path]:
    """Copy all skill directories into *target_dir*.

    Returns a list of created paths.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for skill_name in _SKILL_DIRS:
        dest = target_dir / skill_name
        dest.mkdir(parents=True, exist_ok=True)

        content = load_skill(skill_name)
        skill_file = dest / "SKILL.md"
        skill_file.write_text(content, encoding="utf-8")
        created.append(skill_file)

    return created
