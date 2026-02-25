"""
Tests for Project 03 — Fixtures Advanced (test_project.py)

Additional fixture-based tests that complement test_processor.py. These
demonstrate monkeypatch for environment variables, tmp_path for file I/O,
and combining multiple fixtures.

Why fixtures for this code?
    FileProcessor reads environment variables and processes files. Without
    fixtures, each test would need to set up env vars and temp files manually.
    Fixtures encapsulate that setup so tests stay focused on behavior.

Run with: pytest tests/test_project.py -v
"""

import os

import pytest

from project import FileProcessor


# ── Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def processor():
    """Create a fresh FileProcessor instance.

    WHY: Each test gets its own processor so config from one test
    does not leak into another. This is the same reason create_app()
    exists in FastAPI testing.
    """
    return FileProcessor()


@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary text file with known content.

    WHY: tmp_path gives us an isolated directory that pytest cleans up
    automatically. We never touch real files on disk, so tests cannot
    interfere with each other or leave garbage behind.
    """
    filepath = tmp_path / "input.txt"
    filepath.write_text("  Hello World  \n  Python Rules  \n")
    return str(filepath)


# ── Test: load_config reads environment variables ──────────────────────

def test_load_config_defaults(processor):
    """load_config should use defaults when env vars are not set.

    WHY: The function reads APP_MODE, APP_STRIP, and APP_OUTPUT_DIR from
    the environment. If none are set, it should fall back to sensible
    defaults. This test verifies the defaults match the docstring.
    """
    config = processor.load_config()

    assert config["mode"] == "uppercase", "Default mode should be 'uppercase'"
    assert config["strip_whitespace"] is True, "Default strip should be True"
    assert config["output_dir"] == "output", "Default output dir should be 'output'"


def test_load_config_reads_env_vars(processor, monkeypatch):
    """load_config should read configuration from environment variables.

    WHY: monkeypatch.setenv safely sets environment variables for the
    duration of this test. After the test, monkeypatch restores the
    original values. This prevents tests from polluting each other's
    environment.
    """
    monkeypatch.setenv("APP_MODE", "lowercase")
    monkeypatch.setenv("APP_STRIP", "false")
    monkeypatch.setenv("APP_OUTPUT_DIR", "/tmp/custom")

    config = processor.load_config()

    assert config["mode"] == "lowercase", "Should read APP_MODE from env"
    assert config["strip_whitespace"] is False, "Should parse 'false' as False"
    assert config["output_dir"] == "/tmp/custom", "Should read APP_OUTPUT_DIR from env"


# ── Test: process_file with uppercase mode ─────────────────────────────

def test_process_file_uppercase(processor, sample_file, monkeypatch):
    """process_file in uppercase mode should convert all text to uppercase.

    WHY: This tests the default behavior (APP_MODE=uppercase). The function
    should both strip whitespace and uppercase the text.
    """
    monkeypatch.setenv("APP_MODE", "uppercase")
    monkeypatch.setenv("APP_STRIP", "true")

    result = processor.process_file(sample_file)

    assert result[0] == "HELLO WORLD", "Should strip whitespace and uppercase"
    assert result[1] == "PYTHON RULES", "Second line should also be processed"


def test_process_file_lowercase(processor, sample_file, monkeypatch):
    """process_file in lowercase mode should convert all text to lowercase.

    WHY: Tests the lowercase branch of the mode switch. If only uppercase
    is tested, a bug in the lowercase branch would go unnoticed.
    """
    monkeypatch.setenv("APP_MODE", "lowercase")
    monkeypatch.setenv("APP_STRIP", "true")

    result = processor.process_file(sample_file)

    assert result[0] == "hello world", "Should strip and lowercase"


def test_process_file_passthrough_mode(processor, sample_file, monkeypatch):
    """process_file with an unknown mode should leave text unchanged.

    WHY: The function has an implicit 'else' branch that leaves text
    unchanged when mode is neither uppercase nor lowercase. This test
    verifies that passthrough works correctly.
    """
    monkeypatch.setenv("APP_MODE", "passthrough")
    monkeypatch.setenv("APP_STRIP", "true")

    result = processor.process_file(sample_file)

    assert result[0] == "Hello World", "Should strip but not change case"


# ── Test: process_file without stripping ───────────────────────────────

def test_process_file_no_strip(processor, tmp_path, monkeypatch):
    """process_file with strip_whitespace=False should preserve leading spaces.

    WHY: Some file formats are whitespace-sensitive (e.g., YAML, Makefiles).
    Users need the option to disable stripping. This test verifies the
    APP_STRIP=false path.
    """
    monkeypatch.setenv("APP_MODE", "uppercase")
    monkeypatch.setenv("APP_STRIP", "false")

    filepath = tmp_path / "spaces.txt"
    filepath.write_text("  indented line\n")

    result = processor.process_file(str(filepath))

    # Leading spaces should be preserved, only the newline stripped.
    assert result[0] == "  INDENTED LINE", "Should uppercase but keep leading spaces"


# ── Test: process_file with missing file ───────────────────────────────

def test_process_file_raises_on_missing_file(processor):
    """process_file should raise FileNotFoundError for missing files.

    WHY: The function deliberately does not catch FileNotFoundError because
    the caller needs to know when a file is missing. Silently returning an
    empty list would hide the problem.
    """
    with pytest.raises(FileNotFoundError):
        processor.process_file("/nonexistent/path/file.txt")


# ── Test: save_results writes output correctly ─────────────────────────

def test_save_results_creates_file(processor, tmp_path):
    """save_results should write processed lines to the output file.

    WHY: The save step is the final deliverable. If it fails to write
    or writes corrupt data, all the processing was wasted.
    """
    output_path = str(tmp_path / "output.txt")
    lines = ["HELLO WORLD", "PYTHON RULES"]

    result = processor.save_results(lines, output_path)

    assert result == output_path, "Should return the output path"
    assert os.path.exists(output_path), "Output file should exist"

    content = open(output_path).read()
    assert "HELLO WORLD\n" in content
    assert "PYTHON RULES\n" in content


def test_save_results_creates_directories(processor, tmp_path):
    """save_results should create parent directories if they do not exist.

    WHY: The output directory might not exist yet (especially in CI/CD or
    Docker environments). makedirs with exist_ok=True handles this gracefully.
    """
    nested_path = str(tmp_path / "deep" / "nested" / "output.txt")

    processor.save_results(["test"], nested_path)

    assert os.path.exists(nested_path), "Should create nested directories"
