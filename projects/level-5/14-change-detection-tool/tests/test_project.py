"""Tests for Change Detection Tool."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import file_hash, is_binary_file, line_diff, detect_changes, run


# ---------- file_hash ----------

def test_file_hash_deterministic(tmp_path: Path) -> None:
    f = tmp_path / "a.txt"
    f.write_text("hello world\n", encoding="utf-8")
    h1 = file_hash(f)
    h2 = file_hash(f)
    assert h1 == h2
    assert len(h1) == 64  # SHA-256 hex digest length


def test_file_hash_differs_for_different_content(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("alpha\n", encoding="utf-8")
    b.write_text("beta\n", encoding="utf-8")
    assert file_hash(a) != file_hash(b)


# ---------- is_binary_file ----------

def test_is_binary_file_detects_binary(tmp_path: Path) -> None:
    f = tmp_path / "binary.bin"
    f.write_bytes(b"header\x00data\x00footer")
    assert is_binary_file(f) is True


def test_is_binary_file_text_is_not_binary(tmp_path: Path) -> None:
    f = tmp_path / "text.txt"
    f.write_text("plain text file\n", encoding="utf-8")
    assert is_binary_file(f) is False


# ---------- line_diff ----------

@pytest.mark.parametrize("old_lines,new_lines,exp_added,exp_removed", [
    (["a", "b"], ["a", "b", "c"], 1, 0),
    (["a", "b", "c"], ["a", "b"], 0, 1),
    (["a", "b"], ["a", "b"], 0, 0),
    (["x"], ["y"], 1, 1),
    ([], ["new"], 1, 0),
])
def test_line_diff(
    old_lines: list[str],
    new_lines: list[str],
    exp_added: int,
    exp_removed: int,
) -> None:
    result = line_diff(old_lines, new_lines)
    assert result["added_count"] == exp_added
    assert result["removed_count"] == exp_removed
    assert "change_percentage" in result


# ---------- detect_changes ----------

def test_detect_unchanged(tmp_path: Path) -> None:
    a = tmp_path / "old.txt"
    b = tmp_path / "new.txt"
    a.write_text("same content\n", encoding="utf-8")
    b.write_text("same content\n", encoding="utf-8")
    result = detect_changes(a, b)
    assert result["status"] == "unchanged"


def test_detect_modified(tmp_path: Path) -> None:
    old = tmp_path / "old.txt"
    new = tmp_path / "new.txt"
    old.write_text("line1\nline2\n", encoding="utf-8")
    new.write_text("line1\nline3\n", encoding="utf-8")
    result = detect_changes(old, new)
    assert result["status"] == "modified"
    assert result["diff"]["added_count"] >= 1


def test_detect_new_file(tmp_path: Path) -> None:
    old = tmp_path / "does_not_exist.txt"
    new = tmp_path / "new.txt"
    new.write_text("brand new\n", encoding="utf-8")
    result = detect_changes(old, new)
    assert result["status"] == "new_file"


def test_detect_same_path(tmp_path: Path) -> None:
    f = tmp_path / "same.txt"
    f.write_text("content\n", encoding="utf-8")
    result = detect_changes(f, f)
    assert result["status"] == "unchanged"


# ---------- integration: run ----------

def test_run_writes_report(tmp_path: Path) -> None:
    old = tmp_path / "old.txt"
    new = tmp_path / "new.txt"
    out = tmp_path / "report.json"
    old.write_text("alpha\nbeta\n", encoding="utf-8")
    new.write_text("alpha\ngamma\n", encoding="utf-8")
    report = run(old, new, out)
    assert out.exists()
    assert report["status"] == "modified"
    saved = json.loads(out.read_text())
    assert saved["status"] == "modified"
