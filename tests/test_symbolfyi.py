"""Tests for symbolfyi package."""

from __future__ import annotations

from symbolfyi import (
    GENERAL_CATEGORIES,
    HTML_ENTITIES,
    HTML_ENTITY_TO_CHAR,
    EncodingInfo,
    SymbolInfo,
    get_category_name,
    get_encodings,
    get_info,
    lookup_html_entity,
)


# =============================================================================
# Encoding
# =============================================================================
class TestGetEncodings:
    def test_returns_encoding_info(self) -> None:
        enc = get_encodings("♠")
        assert isinstance(enc, EncodingInfo)

    def test_unicode_notation(self) -> None:
        assert get_encodings("♠").unicode == "U+2660"

    def test_html_decimal(self) -> None:
        assert get_encodings("♠").html_decimal == "&#9824;"

    def test_html_hex(self) -> None:
        assert get_encodings("♠").html_hex == "&#x2660;"

    def test_html_entity(self) -> None:
        assert get_encodings("♠").html_entity == "&spades;"

    def test_html_entity_empty(self) -> None:
        # Characters without HTML entities return empty string
        assert get_encodings("A").html_entity == ""

    def test_css(self) -> None:
        assert get_encodings("♠").css == "\\2660"

    def test_javascript(self) -> None:
        assert get_encodings("♠").javascript == "\\u{2660}"

    def test_python_bmp(self) -> None:
        assert get_encodings("♠").python == "\\u2660"

    def test_python_supplementary(self) -> None:
        # 😀 = U+1F600 (supplementary plane)
        assert get_encodings("😀").python == "\\U0001f600"

    def test_java_bmp(self) -> None:
        assert get_encodings("♠").java == "\\u2660"

    def test_java_surrogate_pair(self) -> None:
        assert get_encodings("😀").java == "\\uD83D\\uDE00"

    def test_utf8_bytes(self) -> None:
        assert get_encodings("♠").utf8_bytes == "e2 99 a0"

    def test_utf16_bytes(self) -> None:
        assert get_encodings("♠").utf16_bytes == "26 60"

    def test_url_encoded(self) -> None:
        assert get_encodings("♠").url_encoded == "%E2%99%A0"

    def test_ascii_character(self) -> None:
        enc = get_encodings("A")
        assert enc.unicode == "U+0041"
        assert enc.utf8_bytes == "41"
        assert enc.url_encoded == "A"


# =============================================================================
# Symbol info
# =============================================================================
class TestGetInfo:
    def test_returns_symbol_info(self) -> None:
        info = get_info("→")
        assert info is not None
        assert isinstance(info, SymbolInfo)

    def test_basic_properties(self) -> None:
        info = get_info("→")
        assert info is not None
        assert info.name == "RIGHTWARDS ARROW"
        assert info.codepoint == 0x2192
        assert info.character == "→"
        assert info.category == "Sm"
        assert info.category_name == "Math Symbol"

    def test_block_with_fonttools(self) -> None:
        info = get_info("→")
        assert info is not None
        # fonttools is installed in dev
        assert info.block == "Arrows"

    def test_script_with_fonttools(self) -> None:
        info = get_info("A")
        assert info is not None
        assert info.script == "Latn"

    def test_encodings_included(self) -> None:
        info = get_info("♠")
        assert info is not None
        assert isinstance(info.encodings, EncodingInfo)
        assert info.encodings.html_entity == "&spades;"

    def test_none_for_control_chars(self) -> None:
        # Control characters have no Unicode name
        assert get_info("\x00") is None

    def test_mirrored(self) -> None:
        info = get_info("(")
        assert info is not None
        assert info.mirrored is True

    def test_not_mirrored(self) -> None:
        info = get_info("A")
        assert info is not None
        assert info.mirrored is False


# =============================================================================
# Category names
# =============================================================================
class TestGetCategoryName:
    def test_known_category(self) -> None:
        assert get_category_name("Sm") == "Math Symbol"
        assert get_category_name("Lu") == "Uppercase Letter"

    def test_unknown_category(self) -> None:
        assert get_category_name("Xx") == "Xx"


# =============================================================================
# HTML entities
# =============================================================================
class TestHTMLEntities:
    def test_lookup_entity(self) -> None:
        assert lookup_html_entity("&amp;") == "&"
        assert lookup_html_entity("&hearts;") == "♥"
        assert lookup_html_entity("&copy;") == "©"

    def test_lookup_not_found(self) -> None:
        assert lookup_html_entity("&nonexistent;") is None

    def test_entities_count(self) -> None:
        assert len(HTML_ENTITIES) == 51

    def test_reverse_mapping(self) -> None:
        assert len(HTML_ENTITY_TO_CHAR) == 51
        assert HTML_ENTITY_TO_CHAR["&euro;"] == "€"


# =============================================================================
# Data constants
# =============================================================================
class TestConstants:
    def test_general_categories(self) -> None:
        assert len(GENERAL_CATEGORIES) == 27
        assert "Lu" in GENERAL_CATEGORIES
        assert "So" in GENERAL_CATEGORIES


# =============================================================================
# Exports
# =============================================================================
class TestExports:
    def test_all_types(self) -> None:
        assert EncodingInfo is not None
        assert SymbolInfo is not None


# =============================================================================
# Edge cases
# =============================================================================
class TestEdgeCases:
    def test_ascii_char(self) -> None:
        enc = get_encodings("A")
        assert enc.unicode == "U+0041"
        assert enc.html_decimal == "&#65;"
        assert enc.url_encoded == "A"  # ASCII not percent-encoded

    def test_space_char(self) -> None:
        enc = get_encodings(" ")
        assert enc.unicode == "U+0020"

    def test_last_bmp(self) -> None:
        enc = get_encodings("\uffff")
        assert enc.unicode == "U+FFFF"

    def test_first_supplementary(self) -> None:
        enc = get_encodings("\U00010000")
        assert enc.unicode == "U+10000"
        assert "\\u" in enc.java  # surrogate pair

    def test_category_unknown(self) -> None:
        name = get_category_name("XX")
        assert name == "XX"  # fallback to code itself

    def test_entity_not_found(self) -> None:
        result = lookup_html_entity("&nonexistent;")
        assert result is None

    def test_info_control_char(self) -> None:
        info = get_info("\x00")
        assert info is None  # control chars return None
