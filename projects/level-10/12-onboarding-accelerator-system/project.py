"""Onboarding Accelerator System — Generate onboarding materials and environment setup.

Architecture: Uses the Builder pattern to compose onboarding plans from modular
components (access requests, tool setup, reading lists, buddy assignments). A
RoleTemplate defines what each role needs; the OnboardingBuilder assembles a
personalized plan. The system tracks task completion and computes ramp-up progress.

Design rationale: New-hire onboarding is expensive and inconsistent when done ad-hoc.
By codifying role-specific checklists, teams ensure every engineer gets the same
high-quality start. The builder pattern allows customization without a combinatorial
explosion of plan variants.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

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
    """A single onboarding task."""
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
    """Template defining onboarding tasks for a specific role."""
    role_name: str
    tasks: list[OnboardingTask] = field(default_factory=list)

    def task_count(self) -> int:
        return len(self.tasks)


# ---------------------------------------------------------------------------
# Pre-built role templates
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Onboarding plan (built from template + customization)
# ---------------------------------------------------------------------------

@dataclass
class OnboardingPlan:
    """Personalized onboarding plan for a specific hire."""
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


# ---------------------------------------------------------------------------
# Builder pattern
# ---------------------------------------------------------------------------

class OnboardingBuilder:
    """Builds personalized onboarding plans from role templates."""

    def __init__(self, employee_name: str, role: str) -> None:
        self._name = employee_name
        self._role = role
        self._buddy = ""
        self._extra_tasks: list[OnboardingTask] = []

    def with_buddy(self, buddy_name: str) -> OnboardingBuilder:
        self._buddy = buddy_name
        return self

    def add_task(self, task: OnboardingTask) -> OnboardingBuilder:
        self._extra_tasks.append(task)
        return self

    def build(self) -> OnboardingPlan:
        template = ROLE_TEMPLATES.get(self._role)
        if template is None:
            raise ValueError(f"Unknown role: {self._role}. Available: {list(ROLE_TEMPLATES.keys())}")

        tasks = list(template.tasks) + self._extra_tasks
        return OnboardingPlan(
            employee_name=self._name,
            role=self._role,
            buddy=self._buddy,
            tasks=tasks,
        )


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def main() -> None:
    plan = (
        OnboardingBuilder("Alice Chen", "backend")
        .with_buddy("Bob Smith")
        .add_task(OnboardingTask("CUSTOM-001", "Set up VPN", TaskCategory.TOOLS, TaskPriority.DAY_ONE))
        .build()
    )

    # Simulate completing some tasks
    plan.complete_task("BE-001")
    plan.complete_task("BE-007")

    print(json.dumps(plan.summary(), indent=2))
    print(f"\nDay-one tasks ({len(plan.tasks_by_priority(TaskPriority.DAY_ONE))}):")
    for task in plan.tasks_by_priority(TaskPriority.DAY_ONE):
        tag = task.status.name.ljust(10)
        print(f"  [{tag}] {task.task_id}: {task.title}")


if __name__ == "__main__":
    main()
