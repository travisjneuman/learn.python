"""Tests for Nested Data Flattener.

Covers:
- Flattening simple and nested dicts
- Flattening lists with indices
- Unflattening back to nested structure
- Depth calculation
- File loading with error handling
"""

from pathlib import Path

import pytest

from project import depth, flatten, flatten_from_file, unflatten


def test_flatten_simple_dict() -> None:
    """A flat dict should remain unchanged."""
    data = {"name": "Ada", "age": 36}
    result = flatten(data)
    assert result == {"name": "Ada", "age": 36}


def test_flatten_nested_dict() -> None:
    """Nested keys should become dot-separated paths."""
    data = {"user": {"name": "Ada", "address": {"city": "London"}}}
    result = flatten(data)
    assert result == {
        "user.name": "Ada",
        "user.address.city": "London",
    }


def test_flatten_with_list() -> None:
    """List items should get numeric index keys."""
    data = {"tags": ["python", "code"]}
    result = flatten(data)
    assert result == {"tags.0": "python", "tags.1": "code"}


@pytest.mark.parametrize(
    "separator,expected_key",
    [(".", "a.b"), ("/", "a/b"), ("_", "a_b")],
)
def test_flatten_custom_separator(separator: str, expected_key: str) -> None:
    """Different separators should produce different key formats."""
    data = {"a": {"b": 1}}
    result = flatten(data, separator=separator)
    assert expected_key in result


def test_unflatten_roundtrip() -> None:
    """Flattening then unflattening should recover the original structure."""
    original = {"user": {"name": "Ada", "role": "programmer"}}
    flat = flatten(original)
    restored = unflatten(flat)
    assert restored == original


def test_depth_calculation() -> None:
    """Depth should count nesting levels correctly."""
    assert depth({}) == 0
    assert depth({"a": 1}) == 1
    assert depth({"a": {"b": 1}}) == 2
    assert depth({"a": {"b": {"c": 1}}}) == 3


def test_flatten_from_file(tmp_path: Path) -> None:
    """Loading from a JSON file should produce flattened output."""
    p = tmp_path / "nested.json"
    p.write_text('{"server": {"host": "localhost", "port": 8080}}', encoding="utf-8")
    result = flatten_from_file(p)
    assert result == {"server.host": "localhost", "server.port": 8080}


def test_flatten_from_file_invalid_json(tmp_path: Path) -> None:
    """Non-JSON files should raise ValueError."""
    p = tmp_path / "bad.json"
    p.write_text("not json at all", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        flatten_from_file(p)


def test_flatten_from_file_missing(tmp_path: Path) -> None:
    """Missing files should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        flatten_from_file(tmp_path / "missing.json")
