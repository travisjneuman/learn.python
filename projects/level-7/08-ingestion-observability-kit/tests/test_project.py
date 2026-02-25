"""Tests for Ingestion Observability Kit."""

from __future__ import annotations

import json

import pytest

from project import ObservabilityKit, ingest_stage, run, run_pipeline, transform_stage


class TestObservabilityKit:
    def test_start_and_end_stage(self) -> None:
        kit = ObservabilityKit()
        kit.start_stage("load", 10)
        kit.end_stage("load", 8, errors=2)
        s = kit.summary()
        assert s["stages"]["load"]["rows_in"] == 10
        assert s["stages"]["load"]["rows_out"] == 8
        assert s["stages"]["load"]["errors"] == 2

    def test_error_rate_calculation(self) -> None:
        kit = ObservabilityKit()
        kit.start_stage("s1", 100)
        kit.end_stage("s1", 90, errors=10)
        assert kit.metrics["s1"].error_rate == 0.1

    def test_log_error_recorded(self) -> None:
        kit = ObservabilityKit()
        kit.start_stage("s1", 5)
        kit.log_error("s1", "abc", "bad row")
        assert any(e.level == "ERROR" and "bad row" in e.message for e in kit.logs)

    def test_log_warn_recorded(self) -> None:
        kit = ObservabilityKit()
        kit.start_stage("s1", 5)
        kit.log_warn("s1", "abc", "slow")
        assert any(e.level == "WARN" for e in kit.logs)


class TestPipelineStages:
    def test_ingest_filters_bad_records(self) -> None:
        kit = ObservabilityKit()
        records = [{"id": "a", "value": "ok"}, {"id": "b"}]  # second missing value
        good = ingest_stage(records, kit)
        assert len(good) == 1
        assert kit.metrics["ingest"].errors == 1

    def test_transform_uppercases(self) -> None:
        kit = ObservabilityKit()
        records = [{"id": "a", "value": "hello"}]
        out = transform_stage(records, kit)
        assert out[0]["value"] == "HELLO"

    @pytest.mark.parametrize("n_records", [0, 1, 10])
    def test_pipeline_various_sizes(self, n_records: int) -> None:
        records = [{"id": str(i), "value": f"v{i}"} for i in range(n_records)]
        data, summary = run_pipeline(records)
        assert len(data) == n_records
        assert summary["total_errors"] == 0


def test_run_end_to_end(tmp_path) -> None:
    config = {"records": [
        {"id": "1", "value": "alpha"},
        {"id": "2"},
        {"id": "3", "value": "gamma"},
    ]}
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["stages"]["ingest"]["errors"] == 1
    assert summary["stages"]["transform"]["rows_out"] == 2
