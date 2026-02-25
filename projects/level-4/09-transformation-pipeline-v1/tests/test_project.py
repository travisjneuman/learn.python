"""Tests for Transformation Pipeline V1."""

from pathlib import Path
import pytest

from project import (
    transform_strip_whitespace,
    transform_lowercase_keys,
    transform_add_row_id,
    transform_filter_empty_rows,
    transform_coerce_numbers,
    run_pipeline,
    run,
)


def test_strip_whitespace() -> None:
    records = [{"name": "  Alice  ", "city": "NYC "}]
    result = transform_strip_whitespace(records)
    assert result[0]["name"] == "Alice"
    assert result[0]["city"] == "NYC"


def test_lowercase_keys() -> None:
    records = [{"Name": "Alice", "AGE": 30}]
    result = transform_lowercase_keys(records)
    assert "name" in result[0]
    assert "age" in result[0]


def test_add_row_id() -> None:
    records = [{"a": 1}, {"a": 2}]
    result = transform_add_row_id(records)
    assert result[0]["row_id"] == 1
    assert result[1]["row_id"] == 2


def test_filter_empty_rows() -> None:
    records = [{"a": "x"}, {"a": "", "b": ""}, {"a": "y"}]
    result = transform_filter_empty_rows(records)
    assert len(result) == 2


@pytest.mark.parametrize(
    "value, expected_type",
    [
        ("42", int),
        ("3.14", float),
        ("hello", str),
    ],
)
def test_coerce_numbers(value: str, expected_type: type) -> None:
    records = [{"val": value}]
    result = transform_coerce_numbers(records)
    assert isinstance(result[0]["val"], expected_type)


def test_run_pipeline_logs_steps() -> None:
    records = [{"Name": " Alice ", "Age": "30"}]
    result, log = run_pipeline(records, ["strip_whitespace", "lowercase_keys", "coerce_numbers"])
    assert len(log) == 3
    assert all(s["status"] == "ok" for s in log)
    assert result[0]["name"] == "Alice"
    assert result[0]["age"] == 30


def test_run_pipeline_skips_unknown() -> None:
    records = [{"a": "1"}]
    _, log = run_pipeline(records, ["nonexistent_step"])
    assert log[0]["status"] == "skipped"


def test_run_integration(tmp_path: Path) -> None:
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("Name,Age\n Alice ,30\n Bob ,25\n", encoding="utf-8")
    output = tmp_path / "out.json"
    report = run(csv_file, output, ["strip_whitespace", "coerce_numbers"])
    assert output.exists()
    assert report["output_records"] == 2
