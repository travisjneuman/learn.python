"""Tests for Stale Data Detector."""

from __future__ import annotations

import json

import pytest

from project import (
    FreshnessRule,
    check_sources,
    classify_age,
    merge_rules,
    run,
    summarise,
)


class TestClassifyAge:
    @pytest.mark.parametrize("age,expected", [
        (10, "fresh"),
        (300, "warning"),
        (600, "stale"),
        (1800, "critical"),
    ])
    def test_default_thresholds(self, age: float, expected: str) -> None:
        rule = FreshnessRule(source="x")
        assert classify_age(age, rule) == expected

    def test_custom_thresholds(self) -> None:
        rule = FreshnessRule(source="x", warning=10, stale=20, critical=30)
        assert classify_age(5, rule) == "fresh"
        assert classify_age(15, rule) == "warning"
        assert classify_age(25, rule) == "stale"
        assert classify_age(35, rule) == "critical"


class TestMergeRules:
    def test_override_replaces_default(self) -> None:
        defaults = {"src_a": FreshnessRule("src_a", 100, 200, 300)}
        overrides = [{"source": "src_a", "warning": 50, "stale": 100, "critical": 150}]
        merged = merge_rules(defaults, overrides)
        assert merged["src_a"].warning == 50

    def test_new_source_added(self) -> None:
        merged = merge_rules({}, [{"source": "new_src", "warning": 10}])
        assert "new_src" in merged


class TestCheckSources:
    def test_fresh_source(self) -> None:
        now = 1000.0
        sources = [{"source": "x", "last_updated": 999.0}]
        rules = {"x": FreshnessRule("x", warning=60, stale=120, critical=300)}
        results = check_sources(sources, rules, now=now)
        assert results[0].severity == "fresh"

    def test_stale_source(self) -> None:
        now = 1000.0
        sources = [{"source": "x", "last_updated": 800.0}]
        rules = {"x": FreshnessRule("x", warning=60, stale=120, critical=300)}
        results = check_sources(sources, rules, now=now)
        assert results[0].severity == "stale"

    def test_unknown_source_uses_fallback(self) -> None:
        now = 1000.0
        sources = [{"source": "unknown", "last_updated": 999.0}]
        results = check_sources(sources, {}, now=now)
        assert results[0].severity == "fresh"


class TestSummarise:
    def test_counts_correct(self) -> None:
        from project import SourceStatus
        statuses = [
            SourceStatus("a", 0, 10, "fresh"),
            SourceStatus("b", 0, 700, "stale"),
            SourceStatus("c", 0, 2000, "critical"),
        ]
        summary = summarise(statuses)
        assert summary["counts"]["fresh"] == 1
        assert summary["counts"]["stale"] == 1
        assert summary["stale_sources"] == ["b", "c"]
        assert summary["all_fresh"] is False


def test_run_end_to_end(tmp_path) -> None:
    now = 1000.0
    config = {
        "now": now,
        "sources": [
            {"source": "api_orders", "last_updated": 999.0},
            {"source": "api_inventory", "last_updated": 100.0},
        ],
        "rules": [],
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["total_sources"] == 2
    assert not summary["all_fresh"]  # inventory is very stale
