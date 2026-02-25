"""Tests for Project Config Bootstrap."""

from pathlib import Path

import pytest

from project import (
    AppConfig,
    build_config,
    coerce_value,
    load_defaults,
    load_from_env,
    load_from_file,
    merge_configs,
    validate_config,
)


def test_load_defaults() -> None:
    """Defaults should include all AppConfig fields."""
    defaults = load_defaults()
    assert defaults["app_name"] == "myapp"
    assert defaults["port"] == 8000
    assert defaults["debug"] is False


def test_load_from_file(tmp_path: Path) -> None:
    """Should load config from a JSON file."""
    config_file = tmp_path / "config.json"
    config_file.write_text('{"port": 9000, "debug": true}', encoding="utf-8")
    config = load_from_file(config_file)
    assert config["port"] == 9000
    assert config["debug"] is True


def test_load_from_file_missing(tmp_path: Path) -> None:
    """Missing file should return empty dict."""
    config = load_from_file(tmp_path / "nope.json")
    assert config == {}


def test_load_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Should read APP_ prefixed environment variables."""
    monkeypatch.setenv("APP_PORT", "3000")
    monkeypatch.setenv("APP_DEBUG", "true")
    monkeypatch.setenv("OTHER_VAR", "ignored")
    config = load_from_env("APP_")
    assert config["port"] == "3000"
    assert config["debug"] == "true"
    assert "other_var" not in config


def test_merge_configs() -> None:
    """Later sources should override earlier ones."""
    defaults = {"port": 8000, "host": "localhost"}
    file_cfg = {"port": 9000}
    env_cfg = {"port": "3000"}
    merged = merge_configs(defaults, file_cfg, env_cfg)
    assert merged["port"] == "3000"  # Last wins.
    assert merged["host"] == "localhost"  # From defaults.


def test_coerce_value() -> None:
    """Should convert string values to target types."""
    assert coerce_value("true", bool) is True
    assert coerce_value("false", bool) is False
    assert coerce_value("42", int) == 42
    assert coerce_value("3.14", float) == 3.14
    assert coerce_value("hello", str) == "hello"


def test_build_config_defaults() -> None:
    """With no file or env, should use defaults."""
    config, sources = build_config()
    assert config.app_name == "myapp"
    assert config.port == 8000
    assert all(s.source == "default" for s in sources)


def test_build_config_with_file(tmp_path: Path) -> None:
    """File values should override defaults."""
    f = tmp_path / "config.json"
    f.write_text('{"port": 5000}', encoding="utf-8")
    config, sources = build_config(config_file=f)
    assert config.port == 5000


def test_build_config_cli_overrides() -> None:
    """CLI overrides should take highest precedence."""
    config, sources = build_config(cli_overrides={"port": "4000"})
    assert config.port == 4000


def test_validate_config_valid() -> None:
    """Valid config should produce no issues."""
    config = AppConfig(port=8000, timeout_seconds=30.0)
    assert validate_config(config) == []


def test_validate_config_bad_port() -> None:
    """Invalid port should be flagged."""
    config = AppConfig(port=0)
    issues = validate_config(config)
    assert any("port" in i.lower() for i in issues)


def test_validate_config_negative_retries() -> None:
    """Negative retries should be flagged."""
    config = AppConfig(max_retries=-1)
    issues = validate_config(config)
    assert any("retries" in i.lower() for i in issues)
