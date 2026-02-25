"""Tests for Checkpoint Recovery Tool."""

from pathlib import Path
import json
import pytest

from project import (
    load_checkpoint,
    save_checkpoint,
    clear_checkpoint,
    process_item,
    process_with_checkpoints,
    run,
)


def test_load_checkpoint_no_file(tmp_path: Path) -> None:
    state = load_checkpoint(tmp_path / "nope.json")
    assert state["last_processed_index"] == -1
    assert state["results"] == []


def test_save_and_load_checkpoint(tmp_path: Path) -> None:
    cp = tmp_path / "cp.json"
    save_checkpoint(cp, 4, [{"a": 1}])
    state = load_checkpoint(cp)
    assert state["last_processed_index"] == 4
    assert len(state["results"]) == 1


def test_clear_checkpoint(tmp_path: Path) -> None:
    cp = tmp_path / "cp.json"
    save_checkpoint(cp, 0, [])
    assert cp.exists()
    clear_checkpoint(cp)
    assert not cp.exists()


@pytest.mark.parametrize(
    "item, expected_keys",
    [
        ("hello world", {"original", "length", "word_count", "uppercase"}),
        ("", {"original", "length", "word_count", "uppercase"}),
    ],
)
def test_process_item(item: str, expected_keys: set) -> None:
    result = process_item(item)
    assert set(result.keys()) == expected_keys


def test_process_with_checkpoints_resumes(tmp_path: Path) -> None:
    """Simulates crash recovery by pre-saving a checkpoint."""
    cp = tmp_path / "cp.json"
    # Pretend we already processed items 0 and 1
    save_checkpoint(cp, 1, [
        {"index": 0, "original": "aaa"},
        {"index": 1, "original": "bbb"},
    ])

    items = ["aaa", "bbb", "ccc", "ddd"]
    results = process_with_checkpoints(items, cp, batch_size=10)
    # Should have 4 total: 2 from checkpoint + 2 newly processed
    assert len(results) == 4
    assert results[2]["index"] == 2


def test_run_integration(tmp_path: Path) -> None:
    input_file = tmp_path / "items.txt"
    input_file.write_text("apple\nbanana\ncherry\ndate\n", encoding="utf-8")

    output = tmp_path / "output.json"
    cp = tmp_path / "cp.json"
    summary = run(input_file, output, cp, batch_size=2)

    assert summary["processed"] == 4
    assert output.exists()
    assert not cp.exists()  # checkpoint cleared on success
