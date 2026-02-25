"""Tests for Incident Mode Switch."""

from __future__ import annotations

import json

import pytest

from project import (
    Criticality,
    IncidentController,
    Mode,
    Stage,
    run,
    stages_from_config,
)


@pytest.fixture
def controller() -> IncidentController:
    stages = [
        Stage("ingest", Criticality.CRITICAL),
        Stage("transform", Criticality.STANDARD),
        Stage("enrich", Criticality.OPTIONAL),
        Stage("export", Criticality.STANDARD),
    ]
    return IncidentController(stages)


class TestModeTransitions:
    def test_normal_to_degraded(self, controller: IncidentController) -> None:
        assert controller.switch_mode(Mode.DEGRADED, "high error rate") is True
        assert controller.mode == Mode.DEGRADED

    def test_invalid_transition_rejected(self, controller: IncidentController) -> None:
        controller.switch_mode(Mode.MAINTENANCE)
        assert controller.switch_mode(Mode.DEGRADED) is False  # maintenance→degraded invalid
        assert controller.mode == Mode.MAINTENANCE  # stays unchanged

    @pytest.mark.parametrize("path", [
        [Mode.DEGRADED, Mode.EMERGENCY, Mode.NORMAL],
        [Mode.EMERGENCY, Mode.DEGRADED, Mode.NORMAL],
        [Mode.MAINTENANCE, Mode.NORMAL],
    ])
    def test_valid_transition_paths(self, controller: IncidentController,
                                     path: list[Mode]) -> None:
        for target in path:
            assert controller.switch_mode(target) is True

    def test_timeline_recorded(self, controller: IncidentController) -> None:
        controller.switch_mode(Mode.DEGRADED, "test")
        assert len(controller.timeline) == 1
        assert controller.timeline[0].reason == "test"


class TestActiveStages:
    def test_normal_all_active(self, controller: IncidentController) -> None:
        assert len(controller.active_stages()) == 4

    def test_degraded_drops_optional(self, controller: IncidentController) -> None:
        controller.switch_mode(Mode.DEGRADED)
        active = controller.active_stages()
        assert "enrich" not in active
        assert "ingest" in active

    def test_emergency_only_critical(self, controller: IncidentController) -> None:
        controller.switch_mode(Mode.EMERGENCY)
        assert controller.active_stages() == ["ingest"]
        assert len(controller.skipped_stages()) == 3


class TestSummary:
    def test_summary_structure(self, controller: IncidentController) -> None:
        s = controller.summary()
        assert s["mode"] == "normal"
        assert "active" in s
        assert "skipped" in s


def test_run_end_to_end(tmp_path) -> None:
    config = {
        "stages": [
            {"name": "ingest", "criticality": "critical"},
            {"name": "transform", "criticality": "standard"},
            {"name": "report", "criticality": "optional"},
        ],
        "transitions": [
            {"mode": "degraded", "reason": "error spike"},
            {"mode": "emergency", "reason": "total outage"},
            {"mode": "normal", "reason": "resolved"},
        ],
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["final_mode"] == "normal"
    assert summary["timeline_events"] == 3
