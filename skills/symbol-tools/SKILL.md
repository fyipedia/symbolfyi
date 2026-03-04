---
name: symbol-tools
description: Encode any Unicode symbol into 11 formats (HTML, CSS, JS, Python, Java, UTF-8, UTF-16, URL), look up Unicode properties, resolve HTML entities.
---

# Symbol Tools

Unicode symbol encoding and property lookup powered by [symbolfyi](https://symbolfyi.com/) -- a pure Python symbol encoder supporting 11 encoding formats with zero dependencies.

## Setup

Install the MCP server:

```bash
pip install "symbolfyi[mcp]"
```

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

## Available Tools

| Tool | Description |
|------|-------------|
| `symbol_info` | Full Unicode properties (name, category, block, script) + all encodings |
| `symbol_encode` | Encode any character into 11 formats (HTML decimal/hex/entity, CSS, JS, Python, Java, UTF-8, UTF-16, URL) |
| `html_entity_lookup` | Reverse lookup -- find the character for an HTML entity name |

## When to Use

- Encoding special characters for HTML, CSS, or JavaScript
- Looking up Unicode properties (category, block, script, bidirectional class)
- Finding HTML entities for symbols (arrows, math operators, currency signs)
- Converting between encoding formats for cross-platform compatibility

## Links

- [Symbol Encoder](https://symbolfyi.com/symbols/)
- [Unicode Collections](https://symbolfyi.com/collections/)
- [API Documentation](https://symbolfyi.com/developers/)
- [PyPI Package](https://pypi.org/project/symbolfyi/)
