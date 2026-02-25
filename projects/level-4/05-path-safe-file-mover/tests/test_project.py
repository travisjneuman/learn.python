"""Tests for Path Safe File Mover."""

from pathlib import Path
import pytest

from project import resolve_collision, plan_moves, execute_moves, run


def test_resolve_collision_no_conflict(tmp_path: Path) -> None:
    target = tmp_path / "report.csv"
    assert resolve_collision(target) == target


def test_resolve_collision_with_existing(tmp_path: Path) -> None:
    existing = tmp_path / "report.csv"
    existing.write_text("data", encoding="utf-8")
    result = resolve_collision(existing)
    assert result == tmp_path / "report_1.csv"


@pytest.mark.parametrize("existing_count", [1, 3, 5])
def test_resolve_collision_multiple(tmp_path: Path, existing_count: int) -> None:
    """Counter increments past all existing collisions."""
    base = tmp_path / "file.txt"
    base.write_text("x", encoding="utf-8")
    for i in range(1, existing_count + 1):
        (tmp_path / f"file_{i}.txt").write_text("x", encoding="utf-8")
    result = resolve_collision(base)
    assert result == tmp_path / f"file_{existing_count + 1}.txt"


def test_plan_moves_lists_files(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.txt").write_text("hello", encoding="utf-8")
    (src / "b.txt").write_text("world", encoding="utf-8")

    dest = tmp_path / "dst"
    plan = plan_moves(src, dest)
    assert len(plan) == 2
    assert all(p["status"] == "planned" for p in plan)


def test_execute_moves_actually_moves(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "data.csv").write_text("content", encoding="utf-8")

    dest = tmp_path / "dst"
    plan = plan_moves(src, dest)
    result = execute_moves(plan)
    assert result[0]["status"] == "moved"
    assert (dest / "data.csv").exists()
    assert not (src / "data.csv").exists()


def test_dry_run_does_not_move(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "file.txt").write_text("keep me", encoding="utf-8")

    dest = tmp_path / "dst"
    plan = plan_moves(src, dest)
    execute_moves(plan, dry_run=True)
    # File should still be in source
    assert (src / "file.txt").exists()
