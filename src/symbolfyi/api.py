"""HTTP API client for symbolfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install symbolfyi[api]``

Usage::

    from symbolfyi.api import SymbolFYI

    with SymbolFYI() as api:
        items = api.list_categories()
        detail = api.get_category("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class SymbolFYI:
    """API client for the symbolfyi.com REST API.

    Provides typed access to all symbolfyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://symbolfyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://symbolfyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_categories(self, **params: Any) -> dict[str, Any]:
        """List all categories."""
        return self._get("/api/v1/categories/", **params)

    def get_category(self, slug: str) -> dict[str, Any]:
        """Get category by slug."""
        return self._get(f"/api/v1/categories/" + slug + "/")

    def list_collections(self, **params: Any) -> dict[str, Any]:
        """List all collections."""
        return self._get("/api/v1/collections/", **params)

    def get_collection(self, slug: str) -> dict[str, Any]:
        """Get collection by slug."""
        return self._get(f"/api/v1/collections/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_glossary(self, **params: Any) -> dict[str, Any]:
        """List all glossary."""
        return self._get("/api/v1/glossary/", **params)

    def get_term(self, slug: str) -> dict[str, Any]:
        """Get term by slug."""
        return self._get(f"/api/v1/glossary/" + slug + "/")

    def list_guide_categories(self, **params: Any) -> dict[str, Any]:
        """List all guide categories."""
        return self._get("/api/v1/guide-categories/", **params)

    def get_guide_category(self, slug: str) -> dict[str, Any]:
        """Get guide category by slug."""
        return self._get(f"/api/v1/guide-categories/" + slug + "/")

    def list_guide_series(self, **params: Any) -> dict[str, Any]:
        """List all guide series."""
        return self._get("/api/v1/guide-series/", **params)

    def get_guide_sery(self, slug: str) -> dict[str, Any]:
        """Get guide sery by slug."""
        return self._get(f"/api/v1/guide-series/" + slug + "/")

    def list_guides(self, **params: Any) -> dict[str, Any]:
        """List all guides."""
        return self._get("/api/v1/guides/", **params)

    def get_guide(self, slug: str) -> dict[str, Any]:
        """Get guide by slug."""
        return self._get(f"/api/v1/guides/" + slug + "/")

    def list_symbols(self, **params: Any) -> dict[str, Any]:
        """List all symbols."""
        return self._get("/api/v1/symbols/", **params)

    def get_symbol(self, slug: str) -> dict[str, Any]:
        """Get symbol by slug."""
        return self._get(f"/api/v1/symbols/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> SymbolFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
