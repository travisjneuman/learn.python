# Solution: Level 10 / Project 02 - Autonomous Run Orchestrator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Autonomous Run Orchestrator -- DAG-based workflow engine with dependency resolution."""
from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Protocol


class StepStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    SKIPPED = auto()


@dataclass
class StepResult:
    step_name: str
    status: StepStatus
    attempts: int = 0
    duration_ms: int = 0
    output: str = ""
    error: str = ""


# WHY Protocol for StepAction? -- Any callable with the right signature works as
# a step without wrapping or inheriting. Existing lambda functions, module-level
# functions, and class methods all satisfy the Protocol automatically.
class StepAction(Protocol):
    def __call__(self) -> str: ...


@dataclass
class WorkflowStep:
    name: str
    action: Callable[[], str]
    depends_on: list[str] = field(default_factory=list)
    max_retries: int = 1
    timeout_ms: int = 30_000

    # WHY hash by name only? -- Steps are identified by name in the dependency
    # graph. Two steps with the same name are the same node, regardless of
    # their action or retry config.
    def __hash__(self) -> int:
        return hash(self.name)


class CyclicDependencyError(Exception):
    """Raised when the workflow graph contains a cycle."""


# WHY Kahn's algorithm over DFS-based toposort? -- Kahn's algorithm naturally
# produces the "tier" structure (all nodes with in-degree 0 at each level).
# This makes it straightforward to identify which steps could run in parallel.
# DFS-based toposort would require a separate pass to compute tiers.
def topological_sort(steps: list[WorkflowStep]) -> list[str]:
    graph: dict[str, list[str]] = defaultdict(list)
    in_degree: dict[str, int] = {s.name: 0 for s in steps}
    name_set = {s.name for s in steps}

    for step in steps:
        for dep in step.depends_on:
            # WHY validate dependencies eagerly? -- A typo in a dependency name
            # would silently succeed until runtime. Failing fast here prevents
            # debugging a "step never ran" mystery.
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

    # WHY check length? -- If order is shorter than steps, some nodes were never
    # dequeued, meaning they are part of a cycle.
    if len(order) != len(steps):
        raise CyclicDependencyError("Workflow contains a cyclic dependency")
    return order


@dataclass
class RunReport:
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
    def __init__(self, steps: list[WorkflowStep], fail_fast: bool = True) -> None:
        self._steps = {s.name: s for s in steps}
        self._fail_fast = fail_fast
        # WHY sort at construction? -- Detecting cycles early (before run()) prevents
        # wasted work. The execution order is immutable once computed.
        self._execution_order = topological_sort(steps)

    @property
    def execution_order(self) -> list[str]:
        return list(self._execution_order)

    def run(self) -> RunReport:
        report = RunReport()
        # WHY track failed_names as a set? -- When fail_fast is False, multiple
        # steps can fail. Downstream steps must check if ANY dependency failed,
        # not just the most recent one. A set makes this O(1) per check.
        failed_names: set[str] = set()
        overall_start = time.monotonic()

        for name in self._execution_order:
            step = self._steps[name]

            # Skip if any upstream dependency failed.
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
                    remaining = self._execution_order[self._execution_order.index(name) + 1:]
                    for r_name in remaining:
                        report.results.append(StepResult(r_name, StepStatus.SKIPPED))
                    break

        report.total_duration_ms = int((time.monotonic() - overall_start) * 1000)
        return report

    @staticmethod
    def _execute_with_retry(step: WorkflowStep) -> StepResult:
        """Retry the step action up to max_retries times before declaring failure."""
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


def demo_workflow() -> RunReport:
    steps = [
        WorkflowStep("extract", action=lambda: "extracted 100 rows"),
        WorkflowStep("validate", action=lambda: "all rows valid", depends_on=["extract"]),
        WorkflowStep("transform", action=lambda: "transformed to target schema", depends_on=["validate"]),
        WorkflowStep("load", action=lambda: "loaded into warehouse", depends_on=["transform"]),
        WorkflowStep("notify", action=lambda: "sent completion email", depends_on=["load"]),
    ]
    return Orchestrator(steps).run()


def main() -> None:
    report = demo_workflow()
    print(f"Pipeline {'PASSED' if report.all_passed else 'FAILED'}")
    for r in report.results:
        tag = r.status.name.ljust(7)
        print(f"  [{tag}] {r.step_name} ({r.attempts} attempt(s), {r.duration_ms}ms)")
    print(f"Total: {report.total_duration_ms}ms")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Kahn's algorithm for topological sort | Naturally produces parallelizable "tier" groupings and detects cycles via length check | DFS-based toposort -- detects cycles differently (back edges) but harder to extract tiers |
| failed_names as a set | O(1) lookup when checking if upstream dependencies failed; supports multiple failures in continue-on-error mode | List of failed names -- O(n) lookup per check |
| Retry in a for loop with attempt counter | Simple, predictable retry behavior; attempt count tracked for observability | Exponential backoff -- better for network calls but adds complexity for a learning project |
| fail_fast flag on Orchestrator | Gives callers control: CI pipelines want fail-fast, batch jobs want continue-on-error | Always fail-fast -- simpler but less flexible for real-world use |

## Alternative approaches

### Approach B: DFS-based topological sort with cycle detection

```python
def topo_sort_dfs(steps: list[WorkflowStep]) -> list[str]:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {s.name: WHITE for s in steps}
    order: list[str] = []
    graph = {s.name: s.depends_on for s in steps}

    def visit(node: str) -> None:
        if color[node] == GRAY:
            raise CyclicDependencyError(f"Cycle detected at '{node}'")
        if color[node] == BLACK:
            return
        color[node] = GRAY
        for dep in graph.get(node, []):
            visit(dep)
        color[node] = BLACK
        order.append(node)

    for name in color:
        visit(name)
    return order
```

**Trade-off:** DFS gives you the exact node where the cycle is detected (better error messages). However, it does not naturally produce parallel tiers and uses recursion, which can hit Python's recursion limit on deep graphs. Kahn's algorithm is iterative and tier-friendly.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Cyclic dependency (A depends on B, B depends on A) | `CyclicDependencyError` raised during construction | Validate the DAG structure before building the Orchestrator |
| Step references non-existent dependency | `ValueError` from `topological_sort` | Validate dependency names against registered step names |
| `max_retries=0` | The retry loop `range(1, 1)` never executes, returning FAILED with 0 attempts | Validate `max_retries >= 1` at WorkflowStep construction |
