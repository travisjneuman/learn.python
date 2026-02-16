"""Tests for Policy and Compliance Engine."""

from __future__ import annotations

import json
from pathlib import Path

import project


def test_build_summary_core_fields() -> None:
    """Ensure summary output contains stable keys and expected calculations."""
    records = [
        {"name": "alpha", "score": 10, "severity": "ok", "is_high_risk": False},
        {"name": "beta", "score": 3, "severity": "critical", "is_high_risk": True},
    ]

    # Verify deterministic computation behavior independent of CLI execution.
    payload = project.build_summary(records, "Policy and Compliance Engine", "test-run")

    assert payload["project_title"] == "Policy and Compliance Engine"
    assert payload["run_id"] == "test-run"
    assert payload["record_count"] == 2
    assert payload["high_risk_count"] == 1
    assert payload["average_score"] == 6.5


def test_main_like_flow_writes_output(tmp_path: Path) -> None:
    """Simulate end-to-end transformation and file output behavior."""
    input_file = tmp_path / "sample_input.txt"
    output_file = tmp_path / "output_summary.json"

    # Input includes one low score to validate high-risk logic.
    input_file.write_text("alpha,10,ok\nbeta,2,warn\n", encoding="utf-8")

    lines = project.load_lines(input_file)
    records = [project.classify_line(line) for line in lines]
    payload = project.build_summary(records, "Policy and Compliance Engine", "integration-test")
    project.write_summary(output_file, payload)

    # Confirm output exists and preserves key fields for downstream consumers.
    loaded = json.loads(output_file.read_text(encoding="utf-8"))
    assert loaded["record_count"] == 2
    assert loaded["high_risk_count"] == 1
    assert loaded["project_title"] == "Policy and Compliance Engine"
