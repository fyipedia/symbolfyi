# symbolfyi

[![PyPI](https://img.shields.io/pypi/v/symbolfyi)](https://pypi.org/project/symbolfyi/)
[![Python](https://img.shields.io/pypi/pyversions/symbolfyi)](https://pypi.org/project/symbolfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python symbol encoder for developers. Compute 11 encoding representations and full Unicode properties for any character. Includes 51 HTML entity mappings, a CLI, MCP server for AI assistants, and an API client for [symbolfyi.com](https://symbolfyi.com/).

> Look up any symbol at [symbolfyi.com](https://symbolfyi.com/) -- [symbol encoder](https://symbolfyi.com/search/), [HTML entity collections](https://symbolfyi.com/collection/), [Unicode blocks](https://symbolfyi.com/search/)

<p align="center">
  <img src="demo.gif" alt="symbolfyi CLI demo" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [CLI](#cli)
- [MCP Server](#mcp-server)
- [API Client](#api-client)
- [API Reference](#api-reference)
  - [Core Functions](#core-functions)
  - [Data Types](#data-types)
  - [Constants](#constants)
- [Features](#features)
- [Learn More About Symbols](#learn-more-about-symbols)
- [FYIPedia Developer Tools](#fyipedia-developer-tools)
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

## CLI

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

- **Browse**: [Symbol Search](https://symbolfyi.com/search/) · [Unicode Blocks](https://symbolfyi.com/block/)
- **Collections**: [HTML Entities](https://symbolfyi.com/collection/) · [Math Symbols](https://symbolfyi.com/collection/math/) · [Currency Symbols](https://symbolfyi.com/collection/currency/)
- **Guides**: [Glossary](https://symbolfyi.com/glossary/)
- **API**: [REST API Docs](https://symbolfyi.com/developers/) · [OpenAPI Spec](https://symbolfyi.com/api/openapi.json)

## FYIPedia Developer Tools

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| colorfyi | [PyPI](https://pypi.org/project/colorfyi/) | [npm](https://www.npmjs.com/package/@fyipedia/colorfyi) | Color conversion, WCAG contrast, harmonies -- [colorfyi.com](https://colorfyi.com/) |
| emojifyi | [PyPI](https://pypi.org/project/emojifyi/) | [npm](https://www.npmjs.com/package/emojifyi) | Emoji encoding & metadata for 3,781 emojis -- [emojifyi.com](https://emojifyi.com/) |
| **symbolfyi** | [PyPI](https://pypi.org/project/symbolfyi/) | [npm](https://www.npmjs.com/package/symbolfyi) | Symbol encoding in 11 formats -- [symbolfyi.com](https://symbolfyi.com/) |
| unicodefyi | [PyPI](https://pypi.org/project/unicodefyi/) | [npm](https://www.npmjs.com/package/unicodefyi) | Unicode lookup with 17 encodings -- [unicodefyi.com](https://unicodefyi.com/) |
| fontfyi | [PyPI](https://pypi.org/project/fontfyi/) | [npm](https://www.npmjs.com/package/fontfyi) | Google Fonts metadata & CSS -- [fontfyi.com](https://fontfyi.com/) |
| distancefyi | [PyPI](https://pypi.org/project/distancefyi/) | [npm](https://www.npmjs.com/package/distancefyi) | Haversine distance & travel times -- [distancefyi.com](https://distancefyi.com/) |
| timefyi | [PyPI](https://pypi.org/project/timefyi/) | [npm](https://www.npmjs.com/package/timefyi) | Timezone ops & business hours -- [timefyi.com](https://timefyi.com/) |
| namefyi | [PyPI](https://pypi.org/project/namefyi/) | [npm](https://www.npmjs.com/package/namefyi) | Korean romanization & Five Elements -- [namefyi.com](https://namefyi.com/) |
| unitfyi | [PyPI](https://pypi.org/project/unitfyi/) | [npm](https://www.npmjs.com/package/unitfyi) | Unit conversion, 220 units -- [unitfyi.com](https://unitfyi.com/) |
| holidayfyi | [PyPI](https://pypi.org/project/holidayfyi/) | [npm](https://www.npmjs.com/package/holidayfyi) | Holiday dates & Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |
| cocktailfyi | [PyPI](https://pypi.org/project/cocktailfyi/) | -- | Cocktail ABV, calories, flavor -- [cocktailfyi.com](https://cocktailfyi.com/) |
| fyipedia | [PyPI](https://pypi.org/project/fyipedia/) | -- | Unified CLI: `fyi color info FF6B35` -- [fyipedia.com](https://fyipedia.com/) |
| fyipedia-mcp | [PyPI](https://pypi.org/project/fyipedia-mcp/) | -- | Unified MCP hub for AI assistants -- [fyipedia.com](https://fyipedia.com/) |

## License

MIT
