"""Configuration management for Odoo Boost."""

from odoo_boost.config.schema import OdooBoostConfig, OdooConnection
from odoo_boost.config.settings import load_config, save_config, find_config_path

__all__ = [
    "OdooBoostConfig",
    "OdooConnection",
    "load_config",
    "save_config",
    "find_config_path",
]
