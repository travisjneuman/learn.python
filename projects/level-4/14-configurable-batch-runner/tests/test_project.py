"""Tests for Configurable Batch Runner."""

from pathlib import Path
import json
import pytest

from project import action_count_lines, action_word_frequency, action_file_stats, run_batch, run


def test_action_count_lines(tmp_path: Path) -> None:
    f = tmp_path / "data.txt"
    f.write_text("hello\nworld\nhello again\n", encoding="utf-8")
    result = action_count_lines(f, {})
    assert result["total_lines"] == 3


def test_action_count_lines_with_pattern(tmp_path: Path) -> None:
    f = tmp_path / "data.txt"
    f.write_text("error: something\ninfo: ok\nerror: another\n", encoding="utf-8")
    result = action_count_lines(f, {"pattern": "error"})
    assert result["matching_lines"] == 2


@pytest.mark.parametrize("top_n", [1, 3, 5])
def test_action_word_frequency(tmp_path: Path, top_n: int) -> None:
    f = tmp_path / "data.txt"
    f.write_text("the cat sat on the mat the cat", encoding="utf-8")
    result = action_word_frequency(f, {"top_n": top_n})
    assert len(result["top_words"]) <= top_n
    assert result["top_words"][0][0] == "the"


def test_action_file_stats(tmp_path: Path) -> None:
    f = tmp_path / "data.txt"
    f.write_text("hello world\n", encoding="utf-8")
    result = action_file_stats(f, {})
    assert result["line_count"] == 1
    assert result["word_count"] == 2


def test_run_batch_handles_unknown_action(tmp_path: Path) -> None:
    config = {"jobs": [{"name": "bad", "action": "nonexistent", "input": "x.txt"}]}
    results = run_batch(config, tmp_path)
    assert results[0]["status"] == "skipped"


def test_run_integration(tmp_path: Path) -> None:
    data_file = tmp_path / "input.txt"
    data_file.write_text("one two three\nfour five six\n", encoding="utf-8")

    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({
        "jobs": [
            {"name": "count", "action": "count_lines", "input": "input.txt", "params": {}},
            {"name": "stats", "action": "file_stats", "input": "input.txt", "params": {}},
        ]
    }), encoding="utf-8")

    output = tmp_path / "report.json"
    report = run(config_file, output)
    assert report["succeeded"] == 2
    assert report["failed"] == 0
