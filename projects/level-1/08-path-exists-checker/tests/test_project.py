"""Tests for Path Exists Checker."""

from pathlib import Path

from project import check_path, format_size, summary


def test_check_existing_file(tmp_path: Path) -> None:
    f = tmp_path / "test.txt"
    f.write_text("hello", encoding="utf-8")
    result = check_path(str(f))
    assert result["exists"] is True
    assert result["type"] == "file"
    assert result["size_bytes"] == 5


def test_check_existing_directory(tmp_path: Path) -> None:
    result = check_path(str(tmp_path))
    assert result["exists"] is True
    assert result["type"] == "directory"


def test_check_missing_path() -> None:
    result = check_path("/nonexistent/path/to/file.txt")
    assert result["exists"] is False
    assert result["type"] == "missing"


def test_format_size() -> None:
    assert format_size(500) == "500.0 B"
    assert format_size(1024) == "1.0 KB"
    assert format_size(1048576) == "1.0 MB"


def test_summary() -> None:
    results = [
        {"exists": True, "type": "file"},
        {"exists": True, "type": "directory"},
        {"exists": False, "type": "missing"},
    ]
    s = summary(results)
    assert s["existing"] == 2
    assert s["missing"] == 1
