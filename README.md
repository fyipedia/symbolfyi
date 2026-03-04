# symbolfyi

[![PyPI](https://img.shields.io/pypi/v/symbolfyi)](https://pypi.org/project/symbolfyi/)
[![Python](https://img.shields.io/pypi/pyversions/symbolfyi)](https://pypi.org/project/symbolfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python symbol & character encoding toolkit. Compute 11 encoding representations and full Unicode properties for any character. Includes 51 HTML entity mappings.

> Look up any symbol at [symbolfyi.com](https://symbolfyi.com/)

## Install

```bash
pip install symbolfyi              # Core (zero deps)
pip install "symbolfyi[full]"      # + fonttools for Unicode block/script
```

## Quick Start

```python
from symbolfyi import get_encodings, get_info, lookup_html_entity

# Encode any character (11 formats)
enc = get_encodings("→")
print(enc.unicode)        # U+2192
print(enc.html_entity)    # &rarr;
print(enc.css)            # \2192
print(enc.javascript)     # \u{2192}
print(enc.utf8_bytes)     # e2 86 92
print(enc.url_encoded)    # %E2%86%92

# Full Unicode properties (requires fonttools for block/script)
info = get_info("♠")
print(info.name)          # BLACK SPADE SUIT
print(info.category_name) # Other Symbol
print(info.block)         # Miscellaneous Symbols
print(info.script)        # Common

# HTML entity reverse lookup
char = lookup_html_entity("&hearts;")
print(char)               # ♥
```

## API Reference

### Core Functions

| Function | Description |
|----------|-------------|
| `get_encodings(char) -> EncodingInfo` | Compute 11 encoding representations |
| `get_info(char) -> SymbolInfo \| None` | Full Unicode properties + encodings |
| `get_category_name(code) -> str` | Category code to human name |
| `lookup_html_entity(entity) -> str \| None` | Entity string to character |

### Data Types

- **`EncodingInfo`** — 11-field NamedTuple: unicode, html_decimal, html_hex, html_entity, css, javascript, python, java, utf8_bytes, utf16_bytes, url_encoded
- **`SymbolInfo`** — 12-field NamedTuple: codepoint, character, name, category, category_name, block, script, bidirectional, combining, mirrored, decomposition, encodings

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
- **Type-safe**: Full type annotations, `py.typed` marker (PEP 561)

## Related Packages

| Package | Description |
|---------|-------------|
| [unicodefyi](https://github.com/fyipedia/unicodefyi) | Extended Unicode toolkit with 17 encodings + character search |
| [colorfyi](https://github.com/fyipedia/colorfyi) | Color conversion, contrast, harmonies, shades |
| [emojifyi](https://github.com/fyipedia/emojifyi) | Emoji encoding & metadata for 3,781 emojis |
| [fontfyi](https://github.com/fyipedia/fontfyi) | Google Fonts metadata, CSS helpers, font pairings |

## Links

- [Symbol Browser](https://symbolfyi.com/) — Look up any symbol online
- [API Documentation](https://symbolfyi.com/developers/) — REST API with free access
- [Source Code](https://github.com/fyipedia/symbolfyi)

## License

MIT
