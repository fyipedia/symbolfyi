"""MCP server for symbolfyi -- symbol encoding tools for AI assistants.

Requires the ``mcp`` extra: ``pip install symbolfyi[mcp]``

Run as a standalone server::

    python -m symbolfyi.mcp_server

Or configure in ``claude_desktop_config.json``::

    {
        "mcpServers": {
            "symbolfyi": {
                "command": "python",
                "args": ["-m", "symbolfyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("symbolfyi")


@mcp.tool()
def symbol_info(character: str) -> str:
    """Get full Unicode properties and encodings for a character.

    Returns character name, codepoint, category, block, script, bidirectional
    properties, and all 11 encoding representations.

    Args:
        character: A single Unicode character (e.g. "->", "*").
    """
    from symbolfyi import get_info

    info = get_info(character[0])
    if info is None:
        return f"No Unicode info found for: {character!r}"

    enc = info.encodings
    return "\n".join(
        [
            f"## {info.character}  {info.name}",
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| Character | {info.character} |",
            f"| Name | {info.name} |",
            f"| Codepoint | `U+{info.codepoint:04X}` |",
            f"| Category | {info.category} ({info.category_name}) |",
            f"| Block | {info.block or 'N/A'} |",
            f"| Script | {info.script or 'N/A'} |",
            f"| Bidirectional | {info.bidirectional} |",
            f"| Combining | {info.combining} |",
            f"| Mirrored | {'Yes' if info.mirrored else 'No'} |",
            f"| Decomposition | {info.decomposition or '(none)'} |",
            "",
            "### Encodings",
            "",
            "| Encoding | Value |",
            "|----------|-------|",
            f"| Unicode | `{enc.unicode}` |",
            f"| HTML Decimal | `{enc.html_decimal}` |",
            f"| HTML Hex | `{enc.html_hex}` |",
            f"| HTML Entity | `{enc.html_entity or '(none)'}` |",
            f"| CSS | `{enc.css}` |",
            f"| JavaScript | `{enc.javascript}` |",
            f"| Python | `{enc.python}` |",
            f"| Java | `{enc.java}` |",
            f"| UTF-8 Bytes | `{enc.utf8_bytes}` |",
            f"| UTF-16 Bytes | `{enc.utf16_bytes}` |",
            f"| URL Encoded | `{enc.url_encoded}` |",
        ]
    )


@mcp.tool()
def symbol_encode(character: str) -> str:
    """Encode a character into 11 different representations.

    Returns Unicode notation, HTML decimal/hex/entity, CSS, JavaScript,
    Python, Java literals, UTF-8/UTF-16 bytes, and URL encoding.

    Args:
        character: A single Unicode character to encode.
    """
    from symbolfyi import get_encodings

    enc = get_encodings(character[0])

    return "\n".join(
        [
            f"## Encodings for {character[0]}",
            "",
            "| Encoding | Value |",
            "|----------|-------|",
            f"| Unicode | `{enc.unicode}` |",
            f"| HTML Decimal | `{enc.html_decimal}` |",
            f"| HTML Hex | `{enc.html_hex}` |",
            f"| HTML Entity | `{enc.html_entity or '(none)'}` |",
            f"| CSS | `{enc.css}` |",
            f"| JavaScript | `{enc.javascript}` |",
            f"| Python | `{enc.python}` |",
            f"| Java | `{enc.java}` |",
            f"| UTF-8 Bytes | `{enc.utf8_bytes}` |",
            f"| UTF-16 Bytes | `{enc.utf16_bytes}` |",
            f"| URL Encoded | `{enc.url_encoded}` |",
        ]
    )


@mcp.tool()
def html_entity_lookup(entity: str) -> str:
    """Reverse HTML entity lookup -- find the character for an entity name.

    Supports named entities like ``&hearts;``, ``&amp;``, ``&rarr;``, etc.

    Args:
        entity: HTML entity string (e.g. "&hearts;", "&amp;").
    """
    from symbolfyi import lookup_html_entity

    # Normalize: add &...; if missing
    query = entity if entity.startswith("&") else f"&{entity};"

    result = lookup_html_entity(query)
    if result is None:
        return f"HTML entity not found: {query}"

    return "\n".join(
        [
            f"## HTML Entity: {query}",
            "",
            "| Property | Value |",
            "|----------|-------|",
            f"| Entity | `{query}` |",
            f"| Character | {result} |",
            f"| Codepoint | `U+{ord(result):04X}` |",
        ]
    )


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
