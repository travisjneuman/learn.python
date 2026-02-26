"""Tests for First File Reader."""

import os

import pytest

from project import file_summary, format_with_line_numbers, read_file_lines


def test_read_file_lines_basic(tmp_path) -> None:
    """Reading a simple file should return each line."""
    f = tmp_path / "test.txt"
    f.write_text("line one\nline two\nline three\n", encoding="utf-8")
    lines = read_file_lines(str(f))
    assert len(lines) == 3
    assert lines[0] == "line one"


def test_read_file_lines_missing_raises(tmp_path) -> None:
    """A missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_file_lines(str(tmp_path / "nope.txt"))


def test_format_with_line_numbers() -> None:
    """Each line should be prefixed with its line number."""
    lines = ["alpha", "beta", "gamma"]
    output = format_with_line_numbers(lines)
    assert "1 | alpha" in output
    assert "3 | gamma" in output


def test_format_empty_file() -> None:
    """An empty file should produce an '(empty file)' message."""
    assert format_with_line_numbers([]) == "(empty file)"


def test_file_summary_counts(tmp_path) -> None:
    """The summary should have correct line and word counts."""
    f = tmp_path / "data.txt"
    f.write_text("hello world\ngoodbye world\n", encoding="utf-8")
    lines = read_file_lines(str(f))
    summary = file_summary(str(f), lines)
    assert summary["lines"] == 2
    assert summary["words"] == 4
    assert summary["non_empty_lines"] == 2
