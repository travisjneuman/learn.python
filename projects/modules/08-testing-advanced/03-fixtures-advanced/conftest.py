"""
conftest.py — Shared Fixtures for Project 03

This file is special to pytest. When pytest discovers a conftest.py file,
it automatically makes all fixtures defined in it available to every test
file in the same directory (and subdirectories).

You never import conftest.py — pytest handles it automatically.
Just define fixtures here and use them as test function parameters.

Fixtures are functions that provide test data or setup. They run before
each test that requests them, and clean up afterwards.
"""

import os
import pytest

from project import FileProcessor


# ── Fixtures ────────────────────────────────────────────────────────────

@pytest.fixture
def sample_config():
    """
    Provide a dictionary of configuration values for testing.

    This fixture has the default scope ("function"), which means it runs
    fresh for every test that uses it. Each test gets its own copy.
    """
    return {
        "mode": "uppercase",
        "strip_whitespace": True,
        "output_dir": "test_output",
    }


@pytest.fixture
def processor():
    """
    Provide a fresh FileProcessor instance.

    Each test gets its own processor so no state leaks between tests.
    """
    return FileProcessor()


@pytest.fixture
def configured_processor(monkeypatch):
    """
    Provide a FileProcessor that has already loaded config from env vars.

    monkeypatch.setenv sets environment variables safely — they are
    automatically restored to their original values after the test.
    This is much safer than directly modifying os.environ.
    """
    # Set environment variables that FileProcessor.load_config() will read.
    monkeypatch.setenv("APP_MODE", "uppercase")
    monkeypatch.setenv("APP_STRIP", "true")
    monkeypatch.setenv("APP_OUTPUT_DIR", "/tmp/test-output")

    proc = FileProcessor()
    proc.load_config()
    return proc


@pytest.fixture
def sample_text_file(tmp_path):
    """
    Create a temporary text file with known content.

    tmp_path is a built-in pytest fixture that provides a fresh temporary
    directory unique to each test. Files created here are automatically
    cleaned up after the test session ends.

    This fixture creates a file and returns the path to it.
    """
    # tmp_path is a pathlib.Path object. The / operator joins paths.
    file_path = tmp_path / "sample.txt"

    # Write some content with deliberate whitespace for testing.
    file_path.write_text(
        "  hello world  \n"
        "  python testing  \n"
        "  pytest fixtures  \n"
    )

    return file_path


@pytest.fixture
def multi_file_dir(tmp_path):
    """
    Create a temporary directory with multiple text files.

    This is useful for testing code that processes a directory of files.
    Returns the path to the directory.
    """
    # Create several files with different content.
    (tmp_path / "file1.txt").write_text("first file content\n")
    (tmp_path / "file2.txt").write_text("second file content\n")
    (tmp_path / "file3.txt").write_text("third file content\n")

    return tmp_path
