"""Tests for Batch Rename Simulator."""

import pytest

from project import (
    apply_rule_lower,
    apply_rule_replace_spaces,
    apply_rule_strip_numbers,
    detect_conflicts,
    simulate_batch,
    simulate_rename,
)


def test_apply_rule_lower() -> None:
    assert apply_rule_lower("README.MD") == "readme.md"
    assert apply_rule_lower("My File.TXT") == "my file.txt"


def test_apply_rule_replace_spaces() -> None:
    assert apply_rule_replace_spaces("my file name.txt") == "my_file_name.txt"
    assert apply_rule_replace_spaces("nochange.py") == "nochange.py"


def test_apply_rule_strip_numbers() -> None:
    assert apply_rule_strip_numbers("001_photo.jpg") == "photo.jpg"
    assert apply_rule_strip_numbers("42-notes.txt") == "notes.txt"


def test_simulate_rename_valid() -> None:
    result = simulate_rename("Hello World.txt", "lower")
    assert result["original"] == "Hello World.txt"
    assert result["renamed"] == "hello world.txt"
    assert result["changed"] is True


def test_simulate_rename_unknown_rule() -> None:
    with pytest.raises(ValueError, match="Unknown rule"):
        simulate_rename("file.txt", "nonexistent")


def test_simulate_batch_skips_blanks() -> None:
    names = ["File.TXT", "", "  ", "Other.TXT"]
    results = simulate_batch(names, "lower")
    assert len(results) == 2
    assert results[0]["renamed"] == "file.txt"


def test_detect_conflicts() -> None:
    results = [
        {"original": "A.TXT", "renamed": "a.txt", "changed": True},
        {"original": "a.txt", "renamed": "a.txt", "changed": False},
    ]
    conflicts = detect_conflicts(results)
    assert "a.txt" in conflicts


def test_no_conflicts() -> None:
    results = [
        {"original": "A.TXT", "renamed": "a.txt", "changed": True},
        {"original": "B.TXT", "renamed": "b.txt", "changed": True},
    ]
    assert detect_conflicts(results) == []
