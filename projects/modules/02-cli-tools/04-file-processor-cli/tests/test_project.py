"""Tests for Module 02 / Project 04 — File Processor CLI.

Tests the analyze_file() and format_report() functions directly, and
the CLI command via CliRunner. Temporary files are used to keep tests
deterministic and self-contained.

WHY test functions separately from the CLI?
- analyze_file() and format_report() are pure logic — testing them directly
  is simpler and gives faster feedback when something breaks.
- The CLI test covers the integration (argument parsing, progress bar, etc.).
"""

import sys
import os
from pathlib import Path

import pytest
from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import analyze_file, format_report, process


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_dir(tmp_path):
    """Create a temporary directory with two text files for testing.

    Returns the directory path. The files have known content so we can
    predict exact word counts and line lengths.
    """
    file1 = tmp_path / "file_a.txt"
    file1.write_text("hello world\nfoo bar baz\n", encoding="utf-8")

    file2 = tmp_path / "file_b.txt"
    file2.write_text("one two three four\n", encoding="utf-8")

    return tmp_path


# ---------------------------------------------------------------------------
# Tests for analyze_file()
# ---------------------------------------------------------------------------

def test_analyze_file_word_count(tmp_path):
    """analyze_file() should count all whitespace-separated words in the file.

    'hello world foo' has 3 words.
    """
    filepath = tmp_path / "test.txt"
    filepath.write_text("hello world foo\n", encoding="utf-8")

    result = analyze_file(filepath)

    assert result["word_count"] == 3


def test_analyze_file_longest_line(tmp_path):
    """analyze_file() should find the character count of the longest line.

    'short' (5 chars) vs 'a longer line' (13 chars) -> longest = 13.
    """
    filepath = tmp_path / "test.txt"
    filepath.write_text("short\na longer line\n", encoding="utf-8")

    result = analyze_file(filepath)

    assert result["longest_line"] == 13


def test_analyze_file_avg_line_length(tmp_path):
    """analyze_file() should compute the average line length in characters.

    Two lines of 5 and 3 chars: average = (5 + 3) / 2 = 4.0
    """
    filepath = tmp_path / "test.txt"
    filepath.write_text("12345\n123\n", encoding="utf-8")

    result = analyze_file(filepath)

    assert result["avg_line_length"] == 4.0


def test_analyze_file_filename(tmp_path):
    """analyze_file() should include the filename (not the full path) in results."""
    filepath = tmp_path / "myfile.txt"
    filepath.write_text("content\n", encoding="utf-8")

    result = analyze_file(filepath)

    assert result["filename"] == "myfile.txt"


def test_analyze_file_empty_file(tmp_path):
    """analyze_file() should handle empty files without crashing.

    An empty file has 0 words, 0 longest line, and 0.0 avg line length.
    """
    filepath = tmp_path / "empty.txt"
    filepath.write_text("", encoding="utf-8")

    result = analyze_file(filepath)

    assert result["word_count"] == 0
    assert result["longest_line"] == 0
    assert result["avg_line_length"] == 0.0


# ---------------------------------------------------------------------------
# Tests for format_report()
# ---------------------------------------------------------------------------

def test_format_report_includes_filenames():
    """format_report() should include each file's name in the output."""
    results = [
        {"filename": "alpha.txt", "word_count": 10, "longest_line": 20, "avg_line_length": 15.0},
        {"filename": "beta.txt", "word_count": 5, "longest_line": 10, "avg_line_length": 8.0},
    ]

    report = format_report(results)

    assert "alpha.txt" in report
    assert "beta.txt" in report


def test_format_report_includes_total_words():
    """format_report() should show the total word count across all files."""
    results = [
        {"filename": "a.txt", "word_count": 10, "longest_line": 5, "avg_line_length": 5.0},
        {"filename": "b.txt", "word_count": 20, "longest_line": 5, "avg_line_length": 5.0},
    ]

    report = format_report(results)

    assert "30" in report  # 10 + 20 = 30 total words


def test_format_report_includes_file_count():
    """format_report() should show the total number of files processed."""
    results = [
        {"filename": "a.txt", "word_count": 5, "longest_line": 5, "avg_line_length": 5.0},
    ]

    report = format_report(results)

    assert "1" in report


# ---------------------------------------------------------------------------
# Tests for the CLI command
# ---------------------------------------------------------------------------

def test_cli_processes_directory(sample_dir):
    """The CLI should process all .txt files in the given directory."""
    runner = CliRunner()
    result = runner.invoke(process, ["--directory", str(sample_dir)])

    assert result.exit_code == 0
    assert "file_a.txt" in result.output
    assert "file_b.txt" in result.output


def test_cli_saves_output_file(sample_dir, tmp_path):
    """The --output flag should write the report to a file."""
    output_file = str(tmp_path / "report.txt")
    runner = CliRunner()
    result = runner.invoke(process, ["--directory", str(sample_dir), "--output", output_file])

    assert result.exit_code == 0
    assert os.path.exists(output_file)


def test_cli_no_matching_files(tmp_path):
    """If no files match the pattern, the CLI should report it gracefully."""
    runner = CliRunner()
    result = runner.invoke(process, ["--directory", str(tmp_path), "--pattern", "*.xyz"])

    assert result.exit_code == 0
    assert "No files" in result.output
