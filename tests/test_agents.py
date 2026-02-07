"""Tests for odoo_boost.agents (base + all 6 concrete agents)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from odoo_boost.agents import AGENTS, ALL_AGENT_IDS, Agent
from odoo_boost.agents.claude_code import ClaudeCodeAgent
from odoo_boost.agents.codex import CodexAgent
from odoo_boost.agents.copilot import CopilotAgent
from odoo_boost.agents.cursor import CursorAgent
from odoo_boost.agents.gemini_cli import GeminiCliAgent
from odoo_boost.agents.junie import JunieAgent
from odoo_boost.config.schema import OdooBoostConfig

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TestAgentRegistry:
    def test_six_agents(self):
        assert len(AGENTS) == 6

    def test_all_ids(self):
        assert list(AGENTS.keys()) == ALL_AGENT_IDS

    def test_known_ids(self):
        for agent_id in ["claude_code", "cursor", "copilot", "codex", "gemini_cli", "junie"]:
            assert agent_id in AGENTS


# ---------------------------------------------------------------------------
# Parametrized: every agent must satisfy these contracts
# ---------------------------------------------------------------------------


AGENT_CLASSES = [
    ClaudeCodeAgent,
    CursorAgent,
    CopilotAgent,
    CodexAgent,
    GeminiCliAgent,
    JunieAgent,
]


@pytest.fixture(params=AGENT_CLASSES, ids=[a.id for a in AGENT_CLASSES])
def agent(request, sample_config: OdooBoostConfig, tmp_path: Path) -> Agent:
    cls = request.param
    return cls(config=sample_config, project_path=tmp_path)


class TestAgentContracts:
    def test_has_id(self, agent: Agent):
        assert isinstance(agent.id, str)
        assert len(agent.id) > 0

    def test_has_display_name(self, agent: Agent):
        assert isinstance(agent.display_name, str)
        assert len(agent.display_name) > 0

    def test_guidelines_path_is_absolute(self, agent: Agent):
        assert agent.guidelines_path.is_absolute()

    def test_mcp_config_path_is_absolute(self, agent: Agent):
        assert agent.mcp_config_path.is_absolute()

    def test_skills_dir_is_absolute(self, agent: Agent):
        assert agent.skills_dir.is_absolute()

    def test_install_creates_files(self, agent: Agent):
        paths = agent.install()
        assert len(paths) > 0
        for p in paths:
            assert p.exists(), f"{p} was not created"

    def test_guidelines_written(self, agent: Agent):
        agent.install()
        assert agent.guidelines_path.exists()
        content = agent.guidelines_path.read_text(encoding="utf-8")
        # All agents write guidelines with the Odoo Development header
        # Cursor wraps in .mdc frontmatter, but it's still there
        assert "Odoo" in content

    def test_mcp_config_written(self, agent: Agent):
        agent.install()
        assert agent.mcp_config_path.exists()
        content = agent.mcp_config_path.read_text(encoding="utf-8")
        assert "odoo-boost" in content

    def test_skills_dir_populated(self, agent: Agent):
        agent.install()
        assert agent.skills_dir.is_dir()
        skill_files = list(agent.skills_dir.rglob("SKILL.md"))
        assert len(skill_files) == 8

    def test_uninstall_removes_files(self, agent: Agent):
        agent.install()
        agent.uninstall()
        assert not agent.guidelines_path.exists()
        assert not agent.mcp_config_path.exists()
        assert not agent.skills_dir.exists()

    def test_mcp_command(self, agent: Agent):
        cmd = agent._mcp_command()
        assert cmd == ["odoo-boost", "mcp"]


# ---------------------------------------------------------------------------
# Agent-specific format tests
# ---------------------------------------------------------------------------


class TestClaudeCodeAgent:
    def test_guidelines_at_claude_md(self, sample_config, tmp_path):
        a = ClaudeCodeAgent(config=sample_config, project_path=tmp_path)
        assert a.guidelines_path.name == "CLAUDE.md"

    def test_mcp_config_json(self, sample_config, tmp_path):
        a = ClaudeCodeAgent(config=sample_config, project_path=tmp_path)
        a.install()
        data = json.loads(a.mcp_config_path.read_text())
        assert "mcpServers" in data
        assert "odoo-boost" in data["mcpServers"]


class TestCursorAgent:
    def test_guidelines_has_frontmatter(self, sample_config, tmp_path):
        a = CursorAgent(config=sample_config, project_path=tmp_path)
        a.install()
        content = a.guidelines_path.read_text()
        assert content.startswith("---\n")
        assert "alwaysApply: true" in content


class TestCopilotAgent:
    def test_mcp_uses_servers_key(self, sample_config, tmp_path):
        a = CopilotAgent(config=sample_config, project_path=tmp_path)
        a.install()
        data = json.loads(a.mcp_config_path.read_text())
        assert "servers" in data  # Copilot uses "servers" not "mcpServers"


class TestCodexAgent:
    def test_mcp_config_is_toml(self, sample_config, tmp_path):
        a = CodexAgent(config=sample_config, project_path=tmp_path)
        a.install()
        content = a.mcp_config_path.read_text()
        assert "[mcp_servers.odoo-boost]" in content
        assert a.mcp_config_path.suffix == ".toml"


class TestGeminiCliAgent:
    def test_guidelines_at_gemini_md(self, sample_config, tmp_path):
        a = GeminiCliAgent(config=sample_config, project_path=tmp_path)
        assert a.guidelines_path.name == "GEMINI.md"


class TestJunieAgent:
    def test_paths_under_junie_dir(self, sample_config, tmp_path):
        a = JunieAgent(config=sample_config, project_path=tmp_path)
        assert ".junie" in str(a.guidelines_path)
        assert ".junie" in str(a.mcp_config_path)
        assert ".junie" in str(a.skills_dir)
