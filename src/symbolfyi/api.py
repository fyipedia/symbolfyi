"""HTTP API client for symbolfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install symbolfyi[api]``

Usage::

    from symbolfyi.api import SymbolFYI

    with SymbolFYI() as api:
        info = api.encode("->")
        print(info["encodings"]["html_entity"])
"""

from __future__ import annotations

from typing import Any

import httpx


class SymbolFYI:
    """API client for the symbolfyi.com REST API.

    Args:
        base_url: API base URL. Defaults to ``https://symbolfyi.com/api``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://symbolfyi.com/api",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    # -- HTTP helpers ----------------------------------------------------------

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -------------------------------------------------------------

    def symbol(self, slug: str) -> dict[str, Any]:
        """Get full symbol details by slug.

        Args:
            slug: Symbol slug (e.g. ``"rightwards-arrow"``).

        Returns:
            Dict with character, name, codepoint, category, encodings, etc.
        """
        return self._get(f"/symbol/{slug}/")

    def search(self, query: str) -> dict[str, Any]:
        """Search symbols by name, character, or codepoint.

        Args:
            query: Search term (e.g. ``"arrow"``, ``"heart"``).

        Returns:
            Dict with results list and query string.
        """
        return self._get("/search/", q=query)

    def category(self, slug: str) -> dict[str, Any]:
        """Get all symbols in a Unicode category.

        Args:
            slug: Category slug (e.g. ``"math-symbol"``).

        Returns:
            Dict with category name, slug, and symbols list.
        """
        return self._get(f"/category/{slug}/")

    def encode(self, char: str) -> dict[str, Any]:
        """Get all 11 encoding representations for a character.

        Args:
            char: Single character to encode (e.g. ``"->"``, ``"*"``).

        Returns:
            Dict with character info and encodings object.
        """
        return self._get("/encode/", char=char)

    def collections(self) -> dict[str, Any]:
        """List all curated symbol collections.

        Returns:
            Dict with count and collections list.
        """
        return self._get("/collections/")

    def collection(self, slug: str) -> dict[str, Any]:
        """Get a curated symbol collection with its symbols.

        Args:
            slug: Collection slug (e.g. ``"arrows"``, ``"math"``).

        Returns:
            Dict with collection details and symbols list.
        """
        return self._get(f"/collection/{slug}/")

    def blocks(self) -> dict[str, Any]:
        """List all Unicode blocks.

        Returns:
            Dict with count and blocks list.
        """
        return self._get("/blocks/")

    def block(self, slug: str) -> dict[str, Any]:
        """Get all symbols in a Unicode block.

        Args:
            slug: Block slug (e.g. ``"arrows"``, ``"mathematical-operators"``).

        Returns:
            Dict with block details and symbols list.
        """
        return self._get(f"/block/{slug}/")

    def symbols(self) -> dict[str, Any]:
        """List all symbols with basic metadata.

        Returns:
            Dict with count and symbols list.
        """
        return self._get("/symbols/")

    # -- Context manager -------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def __enter__(self) -> SymbolFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
