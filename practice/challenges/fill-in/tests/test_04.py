"""Tests for Fill-In Challenge #4 — String Formatter."""

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

_spec = spec_from_file_location("ex04", Path(__file__).parent.parent / "04_string_formatter.py")
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)

left_pad = _mod.left_pad
format_table_row = _mod.format_table_row
build_report = _mod.build_report
truncate = _mod.truncate


class TestLeftPad:
    def test_basic(self):
        assert left_pad("42", 5, "0") == "00042"

    def test_already_long(self):
        assert left_pad("hello", 3) == "hello"

    def test_default_char(self):
        assert left_pad("x", 4) == "   x"

    def test_exact_width(self):
        assert left_pad("abc", 3) == "abc"


class TestFormatTableRow:
    def test_basic(self):
        result = format_table_row(["Name", "Age"], [10, 5])
        assert result == "Name       | Age  "

    def test_single_column(self):
        result = format_table_row(["Hi"], [6])
        assert result == "Hi    "

    def test_long_value(self):
        result = format_table_row(["Hello World"], [5])
        assert result == "Hello World"


class TestBuildReport:
    def test_basic(self):
        report = build_report("Scores", [("Alice", 95), ("Bob", 87)])
        assert "=== Scores ===" in report
        assert "Alice" in report
        assert "95" in report
        assert "Bob" in report
        assert "87" in report

    def test_empty(self):
        report = build_report("Empty", [])
        assert "=== Empty ===" in report


class TestTruncate:
    def test_short_enough(self):
        assert truncate("Hi", 10) == "Hi"

    def test_truncated(self):
        assert truncate("Hello, world!", 10) == "Hello, ..."

    def test_exact_length(self):
        assert truncate("Hello", 5) == "Hello"

    def test_custom_suffix(self):
        assert truncate("abcdefgh", 6, "~") == "abcde~"
