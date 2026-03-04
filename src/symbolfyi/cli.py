"""Command-line interface for symbolfyi.

Requires the ``cli`` extra: ``pip install symbolfyi[cli]``

Usage::

    symbolfyi info "->""             # Full symbol info
    symbolfyi encode "->""           # All 11 encodings
    symbolfyi entity "&hearts;"    # Reverse HTML entity lookup
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="symbolfyi",
    help=("Pure Python symbol encoder -- 11 encoding formats for any Unicode character."),
    no_args_is_help=True,
)
console = Console()


@app.command()
def info(
    character: str = typer.Argument(help="Character to look up (e.g. a single symbol)"),
) -> None:
    """Show full Unicode properties for a character."""
    from symbolfyi import get_info

    result = get_info(character[0])
    if result is None:
        console.print(f"[red]No Unicode info found for:[/red] {character!r}")
        raise typer.Exit(code=1)

    table = Table(title=f"{result.character}  {result.name}")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Character", result.character)
    table.add_row("Name", result.name)
    table.add_row("Codepoint", f"U+{result.codepoint:04X}")
    table.add_row("Category", f"{result.category} ({result.category_name})")
    table.add_row("Block", result.block or "(requires fonttools)")
    table.add_row("Script", result.script or "(requires fonttools)")
    table.add_row("Bidirectional", result.bidirectional)
    table.add_row("Combining", str(result.combining))
    table.add_row("Mirrored", "Yes" if result.mirrored else "No")
    table.add_row("Decomposition", result.decomposition or "(none)")

    enc = result.encodings
    table.add_row("Unicode", enc.unicode)
    table.add_row("HTML Decimal", enc.html_decimal)
    table.add_row("HTML Hex", enc.html_hex)
    table.add_row("HTML Entity", enc.html_entity or "(none)")
    table.add_row("CSS", enc.css)
    table.add_row("JavaScript", enc.javascript)
    table.add_row("Python", enc.python)
    table.add_row("Java", enc.java)
    table.add_row("UTF-8 Bytes", enc.utf8_bytes)
    table.add_row("UTF-16 Bytes", enc.utf16_bytes)
    table.add_row("URL Encoded", enc.url_encoded)

    console.print(table)


@app.command()
def encode(
    character: str = typer.Argument(help="Character to encode"),
) -> None:
    """Show all 11 encoding representations for a character."""
    from symbolfyi import get_encodings

    enc = get_encodings(character[0])

    table = Table(title=f"Encodings for {character[0]}")
    table.add_column("Encoding", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Unicode", enc.unicode)
    table.add_row("HTML Decimal", enc.html_decimal)
    table.add_row("HTML Hex", enc.html_hex)
    table.add_row("HTML Entity", enc.html_entity or "(none)")
    table.add_row("CSS", enc.css)
    table.add_row("JavaScript", enc.javascript)
    table.add_row("Python", enc.python)
    table.add_row("Java", enc.java)
    table.add_row("UTF-8 Bytes", enc.utf8_bytes)
    table.add_row("UTF-16 Bytes", enc.utf16_bytes)
    table.add_row("URL Encoded", enc.url_encoded)

    console.print(table)


@app.command()
def entity(
    name: str = typer.Argument(help='HTML entity name (e.g. "&hearts;" or "hearts")'),
) -> None:
    """Reverse HTML entity lookup -- find the character for an entity name."""
    from symbolfyi import lookup_html_entity

    # Normalize: add &...; if missing
    query = name if name.startswith("&") else f"&{name};"

    result = lookup_html_entity(query)
    if result is None:
        console.print(f"[red]HTML entity not found:[/red] {query}")
        raise typer.Exit(code=1)

    table = Table(title=f"HTML Entity: {query}")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value")

    table.add_row("Entity", query)
    table.add_row("Character", result)
    table.add_row("Codepoint", f"U+{ord(result):04X}")

    console.print(table)
