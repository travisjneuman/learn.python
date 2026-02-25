"""Tests for Onboarding Accelerator System.

Covers builder pattern, role templates, task completion, progress tracking,
and plan customization.
"""
from __future__ import annotations

import pytest

from project import (
    CompletionStatus,
    OnboardingBuilder,
    OnboardingPlan,
    OnboardingTask,
    TaskCategory,
    TaskPriority,
    backend_engineer_template,
    frontend_engineer_template,
)


@pytest.fixture
def backend_plan() -> OnboardingPlan:
    return OnboardingBuilder("Alice", "backend").with_buddy("Bob").build()


# ---------------------------------------------------------------------------
# Role templates
# ---------------------------------------------------------------------------

class TestRoleTemplates:
    def test_backend_has_tasks(self) -> None:
        template = backend_engineer_template()
        assert template.task_count() >= 10

    def test_frontend_has_tasks(self) -> None:
        template = frontend_engineer_template()
        assert template.task_count() >= 7

    def test_templates_have_day_one_tasks(self) -> None:
        for template in [backend_engineer_template(), frontend_engineer_template()]:
            day_one = [t for t in template.tasks if t.priority == TaskPriority.DAY_ONE]
            assert len(day_one) > 0


# ---------------------------------------------------------------------------
# Builder pattern
# ---------------------------------------------------------------------------

class TestOnboardingBuilder:
    def test_builds_plan_from_template(self) -> None:
        plan = OnboardingBuilder("Test", "backend").build()
        assert plan.employee_name == "Test"
        assert len(plan.tasks) >= 10

    def test_buddy_assignment(self) -> None:
        plan = OnboardingBuilder("Test", "backend").with_buddy("Mentor").build()
        assert plan.buddy == "Mentor"

    def test_custom_task_added(self) -> None:
        extra = OnboardingTask("X-001", "Custom task", TaskCategory.TOOLS, TaskPriority.DAY_ONE)
        plan = OnboardingBuilder("Test", "backend").add_task(extra).build()
        ids = [t.task_id for t in plan.tasks]
        assert "X-001" in ids

    def test_unknown_role_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown role"):
            OnboardingBuilder("Test", "data-scientist").build()


# ---------------------------------------------------------------------------
# Task completion and progress
# ---------------------------------------------------------------------------

class TestOnboardingPlan:
    def test_initial_completion_zero(self, backend_plan: OnboardingPlan) -> None:
        assert backend_plan.completion_pct == 0.0

    def test_complete_task_increases_progress(self, backend_plan: OnboardingPlan) -> None:
        backend_plan.complete_task("BE-001")
        assert backend_plan.completion_pct > 0.0

    def test_complete_all_tasks_reaches_100(self, backend_plan: OnboardingPlan) -> None:
        for task in backend_plan.tasks:
            task.status = CompletionStatus.DONE
        assert backend_plan.completion_pct == 100.0

    def test_complete_nonexistent_returns_false(self, backend_plan: OnboardingPlan) -> None:
        assert backend_plan.complete_task("FAKE-999") is False

    def test_tasks_by_priority(self, backend_plan: OnboardingPlan) -> None:
        day_one = backend_plan.tasks_by_priority(TaskPriority.DAY_ONE)
        assert len(day_one) > 0
        assert all(t.priority == TaskPriority.DAY_ONE for t in day_one)

    def test_summary_structure(self, backend_plan: OnboardingPlan) -> None:
        summary = backend_plan.summary()
        assert "employee" in summary
        assert "completion" in summary
        assert "by_priority" in summary
