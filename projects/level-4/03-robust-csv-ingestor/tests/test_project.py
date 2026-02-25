"""Tests for Robust CSV Ingestor."""

from pathlib import Path
import csv
import json
import pytest

from project import validate_row, ingest_csv, run


@pytest.mark.parametrize(
    "row, expected_cols, should_pass",
    [
        (["Alice", "30", "NYC"], 3, True),       # correct columns
        (["Bob", "25"], 3, False),                # too few columns
        (["Eve", "28", "LA", "extra"], 3, False), # too many columns
        (["", "", ""], 3, False),                  # all empty
        (["Alice", "", "NYC"], 3, True),           # one empty is OK
    ],
)
def test_validate_row(row: list[str], expected_cols: int, should_pass: bool) -> None:
    result = validate_row(row, expected_cols, row_num=1)
    if should_pass:
        assert result is None
    else:
        assert result is not None


def test_ingest_csv_separates_good_and_bad(tmp_path: Path) -> None:
    """Good rows go to clean file, bad rows go to quarantine."""
    input_file = tmp_path / "input.csv"
    input_file.write_text(
        "name,age,city\nAlice,30,NYC\nBob,25\nCharlie,28,LA\n",
        encoding="utf-8",
    )

    good = tmp_path / "good.csv"
    bad = tmp_path / "bad.csv"
    summary = ingest_csv(input_file, good, bad)

    assert summary["good"] == 2
    assert summary["quarantined"] == 1
    assert good.exists()
    assert bad.exists()


def test_ingest_csv_empty_file(tmp_path: Path) -> None:
    input_file = tmp_path / "empty.csv"
    input_file.write_text("", encoding="utf-8")

    summary = ingest_csv(
        input_file, tmp_path / "g.csv", tmp_path / "b.csv"
    )
    assert summary["total_rows"] == 0


def test_run_creates_all_outputs(tmp_path: Path) -> None:
    """Integration: run() creates clean CSV, quarantine CSV, and JSON report."""
    input_file = tmp_path / "data.csv"
    input_file.write_text(
        "id,value\n1,hello\n2\n3,world\n",
        encoding="utf-8",
    )
    output_dir = tmp_path / "output"
    summary = run(input_file, output_dir)

    assert (output_dir / "clean_data.csv").exists()
    assert (output_dir / "quarantined_rows.csv").exists()
    assert (output_dir / "ingestion_report.json").exists()
    assert summary["good"] + summary["quarantined"] == summary["total_rows"]


def test_ingest_csv_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        ingest_csv(tmp_path / "nope.csv", tmp_path / "g.csv", tmp_path / "b.csv")
