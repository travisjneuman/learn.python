"""Tests for Data Contract Enforcer."""

import json
from pathlib import Path
import pytest

from project import coerce_value, enforce_contract, run


@pytest.mark.parametrize(
    "raw, expected_type, should_succeed",
    [
        ("42", "int", True),
        ("abc", "int", False),
        ("3.14", "float", True),
        ("nope", "float", False),
        ("true", "bool", True),
        ("yes", "bool", True),
        ("maybe", "bool", False),
        ("hello", "str", True),
    ],
)
def test_coerce_value(raw: str, expected_type: str, should_succeed: bool) -> None:
    _, err = coerce_value(raw, expected_type)
    if should_succeed:
        assert err is None
    else:
        assert err is not None


def test_enforce_contract_required_field() -> None:
    contract = {"columns": {"name": {"type": "str", "required": True}}}
    headers = ["name"]
    rows = [{"name": "Alice"}, {"name": ""}]
    report = enforce_contract(headers, rows, contract)
    assert report["clean_rows"] == 1
    assert report["violation_count"] == 1


def test_enforce_contract_range_check() -> None:
    contract = {"columns": {"age": {"type": "int", "required": True, "min": 0, "max": 150}}}
    headers = ["age"]
    rows = [{"age": "25"}, {"age": "-5"}, {"age": "200"}]
    report = enforce_contract(headers, rows, contract)
    assert report["clean_rows"] == 1
    assert report["violation_count"] == 2


def test_enforce_contract_allowed_values() -> None:
    contract = {"columns": {"status": {"type": "str", "required": True, "allowed": ["active", "inactive"]}}}
    headers = ["status"]
    rows = [{"status": "active"}, {"status": "deleted"}]
    report = enforce_contract(headers, rows, contract)
    assert report["violation_count"] == 1


def test_enforce_contract_detects_missing_columns() -> None:
    contract = {"columns": {"a": {"type": "str"}, "b": {"type": "str"}}}
    headers = ["a"]  # 'b' is missing from the actual data
    rows = [{"a": "x"}]
    report = enforce_contract(headers, rows, contract)
    assert "b" in report["missing_columns"]


def test_full_run(tmp_path: Path) -> None:
    contract_file = tmp_path / "contract.json"
    contract_file.write_text(json.dumps({
        "columns": {
            "name": {"type": "str", "required": True},
            "age": {"type": "int", "required": True, "min": 0},
        }
    }), encoding="utf-8")

    data_file = tmp_path / "data.csv"
    data_file.write_text("name,age\nAlice,30\nBob,abc\n", encoding="utf-8")

    output = tmp_path / "report.json"
    report = run(contract_file, data_file, output)
    assert output.exists()
    assert report["clean_rows"] == 1
    assert report["violation_count"] >= 1
