"""Tests for Module 05 / Project 03 — Async File Processing.

Tests the synchronous and asynchronous file processing functions, as well
as the async generator. Uses tmp_path for temporary test files.

WHY test both sync and async versions?
- The project compares both approaches. Testing both ensures they produce
  the same results, proving the async version is a correct translation.
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import process_file_sync, process_file_async, generate_sample_files


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary text file with known content.

    3 lines, 9 words total. This gives us predictable counts to assert on.
    """
    filepath = tmp_path / "test_file.txt"
    filepath.write_text("hello world foo\nbar baz qux\nalpha beta gamma\n", encoding="utf-8")
    return filepath


# ---------------------------------------------------------------------------
# Tests for process_file_sync()
# ---------------------------------------------------------------------------

def test_sync_word_count(sample_file):
    """process_file_sync() should count all whitespace-separated words.

    Our file has 9 words across 3 lines.
    """
    result = process_file_sync(str(sample_file))

    assert result["words"] == 9


def test_sync_line_count(sample_file):
    """process_file_sync() should count the number of lines in the file."""
    result = process_file_sync(str(sample_file))

    assert result["lines"] == 3


def test_sync_filename(sample_file):
    """process_file_sync() should include just the filename, not the full path."""
    result = process_file_sync(str(sample_file))

    assert result["file"] == "test_file.txt"


# ---------------------------------------------------------------------------
# Tests for process_file_async()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_async_word_count(sample_file):
    """process_file_async() should produce the same word count as the sync version.

    This verifies the async implementation is correct by comparing to sync.
    """
    result = await process_file_async(str(sample_file))

    assert result["words"] == 9


@pytest.mark.asyncio
async def test_async_line_count(sample_file):
    """process_file_async() should count lines the same as the sync version."""
    result = await process_file_async(str(sample_file))

    assert result["lines"] == 3


@pytest.mark.asyncio
async def test_async_matches_sync(sample_file):
    """The async and sync versions should produce identical results.

    This is the key test: it proves the async port did not change behavior.
    """
    sync_result = process_file_sync(str(sample_file))
    async_result = await process_file_async(str(sample_file))

    assert sync_result["words"] == async_result["words"]
    assert sync_result["lines"] == async_result["lines"]
    assert sync_result["file"] == async_result["file"]


# ---------------------------------------------------------------------------
# Tests for generate_sample_files()
# ---------------------------------------------------------------------------

def test_generate_sample_files_creates_files(tmp_path, monkeypatch):
    """generate_sample_files() should create the expected number of files.

    We monkeypatch DATA_DIR to use tmp_path so we don't pollute the project.
    """
    import project

    test_data_dir = str(tmp_path / "data")
    monkeypatch.setattr(project, "DATA_DIR", test_data_dir)
    monkeypatch.setattr(project, "NUM_FILES", 3)

    generate_sample_files()

    files = list(tmp_path.glob("data/file_*.txt"))
    assert len(files) == 3


def test_generate_sample_files_content_is_nonempty(tmp_path, monkeypatch):
    """Each generated file should have content (not be empty)."""
    import project

    test_data_dir = str(tmp_path / "data")
    monkeypatch.setattr(project, "DATA_DIR", test_data_dir)
    monkeypatch.setattr(project, "NUM_FILES", 1)

    generate_sample_files()

    files = list(tmp_path.glob("data/file_*.txt"))
    assert len(files) == 1
    content = files[0].read_text()
    assert len(content) > 0
