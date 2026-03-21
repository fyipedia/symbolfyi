# symbolfyi

[![PyPI version](https://agentgif.com/badge/pypi/symbolfyi/version.svg)](https://pypi.org/project/symbolfyi/)
[![Python](https://img.shields.io/pypi/pyversions/symbolfyi)](https://pypi.org/project/symbolfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python symbol encoder for developers. Compute 11 encoding representations and full Unicode properties for any character. Includes 51 HTML entity mappings, a CLI, MCP server for AI assistants, and an API client for [symbolfyi.com](https://symbolfyi.com/).

> Look up any symbol at [symbolfyi.com](https://symbolfyi.com/) -- [symbol encoder](https://symbolfyi.com/search/), [HTML entity collections](https://symbolfyi.com/collection/), [Unicode blocks](https://symbolfyi.com/search/)

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/symbolfyi/main/demo.gif" alt="symbolfyi CLI demo" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You Can Do](#what-you-can-do)
  - [Symbol Encoding](#symbol-encoding)
  - [Unicode Properties](#unicode-properties)
- [CLI](#cli)
- [MCP Server](#mcp-server)
- [API Client](#api-client)
- [API Reference](#api-reference)
  - [Core Functions](#core-functions)
  - [Data Types](#data-types)
  - [Constants](#constants)
- [Features](#features)
- [Learn More About Symbols](#learn-more-about-symbols)
- [Creative FYI Family](#creative-fyi-family)
- [License](#license)

## Install

```bash
pip install symbolfyi              # Core (zero dependencies)
pip install "symbolfyi[full]"      # + fonttools for Unicode block/script
pip install "symbolfyi[cli]"       # + CLI (typer, rich)
pip install "symbolfyi[mcp]"       # + MCP server for AI assistants
pip install "symbolfyi[api]"       # + HTTP client for symbolfyi.com API
pip install "symbolfyi[all]"       # Everything
```

## Quick Start

```python
from symbolfyi import get_encodings, get_info, lookup_html_entity

# Encode any character (11 formats)
enc = get_encodings("->")
print(enc.unicode)        # U+2192
print(enc.html_entity)    # &rarr;
print(enc.css)            # \2192
print(enc.javascript)     # \u{2192}
print(enc.utf8_bytes)     # e2 86 92
print(enc.url_encoded)    # %E2%86%92

# Full Unicode properties (requires fonttools for block/script)
info = get_info("*")
print(info.name)          # BLACK SPADE SUIT
print(info.category_name) # Other Symbol
print(info.block)         # Miscellaneous Symbols
print(info.script)        # Common

# HTML entity reverse lookup
char = lookup_html_entity("&hearts;")
print(char)               # (heart character)
```

## What You Can Do

### Symbol Encoding

When working with special characters in web development, you often need the same symbol in different encoding formats -- an HTML entity for markup, a CSS escape for stylesheets, a JavaScript literal for scripts, or raw UTF-8 bytes for server-side processing. The `get_encodings()` function computes all 11 representations from a single character input, covering every major platform and language.

| Format | Example (U+2192 RIGHTWARDS ARROW) | Use Case |
|--------|-----------------------------------|----------|
| Unicode | `U+2192` | Documentation, Unicode charts |
| HTML Decimal | `&#8594;` | HTML numeric character references |
| HTML Hex | `&#x2192;` | HTML hexadecimal references |
| HTML Entity | `&rarr;` | Named HTML entities (51 supported) |
| CSS | `\2192` | CSS `content` property, pseudo-elements |
| JavaScript | `\u{2192}` | ES6+ string literals |
| Python | `\u2192` | Python source code escapes |
| Java | `\u2192` | Java string literals |
| UTF-8 Bytes | `e2 86 92` | Network protocols, file encoding |
| UTF-16 Bytes | `21 92` | Windows APIs, Java internals |
| URL Encoded | `%E2%86%92` | Query strings, URL paths |

```python
from symbolfyi import get_encodings

# Encode any symbol into all 11 representation formats
enc = get_encodings("\u00a9")  # Copyright sign
print(enc.unicode)        # U+00A9
print(enc.html_entity)    # &copy;
print(enc.html_decimal)   # &#169;
print(enc.css)            # \00A9
print(enc.javascript)     # \u{A9}
print(enc.python)         # \u00a9
print(enc.utf8_bytes)     # c2 a9
print(enc.url_encoded)    # %C2%A9
```

Learn more: [Symbol Encoding Tools](https://symbolfyi.com/tools/) · [HTML Entity Collections](https://symbolfyi.com/collection/)

### Unicode Properties

Every character in the Unicode Standard carries a set of properties that describe its behavior and classification. The Unicode General Category (e.g., "Lu" for uppercase letter, "Sm" for math symbol) determines how text processors handle the character. The block identifies which range of the Unicode codespace the character belongs to (e.g., "Arrows", "Mathematical Operators"), while the script property indicates the writing system (e.g., "Latin", "Common"). Bidirectional properties control text layout in mixed left-to-right and right-to-left content.

| Property | Description | Example (U+2665 BLACK HEART SUIT) |
|----------|-------------|-----------------------------------|
| Name | Official Unicode character name | `BLACK HEART SUIT` |
| Category | General category code + name | `So` (Other Symbol) |
| Block | Unicode block range | `Miscellaneous Symbols` |
| Script | Writing system | `Common` |
| Bidirectional | Text direction class | `ON` (Other Neutral) |
| Combining | Combining class value | `0` (Not Reordered) |
| Mirrored | Whether glyph mirrors in RTL | `N` |
| Decomposition | Canonical decomposition | (empty for most symbols) |

```python
from symbolfyi import get_info

# Retrieve full Unicode properties for any character
info = get_info("\u2665")  # Black heart suit
print(info.name)           # BLACK HEART SUIT
print(info.category)       # So
print(info.category_name)  # Other Symbol
print(info.block)          # Miscellaneous Symbols
print(info.script)         # Common
print(info.bidirectional)  # ON

# Access the encodings alongside Unicode properties
print(info.encodings.html_entity)  # &hearts;
print(info.encodings.css)          # \2665
```

Learn more: ## CLI

Requires the `cli` extra: `pip install symbolfyi[cli]`

```bash
# Full symbol info (Unicode properties + all encodings)
symbolfyi info "->"

# Show all 11 encodings
symbolfyi encode "*"

# Reverse HTML entity lookup
symbolfyi entity "&hearts;"
symbolfyi entity amp
```

## MCP Server

Requires the `mcp` extra: `pip install symbolfyi[mcp]`

Add to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "symbolfyi": {
            "command": "python",
            "args": ["-m", "symbolfyi.mcp_server"]
        }
    }
}
```

Available tools:

| Tool | Description |
|------|-------------|
| `symbol_info` | Full Unicode properties + 11 encodings |
| `symbol_encode` | Encode a character into 11 representations |
| `html_entity_lookup` | Reverse HTML entity lookup |

## API Client

Requires the `api` extra: `pip install symbolfyi[api]`

```python
from symbolfyi.api import SymbolFYI

with SymbolFYI() as api:
    # Encode a character
    info = api.encode("->")
    print(info["encodings"]["html_entity"])

    # Search symbols
    results = api.search("arrow")
    for r in results["results"]:
        print(r["character"], r["name"])

    # Browse Unicode blocks
    blocks = api.blocks()
    print(blocks["count"])

    # Get collection details
    arrows = api.collection("arrows")
    print(arrows["name"])
```

Full API documentation at [symbolfyi.com/developers](https://symbolfyi.com/developers/).

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `get_encodings(char) -> EncodingInfo` | Compute 11 encoding representations |
| `get_info(char) -> SymbolInfo \| None` | Full Unicode properties + encodings |
| `get_category_name(code) -> str` | Category code to human name |
| `lookup_html_entity(entity) -> str \| None` | Entity string to character |

### Data Types

- **`EncodingInfo`** -- 11-field NamedTuple: unicode, html_decimal, html_hex, html_entity, css, javascript, python, java, utf8_bytes, utf16_bytes, url_encoded
- **`SymbolInfo`** -- 12-field NamedTuple: codepoint, character, name, category, category_name, block, script, bidirectional, combining, mirrored, decomposition, encodings

### Constants

| Constant | Description |
|----------|-------------|
| `GENERAL_CATEGORIES` | 27 Unicode category codes with names |
| `HTML_ENTITIES` | 51 codepoint-to-entity mappings |
| `HTML_ENTITY_TO_CHAR` | 51 entity-to-character reverse mappings |

## Features

- **11 encoding types**: Unicode, HTML decimal/hex/entity, CSS, JavaScript, Python, Java, UTF-8/UTF-16 bytes, URL-encoded
- **Unicode properties**: name, category, block, script, bidirectional, combining, mirrored, decomposition
- **51 HTML entities**: Common entities with bidirectional lookup
- **Zero required deps**: Core uses only stdlib (`unicodedata`, `urllib.parse`)
- **Optional fonttools**: Install `symbolfyi[full]` for Unicode block and script info
- **CLI**: Rich terminal interface for symbol info, encoding, and entity lookup
- **MCP server**: AI assistant integration with 3 tools
- **API client**: HTTP client for symbolfyi.com REST API
- **Type-safe**: Full type annotations, `py.typed` marker (PEP 561)

## Learn More About Symbols

- **Browse**: [Symbol Search](https://symbolfyi.com/search/) · - **Collections**: [HTML Entities](https://symbolfyi.com/collection/) · - **Guides**: [Glossary](https://symbolfyi.com/glossary/)
- **API**: [REST API Docs](https://symbolfyi.com/developers/) · [OpenAPI Spec](https://symbolfyi.com/api/openapi.json)

## Creative FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem — design, typography, and character encoding.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| colorfyi | [PyPI](https://pypi.org/project/colorfyi/) | [npm](https://www.npmjs.com/package/@fyipedia/colorfyi) | Color conversion, WCAG contrast, harmonies -- [colorfyi.com](https://colorfyi.com/) |
| emojifyi | [PyPI](https://pypi.org/project/emojifyi/) | [npm](https://www.npmjs.com/package/emojifyi) | Emoji encoding & metadata for 3,953 emojis -- [emojifyi.com](https://emojifyi.com/) |
| **symbolfyi** | [PyPI](https://pypi.org/project/symbolfyi/) | [npm](https://www.npmjs.com/package/symbolfyi) | **Symbol encoding in 11 formats -- [symbolfyi.com](https://symbolfyi.com/)** |
| unicodefyi | [PyPI](https://pypi.org/project/unicodefyi/) | [npm](https://www.npmjs.com/package/unicodefyi) | Unicode lookup with 17 encodings -- [unicodefyi.com](https://unicodefyi.com/) |
| fontfyi | [PyPI](https://pypi.org/project/fontfyi/) | [npm](https://www.npmjs.com/package/fontfyi) | Google Fonts metadata & CSS -- [fontfyi.com](https://fontfyi.com/) |

## License

MIT
