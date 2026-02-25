"""Tests for Level 7 Mini-Capstone."""

from __future__ import annotations

import json

import pytest

from project import (
    SimpleCache,
    adapt_source,
    check_freshness,
    reconcile_sources,
    run,
    run_pipeline,
    validate_contract,
)


class TestAdaptSource:
    def test_alpha_format(self) -> None:
        raw = [{"uid": "1", "data": "hello"}]
        out = adapt_source("alpha", raw)
        assert out[0]["id"] == "1"
        assert out[0]["source"] == "alpha"

    def test_beta_format(self) -> None:
        raw = [{"identifier": "2", "payload": "world"}]
        out = adapt_source("beta", raw)
        assert out[0]["id"] == "2"

    def test_unknown_passthrough(self) -> None:
        raw = [{"id": "3", "value": "x"}]
        out = adapt_source("gamma", raw)
        assert out[0]["source"] == "gamma"


class TestCache:
    def test_hit_and_miss(self) -> None:
        c = SimpleCache()
        c.put("k1", {"v": 1})
        assert c.get("k1") is not None
        assert c.get("k2") is None
        assert c.stats["hits"] == 1
        assert c.stats["misses"] == 1


class TestValidation:
    @pytest.mark.parametrize("rec,required,expected_missing", [
        ({"id": 1, "value": "x"}, ["id", "value"], []),
        ({"id": 1}, ["id", "value"], ["value"]),
        ({}, ["id"], ["id"]),
    ])
    def test_contract(self, rec: dict, required: list, expected_missing: list) -> None:
        assert validate_contract(rec, required) == expected_missing


class TestFreshness:
    def test_fresh(self) -> None:
        assert check_freshness(990, 100, 1000) == "fresh"

    def test_stale(self) -> None:
        assert check_freshness(800, 100, 1000) == "stale"


class TestReconciliation:
    def test_matched(self) -> None:
        groups = {
            "a": [{"id": "1", "value": "x"}],
            "b": [{"id": "1", "value": "x"}],
        }
        r = reconcile_sources(groups, "id")
        assert r["matched"] == 1

    def test_mismatched(self) -> None:
        groups = {
            "a": [{"id": "1", "value": "x"}],
            "b": [{"id": "1", "value": "y"}],
        }
        r = reconcile_sources(groups, "id")
        assert r["mismatched"] == 1


class TestPipeline:
    def test_full_pipeline(self) -> None:
        config = {
            "now": 1000,
            "max_age_seconds": 600,
            "sources": {
                "alpha": {"records": [
                    {"uid": "1", "data": "hello"},
                    {"uid": "2", "data": "world"},
                ]},
                "beta": {"records": [
                    {"identifier": "1", "payload": "hello"},
                ]},
            },
            "flags": {"adapt": True, "cache": True, "validate": True,
                      "freshness": True, "reconcile": True},
        }
        result = run_pipeline(config)
        assert result["records_in"] == 3
        assert "adapt" in result["stages_run"]
        assert "reconcile" in result["stages_run"]

    def test_flags_disable_stages(self) -> None:
        config = {
            "sources": {"alpha": {"records": [{"uid": "1", "data": "x"}]}},
            "flags": {"adapt": True, "cache": False, "validate": False,
                      "freshness": False, "reconcile": False},
        }
        result = run_pipeline(config)
        assert "cache" not in result["stages_run"]
        assert "validate" not in result["stages_run"]


def test_run_end_to_end(tmp_path) -> None:
    config = {
        "now": 1000,
        "sources": {
            "alpha": {"records": [{"uid": "1", "data": "x"}, {"uid": "2", "data": "y"}]},
            "beta": {"records": [{"identifier": "1", "payload": "x"}]},
        },
        "flags": {"adapt": True, "cache": True, "validate": True,
                  "freshness": True, "reconcile": True},
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["records_in"] == 3
    assert summary["records_out"] >= 1
    assert len(summary["stages_run"]) >= 4
