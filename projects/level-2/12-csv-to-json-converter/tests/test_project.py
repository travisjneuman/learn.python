"""Tests for CSV to JSON Converter.

Covers:
- Delimiter detection
- Type inference (int, float, bool, null, str)
- CSV parsing (objects and columns format)
- File conversion
- Edge cases
"""

from pathlib import Path

import pytest

from project import (
    convert_file,
    csv_to_json_columns,
    csv_to_json_objects,
    detect_delimiter,
    infer_type,
    parse_csv,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("42", 42),
        ("3.14", 3.14),
        ("true", True),
        ("false", False),
        ("yes", True),
        ("hello", "hello"),
        ("", None),
        ("null", None),
        ("N/A", None),
    ],
)
def test_infer_type(value: str, expected: object) -> None:
    """Type inference should convert strings to appropriate Python types."""
    assert infer_type(value) == expected


def test_detect_delimiter_comma() -> None:
    """Comma-separated header should detect comma."""
    assert detect_delimiter("name,age,city") == ","


def test_detect_delimiter_tab() -> None:
    """Tab-separated header should detect tab."""
    assert detect_delimiter("name\tage\tcity") == "\t"


def test_detect_delimiter_semicolon() -> None:
    """Semicolon-separated header should detect semicolon."""
    assert detect_delimiter("name;age;city") == ";"


def test_parse_csv_basic() -> None:
    """Basic CSV should produce correct headers and records."""
    text = "name,age,active\nAlice,30,true\nBob,25,false"
    headers, records = parse_csv(text)
    assert headers == ["name", "age", "active"]
    assert len(records) == 2
    assert records[0]["name"] == "Alice"
    assert records[0]["age"] == 30
    assert records[0]["active"] is True


def test_parse_csv_no_type_inference() -> None:
    """With infer_types=False, all values should remain strings."""
    text = "name,age\nAlice,30"
    _, records = parse_csv(text, infer_types=False)
    assert records[0]["age"] == "30"  # string, not int


def test_csv_to_json_objects() -> None:
    """Array-of-objects format should produce a list of dicts."""
    text = "name,score\nAlice,95\nBob,87"
    result = csv_to_json_objects(text)
    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[0]["score"] == 95


def test_csv_to_json_columns() -> None:
    """Columnar format should produce a dict of lists."""
    text = "name,score\nAlice,95\nBob,87"
    result = csv_to_json_columns(text)
    assert result["name"] == ["Alice", "Bob"]
    assert result["score"] == [95, 87]


def test_convert_file(tmp_path: Path) -> None:
    """Full file conversion should work end to end."""
    p = tmp_path / "data.csv"
    p.write_text("item,price,in_stock\nWidget,9.99,true\nGadget,19.99,false\n",
                 encoding="utf-8")
    result = convert_file(p)
    assert result["row_count"] == 2
    assert result["headers"] == ["item", "price", "in_stock"]


def test_convert_file_missing(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        convert_file(tmp_path / "nope.csv")


def test_parse_csv_short_rows() -> None:
    """Rows with fewer values than headers should be padded."""
    text = "a,b,c\n1,2\n4,5,6"
    _, records = parse_csv(text)
    assert records[0]["c"] is None  # padded empty -> None
    assert records[1]["c"] == 6
