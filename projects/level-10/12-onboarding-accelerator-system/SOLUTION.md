# Solution: Level 10 / Project 12 - Onboarding Accelerator System

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Onboarding Accelerator System -- Generate onboarding materials and environment setup."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class TaskCategory(Enum):
    ACCESS = auto()
    TOOLS = auto()
    READING = auto()
    MEETINGS = auto()
    CODING = auto()


# WHY time-based priority tiers? -- Onboarding tasks have natural ordering:
# DAY_ONE (laptop access, email) must happen before FIRST_WEEK (codebase
# walkthrough). Encoding priority as an enum rather than a raw number makes
# the timeline self-documenting and prevents meaningless values like "priority 47."
class TaskPriority(Enum):
    DAY_ONE = auto()
    FIRST_WEEK = auto()
    FIRST_MONTH = auto()
    FIRST_QUARTER = auto()


class CompletionStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    BLOCKED = auto()


@dataclass
class OnboardingTask:
    task_id: str
    title: str
    category: TaskCategory
    priority: TaskPriority
    description: str = ""
    status: CompletionStatus = CompletionStatus.PENDING
    assigned_to: str = ""
    depends_on: list[str] = field(default_factory=list)


@dataclass
class RoleTemplate:
    role_name: str
    tasks: list[OnboardingTask] = field(default_factory=list)

    def task_count(self) -> int:
        return len(self.tasks)


def backend_engineer_template() -> RoleTemplate:
    return RoleTemplate("Backend Engineer", [
        OnboardingTask("BE-001", "Request GitHub access", TaskCategory.ACCESS, TaskPriority.DAY_ONE),
        OnboardingTask("BE-002", "Request AWS console access", TaskCategory.ACCESS, TaskPriority.DAY_ONE),
        OnboardingTask("BE-003", "Install Python + toolchain", TaskCategory.TOOLS, TaskPriority.DAY_ONE,
                       "Install Python 3.11+, pip, ruff, black, pytest"),
        OnboardingTask("BE-004", "Clone core repositories", TaskCategory.TOOLS, TaskPriority.DAY_ONE,
                       depends_on=["BE-001"]),
        OnboardingTask("BE-005", "Read architecture overview", TaskCategory.READING, TaskPriority.FIRST_WEEK),
        OnboardingTask("BE-006", "Read API design guidelines", TaskCategory.READING, TaskPriority.FIRST_WEEK),
        OnboardingTask("BE-007", "Meet team lead", TaskCategory.MEETINGS, TaskPriority.DAY_ONE),
        OnboardingTask("BE-008", "Complete first code review", TaskCategory.CODING, TaskPriority.FIRST_WEEK,
                       depends_on=["BE-004"]),
        OnboardingTask("BE-009", "Submit first PR", TaskCategory.CODING, TaskPriority.FIRST_MONTH,
                       depends_on=["BE-008"]),
        OnboardingTask("BE-010", "Complete on-call shadow", TaskCategory.CODING, TaskPriority.FIRST_QUARTER),
    ])


def frontend_engineer_template() -> RoleTemplate:
    return RoleTemplate("Frontend Engineer", [
        OnboardingTask("FE-001", "Request GitHub access", TaskCategory.ACCESS, TaskPriority.DAY_ONE),
        OnboardingTask("FE-002", "Install Node.js + toolchain", TaskCategory.TOOLS, TaskPriority.DAY_ONE),
        OnboardingTask("FE-003", "Clone frontend repos", TaskCategory.TOOLS, TaskPriority.DAY_ONE,
                       depends_on=["FE-001"]),
        OnboardingTask("FE-004", "Read component library docs", TaskCategory.READING, TaskPriority.FIRST_WEEK),
        OnboardingTask("FE-005", "Meet design team", TaskCategory.MEETINGS, TaskPriority.DAY_ONE),
        OnboardingTask("FE-006", "Build a sample feature", TaskCategory.CODING, TaskPriority.FIRST_WEEK,
                       depends_on=["FE-003"]),
        OnboardingTask("FE-007", "Submit first PR", TaskCategory.CODING, TaskPriority.FIRST_MONTH,
                       depends_on=["FE-006"]),
    ])


ROLE_TEMPLATES: dict[str, RoleTemplate] = {
    "backend": backend_engineer_template(),
    "frontend": frontend_engineer_template(),
}


@dataclass
class OnboardingPlan:
    employee_name: str
    role: str
    buddy: str = ""
    tasks: list[OnboardingTask] = field(default_factory=list)

    @property
    def completion_pct(self) -> float:
        if not self.tasks:
            return 0.0
        done = sum(1 for t in self.tasks if t.status == CompletionStatus.DONE)
        return (done / len(self.tasks)) * 100

    @property
    def blocked_tasks(self) -> list[OnboardingTask]:
        return [t for t in self.tasks if t.status == CompletionStatus.BLOCKED]

    def tasks_by_priority(self, priority: TaskPriority) -> list[OnboardingTask]:
        return [t for t in self.tasks if t.priority == priority]

    def complete_task(self, task_id: str) -> bool:
        for task in self.tasks:
            if task.task_id == task_id:
                task.status = CompletionStatus.DONE
                return True
        return False

    def summary(self) -> dict[str, Any]:
        by_priority: dict[str, int] = {}
        for p in TaskPriority:
            tasks = self.tasks_by_priority(p)
            by_priority[p.name.lower()] = len(tasks)
        return {
            "employee": self.employee_name,
            "role": self.role,
            "buddy": self.buddy,
            "total_tasks": len(self.tasks),
            "completion": f"{self.completion_pct:.0f}%",
            "blocked": len(self.blocked_tasks),
            "by_priority": by_priority,
        }


# WHY Builder pattern instead of a constructor with many parameters? -- The
# Builder lets you chain optional customizations (buddy, extra tasks) without
# a constructor that takes 10+ arguments. Method chaining reads like English:
# OnboardingBuilder("Alice", "backend").with_buddy("Bob").add_task(...).build()
class OnboardingBuilder:
    def __init__(self, employee_name: str, role: str) -> None:
        self._name = employee_name
        self._role = role
        self._buddy = ""
        self._extra_tasks: list[OnboardingTask] = []

    # WHY return self? -- Returning self enables method chaining (fluent API).
    # Each method modifies state and returns the same builder, so calls
    # can be strung together on one line.
    def with_buddy(self, buddy_name: str) -> OnboardingBuilder:
        self._buddy = buddy_name
        return self

    def add_task(self, task: OnboardingTask) -> OnboardingBuilder:
        self._extra_tasks.append(task)
        return self

    # WHY ValueError for unknown role? -- Silently falling back to an empty
    # plan would leave the new hire without any onboarding tasks. Failing
    # loudly forces the caller to either add a template or fix the typo.
    def build(self) -> OnboardingPlan:
        template = ROLE_TEMPLATES.get(self._role)
        if template is None:
            raise ValueError(f"Unknown role: {self._role}. Available: {list(ROLE_TEMPLATES.keys())}")
        tasks = list(template.tasks) + self._extra_tasks
        return OnboardingPlan(
            employee_name=self._name, role=self._role,
            buddy=self._buddy, tasks=tasks,
        )


def main() -> None:
    plan = (
        OnboardingBuilder("Alice Chen", "backend")
        .with_buddy("Bob Smith")
        .add_task(OnboardingTask("CUSTOM-001", "Set up VPN", TaskCategory.TOOLS, TaskPriority.DAY_ONE))
        .build()
    )
    plan.complete_task("BE-001")
    plan.complete_task("BE-007")

    print(json.dumps(plan.summary(), indent=2))
    print(f"\nDay-one tasks ({len(plan.tasks_by_priority(TaskPriority.DAY_ONE))}):")
    for task in plan.tasks_by_priority(TaskPriority.DAY_ONE):
        tag = task.status.name.ljust(10)
        print(f"  [{tag}] {task.task_id}: {task.title}")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Builder pattern with method chaining | Reads like English, handles optional customizations cleanly, avoids a constructor with 10+ parameters | Constructor with keyword arguments -- works but does not guide the caller through the customization steps |
| Enum-based priority tiers (DAY_ONE, FIRST_WEEK, etc.) | Self-documenting timeline; prevents meaningless numeric priorities like "42" | Integer priorities -- flexible but require external documentation to explain what the numbers mean |
| Role templates as factory functions | Each template can have different task counts and structures; functions are easy to test independently | YAML/JSON config files -- more flexible but require parsing and validation |
| Task dependency tracking via `depends_on` list | Models real-world prerequisites (cannot clone repos before getting GitHub access) | Flat ordered list -- simpler but does not express which tasks are truly blocked vs merely sequenced |
| Mutable OnboardingTask status | Tasks are updated as the new hire progresses; immutable tasks would require replacing the entire task on each update | Immutable with copy-and-replace -- correct but adds ceremony for a simple state change |

## Alternative approaches

### Approach B: Config-driven templates from YAML

```python
import yaml
from pathlib import Path

def load_template_from_yaml(path: Path) -> RoleTemplate:
    data = yaml.safe_load(path.read_text())
    tasks = [
        OnboardingTask(
            task_id=t["id"], title=t["title"],
            category=TaskCategory[t["category"]],
            priority=TaskPriority[t["priority"]],
            depends_on=t.get("depends_on", []),
        )
        for t in data["tasks"]
    ]
    return RoleTemplate(role_name=data["role"], tasks=tasks)
```

**Trade-off:** YAML-driven templates let HR or managers define onboarding plans without writing Python. They can add new roles by creating a file rather than editing code. However, YAML templates lack type safety and validation at parse time, meaning errors are caught at runtime rather than at import.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Unknown role passed to builder | `ValueError` with a clear message listing available roles | Validate role against `ROLE_TEMPLATES` keys before building |
| Completing a non-existent task ID | `complete_task` returns `False` silently | Check the return value and surface an error to the user |
| Circular task dependencies (A depends on B, B depends on A) | Neither task can be completed if dependency enforcement is added | Detect cycles at plan build time using topological sort |
