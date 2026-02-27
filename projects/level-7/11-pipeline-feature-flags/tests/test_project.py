"""Tests for Pipeline Feature Flags."""

from __future__ import annotations

import json

import pytest

from project import Flag, FlagManager, flags_from_config, run


class TestFlagManager:
    def test_enabled_flag_returns_true(self) -> None:
        mgr = FlagManager([Flag("f1", enabled=True)])
        assert mgr.is_enabled("f1") is True

    def test_disabled_flag_returns_false(self) -> None:
        mgr = FlagManager([Flag("f1", enabled=False)])
        assert mgr.is_enabled("f1") is False

    def test_unknown_flag_returns_false(self) -> None:
        mgr = FlagManager()
        assert mgr.is_enabled("nonexistent") is False

    def test_dependency_chain(self) -> None:
        mgr = FlagManager([
            Flag("base", enabled=True),
            Flag("child", enabled=True, requires=["base"]),
        ])
        assert mgr.is_enabled("child") is True

    def test_unmet_dependency_disables(self) -> None:
        mgr = FlagManager([
            Flag("base", enabled=False),
            Flag("child", enabled=True, requires=["base"]),
        ])
        assert mgr.is_enabled("child") is False

    def test_rollout_zero_always_off(self) -> None:
        mgr = FlagManager([Flag("f1", enabled=True, rollout_pct=0.0)])
        assert mgr.is_enabled("f1", "any_user") is False

    def test_rollout_hundred_always_on(self) -> None:
        mgr = FlagManager([Flag("f1", enabled=True, rollout_pct=100.0)])
        assert mgr.is_enabled("f1", "any_user") is True

    @pytest.mark.parametrize("pct", [25.0, 50.0, 75.0])
    def test_rollout_deterministic(self, pct: float) -> None:
        mgr = FlagManager([Flag("f1", enabled=True, rollout_pct=pct)])
        result1 = mgr.is_enabled("f1", "user_42")
        mgr2 = FlagManager([Flag("f1", enabled=True, rollout_pct=pct)])
        result2 = mgr2.is_enabled("f1", "user_42")
        assert result1 == result2  # same input → same output

    def test_audit_log_populated(self) -> None:
        mgr = FlagManager([Flag("f1")])
        mgr.is_enabled("f1")
        assert len(mgr.audit_log) >= 1

    def test_stats(self) -> None:
        mgr = FlagManager([Flag("a", enabled=True), Flag("b", enabled=False)])
        s = mgr.stats()
        assert s["total"] == 2
        assert s["enabled"] == 1
        assert s["disabled"] == 1

    def test_evaluate_all(self) -> None:
        mgr = FlagManager([Flag("a"), Flag("b", enabled=False)])
        result = mgr.evaluate_all()
        assert result["a"] is True
        assert result["b"] is False


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {
        "flags": [
            {"name": "stage_ingest", "enabled": True},
            {"name": "stage_transform", "enabled": True, "requires": ["stage_ingest"]},
            {"name": "stage_export", "enabled": False},
        ],
        "context_key": "run_001",
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["evaluations"]["stage_ingest"] is True
    assert summary["evaluations"]["stage_export"] is False
    assert summary["stats"]["disabled"] == 1
