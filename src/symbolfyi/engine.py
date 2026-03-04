"""Symbol encoding and Unicode property engine — stateless, <1ms per call.

Computes 11 encoding representations and Unicode properties for any character.
Uses stdlib ``unicodedata`` for core properties; ``fontTools`` (optional) for
Unicode block and script data.

Zero required dependencies. Install ``fonttools`` for block/script info::

    pip install symbolfyi[full]
"""

from __future__ import annotations

import unicodedata
from typing import NamedTuple
from urllib.parse import quote

# Try fontTools for block/script (optional dependency)
try:
    from fontTools.unicodedata import block as ft_block
    from fontTools.unicodedata import script as ft_script

    _HAS_FONTTOOLS = True
except ImportError:
    _HAS_FONTTOOLS = False


# ─── Unicode general category names ──────────────────────────────────────────

GENERAL_CATEGORIES: dict[str, str] = {
    "Lu": "Uppercase Letter",
    "Ll": "Lowercase Letter",
    "Lt": "Titlecase Letter",
    "Lm": "Modifier Letter",
    "Lo": "Other Letter",
    "Mn": "Nonspacing Mark",
    "Mc": "Spacing Mark",
    "Me": "Enclosing Mark",
    "Nd": "Decimal Number",
    "Nl": "Letter Number",
    "No": "Other Number",
    "Pc": "Connector Punctuation",
    "Pd": "Dash Punctuation",
    "Ps": "Open Punctuation",
    "Pe": "Close Punctuation",
    "Pi": "Initial Punctuation",
    "Pf": "Final Punctuation",
    "Po": "Other Punctuation",
    "Sm": "Math Symbol",
    "Sc": "Currency Symbol",
    "Sk": "Modifier Symbol",
    "So": "Other Symbol",
    "Zs": "Space Separator",
    "Zl": "Line Separator",
    "Zp": "Paragraph Separator",
    "Cc": "Control",
    "Cf": "Format",
}


# ─── HTML entity mappings ────────────────────────────────────────────────────

HTML_ENTITIES: dict[int, str] = {
    0x0026: "&amp;",
    0x003C: "&lt;",
    0x003E: "&gt;",
    0x0022: "&quot;",
    0x00A9: "&copy;",
    0x00AE: "&reg;",
    0x2122: "&trade;",
    0x00A3: "&pound;",
    0x00A5: "&yen;",
    0x20AC: "&euro;",
    0x00B0: "&deg;",
    0x00B1: "&plusmn;",
    0x00D7: "&times;",
    0x00F7: "&divide;",
    0x2190: "&larr;",
    0x2191: "&uarr;",
    0x2192: "&rarr;",
    0x2193: "&darr;",
    0x2194: "&harr;",
    0x21D0: "&lArr;",
    0x21D2: "&rArr;",
    0x21D4: "&hArr;",
    0x2200: "&forall;",
    0x2202: "&part;",
    0x2203: "&exist;",
    0x2205: "&empty;",
    0x2207: "&nabla;",
    0x2208: "&isin;",
    0x2209: "&notin;",
    0x220B: "&ni;",
    0x220F: "&prod;",
    0x2211: "&sum;",
    0x221A: "&radic;",
    0x221E: "&infin;",
    0x2227: "&and;",
    0x2228: "&or;",
    0x2229: "&cap;",
    0x222A: "&cup;",
    0x222B: "&int;",
    0x2260: "&ne;",
    0x2264: "&le;",
    0x2265: "&ge;",
    0x2282: "&sub;",
    0x2283: "&sup;",
    0x2286: "&sube;",
    0x2287: "&supe;",
    0x25CA: "&loz;",
    0x2660: "&spades;",
    0x2663: "&clubs;",
    0x2665: "&hearts;",
    0x2666: "&diams;",
}

# Reverse mapping: entity string → character
HTML_ENTITY_TO_CHAR: dict[str, str] = {v: chr(k) for k, v in HTML_ENTITIES.items()}


# ─── Data types ──────────────────────────────────────────────────────────────


class EncodingInfo(NamedTuple):
    """11 encoding representations for a character."""

    unicode: str
    html_decimal: str
    html_hex: str
    html_entity: str
    css: str
    javascript: str
    python: str
    java: str
    utf8_bytes: str
    utf16_bytes: str
    url_encoded: str


class SymbolInfo(NamedTuple):
    """Full Unicode properties + encodings for a character."""

    codepoint: int
    character: str
    name: str
    category: str
    category_name: str
    block: str
    script: str
    bidirectional: str
    combining: int
    mirrored: bool
    decomposition: str
    encodings: EncodingInfo


# ─── Core functions ──────────────────────────────────────────────────────────


def get_encodings(char: str) -> EncodingInfo:
    """Compute 11 encoding representations for a single character.

    >>> enc = get_encodings("♠")
    >>> enc.unicode
    'U+2660'
    >>> enc.html_entity
    '&spades;'
    >>> enc.utf8_bytes
    'e2 99 a0'
    """
    cp = ord(char)
    if cp <= 0xFFFF:
        python_repr = f"\\u{cp:04x}"
        java_repr = f"\\u{cp:04X}"
    else:
        python_repr = f"\\U{cp:08x}"
        high = 0xD800 + ((cp - 0x10000) >> 10)
        low = 0xDC00 + ((cp - 0x10000) & 0x3FF)
        java_repr = f"\\u{high:04X}\\u{low:04X}"

    return EncodingInfo(
        unicode=f"U+{cp:04X}",
        html_decimal=f"&#{cp};",
        html_hex=f"&#x{cp:X};",
        html_entity=HTML_ENTITIES.get(cp, ""),
        css=f"\\{cp:04X}",
        javascript=f"\\u{{{cp:X}}}",
        python=python_repr,
        java=java_repr,
        utf8_bytes=char.encode("utf-8").hex(" "),
        utf16_bytes=char.encode("utf-16-be").hex(" "),
        url_encoded=quote(char),
    )


def get_info(char: str) -> SymbolInfo | None:
    """Get full Unicode properties and encodings for a character.

    Returns ``None`` if the character has no Unicode name (control chars, etc.).

    >>> info = get_info("→")
    >>> info.name if info else None
    'RIGHTWARDS ARROW'
    >>> info.block if info else None  # requires fonttools
    'Arrows'
    """
    try:
        cp = ord(char)
        name = unicodedata.name(char, None)
        if name is None:
            return None
        cat = unicodedata.category(char)

        if _HAS_FONTTOOLS:
            block = ft_block(cp)
            script = ft_script(cp)
        else:
            block = ""
            script = ""

        return SymbolInfo(
            codepoint=cp,
            character=char,
            name=name,
            category=cat,
            category_name=GENERAL_CATEGORIES.get(cat, cat),
            block=block,
            script=script,
            bidirectional=unicodedata.bidirectional(char),
            combining=unicodedata.combining(char),
            mirrored=bool(unicodedata.mirrored(char)),
            decomposition=unicodedata.decomposition(char),
            encodings=get_encodings(char),
        )
    except (ValueError, OverflowError):
        return None


def get_category_name(category_code: str) -> str:
    """Get the full name for a Unicode general category code.

    >>> get_category_name("Sm")
    'Math Symbol'
    """
    return GENERAL_CATEGORIES.get(category_code, category_code)


def lookup_html_entity(entity: str) -> str | None:
    """Look up the character for an HTML entity string.

    >>> lookup_html_entity("&amp;")
    '&'
    >>> lookup_html_entity("&hearts;")
    '♥'
    """
    return HTML_ENTITY_TO_CHAR.get(entity)
