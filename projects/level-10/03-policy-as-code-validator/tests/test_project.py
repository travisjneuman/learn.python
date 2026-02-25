"""Tests for Policy-as-Code Validator.

Covers individual rule types, engine composition, batch evaluation,
config loading, and edge cases.
"""
from __future__ import annotations

from typing import Any

import pytest

from project import (
    CustomPredicateRule,
    EvaluationReport,
    NumericRangeRule,
    PolicyEngine,
    RequiredFieldRule,
    Severity,
    ValueInSetRule,
    Verdict,
    load_policies_from_config,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_resource() -> dict[str, Any]:
    return {
        "name": "billing-svc",
        "environment": "production",
        "replicas": 3,
        "owner": "platform-team",
    }


@pytest.fixture
def engine_with_rules() -> PolicyEngine:
    engine = PolicyEngine()
    engine.add_rule(RequiredFieldRule("R001", "name"))
    engine.add_rule(RequiredFieldRule("R002", "owner"))
    engine.add_rule(ValueInSetRule("R003", "environment", {"production", "staging", "development"}))
    engine.add_rule(NumericRangeRule("R004", "replicas", min_val=1, max_val=10))
    return engine


# ---------------------------------------------------------------------------
# Individual rules
# ---------------------------------------------------------------------------

class TestRequiredFieldRule:
    def test_present_field_passes(self, sample_resource: dict[str, Any]) -> None:
        result = RequiredFieldRule("R1", "name").evaluate(sample_resource)
        assert result.verdict == Verdict.PASS

    def test_missing_field_fails(self) -> None:
        result = RequiredFieldRule("R1", "missing").evaluate({})
        assert result.verdict == Verdict.FAIL

    def test_empty_string_fails(self) -> None:
        result = RequiredFieldRule("R1", "name").evaluate({"name": ""})
        assert result.verdict == Verdict.FAIL


class TestValueInSetRule:
    @pytest.mark.parametrize("value,expected", [
        ("production", Verdict.PASS),
        ("staging", Verdict.PASS),
        ("invalid", Verdict.FAIL),
    ])
    def test_value_in_set_variants(self, value: str, expected: Verdict) -> None:
        rule = ValueInSetRule("R1", "env", {"production", "staging"})
        result = rule.evaluate({"env": value})
        assert result.verdict == expected


class TestNumericRangeRule:
    def test_within_range_passes(self) -> None:
        result = NumericRangeRule("R1", "count", min_val=1, max_val=10).evaluate({"count": 5})
        assert result.verdict == Verdict.PASS

    def test_below_minimum_fails(self) -> None:
        result = NumericRangeRule("R1", "count", min_val=1).evaluate({"count": 0})
        assert result.verdict == Verdict.FAIL

    def test_missing_field_skips(self) -> None:
        result = NumericRangeRule("R1", "count", min_val=1).evaluate({})
        assert result.verdict == Verdict.SKIP

    def test_non_numeric_fails(self) -> None:
        result = NumericRangeRule("R1", "count", min_val=1).evaluate({"count": "abc"})
        assert result.verdict == Verdict.FAIL


class TestCustomPredicateRule:
    def test_predicate_passes(self) -> None:
        rule = CustomPredicateRule("R1", lambda r: len(r) > 0, "Resource empty")
        result = rule.evaluate({"key": "val"})
        assert result.verdict == Verdict.PASS

    def test_predicate_fails(self) -> None:
        rule = CustomPredicateRule("R1", lambda r: "required" in r, "Missing 'required' key")
        result = rule.evaluate({})
        assert result.verdict == Verdict.FAIL


# ---------------------------------------------------------------------------
# Engine and report
# ---------------------------------------------------------------------------

class TestPolicyEngine:
    def test_all_rules_pass(self, engine_with_rules: PolicyEngine, sample_resource: dict[str, Any]) -> None:
        report = engine_with_rules.evaluate("res-1", sample_resource)
        assert report.passed
        assert len(report.results) == 4

    def test_failure_detected(self, engine_with_rules: PolicyEngine) -> None:
        bad_resource = {"name": "svc", "environment": "unknown", "replicas": 3, "owner": "team"}
        report = engine_with_rules.evaluate("res-2", bad_resource)
        assert not report.passed
        assert len(report.failures) == 1

    def test_batch_evaluation(self, engine_with_rules: PolicyEngine, sample_resource: dict[str, Any]) -> None:
        results = engine_with_rules.evaluate_batch({
            "good": sample_resource,
            "bad": {"name": "", "environment": "x", "replicas": 0, "owner": ""},
        })
        assert results["good"].passed
        assert not results["bad"].passed


class TestConfigLoading:
    def test_load_from_json_config(self) -> None:
        config = {
            "rules": [
                {"id": "R1", "type": "required_field", "field": "name"},
                {"id": "R2", "type": "value_in_set", "field": "env", "allowed": ["prod", "dev"]},
                {"id": "R3", "type": "numeric_range", "field": "count", "min": 1, "max": 100},
            ]
        }
        engine = load_policies_from_config(config)
        assert engine.rule_count == 3

    def test_unknown_rule_type_raises(self) -> None:
        config = {"rules": [{"id": "R1", "type": "nonexistent", "field": "x"}]}
        with pytest.raises(ValueError, match="Unknown rule type"):
            load_policies_from_config(config)
