"""Tests for Module 02 / Project 02 — Multi-Command CLI.

Tests the three subcommands (info, count, head) using Click's CliRunner.
We use tmp_path to create temporary files with known content so that the
command output is deterministic.

WHY create temporary files?
- The CLI operates on real files (reads them, gets their size, etc.).
- Using tmp_path gives us files with known content and predictable metadata.
- Tests don't depend on any specific files existing on the developer's machine.
"""

import sys
import os

import pytest
from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import cli


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary text file with known content for testing.

    Returns the file path as a string. The file contains 3 lines
    with a total of 9 words.
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
    result = runner.invoke(cli, ["info", sample_file])

    assert result.exit_code == 0
    assert "sample.txt" in result.output


def test_info_shows_file_size(sample_file):
    """'info' should display the file size in bytes.

    We check that 'bytes' appears in the output — the exact number may
    vary slightly between platforms due to line endings.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["info", sample_file])

    assert result.exit_code == 0
    assert "bytes" in result.output


def test_info_shows_modified_date(sample_file):
    """'info' should display the last-modified date in YYYY-MM-DD format."""
    runner = CliRunner()
    result = runner.invoke(cli, ["info", sample_file])

    assert result.exit_code == 0
    assert "Modified" in result.output


def test_info_nonexistent_file():
    """'info' with a nonexistent file should fail with a Click error.

    Click's Path(exists=True) validates the file before the function runs.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["info", "/nonexistent/file.txt"])

    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# Tests for the 'count' subcommand
# ---------------------------------------------------------------------------

def test_count_shows_lines(sample_file):
    """'count' should display the line count. Our sample has 3 lines."""
    runner = CliRunner()
    result = runner.invoke(cli, ["count", sample_file])

    assert result.exit_code == 0
    assert "Lines:" in result.output


def test_count_shows_words(sample_file):
    """'count' should display the word count. Our sample has 9 words."""
    runner = CliRunner()
    result = runner.invoke(cli, ["count", sample_file])

    assert result.exit_code == 0
    assert "Words:" in result.output


def test_count_shows_chars(sample_file):
    """'count' should display the character count."""
    runner = CliRunner()
    result = runner.invoke(cli, ["count", sample_file])

    assert result.exit_code == 0
    assert "Chars:" in result.output


# ---------------------------------------------------------------------------
# Tests for the 'head' subcommand
# ---------------------------------------------------------------------------

def test_head_default_lines(sample_file):
    """'head' with no --lines option should print the first 5 lines (or all if fewer).

    Our sample file has 3 lines, so all 3 should appear.
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["head", sample_file])

    assert result.exit_code == 0
    assert "hello world foo" in result.output
    assert "bar baz qux" in result.output
    assert "alpha beta gamma" in result.output


def test_head_custom_line_count(sample_file):
    """'head --lines 1' should print only the first line of the file."""
    runner = CliRunner()
    result = runner.invoke(cli, ["head", sample_file, "--lines", "1"])

    assert result.exit_code == 0
    assert "hello world foo" in result.output
    # The second line should NOT appear.
    assert "bar baz qux" not in result.output


def test_head_short_flag(sample_file):
    """'head -n 2' should work the same as '--lines 2' (short option)."""
    runner = CliRunner()
    result = runner.invoke(cli, ["head", sample_file, "-n", "2"])

    assert result.exit_code == 0
    assert "hello world foo" in result.output
    assert "bar baz qux" in result.output


# ---------------------------------------------------------------------------
# Tests for the group help
# ---------------------------------------------------------------------------

def test_cli_help_lists_subcommands():
    """The top-level --help should list all three subcommands."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "info" in result.output
    assert "count" in result.output
    assert "head" in result.output
