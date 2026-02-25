"""Tests for Parser With Fixtures.

Demonstrates pytest fixtures that create temporary files
for each input format, keeping tests isolated and repeatable.
"""

from pathlib import Path

import pytest

from project import (
    ParseResult,
    detect_format,
    parse_csv_simple,
    parse_file,
    parse_ini,
    parse_key_value,
)


# --- Fixtures that create temporary test files ---

@pytest.fixture
def ini_file(tmp_path: Path) -> Path:
    """Create a sample INI file."""
    f = tmp_path / "config.ini"
    f.write_text(
        "[database]\n"
        "host = localhost\n"
        "port = 5432\n"
        "\n"
        "[server]\n"
        "debug = true\n",
        encoding="utf-8",
    )
    return f


@pytest.fixture
def kv_file(tmp_path: Path) -> Path:
    """Create a sample key=value file."""
    f = tmp_path / "settings.env"
    f.write_text(
        "# Environment settings\n"
        "APP_NAME=myapp\n"
        "DEBUG=true\n"
        "PORT=8000\n",
        encoding="utf-8",
    )
    return f


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    """Create a sample CSV file."""
    f = tmp_path / "data.csv"
    f.write_text(
        "name, age, city\n"
        "Alice, 30, New York\n"
        "Bob, 25, London\n",
        encoding="utf-8",
    )
    return f


# --- INI parser tests ---

def test_parse_ini_sections() -> None:
    """Should parse sections and key-value pairs."""
    text = "[db]\nhost = localhost\nport = 5432\n"
    result = parse_ini(text)
    assert len(result.sections) == 1
    assert result.sections[0].name == "db"
    assert result.sections[0].entries["host"] == "localhost"


def test_parse_ini_multiple_sections() -> None:
    """Should handle multiple sections."""
    text = "[a]\nx = 1\n[b]\ny = 2\n"
    result = parse_ini(text)
    assert len(result.sections) == 2


def test_parse_ini_comments() -> None:
    """Comments and blank lines should be skipped."""
    text = "# comment\n; another\n[s]\nk = v\n"
    result = parse_ini(text)
    assert len(result.sections) == 1


# --- Key-value parser tests ---

def test_parse_key_value() -> None:
    """Should parse key=value pairs."""
    text = "name=Alice\nage=30\n"
    result = parse_key_value(text)
    assert len(result.records) == 2
    assert result.records[0]["key"] == "name"
    assert result.records[0]["value"] == "Alice"


def test_parse_key_value_custom_delimiter() -> None:
    """Should support custom delimiters."""
    text = "name:Alice\nage:30\n"
    result = parse_key_value(text, delimiter=":")
    assert result.records[0]["value"] == "Alice"


# --- CSV parser tests ---

def test_parse_csv_simple() -> None:
    """Should parse CSV with header row."""
    text = "name,age\nAlice,30\nBob,25\n"
    result = parse_csv_simple(text)
    assert len(result.records) == 2
    assert result.records[0]["name"] == "Alice"


def test_parse_csv_column_mismatch() -> None:
    """Mismatched columns should produce an error."""
    text = "a,b,c\n1,2\n"
    result = parse_csv_simple(text)
    assert len(result.errors) == 1


# --- Format detection ---

def test_detect_ini() -> None:
    assert detect_format("[section]\nkey=val\n") == "ini"


def test_detect_csv() -> None:
    assert detect_format("a,b,c\n1,2,3\n") == "csv"


def test_detect_kv() -> None:
    assert detect_format("key=value\n") == "kv"


# --- File-based integration tests ---

def test_parse_ini_file(ini_file: Path) -> None:
    """Should parse INI from real file."""
    result = parse_file(ini_file, "ini")
    assert result.format == "ini"
    assert len(result.sections) == 2


def test_parse_kv_file(kv_file: Path) -> None:
    """Should parse key-value from real file."""
    result = parse_file(kv_file, "kv")
    assert len(result.records) == 3


def test_parse_csv_file(csv_file: Path) -> None:
    """Should parse CSV from real file."""
    result = parse_file(csv_file, "csv")
    assert len(result.records) == 2


def test_parse_file_auto_detect(ini_file: Path) -> None:
    """Should auto-detect INI format."""
    result = parse_file(ini_file)
    assert result.format == "ini"


def test_parse_file_missing(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_file(tmp_path / "nope.txt")
