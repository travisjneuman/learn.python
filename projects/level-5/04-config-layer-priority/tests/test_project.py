"""Tests for Config Layer Priority."""
from pathlib import Path
import json
import os
import pytest
from project import load_file_config, load_env_config, coerce_types, resolve_config, run, DEFAULT_CONFIG

def test_load_file_config_missing(tmp_path: Path):
    result = load_file_config(tmp_path / "nope.json")
    assert result == {}

def test_load_file_config_valid(tmp_path: Path):
    f = tmp_path / "config.json"
    f.write_text('{"port": 9090}', encoding="utf-8")
    assert load_file_config(f) == {"port": 9090}

def test_load_env_config(monkeypatch):
    monkeypatch.setenv("APP_PORT", "9090")
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("OTHER_VAR", "ignored")
    result = load_env_config("APP_")
    assert result == {"port": "9090", "debug": "true"}
    assert "other_var" not in result

@pytest.mark.parametrize("value,default_val,expected", [
    ("9090", 8080, 9090),
    ("true", False, True),
    ("false", True, False),
    ("3.14", 0.0, 3.14),
])
def test_coerce_types(value, default_val, expected):
    result = coerce_types({"key": value}, {"key": default_val})
    assert result["key"] == expected

def test_resolve_config_priority():
    defaults = {"port": 8080, "debug": False}
    file_config = {"port": 9090}
    env_config = {"port": "3000"}
    resolved = resolve_config(defaults, file_config, env_config)
    assert resolved["port"] == 3000  # env wins
    assert resolved["debug"] is False  # default

def test_run_integration(tmp_path: Path):
    config = tmp_path / "config.json"
    config.write_text('{"log_level": "DEBUG"}', encoding="utf-8")
    output = tmp_path / "out.json"
    report = run(config, output)
    assert report["config"]["log_level"] == "DEBUG"
    assert report["sources"]["log_level"] == "file"
