"""Autonomous Run Orchestrator — Multi-step workflow engine with dependency resolution.

Architecture: Implements a directed acyclic graph (DAG) scheduler using topological
sort. Each step declares its dependencies; the orchestrator resolves execution order,
runs steps with retry logic, and collects structured results. Uses the Command pattern
so steps are self-contained units of work.

Design rationale: Production pipelines (ETL, CI/CD, ML training) involve steps that
depend on each other. A topological scheduler prevents running a step before its
inputs are ready, while retry logic handles transient failures without restarting
the entire pipeline.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Protocol


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class StepStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    SKIPPED = auto()


@dataclass
class StepResult:
    """Outcome of a single step execution."""
    step_name: str
    status: StepStatus
    attempts: int = 0
    duration_ms: int = 0
    output: str = ""
    error: str = ""


# ---------------------------------------------------------------------------
# Command pattern — self-contained workflow steps
# ---------------------------------------------------------------------------

# WHY a Protocol instead of an ABC? -- Protocol enables structural subtyping:
# any callable with the right signature works without inheriting from a base
# class. This means existing functions can be used as steps without wrapping
# them — lowering the barrier to composing complex DAG workflows.
class StepAction(Protocol):
    """Command interface: every step must be callable and return a string."""
    def __call__(self) -> str: ...


@dataclass
class WorkflowStep:
    """A single unit of work in the orchestration graph."""
    name: str
    action: Callable[[], str]
    depends_on: list[str] = field(default_factory=list)
    max_retries: int = 1
    timeout_ms: int = 30_000

    def __hash__(self) -> int:
        return hash(self.name)


# ---------------------------------------------------------------------------
# DAG resolution via topological sort
# ---------------------------------------------------------------------------

class CyclicDependencyError(Exception):
    """Raised when the workflow graph contains a cycle."""


def topological_sort(steps: list[WorkflowStep]) -> list[str]:
    """Kahn's algorithm — returns step names in valid execution order."""
    graph: dict[str, list[str]] = defaultdict(list)
    in_degree: dict[str, int] = {s.name: 0 for s in steps}
    name_set = {s.name for s in steps}

    for step in steps:
        for dep in step.depends_on:
            if dep not in name_set:
                raise ValueError(f"Step '{step.name}' depends on unknown step '{dep}'")
            graph[dep].append(step.name)
            in_degree[step.name] += 1

    queue: deque[str] = deque(name for name, deg in in_degree.items() if deg == 0)
    order: list[str] = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(steps):
        raise CyclicDependencyError("Workflow contains a cyclic dependency")
    return order


# ---------------------------------------------------------------------------
# Orchestrator engine
# ---------------------------------------------------------------------------

@dataclass
class RunReport:
    """Aggregate result of a full orchestration run."""
    results: list[StepResult] = field(default_factory=list)
    total_duration_ms: int = 0

    @property
    def succeeded(self) -> list[StepResult]:
        return [r for r in self.results if r.status == StepStatus.SUCCESS]

    @property
    def failed(self) -> list[StepResult]:
        return [r for r in self.results if r.status == StepStatus.FAILED]

    @property
    def all_passed(self) -> bool:
        return len(self.failed) == 0

    def summary(self) -> dict[str, object]:
        return {
            "total_steps": len(self.results),
            "succeeded": len(self.succeeded),
            "failed": len(self.failed),
            "total_duration_ms": self.total_duration_ms,
        }


class Orchestrator:
    """Resolves dependencies and executes steps in topological order."""

    def __init__(self, steps: list[WorkflowStep], fail_fast: bool = True) -> None:
        self._steps = {s.name: s for s in steps}
        self._fail_fast = fail_fast
        self._execution_order = topological_sort(steps)

    @property
    def execution_order(self) -> list[str]:
        return list(self._execution_order)

    def run(self) -> RunReport:
        """Execute all steps respecting dependency order and retry policy."""
        report = RunReport()
        failed_names: set[str] = set()
        overall_start = time.monotonic()

        for name in self._execution_order:
            step = self._steps[name]

            # Skip if any dependency failed.
            upstream_failed = any(d in failed_names for d in step.depends_on)
            if upstream_failed:
                report.results.append(StepResult(name, StepStatus.SKIPPED))
                failed_names.add(name)
                continue

            result = self._execute_with_retry(step)
            report.results.append(result)

            if result.status == StepStatus.FAILED:
                failed_names.add(name)
                if self._fail_fast:
                    # Mark remaining steps as skipped.
                    remaining = self._execution_order[self._execution_order.index(name) + 1 :]
                    for r_name in remaining:
                        report.results.append(StepResult(r_name, StepStatus.SKIPPED))
                    break

        report.total_duration_ms = int((time.monotonic() - overall_start) * 1000)
        return report

    @staticmethod
    def _execute_with_retry(step: WorkflowStep) -> StepResult:
        last_error = ""
        for attempt in range(1, step.max_retries + 1):
            start = time.monotonic()
            try:
                output = step.action()
                elapsed = int((time.monotonic() - start) * 1000)
                return StepResult(step.name, StepStatus.SUCCESS, attempt, elapsed, output)
            except Exception as exc:
                last_error = str(exc)
        elapsed = int((time.monotonic() - start) * 1000)
        return StepResult(step.name, StepStatus.FAILED, step.max_retries, elapsed, error=last_error)


# ---------------------------------------------------------------------------
# Demo helpers
# ---------------------------------------------------------------------------

def demo_workflow() -> RunReport:
    """Build and run a sample ETL-style pipeline."""
    steps = [
        WorkflowStep("extract", action=lambda: "extracted 100 rows"),
        WorkflowStep("validate", action=lambda: "all rows valid", depends_on=["extract"]),
        WorkflowStep("transform", action=lambda: "transformed to target schema", depends_on=["validate"]),
        WorkflowStep("load", action=lambda: "loaded into warehouse", depends_on=["transform"]),
        WorkflowStep("notify", action=lambda: "sent completion email", depends_on=["load"]),
    ]
    orchestrator = Orchestrator(steps)
    return orchestrator.run()


def main() -> None:
    report = demo_workflow()
    print(f"Pipeline {'PASSED' if report.all_passed else 'FAILED'}")
    for r in report.results:
        tag = r.status.name.ljust(7)
        print(f"  [{tag}] {r.step_name} ({r.attempts} attempt(s), {r.duration_ms}ms)")
    print(f"Total: {report.total_duration_ms}ms")


if __name__ == "__main__":
    main()
