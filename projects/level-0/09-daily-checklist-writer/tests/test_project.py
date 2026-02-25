"""Tests for Daily Checklist Writer."""

from pathlib import Path

from project import checklist_summary, format_checklist, load_tasks, write_checklist


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


def test_load_tasks_from_file(tmp_path: Path) -> None:
    """Tasks should be loaded from a file, blank lines skipped."""
    f = tmp_path / "tasks.txt"
    f.write_text("Task A\n\nTask B\n  \nTask C\n", encoding="utf-8")
    tasks = load_tasks(f)
    assert tasks == ["Task A", "Task B", "Task C"]


def test_write_checklist_creates_file(tmp_path: Path) -> None:
    """write_checklist should create the output file."""
    out = tmp_path / "output" / "checklist.txt"
    write_checklist(out, "test content")
    assert out.exists()
    assert out.read_text(encoding="utf-8") == "test content"


def test_checklist_summary_counts() -> None:
    """Summary should have correct total and remaining counts."""
    summary = checklist_summary(["A", "B", "C"])
    assert summary["total_tasks"] == 3
    assert summary["remaining"] == 3
    assert summary["completed"] == 0
