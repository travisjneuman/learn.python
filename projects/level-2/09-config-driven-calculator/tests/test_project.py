"""Tests for Config Driven Calculator.

Covers:
- Basic arithmetic operations
- Error handling (division by zero, unknown ops)
- Config loading (valid, missing, invalid)
- Batch calculations
- Operation chaining
"""

from pathlib import Path

import pytest

from project import (
    batch_calculate,
    calculate,
    calculate_chain,
    list_operations,
    load_config,
)


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("add", 10, 5, 15),
        ("subtract", 10, 3, 7),
        ("multiply", 4, 5, 20),
        ("divide", 15, 3, 5),
        ("power", 2, 8, 256),
        ("modulo", 17, 5, 2),
    ],
)
def test_calculate_operations(op: str, a: float, b: float, expected: float) -> None:
    """All basic operations should produce correct results."""
    result = calculate(op, a, b)
    assert result["success"] is True
    assert result["result"] == expected


def test_calculate_divide_by_zero() -> None:
    """Division by zero should return an error, not crash."""
    result = calculate("divide", 10, 0)
    assert result["success"] is False
    assert "zero" in result["error"].lower()


def test_calculate_unknown_operation() -> None:
    """Unknown operations should return a descriptive error."""
    result = calculate("unknown_op", 1, 2)
    assert result["success"] is False
    assert "Unknown operation" in result["error"]


def test_load_config_valid(tmp_path: Path) -> None:
    """A valid JSON config should load operations."""
    config_data = {
        "operations": {
            "add": {"symbol": "+", "description": "Addition"},
        },
        "settings": {"precision": 4},
    }
    p = tmp_path / "config.json"
    p.write_text(json.dumps(config_data), encoding="utf-8")
    config = load_config(p)
    assert "add" in config["operations"]


def test_load_config_missing_file(tmp_path: Path) -> None:
    """Missing config should fall back to defaults."""
    config = load_config(tmp_path / "nope.json")
    assert "add" in config["operations"]


def test_load_config_invalid_json(tmp_path: Path) -> None:
    """Invalid JSON should fall back to defaults with error info."""
    p = tmp_path / "bad.json"
    p.write_text("not json", encoding="utf-8")
    config = load_config(p)
    assert "config_error" in config


def test_batch_calculate() -> None:
    """Batch should process multiple operations and preserve order."""
    ops = [
        {"operation": "add", "a": 1, "b": 2},
        {"operation": "divide", "a": 10, "b": 0},
        {"operation": "multiply", "a": 3, "b": 4},
    ]
    results = batch_calculate(ops)
    assert len(results) == 3
    assert results[0]["success"] is True
    assert results[1]["success"] is False
    assert results[2]["result"] == 12


def test_calculate_chain() -> None:
    """Chained operations should feed results forward."""
    chain = [("add", 5), ("multiply", 2)]
    result = calculate_chain(chain, start=10)
    assert result["success"] is True
    assert result["final"] == 30  # (10+5)*2


def test_list_operations() -> None:
    """List should return sorted operation info."""
    config = {"operations": {"z_op": {}, "a_op": {}}}
    ops = list_operations(config)
    assert ops[0]["name"] == "a_op"
    assert ops[1]["name"] == "z_op"


# Need json import for test_load_config_valid
import json
