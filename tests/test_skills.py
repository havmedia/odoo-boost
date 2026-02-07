"""Tests for odoo_boost.skills.loader."""

from __future__ import annotations

import pytest

from odoo_boost.skills.loader import _SKILL_DIRS, install_skills, list_skills, load_skill


class TestListSkills:
    def test_returns_list(self):
        skills = list_skills()
        assert isinstance(skills, list)

    def test_count(self):
        assert len(list_skills()) == 8

    def test_known_skills_present(self):
        skills = list_skills()
        for expected in ["creating_models", "xml_views", "security_rules", "owl_components"]:
            assert expected in skills

    def test_returns_copy(self):
        """list_skills() should not expose the internal list."""
        a = list_skills()
        b = list_skills()
        assert a == b
        a.append("fake")
        assert "fake" not in list_skills()


class TestLoadSkill:
    def test_load_each_skill(self):
        for skill_name in list_skills():
            content = load_skill(skill_name)
            assert isinstance(content, str)
            assert len(content) > 10  # not empty
            assert "SKILL" in content.upper() or "#" in content

    def test_unknown_skill_raises(self):
        with pytest.raises((FileNotFoundError, TypeError, ModuleNotFoundError)):
            load_skill("nonexistent_skill_xyz")


class TestInstallSkills:
    def test_creates_files(self, tmp_path):
        created = install_skills(tmp_path / "skills")
        assert len(created) == 8
        for path in created:
            assert path.exists()
            assert path.name == "SKILL.md"

    def test_target_dir_created(self, tmp_path):
        target = tmp_path / "new" / "nested" / "skills"
        install_skills(target)
        assert target.is_dir()

    def test_subdirs_match_skill_names(self, tmp_path):
        target = tmp_path / "skills"
        install_skills(target)
        subdirs = sorted(d.name for d in target.iterdir() if d.is_dir())
        assert subdirs == sorted(_SKILL_DIRS)

    def test_idempotent(self, tmp_path):
        target = tmp_path / "skills"
        first = install_skills(target)
        second = install_skills(target)
        assert len(first) == len(second)
        # Files should still exist and be valid
        for path in second:
            assert path.exists()

    def test_content_matches_load(self, tmp_path):
        target = tmp_path / "skills"
        install_skills(target)
        for skill_name in list_skills():
            installed = (target / skill_name / "SKILL.md").read_text(encoding="utf-8")
            loaded = load_skill(skill_name)
            assert installed == loaded
