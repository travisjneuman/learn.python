"""Tests for Resilient JSON Loader."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from project import try_load_json, try_repair_json, load_with_fallbacks, run


# ---------- try_load_json ----------

@pytest.mark.parametrize("content,should_succeed", [
    ('[{"a": 1}]', True),
    ('{"key": "value"}', True),
    ("{invalid json", False),
    ("not json", False),
])
def test_try_load_json_parsing(tmp_path: Path, content: str, should_succeed: bool) -> None:
    f = tmp_path / "test.json"
    f.write_text(content, encoding="utf-8")
    data, err = try_load_json(f)
    if should_succeed:
        assert data is not None and err is None
    else:
        assert data is None and err is not None


def test_try_load_json_missing(tmp_path: Path) -> None:
    data, err = try_load_json(tmp_path / "nope.json")
    assert data is None and "not found" in err


# ---------- try_repair_json ----------

@pytest.mark.parametrize("broken_text,should_repair,expected_len", [
    ('[{"a": 1},{"b": 2},]', True, 2),   # trailing comma in array
    ('{"key": "val",}', True, None),       # trailing comma in object
    ('{"a": 1}\n{"b": 2}\n', True, 2),    # JSON Lines
    ("totally {{{ broken", False, None),   # unrepairable
])
def test_try_repair_json(
    broken_text: str,
    should_repair: bool,
    expected_len: int | None,
) -> None:
    result = try_repair_json(broken_text)
    if should_repair:
        assert result is not None
        if expected_len is not None:
            assert len(result) == expected_len
    else:
        assert result is None


# ---------- load_with_fallbacks ----------

def test_load_primary_success(tmp_path: Path) -> None:
    primary = tmp_path / "p.json"
    primary.write_text("[1,2,3]", encoding="utf-8")
    data, status = load_with_fallbacks(primary, [])
    assert status["method"] == "primary"
    assert data == [1, 2, 3]


def test_load_uses_fallback_when_primary_fails(tmp_path: Path) -> None:
    primary = tmp_path / "p.json"
    primary.write_text("{bad", encoding="utf-8")
    backup = tmp_path / "b.json"
    backup.write_text("[1,2]", encoding="utf-8")
    data, status = load_with_fallbacks(primary, [backup])
    assert status["method"] == "fallback"
    assert data == [1, 2]


def test_load_uses_repair_when_all_files_fail(tmp_path: Path) -> None:
    primary = tmp_path / "p.json"
    primary.write_text("[1,2,3,]", encoding="utf-8")  # trailing comma — repairable
    data, status = load_with_fallbacks(primary, [])
    assert status["method"] == "repair"
    assert data == [1, 2, 3]


def test_load_all_fail_returns_empty(tmp_path: Path) -> None:
    primary = tmp_path / "missing.json"
    data, status = load_with_fallbacks(primary, [])
    assert status["method"] == "none"
    assert data == []


# ---------- integration: run ----------

def test_run_writes_report(tmp_path: Path) -> None:
    f = tmp_path / "data.json"
    f.write_text('[{"name": "test"}]', encoding="utf-8")
    output = tmp_path / "out.json"
    report = run(f, output)
    assert output.exists()
    assert report["records_loaded"] == 1
    assert report["load_status"]["method"] == "primary"
    saved = json.loads(output.read_text())
    assert saved["records_loaded"] == 1
