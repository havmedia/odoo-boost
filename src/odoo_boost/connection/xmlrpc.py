"""XML-RPC client for Odoo 17/18/19."""

from __future__ import annotations

import xmlrpc.client
from typing import Any

from odoo_boost.connection.base import OdooConnection as BaseConnection


class XmlRpcConnection(BaseConnection):
    """Connects to Odoo via XML-RPC (works on all supported versions)."""

    def __init__(
        self,
        url: str,
        database: str,
        username: str,
        password: str,
    ) -> None:
        self._url = url.rstrip("/")
        self._database = database
        self._username = username
        self._password = password
        self._uid: int | None = None
        self._common: xmlrpc.client.ServerProxy | None = None
        self._object: xmlrpc.client.ServerProxy | None = None

    # -- lazy proxy helpers --------------------------------------------------

    @property
    def _common_proxy(self) -> xmlrpc.client.ServerProxy:
        if self._common is None:
            self._common = xmlrpc.client.ServerProxy(
                f"{self._url}/xmlrpc/2/common", allow_none=True
            )
        return self._common

    @property
    def _object_proxy(self) -> xmlrpc.client.ServerProxy:
        if self._object is None:
            self._object = xmlrpc.client.ServerProxy(
                f"{self._url}/xmlrpc/2/object", allow_none=True
            )
        return self._object

    # -- public interface ----------------------------------------------------

    def authenticate(self) -> int:
        uid = self._common_proxy.authenticate(
            self._database, self._username, self._password, {}
        )
        if not uid:
            raise ConnectionError(
                f"Authentication failed for {self._username}@{self._database}"
            )
        self._uid = int(uid)
        return self._uid

    @property
    def uid(self) -> int:
        if self._uid is None:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self._uid

    def execute(
        self,
        model: str,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        return self._object_proxy.execute_kw(
            self._database,
            self.uid,
            self._password,
            model,
            method,
            list(args),
            kwargs or {},
        )

    def search_read(
        self,
        model: str,
        domain: list[Any] | None = None,
        fields: list[str] | None = None,
        limit: int | None = None,
        offset: int = 0,
        order: str | None = None,
    ) -> list[dict[str, Any]]:
        kwargs: dict[str, Any] = {"offset": offset}
        if fields is not None:
            kwargs["fields"] = fields
        if limit is not None:
            kwargs["limit"] = limit
        if order is not None:
            kwargs["order"] = order
        return self.execute(model, "search_read", domain or [], **kwargs)

    def search_count(
        self,
        model: str,
        domain: list[Any] | None = None,
    ) -> int:
        return self.execute(model, "search_count", domain or [])

    def get_version(self) -> dict[str, Any]:
        return self._common_proxy.version()
