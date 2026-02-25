"""Tests for CSV First Reader."""

from pathlib import Path

from project import column_stats, detect_numeric_columns, format_table, load_csv


def test_load_csv(tmp_path: Path) -> None:
    f = tmp_path / "data.csv"
    f.write_text("name,age\nAlice,30\nBob,25\n", encoding="utf-8")
    rows = load_csv(f)
    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"


def test_detect_numeric_columns() -> None:
    rows = [{"name": "A", "score": "90"}, {"name": "B", "score": "85"}]
    numeric = detect_numeric_columns(rows)
    assert "score" in numeric
    assert "name" not in numeric


def test_column_stats() -> None:
    rows = [{"val": "10"}, {"val": "20"}, {"val": "30"}]
    stats = column_stats(rows, "val")
    assert stats["min"] == 10.0
    assert stats["max"] == 30.0
    assert stats["average"] == 20.0


def test_format_table_not_empty() -> None:
    rows = [{"a": "1", "b": "2"}]
    table = format_table(rows)
    assert "a" in table
    assert "1" in table
