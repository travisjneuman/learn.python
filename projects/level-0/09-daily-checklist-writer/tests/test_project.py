"""Tests for Daily Checklist Writer."""

from project import checklist_summary, format_checklist


def test_format_checklist_has_numbers() -> None:
    """Each task should be numbered with a checkbox."""
    result = format_checklist("My Tasks", ["Buy milk", "Walk dog"])
    assert "1. [ ] Buy milk" in result
    assert "2. [ ] Walk dog" in result
    assert "Total tasks: 2" in result


def test_format_checklist_empty() -> None:
    """An empty task list should show '(no tasks)'."""
    result = format_checklist("Empty", [])
    assert "(no tasks)" in result


def test_format_checklist_title() -> None:
    """The title should appear at the top of the checklist."""
    result = format_checklist("Morning Routine", ["Wake up", "Brush teeth"])
    assert result.startswith("Morning Routine")


def test_checklist_summary_counts() -> None:
    """Summary should have correct total and remaining counts."""
    summary = checklist_summary(["A", "B", "C"])
    assert summary["total_tasks"] == 3
    assert summary["remaining"] == 3
    assert summary["completed"] == 0
