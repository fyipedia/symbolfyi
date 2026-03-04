"""Tests for symbolfyi.api -- HTTP client for symbolfyi.com."""

from __future__ import annotations

from symbolfyi.api import SymbolFYI


class TestSymbolFYIClient:
    """Verify the client initializes and has all expected methods."""

    def test_init_default(self) -> None:
        client = SymbolFYI()
        assert str(client._client.base_url) == "https://symbolfyi.com/api/"
        client.close()

    def test_init_custom_url(self) -> None:
        client = SymbolFYI(base_url="http://localhost:8000/api", timeout=5.0)
        assert "localhost" in str(client._client.base_url)
        client.close()

    def test_context_manager(self) -> None:
        with SymbolFYI() as client:
            assert client is not None

    def test_has_all_methods(self) -> None:
        client = SymbolFYI()
        methods = [
            "symbol",
            "search",
            "category",
            "encode",
            "collections",
            "collection",
            "blocks",
            "block",
            "symbols",
        ]
        for method in methods:
            assert hasattr(client, method), f"Missing method: {method}"
            assert callable(getattr(client, method))
        client.close()
