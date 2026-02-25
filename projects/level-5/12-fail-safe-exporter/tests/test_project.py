"""Tests for Fail Safe Exporter."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import (
    atomic_write_json,
    atomic_write_csv,
    validate_records,
    export_data,
    create_backup,
    run,
)


# ---------- atomic_write_json ----------

def test_atomic_write_json_creates_file(tmp_path: Path) -> None:
    path = tmp_path / "out.json"
    atomic_write_json({"a": 1}, path)
    assert path.exists()
    assert json.loads(path.read_text())["a"] == 1


def test_atomic_write_json_no_tmp_leftover(tmp_path: Path) -> None:
    path = tmp_path / "out.json"
    atomic_write_json([1, 2], path)
    assert not path.with_suffix(".tmp").exists()


# ---------- atomic_write_csv ----------

def test_atomic_write_csv_creates_file(tmp_path: Path) -> None:
    path = tmp_path / "out.csv"
    rows = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    atomic_write_csv(rows, path)
    lines = path.read_text().splitlines()
    assert len(lines) == 3  # header + 2 rows


def test_atomic_write_csv_handles_empty(tmp_path: Path) -> None:
    path = tmp_path / "out.csv"
    atomic_write_csv([], path)
    assert path.read_text() == ""


# ---------- validate_records ----------

@pytest.mark.parametrize("data,expected_errors", [
    ([{"a": 1}], 0),
    ("not a list", 1),
    ([{"a": 1}, "bad"], 1),
    ([], 0),
])
def test_validate_records(data: object, expected_errors: int) -> None:
    errors = validate_records(data)  # type: ignore[arg-type]
    assert len(errors) == expected_errors


# ---------- create_backup ----------

def test_create_backup_copies_file(tmp_path: Path) -> None:
    original = tmp_path / "data.json"
    original.write_text('{"v": 1}')
    backup_path = create_backup(original)
    assert backup_path is not None
    assert backup_path.exists()
    assert json.loads(backup_path.read_text())["v"] == 1


def test_create_backup_returns_none_if_missing(tmp_path: Path) -> None:
    assert create_backup(tmp_path / "nonexistent.json") is None


# ---------- export_data ----------

@pytest.mark.parametrize("fmt", ["json", "csv"])
def test_export_data_formats(tmp_path: Path, fmt: str) -> None:
    data = [{"name": "Alice", "age": "30"}]
    path = tmp_path / f"out.{fmt}"
    result = export_data(data, path, fmt=fmt)
    assert result["status"] == "success"
    assert result["exported"] == 1
    assert path.exists()


def test_export_data_validation_failure(tmp_path: Path) -> None:
    result = export_data("not a list", tmp_path / "out.json")  # type: ignore[arg-type]
    assert result["status"] == "validation_failed"


# ---------- integration: run ----------

def test_run_writes_exported_file(tmp_path: Path) -> None:
    input_file = tmp_path / "data.json"
    input_file.write_text('[{"x": 1}, {"x": 2}]', encoding="utf-8")
    output = tmp_path / "exported.json"
    result = run(input_file, output)
    assert result["exported"] == 2
    assert output.exists()
    saved = json.loads(output.read_text())
    assert len(saved) == 2
