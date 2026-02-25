"""Tests for Module 02 / Project 05 — Typer Migration.

Tests the same three subcommands (info, count, head) as Project 02, but
now built with Typer instead of Click. Typer includes its own CliRunner
that works similarly to Click's version.

WHY test both Click and Typer versions?
- Even though the behavior is identical, the internal wiring is different.
- These tests verify that the Typer migration preserved the same behavior.
"""

import sys
import os

import pytest
from typer.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary text file with known content.

    3 lines, 9 words — same structure as the Click version's tests.
    """
    filepath = tmp_path / "sample.txt"
    filepath.write_text("hello world foo\nbar baz qux\nalpha beta gamma\n", encoding="utf-8")
    return str(filepath)


# ---------------------------------------------------------------------------
# Tests for the 'info' subcommand
# ---------------------------------------------------------------------------

def test_info_shows_file_path(sample_file):
    """'info' should display the file path in its output."""
    runner = CliRunner()
    result = runner.invoke(app, ["info", sample_file])

    assert result.exit_code == 0
    assert "sample.txt" in result.output


def test_info_shows_size(sample_file):
    """'info' should display the file size in bytes."""
    runner = CliRunner()
    result = runner.invoke(app, ["info", sample_file])

    assert result.exit_code == 0
    assert "bytes" in result.output


def test_info_shows_modified_date(sample_file):
    """'info' should display the last-modified timestamp."""
    runner = CliRunner()
    result = runner.invoke(app, ["info", sample_file])

    assert result.exit_code == 0
    assert "Modified" in result.output


def test_info_nonexistent_file():
    """'info' should exit with error code 1 for a nonexistent file.

    Unlike Click's Path(exists=True), Typer checks manually and raises typer.Exit(1).
    """
    runner = CliRunner()
    result = runner.invoke(app, ["info", "/nonexistent/path.txt"])

    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# Tests for the 'count' subcommand
# ---------------------------------------------------------------------------

def test_count_shows_lines(sample_file):
    """'count' should display the number of lines in the file."""
    runner = CliRunner()
    result = runner.invoke(app, ["count", sample_file])

    assert result.exit_code == 0
    assert "Lines:" in result.output


def test_count_shows_words(sample_file):
    """'count' should display the number of words in the file."""
    runner = CliRunner()
    result = runner.invoke(app, ["count", sample_file])

    assert result.exit_code == 0
    assert "Words:" in result.output


def test_count_shows_chars(sample_file):
    """'count' should display the character count."""
    runner = CliRunner()
    result = runner.invoke(app, ["count", sample_file])

    assert result.exit_code == 0
    assert "Chars:" in result.output


def test_count_nonexistent_file():
    """'count' should exit with error code 1 for a nonexistent file."""
    runner = CliRunner()
    result = runner.invoke(app, ["count", "/nonexistent/path.txt"])

    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# Tests for the 'head' subcommand
# ---------------------------------------------------------------------------

def test_head_default_lines(sample_file):
    """'head' with no --lines flag should show the first 5 lines (or all if fewer)."""
    runner = CliRunner()
    result = runner.invoke(app, ["head", sample_file])

    assert result.exit_code == 0
    assert "hello world foo" in result.output


def test_head_custom_line_count(sample_file):
    """'head --lines 1' should show only the first line."""
    runner = CliRunner()
    result = runner.invoke(app, ["head", sample_file, "--lines", "1"])

    assert result.exit_code == 0
    assert "hello world foo" in result.output
    assert "bar baz qux" not in result.output


def test_head_short_flag(sample_file):
    """'head -n 2' should work the same as '--lines 2'."""
    runner = CliRunner()
    result = runner.invoke(app, ["head", sample_file, "-n", "2"])

    assert result.exit_code == 0
    assert "hello world foo" in result.output
    assert "bar baz qux" in result.output


def test_head_nonexistent_file():
    """'head' should exit with error code 1 for a nonexistent file."""
    runner = CliRunner()
    result = runner.invoke(app, ["head", "/nonexistent/path.txt"])

    assert result.exit_code == 1
