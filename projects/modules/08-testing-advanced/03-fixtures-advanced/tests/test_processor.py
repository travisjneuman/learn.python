"""
Tests for Project 03 — Fixtures Advanced

These tests demonstrate advanced pytest fixture usage:
- Fixtures from conftest.py (shared setup code)
- tmp_path for temporary file operations
- monkeypatch for safely modifying environment variables
- Combining multiple fixtures in one test

Run with: pytest tests/ -v
"""

import os
import pytest

from project import FileProcessor


# ── load_config tests ───────────────────────────────────────────────────

# WHY: load_config reads from environment variables. We need monkeypatch
# to set those variables safely, without affecting other tests or the
# actual system environment.

def test_load_config_reads_env_vars(monkeypatch):
    """Test that load_config reads environment variables correctly."""
    # monkeypatch.setenv sets an environment variable for this test only.
    # After the test finishes, the variable is automatically removed.
    monkeypatch.setenv("APP_MODE", "lowercase")
    monkeypatch.setenv("APP_STRIP", "false")
    monkeypatch.setenv("APP_OUTPUT_DIR", "/custom/path")

    processor = FileProcessor()
    config = processor.load_config()

    assert config["mode"] == "lowercase"
    assert config["strip_whitespace"] is False
    assert config["output_dir"] == "/custom/path"


# WHY: When no environment variables are set, the defaults should apply.
# monkeypatch.delenv ensures variables are absent even if they happen
# to be set in the real environment.

def test_load_config_uses_defaults(monkeypatch):
    """Test that load_config uses default values when env vars are missing."""
    # Remove these variables if they happen to exist in the real environment.
    monkeypatch.delenv("APP_MODE", raising=False)
    monkeypatch.delenv("APP_STRIP", raising=False)
    monkeypatch.delenv("APP_OUTPUT_DIR", raising=False)

    processor = FileProcessor()
    config = processor.load_config()

    assert config["mode"] == "uppercase"
    assert config["strip_whitespace"] is True
    assert config["output_dir"] == "output"


# ── process_file tests ─────────────────────────────────────────────────

# WHY: The core processing logic (uppercase + strip) needs to be tested
# with real files. The configured_processor and sample_text_file fixtures
# from conftest.py handle all the setup.

def test_process_file_uppercase(configured_processor, sample_text_file):
    """Test that process_file converts text to uppercase."""
    # configured_processor comes from conftest.py — it already has
    # config loaded with mode="uppercase".
    # sample_text_file comes from conftest.py — it is a temporary file
    # with known content.
    results = configured_processor.process_file(str(sample_text_file))

    assert results[0] == "HELLO WORLD"
    assert results[1] == "PYTHON TESTING"
    assert results[2] == "PYTEST FIXTURES"


# WHY: Whitespace stripping is a separate concern from case conversion.
# Testing it separately makes failures easier to diagnose — if this test
# fails but the uppercase test passes, you know the bug is in stripping.

def test_process_file_strips_whitespace(monkeypatch, sample_text_file):
    """Test that leading/trailing whitespace is stripped."""
    monkeypatch.setenv("APP_MODE", "lowercase")
    monkeypatch.setenv("APP_STRIP", "true")

    processor = FileProcessor()
    processor.load_config()
    results = processor.process_file(str(sample_text_file))

    # Each line should have whitespace stripped and be lowercased.
    for line in results:
        assert line == line.strip()
        assert line == line.lower()


# WHY: Error handling is just as important as the happy path. We need to
# verify that a missing file raises the expected exception, not a
# confusing internal error.

def test_process_file_missing_file(configured_processor, tmp_path):
    """Test that a missing file raises FileNotFoundError."""
    fake_path = str(tmp_path / "does_not_exist.txt")

    with pytest.raises(FileNotFoundError):
        configured_processor.process_file(fake_path)


# ── save_results tests ─────────────────────────────────────────────────

# WHY: save_results creates files on disk. tmp_path gives us a safe
# location to write files that will not interfere with real data.

def test_save_results_creates_file(configured_processor, tmp_path):
    """Test that save_results creates the output file."""
    output_path = str(tmp_path / "output.txt")
    lines = ["LINE ONE", "LINE TWO"]

    configured_processor.save_results(lines, output_path)

    # Verify the file exists.
    assert os.path.exists(output_path)


# WHY: It is not enough that the file exists — the content must be correct.
# This test verifies both the existence and the content.

def test_save_results_content(configured_processor, tmp_path):
    """Test that save_results writes the correct content."""
    output_path = str(tmp_path / "output.txt")
    lines = ["FIRST", "SECOND", "THIRD"]

    configured_processor.save_results(lines, output_path)

    # Read the file back and verify the content.
    with open(output_path, "r") as f:
        written = f.read()

    # Each line should end with a newline.
    assert written == "FIRST\nSECOND\nTHIRD\n"


# ── Full pipeline test ──────────────────────────────────────────────────

# WHY: Individual method tests are necessary, but you also need a test
# that runs the whole pipeline end to end. This catches integration bugs
# where methods work alone but fail when combined.

def test_full_pipeline(monkeypatch, tmp_path):
    """Test the entire process: load config, process file, save results."""
    # Set up config via environment variables.
    monkeypatch.setenv("APP_MODE", "uppercase")
    monkeypatch.setenv("APP_STRIP", "true")

    # Create an input file in the temporary directory.
    input_file = tmp_path / "input.txt"
    input_file.write_text("  hello  \n  world  \n")

    # Create the output path.
    output_file = tmp_path / "result.txt"

    # Run the full pipeline.
    processor = FileProcessor()
    processor.load_config()
    results = processor.process_file(str(input_file))
    processor.save_results(results, str(output_file))

    # Verify the final output.
    content = output_file.read_text()
    assert content == "HELLO\nWORLD\n"
