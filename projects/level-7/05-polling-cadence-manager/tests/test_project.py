"""Tests for Polling Cadence Manager."""

from __future__ import annotations

import json

import pytest

from project import PollConfig, PollState, compute_hash, poll_once, run, simulate_polling


class TestPolling:
    def test_no_change_backs_off(self) -> None:
        config = PollConfig(min_interval=1, max_interval=100, backoff_factor=2.0)
        state = PollState(current_interval=5.0)
        poll_once(state, "same", config)
        poll_once(state, "same", config)
        assert state.current_interval > 5.0

    def test_change_speeds_up(self) -> None:
        config = PollConfig(min_interval=1, max_interval=100, speedup_factor=0.5)
        state = PollState(current_interval=20.0, last_hash="old")
        poll_once(state, "new_data", config)
        assert state.current_interval < 20.0

    def test_interval_respects_min(self) -> None:
        config = PollConfig(min_interval=2.0, speedup_factor=0.1)
        state = PollState(current_interval=3.0, last_hash="old")
        poll_once(state, "changed", config)
        assert state.current_interval >= 2.0

    @pytest.mark.parametrize("max_int", [10, 30, 60])
    def test_interval_respects_max(self, max_int: float) -> None:
        config = PollConfig(max_interval=max_int, backoff_factor=100.0)
        state = PollState(current_interval=5.0)
        poll_once(state, "same", config)
        poll_once(state, "same", config)
        assert state.current_interval <= max_int


class TestSimulation:
    def test_detects_changes(self) -> None:
        snapshots = ["v1", "v1", "v2", "v2", "v3"]
        state = simulate_polling(snapshots)
        assert state.changes_detected == 2
        assert state.polls_done == 5

    def test_all_same_no_changes(self) -> None:
        state = simulate_polling(["same"] * 5)
        assert state.changes_detected == 0


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {"snapshots": ["a", "a", "b", "b"], "config": {"min_interval": 1}}
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["polls"] == 4
    assert summary["changes"] == 1
