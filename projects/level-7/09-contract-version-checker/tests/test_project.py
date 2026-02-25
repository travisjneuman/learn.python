"""Tests for Contract Version Checker."""

from __future__ import annotations

import json

import pytest

from project import (
    Contract,
    ContractField,
    ValidationResult,
    contract_from_dict,
    diff_contracts,
    is_breaking,
    parse_version,
    run,
    validate_batch,
    validate_payload,
)


class TestVersionParsing:
    @pytest.mark.parametrize("v,expected", [
        ("1.0.0", (1, 0, 0)),
        ("2.3.1", (2, 3, 1)),
        ("10.20.30", (10, 20, 30)),
    ])
    def test_parse_version(self, v: str, expected: tuple) -> None:
        assert parse_version(v) == expected

    def test_major_bump_is_breaking(self) -> None:
        assert is_breaking("1.2.3", "2.0.0") is True

    def test_minor_bump_not_breaking(self) -> None:
        assert is_breaking("1.2.3", "1.3.0") is False


class TestValidation:
    def test_valid_payload(self) -> None:
        contract = Contract("1.0.0", [ContractField("name", "str"), ContractField("age", "int")])
        result = validate_payload({"name": "Alice", "age": 30}, contract)
        assert result.valid

    def test_missing_required_field(self) -> None:
        contract = Contract("1.0.0", [ContractField("name", "str")])
        result = validate_payload({}, contract)
        assert not result.valid
        assert "name" in result.missing

    def test_type_mismatch(self) -> None:
        contract = Contract("1.0.0", [ContractField("age", "int")])
        result = validate_payload({"age": "not_int"}, contract)
        assert not result.valid
        assert len(result.type_errors) == 1

    def test_optional_field_ok_when_absent(self) -> None:
        contract = Contract("1.0.0", [ContractField("note", "str", required=False)])
        result = validate_payload({}, contract)
        assert result.valid

    def test_extra_fields_detected(self) -> None:
        contract = Contract("1.0.0", [ContractField("name", "str")])
        result = validate_payload({"name": "x", "bonus": 1}, contract)
        assert result.valid  # extra fields don't invalidate
        assert "bonus" in result.extra_fields


class TestDiffContracts:
    def test_added_field(self) -> None:
        old = Contract("1.0.0", [ContractField("a", "str")])
        new = Contract("1.1.0", [ContractField("a", "str"), ContractField("b", "int")])
        diff = diff_contracts(old, new)
        assert "b" in diff["added"]
        assert diff["breaking"] is False

    def test_removed_field_is_breaking(self) -> None:
        old = Contract("1.0.0", [ContractField("a", "str"), ContractField("b", "int")])
        new = Contract("1.1.0", [ContractField("a", "str")])
        diff = diff_contracts(old, new)
        assert "b" in diff["removed"]
        assert diff["breaking"] is True


def test_run_end_to_end(tmp_path) -> None:
    config = {
        "contract": {
            "version": "2.0.0",
            "fields": [{"name": "id", "type": "int"}, {"name": "label", "type": "str"}],
        },
        "payloads": [
            {"id": 1, "label": "ok"},
            {"id": "bad", "label": "oops"},
        ],
        "old_contract": {
            "version": "1.0.0",
            "fields": [{"name": "id", "type": "int"}],
        },
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["valid"] == 1
    assert summary["invalid"] == 1
    assert summary["diff"]["breaking"] is True
