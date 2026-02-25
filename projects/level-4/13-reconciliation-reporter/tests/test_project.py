"""Tests for Reconciliation Reporter."""

from pathlib import Path
import json
import pytest

from project import load_csv_as_dict, reconcile, run


def test_reconcile_all_matched() -> None:
    source = {"1": {"id": "1", "name": "Alice"}, "2": {"id": "2", "name": "Bob"}}
    target = {"1": {"id": "1", "name": "Alice"}, "2": {"id": "2", "name": "Bob"}}
    result = reconcile(source, target)
    assert result["matched"] == 2
    assert result["only_in_source"] == []
    assert result["mismatches"] == []


def test_reconcile_only_in_source() -> None:
    source = {"1": {"id": "1"}, "2": {"id": "2"}}
    target = {"1": {"id": "1"}}
    result = reconcile(source, target)
    assert result["only_in_source"] == ["2"]


def test_reconcile_mismatches() -> None:
    source = {"1": {"id": "1", "name": "Alice", "age": "30"}}
    target = {"1": {"id": "1", "name": "Alice", "age": "31"}}
    result = reconcile(source, target)
    assert len(result["mismatches"]) == 1
    assert "age" in result["mismatches"][0]["differences"]


@pytest.mark.parametrize(
    "source_keys, target_keys, expected_source_only, expected_target_only",
    [
        ({"a", "b", "c"}, {"b", "c", "d"}, ["a"], ["d"]),
        ({"x"}, {"x"}, [], []),
        (set(), {"y"}, [], ["y"]),
    ],
)
def test_reconcile_set_operations(
    source_keys: set, target_keys: set,
    expected_source_only: list, expected_target_only: list,
) -> None:
    source = {k: {"id": k} for k in source_keys}
    target = {k: {"id": k} for k in target_keys}
    result = reconcile(source, target)
    assert result["only_in_source"] == expected_source_only
    assert result["only_in_target"] == expected_target_only


def test_load_csv_as_dict_rejects_bad_key(tmp_path: Path) -> None:
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name,age\nAlice,30\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Key field"):
        load_csv_as_dict(csv_file, "nonexistent")


def test_run_integration(tmp_path: Path) -> None:
    source = tmp_path / "source.csv"
    target = tmp_path / "target.csv"
    source.write_text("id,name,age\n1,Alice,30\n2,Bob,25\n3,Charlie,28\n", encoding="utf-8")
    target.write_text("id,name,age\n1,Alice,30\n2,Bob,26\n4,Diana,32\n", encoding="utf-8")

    output = tmp_path / "report.json"
    report = run(source, target, output, "id")
    assert report["matched"] == 1       # Alice
    assert len(report["mismatches"]) == 1  # Bob (age differs)
    assert "3" in report["only_in_source"]  # Charlie
    assert "4" in report["only_in_target"]  # Diana
