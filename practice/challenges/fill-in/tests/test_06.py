"""Tests for Fill-In Challenge #6 — Error Handler."""

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

_spec = spec_from_file_location("ex06", Path(__file__).parent.parent / "06_error_handler.py")
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)

safe_divide = _mod.safe_divide
safe_int = _mod.safe_int
safe_key_access = _mod.safe_key_access
process_records = _mod.process_records


class TestSafeDivide:
    def test_basic(self):
        assert safe_divide(10, 2) == 5.0

    def test_zero(self):
        assert safe_divide(10, 0) is None

    def test_float(self):
        result = safe_divide(7, 3)
        assert abs(result - 2.3333333) < 0.001


class TestSafeInt:
    def test_string(self):
        assert safe_int("42") == 42

    def test_invalid(self):
        assert safe_int("hello") is None

    def test_float(self):
        assert safe_int(3.7) == 3

    def test_none(self):
        assert safe_int(None) is None


class TestSafeKeyAccess:
    def test_basic(self):
        d = {"user": {"name": "Alice", "age": 25}}
        assert safe_key_access(d, "user", "name") == "Alice"

    def test_missing(self):
        d = {"user": {"name": "Alice"}}
        assert safe_key_access(d, "user", "email") is None

    def test_top_level_missing(self):
        assert safe_key_access({}, "missing") is None

    def test_single_key(self):
        assert safe_key_access({"a": 1}, "a") == 1


class TestProcessRecords:
    def test_all_valid(self):
        records = [{"name": "A", "score": "95"}, {"name": "B", "score": "87.5"}]
        successes, errors = process_records(records)
        assert len(successes) == 2
        assert successes[0] == {"name": "A", "score": 95.0}
        assert len(errors) == 0

    def test_some_invalid(self):
        records = [{"name": "A", "score": "95"}, {"name": "B", "score": "N/A"}]
        successes, errors = process_records(records)
        assert len(successes) == 1
        assert len(errors) == 1
        assert errors[0]["name"] == "B"
        assert "error" in errors[0]

    def test_empty(self):
        successes, errors = process_records([])
        assert successes == []
        assert errors == []
