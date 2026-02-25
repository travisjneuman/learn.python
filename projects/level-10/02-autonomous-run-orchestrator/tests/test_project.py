"""Tests for Autonomous Run Orchestrator.

Covers DAG resolution, execution order, retry logic, fail-fast behavior,
dependency skipping, and cycle detection.
"""
from __future__ import annotations

import pytest

from project import (
    CyclicDependencyError,
    Orchestrator,
    RunReport,
    StepStatus,
    WorkflowStep,
    topological_sort,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def linear_pipeline() -> list[WorkflowStep]:
    return [
        WorkflowStep("a", action=lambda: "done-a"),
        WorkflowStep("b", action=lambda: "done-b", depends_on=["a"]),
        WorkflowStep("c", action=lambda: "done-c", depends_on=["b"]),
    ]


@pytest.fixture
def diamond_pipeline() -> list[WorkflowStep]:
    """A -> B, A -> C, B+C -> D  (diamond shape)."""
    return [
        WorkflowStep("a", action=lambda: "a"),
        WorkflowStep("b", action=lambda: "b", depends_on=["a"]),
        WorkflowStep("c", action=lambda: "c", depends_on=["a"]),
        WorkflowStep("d", action=lambda: "d", depends_on=["b", "c"]),
    ]


# ---------------------------------------------------------------------------
# Topological sort
# ---------------------------------------------------------------------------

class TestTopologicalSort:
    def test_linear_order(self, linear_pipeline: list[WorkflowStep]) -> None:
        order = topological_sort(linear_pipeline)
        assert order == ["a", "b", "c"]

    def test_cycle_detected(self) -> None:
        steps = [
            WorkflowStep("x", action=lambda: "", depends_on=["y"]),
            WorkflowStep("y", action=lambda: "", depends_on=["x"]),
        ]
        with pytest.raises(CyclicDependencyError):
            topological_sort(steps)

    def test_unknown_dependency_rejected(self) -> None:
        steps = [WorkflowStep("a", action=lambda: "", depends_on=["ghost"])]
        with pytest.raises(ValueError, match="unknown step"):
            topological_sort(steps)

    def test_diamond_respects_all_edges(self, diamond_pipeline: list[WorkflowStep]) -> None:
        order = topological_sort(diamond_pipeline)
        assert order.index("a") < order.index("b")
        assert order.index("a") < order.index("c")
        assert order.index("b") < order.index("d")
        assert order.index("c") < order.index("d")


# ---------------------------------------------------------------------------
# Orchestrator execution
# ---------------------------------------------------------------------------

class TestOrchestrator:
    def test_all_steps_succeed(self, linear_pipeline: list[WorkflowStep]) -> None:
        report = Orchestrator(linear_pipeline).run()
        assert report.all_passed
        assert len(report.succeeded) == 3

    def test_fail_fast_skips_downstream(self) -> None:
        def boom() -> str:
            raise RuntimeError("boom")
        steps = [
            WorkflowStep("a", action=boom),
            WorkflowStep("b", action=lambda: "ok", depends_on=["a"]),
        ]
        report = Orchestrator(steps, fail_fast=True).run()
        assert not report.all_passed
        assert report.results[1].status == StepStatus.SKIPPED

    def test_retry_on_transient_failure(self) -> None:
        call_count = {"n": 0}
        def flaky() -> str:
            call_count["n"] += 1
            if call_count["n"] < 2:
                raise RuntimeError("transient")
            return "recovered"
        steps = [WorkflowStep("flaky", action=flaky, max_retries=3)]
        report = Orchestrator(steps).run()
        assert report.all_passed
        assert report.results[0].attempts == 2

    def test_dependency_failure_cascades_skip(self, diamond_pipeline: list[WorkflowStep]) -> None:
        def fail_b() -> str:
            raise RuntimeError("fail")
        diamond_pipeline[1] = WorkflowStep(
            "b", action=fail_b, depends_on=["a"]
        )
        report = Orchestrator(diamond_pipeline, fail_fast=False).run()
        d_result = next(r for r in report.results if r.step_name == "d")
        assert d_result.status == StepStatus.SKIPPED


class TestRunReport:
    def test_summary_keys(self) -> None:
        report = RunReport()
        summary = report.summary()
        assert "total_steps" in summary
        assert "succeeded" in summary
        assert "failed" in summary
