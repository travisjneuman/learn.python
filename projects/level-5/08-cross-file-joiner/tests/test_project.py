"""Tests for Cross File Joiner."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import (
    index_by_key,
    join_inner,
    join_left,
    join_full,
    validate_key_exists,
    run,
)


# ---------- index_by_key ----------

def test_index_by_key_basic() -> None:
    records = [{"id": "1", "name": "Alice"}, {"id": "2", "name": "Bob"}]
    idx = index_by_key(records, "id")
    assert "1" in idx and "2" in idx
    assert idx["1"]["name"] == "Alice"


def test_index_by_key_skips_empty_keys() -> None:
    records = [{"id": "", "name": "Ghost"}, {"id": "1", "name": "Alice"}]
    idx = index_by_key(records, "id")
    assert len(idx) == 1


# ---------- join strategies ----------

@pytest.mark.parametrize("strategy_fn,expected_count", [
    (join_inner, 1),
    (join_left, 2),
    (join_full, 3),
])
def test_join_strategies(strategy_fn, expected_count: int) -> None:
    left = {"1": {"id": "1", "name": "Alice"}, "2": {"id": "2", "name": "Bob"}}
    right = {"1": {"id": "1", "dept": "Eng"}, "3": {"id": "3", "dept": "Sales"}}
    result = strategy_fn(left, right)
    assert len(result) == expected_count


def test_join_inner_merges_fields() -> None:
    left = {"1": {"id": "1", "name": "Alice"}}
    right = {"1": {"id": "1", "dept": "Eng"}}
    result = join_inner(left, right)
    assert result[0]["name"] == "Alice"
    assert result[0]["dept"] == "Eng"


# ---------- validate_key_exists ----------

def test_validate_key_exists_passes() -> None:
    records = [{"id": "1", "name": "Alice"}]
    validate_key_exists(records, "id", "test.csv")  # should not raise


def test_validate_key_exists_raises_on_missing() -> None:
    records = [{"name": "Alice"}]
    with pytest.raises(ValueError, match="not found"):
        validate_key_exists(records, "id", "test.csv")


# ---------- integration: run with CSV files ----------

@pytest.mark.parametrize("strategy,expected_count", [
    ("inner", 2),
    ("left", 3),
    ("full", 4),
])
def test_run_strategies(tmp_path: Path, strategy: str, expected_count: int) -> None:
    left = tmp_path / "left.csv"
    left.write_text("id,name\n1,Alice\n2,Bob\n3,Charlie\n", encoding="utf-8")
    right = tmp_path / "right.csv"
    right.write_text("id,dept\n1,Eng\n2,Design\n4,Sales\n", encoding="utf-8")
    output = tmp_path / "out.json"
    report = run(left, right, output, "id", strategy)
    assert report["joined_records"] == expected_count
    assert output.exists()
    saved = json.loads(output.read_text())
    assert saved["strategy"] == strategy


def test_run_with_json_files(tmp_path: Path) -> None:
    left = tmp_path / "left.json"
    left.write_text(json.dumps([{"k": "a", "v": 1}, {"k": "b", "v": 2}]))
    right = tmp_path / "right.json"
    right.write_text(json.dumps([{"k": "a", "x": 10}]))
    output = tmp_path / "out.json"
    report = run(left, right, output, "k", "inner")
    assert report["joined_records"] == 1
    assert report["data"][0]["v"] == 1
    assert report["data"][0]["x"] == 10
