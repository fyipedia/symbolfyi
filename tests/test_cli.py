"""Tests for symbolfyi.cli -- command-line interface."""

from __future__ import annotations

from typer.testing import CliRunner

from symbolfyi.cli import app

runner = CliRunner()


class TestCLIInfo:
    def test_info_arrow(self) -> None:
        result = runner.invoke(app, ["info", "\u2192"])
        assert result.exit_code == 0
        assert "RIGHTWARDS ARROW" in result.output

    def test_info_spade(self) -> None:
        result = runner.invoke(app, ["info", "\u2660"])
        assert result.exit_code == 0
        assert "BLACK SPADE SUIT" in result.output
        assert "U+2660" in result.output

    def test_info_control_char(self) -> None:
        result = runner.invoke(app, ["info", "\x00"])
        assert result.exit_code == 1
        assert "No Unicode info" in result.output


class TestCLIEncode:
    def test_encode_arrow(self) -> None:
        result = runner.invoke(app, ["encode", "\u2192"])
        assert result.exit_code == 0
        assert "U+2192" in result.output
        assert "e2 86 92" in result.output

    def test_encode_spade(self) -> None:
        result = runner.invoke(app, ["encode", "\u2660"])
        assert result.exit_code == 0
        assert "U+2660" in result.output
        assert "&spades;" in result.output

    def test_encode_ascii(self) -> None:
        result = runner.invoke(app, ["encode", "A"])
        assert result.exit_code == 0
        assert "U+0041" in result.output


class TestCLIEntity:
    def test_entity_hearts(self) -> None:
        result = runner.invoke(app, ["entity", "&hearts;"])
        assert result.exit_code == 0
        assert "\u2665" in result.output

    def test_entity_without_delimiters(self) -> None:
        result = runner.invoke(app, ["entity", "amp"])
        assert result.exit_code == 0
        assert "&" in result.output

    def test_entity_not_found(self) -> None:
        result = runner.invoke(app, ["entity", "&nonexistent;"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()


class TestCLINoArgs:
    def test_no_args_shows_help(self) -> None:
        result = runner.invoke(app, [])
        # Typer no_args_is_help=True returns exit code 0 or 2 depending on version
        assert result.exit_code in (0, 2)
        assert "Usage" in result.output or "symbolfyi" in result.output.lower()
