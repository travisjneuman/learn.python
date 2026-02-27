"""Tests for JSON Settings Loader."""

from pathlib import Path

import pytest

from project import load_json, merge_settings, validate_settings


def test_load_json_valid(tmp_path: Path) -> None:
    f = tmp_path / "settings.json"
    f.write_text('{"debug": true, "port": 9090}', encoding="utf-8")
    result = load_json(f)
    assert result["debug"] is True
    assert result["port"] == 9090


def test_load_json_invalid(tmp_path: Path) -> None:
    f = tmp_path / "bad.json"
    f.write_text("{not valid json}", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_json(f)


def test_load_json_malformed_shows_location(tmp_path: Path) -> None:
    """Malformed JSON error message includes line number and position."""
    # Trailing comma after "port" makes this invalid JSON.
    bad_content = '{\n  "debug": true,\n  "port": 9090,\n}'
    f = tmp_path / "malformed.json"
    f.write_text(bad_content, encoding="utf-8")
    with pytest.raises(ValueError, match=r"line \d+, position \d+"):
        load_json(f)


def test_merge_settings_overrides() -> None:
    defaults = {"a": 1, "b": 2}
    overrides = {"b": 99, "c": 3}
    merged = merge_settings(defaults, overrides)
    assert merged == {"a": 1, "b": 99, "c": 3}


def test_merge_preserves_original() -> None:
    defaults = {"a": 1}
    merge_settings(defaults, {"a": 2})
    assert defaults["a"] == 1  # Original unchanged.


def test_validate_settings_finds_missing() -> None:
    settings = {"app_name": "Test"}
    missing = validate_settings(settings, ["app_name", "port"])
    assert "port" in missing
    assert "app_name" not in missing
