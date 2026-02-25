"""Tests for Level 5 Mini Capstone — Operational Pipeline."""
from pathlib import Path
import json
import pytest
from project import load_config, extract_csv_files, transform_rows, check_thresholds, atomic_write, run_pipeline


def test_load_config_defaults() -> None:
    """Defaults are returned when no file or env vars exist."""
    config = load_config(None)
    assert config["max_retries"] == 3
    assert config["threshold_warn"] == 50


def test_load_config_file_override(tmp_path: Path) -> None:
    """File config overrides defaults."""
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"max_retries": 7}), encoding="utf-8")
    config = load_config(cfg)
    assert config["max_retries"] == 7
    assert config["threshold_warn"] == 50  # unchanged default


def test_load_config_env_override(tmp_path: Path, monkeypatch) -> None:
    """Environment variables take highest precedence."""
    monkeypatch.setenv("PIPELINE_MAX_RETRIES", "10")
    config = load_config(None)
    assert config["max_retries"] == 10


def test_extract_csv_files(tmp_path: Path) -> None:
    """Extracts rows from all CSV files in directory."""
    src = tmp_path / "sources"
    src.mkdir()
    (src / "a.csv").write_text("name,amount\nalice,55\nbob,30\n", encoding="utf-8")
    (src / "b.csv").write_text("name,amount\ncharlie,95\n", encoding="utf-8")
    rows = extract_csv_files(src)
    assert len(rows) == 3


@pytest.mark.parametrize("value_str,expected_numeric", [
    ("75", 75.0),
    ("abc", 0.0),
    ("0", 0.0),
])
def test_transform_rows(value_str, expected_numeric) -> None:
    """Transform parses numeric values and handles non-numeric gracefully."""
    rows = [{"name": "test", "amount": value_str}]
    result = transform_rows(rows)
    assert result[0]["_numeric"] == expected_numeric
    assert result[0]["_row_index"] == 1


@pytest.mark.parametrize("values,warn,crit,expected_warn,expected_crit", [
    ([10, 20, 30], 50, 90, 0, 0),
    ([55, 60, 95], 50, 90, 2, 1),
    ([90, 91], 50, 90, 0, 2),
])
def test_check_thresholds(values, warn, crit, expected_warn, expected_crit) -> None:
    rows = [{"_numeric": v, "_row_index": i} for i, v in enumerate(values, 1)]
    report = check_thresholds(rows, warn, crit)
    assert report["warnings"] == expected_warn
    assert report["criticals"] == expected_crit


def test_atomic_write(tmp_path: Path) -> None:
    """Atomic write creates the file with correct content."""
    target = tmp_path / "sub" / "output.json"
    atomic_write(target, '{"ok": true}')
    assert target.exists()
    assert json.loads(target.read_text(encoding="utf-8")) == {"ok": True}


def test_run_pipeline_integration(tmp_path: Path) -> None:
    """Full pipeline runs end-to-end and produces summary."""
    src = tmp_path / "sources"
    src.mkdir()
    (src / "data.csv").write_text("name,amount\nalice,55\nbob,95\n", encoding="utf-8")
    out = tmp_path / "output"
    config = {
        "input_dir": str(src),
        "output_dir": str(out),
        "threshold_warn": 50,
        "threshold_crit": 90,
        "max_retries": 3,
    }
    summary = run_pipeline(config)
    assert summary["status"] == "completed"
    assert summary["rows_extracted"] == 2
    assert (out / "summary.json").exists()
