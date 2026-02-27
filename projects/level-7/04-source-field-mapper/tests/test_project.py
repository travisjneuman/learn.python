"""Tests for Source Field Mapper."""

from __future__ import annotations

import json

import pytest

from project import (
    FieldRule,
    apply_mapping,
    map_records,
    parse_rules,
    run,
    validate_mapped,
)


RULES = [
    FieldRule(source_field="item_id", target_field="id", cast="str"),
    FieldRule(source_field="item_name", target_field="name", cast="str"),
    FieldRule(source_field="price", target_field="amount", cast="float"),
    FieldRule(source_field="qty", target_field="quantity", cast="int", default="0"),
]


class TestApplyMapping:
    def test_basic_mapping(self) -> None:
        rec = {"item_id": "A1", "item_name": "Widget", "price": "9.99", "qty": "5"}
        result = apply_mapping(rec, RULES)
        assert result["id"] == "A1"
        assert result["amount"] == 9.99
        assert result["quantity"] == 5

    def test_default_value(self) -> None:
        rec = {"item_id": "A2", "item_name": "Gadget", "price": "4.99"}
        result = apply_mapping(rec, RULES)
        assert result["quantity"] == 0  # from default

    def test_missing_without_default(self) -> None:
        rec = {"item_name": "Orphan", "price": "1.00"}
        result = apply_mapping(rec, RULES)
        assert "id" not in result  # no default, no source

    @pytest.mark.parametrize("cast,value,expected", [
        ("int", "42", 42),
        ("float", "3.14", 3.14),
        ("bool", "true", True),
        ("bool", "0", False),
    ])
    def test_type_casting(self, cast: str, value: str, expected) -> None:
        rules = [FieldRule(source_field="x", target_field="y", cast=cast)]
        result = apply_mapping({"x": value}, rules)
        assert result["y"] == expected


class TestMapRecords:
    def test_batch_mapping(self) -> None:
        records = [
            {"item_id": "1", "item_name": "A", "price": "1.0"},
            {"item_id": "2", "item_name": "B", "price": "2.0"},
        ]
        mapped, errors = map_records(records, RULES)
        assert len(mapped) == 2
        assert errors == []


class TestValidation:
    def test_missing_required_field(self) -> None:
        records = [{"name": "ok"}]  # missing "id"
        issues = validate_mapped(records, ["id", "name"])
        assert any("missing=id" in i for i in issues)


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {
        "rules": [{"source": "x", "target": "y", "cast": "int"}],
        "records": [{"x": "42"}, {"x": "7"}],
        "required_fields": ["y"],
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["mapped_records"] == 2
    assert summary["validation_issues"] == []
