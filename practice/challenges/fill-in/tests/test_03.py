"""Tests for Fill-In Challenge #3 — File Reader."""

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

_spec = spec_from_file_location("ex03", Path(__file__).parent.parent / "03_file_reader.py")
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)

parse_csv_line = _mod.parse_csv_line
parse_key_value = _mod.parse_key_value
parse_table = _mod.parse_table


class TestParseCsvLine:
    def test_basic(self):
        assert parse_csv_line("Alice, 25, Engineer") == ["Alice", "25", "Engineer"]

    def test_no_spaces(self):
        assert parse_csv_line("a,b,c") == ["a", "b", "c"]

    def test_single(self):
        assert parse_csv_line("hello") == ["hello"]

    def test_extra_whitespace(self):
        assert parse_csv_line("  x ,  y  , z  ") == ["x", "y", "z"]


class TestParseKeyValue:
    def test_basic(self):
        text = "name=Alice\nage=25\nrole=admin"
        assert parse_key_value(text) == {"name": "Alice", "age": "25", "role": "admin"}

    def test_with_comments_and_blanks(self):
        text = "name=Alice\n# comment\n\nage=25"
        assert parse_key_value(text) == {"name": "Alice", "age": "25"}

    def test_empty(self):
        assert parse_key_value("") == {}

    def test_value_with_equals(self):
        text = "equation=x=5"
        assert parse_key_value(text) == {"equation": "x=5"}


class TestParseTable:
    def test_basic(self):
        lines = ["name,age", "Alice,25", "Bob,30"]
        expected = [{"name": "Alice", "age": "25"}, {"name": "Bob", "age": "30"}]
        assert parse_table(lines) == expected

    def test_single_row(self):
        lines = ["col", "val"]
        assert parse_table(lines) == [{"col": "val"}]

    def test_header_only(self):
        lines = ["name,age"]
        assert parse_table(lines) == []
