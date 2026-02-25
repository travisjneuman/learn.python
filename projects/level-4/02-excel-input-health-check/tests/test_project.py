"""Tests for Excel Input Health Check."""

from pathlib import Path
import pytest

from project import (
    detect_delimiter,
    check_headers,
    check_row_completeness,
    check_empty_columns,
    health_check,
)


@pytest.mark.parametrize(
    "lines, expected",
    [
        (["a,b,c", "1,2,3"], ","),
        (["a\tb\tc", "1\t2\t3"], "\t"),
        (["a;b;c", "1;2;3"], ";"),
        (["a|b|c", "1|2|3"], "|"),
    ],
)
def test_detect_delimiter(lines: list[str], expected: str) -> None:
    assert detect_delimiter(lines) == expected


def test_check_headers_detects_blanks_and_dupes() -> None:
    rows = [["name", "", "name", "age"]]
    result = check_headers(rows)
    assert result["present"] is True
    assert len(result["issues"]) == 2  # one blank, one duplicate


def test_check_row_completeness_finds_short_rows() -> None:
    rows = [
        ["a", "b", "c"],
        ["1", "2", "3"],
        ["4", "5"],          # short — only 2 columns
        ["6", "7", "8", "9"],  # long — 4 columns
    ]
    result = check_row_completeness(rows)
    assert result["short_rows"] == [3]
    assert result["long_rows"] == [4]


def test_check_empty_columns() -> None:
    rows = [
        ["a", "b", "c"],
        ["1", "", "3"],
        ["2", "", "4"],
    ]
    assert check_empty_columns(rows) == [1]


def test_health_check_ok_file(tmp_path: Path) -> None:
    csv_file = tmp_path / "good.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25\n", encoding="utf-8")
    report = health_check(csv_file)
    assert report["status"] == "OK"
    assert report["completeness"]["data_rows"] == 2


def test_health_check_empty_file(tmp_path: Path) -> None:
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")
    report = health_check(csv_file)
    assert report["status"] == "FAIL"
