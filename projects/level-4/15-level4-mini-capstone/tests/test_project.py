"""Tests for Level 4 Mini Capstone."""

from pathlib import Path
import json
import pytest

from project import validate_row, transform_row, run_pipeline


@pytest.mark.parametrize(
    "row, required, error_count",
    [
        ({"name": "Alice", "age": "30"}, ["name", "age"], 0),
        ({"name": "Alice"}, ["name", "age"], 1),
        ({"name": "", "age": "30"}, ["name", "age"], 1),
        ({}, ["name", "age"], 2),
    ],
)
def test_validate_row(row: dict, required: list, error_count: int) -> None:
    errors = validate_row(row, required)
    assert len(errors) == error_count


def test_transform_row_normalizes() -> None:
    row = {"  Name  ": "  Alice  ", "Age": "30", "Salary": "95000.50"}
    result = transform_row(row)
    assert result["name"] == "Alice"
    assert result["age"] == 30
    assert result["salary"] == 95000.50


def test_transform_row_handles_non_numeric() -> None:
    row = {"city": "New York"}
    result = transform_row(row)
    assert result["city"] == "New York"


def test_run_pipeline_end_to_end(tmp_path: Path) -> None:
    input_file = tmp_path / "data.csv"
    input_file.write_text(
        "name,age,city\nAlice,30,NYC\n,25,LA\nBob,28,Chicago\n",
        encoding="utf-8",
    )
    output_dir = tmp_path / "output"
    summary = run_pipeline(input_file, output_dir, ["name", "age"])

    assert summary["valid"] == 2
    assert summary["quarantined"] == 1
    assert (output_dir / "valid_data.json").exists()
    assert (output_dir / "quarantined.json").exists()
    assert (output_dir / "manifest.json").exists()


def test_run_pipeline_checkpoint_recovery(tmp_path: Path) -> None:
    """Verify that checkpoint allows resumption."""
    input_file = tmp_path / "data.csv"
    input_file.write_text(
        "name,age\nAlice,30\nBob,25\nCharlie,28\nDiana,32\n",
        encoding="utf-8",
    )
    output_dir = tmp_path / "output"
    cp = tmp_path / "cp.json"

    # Pre-save a checkpoint as if we crashed after 2 rows
    cp.write_text(json.dumps({
        "processed_count": 2,
        "valid": [{"name": "Alice", "age": 30, "_row_num": 1}, {"name": "Bob", "age": 25, "_row_num": 2}],
        "quarantined": [],
    }), encoding="utf-8")

    summary = run_pipeline(input_file, output_dir, ["name", "age"], checkpoint_path=cp)
    assert summary["valid"] == 4  # all 4 rows
    assert not cp.exists()  # checkpoint cleared


def test_run_pipeline_empty_input(tmp_path: Path) -> None:
    input_file = tmp_path / "empty.csv"
    input_file.write_text("name,age\n", encoding="utf-8")
    output_dir = tmp_path / "output"
    summary = run_pipeline(input_file, output_dir, ["name"])
    assert summary["total_rows"] == 0
