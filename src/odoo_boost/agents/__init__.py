"""Agent registry – all supported AI coding agents."""

from __future__ import annotations

from odoo_boost.agents.base import Agent
from odoo_boost.agents.claude_code import ClaudeCodeAgent
from odoo_boost.agents.cursor import CursorAgent
from odoo_boost.agents.copilot import CopilotAgent
from odoo_boost.agents.codex import CodexAgent
from odoo_boost.agents.gemini_cli import GeminiCliAgent
from odoo_boost.agents.junie import JunieAgent

AGENTS: dict[str, type[Agent]] = {
    "claude_code": ClaudeCodeAgent,
    "cursor": CursorAgent,
    "copilot": CopilotAgent,
    "codex": CodexAgent,
    "gemini_cli": GeminiCliAgent,
    "junie": JunieAgent,
}

ALL_AGENT_IDS = list(AGENTS.keys())

__all__ = [
    "Agent",
    "AGENTS",
    "ALL_AGENT_IDS",
    "ClaudeCodeAgent",
    "CursorAgent",
    "CopilotAgent",
    "CodexAgent",
    "GeminiCliAgent",
    "JunieAgent",
]
