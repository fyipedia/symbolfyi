"""Tests for symbolfyi.mcp_server -- MCP tools."""

from __future__ import annotations

from symbolfyi.mcp_server import (
    html_entity_lookup,
    symbol_encode,
    symbol_info,
)


class TestMCPSymbolInfo:
    def test_info_arrow(self) -> None:
        result = symbol_info("\u2192")
        assert "RIGHTWARDS ARROW" in result
        assert "U+2192" in result
        assert "Math Symbol" in result

    def test_info_spade(self) -> None:
        result = symbol_info("\u2660")
        assert "BLACK SPADE SUIT" in result
        assert "U+2660" in result
        assert "|" in result  # markdown table

    def test_info_ascii(self) -> None:
        result = symbol_info("A")
        assert "LATIN CAPITAL LETTER A" in result
        assert "U+0041" in result

    def test_info_control_char(self) -> None:
        result = symbol_info("\x00")
        assert "No Unicode info" in result


class TestMCPSymbolEncode:
    def test_encode_arrow(self) -> None:
        result = symbol_encode("\u2192")
        assert "U+2192" in result
        assert "e2 86 92" in result
        assert "&rarr;" in result

    def test_encode_spade(self) -> None:
        result = symbol_encode("\u2660")
        assert "U+2660" in result
        assert "&spades;" in result
        assert "UTF-8 Bytes" in result
        assert "UTF-16 Bytes" in result
        assert "JavaScript" in result
        assert "Python" in result

    def test_encode_ascii(self) -> None:
        result = symbol_encode("A")
        assert "U+0041" in result
        assert "(none)" in result  # no HTML entity for A


class TestMCPHTMLEntityLookup:
    def test_lookup_hearts(self) -> None:
        result = html_entity_lookup("&hearts;")
        assert "\u2665" in result
        assert "U+2665" in result

    def test_lookup_amp(self) -> None:
        result = html_entity_lookup("&amp;")
        assert "&" in result

    def test_lookup_without_delimiters(self) -> None:
        result = html_entity_lookup("euro")
        assert "\u20ac" in result  # Euro sign

    def test_lookup_not_found(self) -> None:
        result = html_entity_lookup("&nonexistent;")
        assert "not found" in result.lower()
