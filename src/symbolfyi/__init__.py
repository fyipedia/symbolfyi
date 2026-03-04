"""symbolfyi — Pure Python symbol & character encoding toolkit.

Compute 11 encoding representations (Unicode, HTML, CSS, JavaScript,
Python, Java, UTF-8, UTF-16, URL) and Unicode properties for any character.
Includes 47 HTML entity mappings.

Zero required dependencies. Optional ``fonttools`` for block/script info.

Usage::

    from symbolfyi import get_encodings, get_info, lookup_html_entity

    # Encode any character
    enc = get_encodings("→")
    print(enc.unicode)        # U+2192
    print(enc.html_entity)    # &rarr;
    print(enc.css)            # \\2192
    print(enc.utf8_bytes)     # e2 86 92

    # Full Unicode properties
    info = get_info("♠")
    print(info.name)          # BLACK SPADE SUIT
    print(info.block)         # Miscellaneous Symbols (requires fonttools)
    print(info.category_name) # Other Symbol

    # HTML entity lookup
    char = lookup_html_entity("&hearts;")
    print(char)               # ♥
"""

from symbolfyi.engine import (
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

__version__ = "0.2.0"

__all__ = [
    # Data types
    "EncodingInfo",
    "SymbolInfo",
    # Core functions
    "get_encodings",
    "get_info",
    "get_category_name",
    "lookup_html_entity",
    # Data
    "GENERAL_CATEGORIES",
    "HTML_ENTITIES",
    "HTML_ENTITY_TO_CHAR",
]
