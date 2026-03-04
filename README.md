# symbolfyi

[![PyPI](https://img.shields.io/pypi/v/symbolfyi)](https://pypi.org/project/symbolfyi/)
[![Python](https://img.shields.io/pypi/pyversions/symbolfyi)](https://pypi.org/project/symbolfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python symbol encoder for developers. Compute 11 encoding representations and full Unicode properties for any character. Includes 51 HTML entity mappings, a CLI, MCP server for AI assistants, and an API client for [symbolfyi.com](https://symbolfyi.com/).

> Look up any symbol at [symbolfyi.com](https://symbolfyi.com/) -- [symbol encoder](https://symbolfyi.com/symbols/), [HTML entity collections](https://symbolfyi.com/collections/), [Unicode blocks](https://symbolfyi.com/blocks/)

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
symbolfyi info "->""

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

## FYIPedia Packages

| Package | Description |
|---------|-------------|
| [colorfyi](https://colorfyi.com/) | [Hex to RGB converter](https://colorfyi.com/tools/converter/), [WCAG contrast checker](https://colorfyi.com/tools/contrast-checker/) |
| [emojifyi](https://emojifyi.com/) | [Emoji encoding](https://emojifyi.com/developers/) & metadata for 3,953 Unicode emojis |
| **symbolfyi** | [Symbol encoder](https://symbolfyi.com/developers/) -- 11 encoding formats for any character |
| [unicodefyi](https://unicodefyi.com/) | [Unicode character lookup](https://unicodefyi.com/developers/) -- 17 encodings |
| [fontfyi](https://fontfyi.com/) | [Google Fonts explorer](https://fontfyi.com/developers/) -- metadata, CSS, pairings |
| [distancefyi](https://pypi.org/project/distancefyi/) | Haversine distance, bearing, travel times -- [distancefyi.com](https://distancefyi.com/) |
| [timefyi](https://pypi.org/project/timefyi/) | Timezone operations, time differences -- [timefyi.com](https://timefyi.com/) |
| [namefyi](https://pypi.org/project/namefyi/) | Korean romanization, Five Elements -- [namefyi.com](https://namefyi.com/) |
| [unitfyi](https://pypi.org/project/unitfyi/) | Unit conversion, 200 units, 20 categories -- [unitfyi.com](https://unitfyi.com/) |
| [holidayfyi](https://pypi.org/project/holidayfyi/) | Holiday dates, Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |

## Links

- [Symbol Browser](https://symbolfyi.com/) -- Look up any symbol online
- [Symbol Encoder](https://symbolfyi.com/symbols/) -- Encode any character into 11 formats
- [HTML Entity Collections](https://symbolfyi.com/collections/) -- Browse curated symbol collections
- [Unicode Blocks](https://symbolfyi.com/blocks/) -- Browse symbols by Unicode block
- [API Documentation](https://symbolfyi.com/developers/) -- REST API with free access
- [Source Code](https://github.com/fyipedia/symbolfyi)

## License

MIT
