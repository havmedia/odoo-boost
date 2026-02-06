"""Odoo connection layer."""

from odoo_boost.connection.base import OdooConnection
from odoo_boost.connection.factory import create_connection

__all__ = ["OdooConnection", "create_connection"]
