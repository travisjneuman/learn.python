"""
Tests for Project 03 — Publish to PyPI

This project's main file (publish_guide.py) is an interactive walkthrough
that checks prerequisites and prints instructions. We test the helper
functions that check for tools and built files.

Why test an interactive guide?
    The guide checks for installed tools (twine, build) and existing files
    (dist/). If these checks are wrong, the guide gives incorrect advice.
    Testing the helpers ensures the prerequisites check is accurate.

Run with: pytest tests/test_project.py -v
"""

import os
from unittest.mock import patch

import pytest

from publish_guide import check_tool, check_dist, PACKAGE_DIR


# ── Test: check_tool finds installed tools ─────────────────────────────

def test_check_tool_finds_python():
    """check_tool should return True for tools that are installed.

    WHY: check_tool uses shutil.which() to find executables on PATH.
    Python itself is always available, so this is a reliable test case.
    If check_tool returns False for python, shutil.which is broken or
    PATH is not set.
    """
    # "python" or "python3" should be available in any Python environment.
    result = check_tool("python") or check_tool("python3")

    assert result is True, "Python should be findable on PATH"


def test_check_tool_returns_false_for_missing_tool():
    """check_tool should return False for tools that are not installed.

    WHY: When a prerequisite is missing, the guide should tell the user
    to install it. If check_tool returns True for missing tools, the guide
    would skip the installation advice.
    """
    result = check_tool("definitely_not_a_real_tool_xyz123")

    assert result is False, "Non-existent tool should return False"


# ── Test: check_dist finds built files ─────────────────────────────────

def test_check_dist_returns_list():
    """check_dist should return a list (possibly empty).

    WHY: The function checks if dist/ exists and lists its contents.
    It should always return a list, not None or raise an exception.
    This makes the caller's code simpler: just check len(result).
    """
    result = check_dist()

    assert isinstance(result, list), "Should return a list"


@patch("publish_guide.os.path.exists")
@patch("publish_guide.os.listdir")
def test_check_dist_returns_files_when_dist_exists(mock_listdir, mock_exists):
    """check_dist should list files when the dist/ directory exists.

    WHY: After running 'python -m build', the dist/ directory contains
    .whl and .tar.gz files. check_dist should find and return them.
    """
    mock_exists.return_value = True
    mock_listdir.return_value = ["mymath-0.1.0.tar.gz", "mymath-0.1.0-py3-none-any.whl"]

    result = check_dist()

    assert len(result) == 2, "Should return 2 built files"
    assert any(".whl" in f for f in result), "Should include a wheel file"
    assert any(".tar.gz" in f for f in result), "Should include a source distribution"


@patch("publish_guide.os.path.exists")
def test_check_dist_returns_empty_when_no_dist(mock_exists):
    """check_dist should return an empty list when dist/ does not exist.

    WHY: Before the first build, dist/ does not exist. The function should
    handle this gracefully by returning an empty list, not crashing.
    """
    mock_exists.return_value = False

    result = check_dist()

    assert result == [], "Should return empty list when dist/ does not exist"


# ── Test: PACKAGE_DIR configuration ────────────────────────────────────

def test_package_dir_references_correct_project():
    """PACKAGE_DIR should point to the 01-package-structure project.

    WHY: The publish guide checks for built files in the package structure
    project. If PACKAGE_DIR is wrong, the file checks would look in the
    wrong place and give misleading results.
    """
    assert "01-package-structure" in PACKAGE_DIR, (
        "PACKAGE_DIR should reference the 01-package-structure project"
    )


# ── Test: main function runs without error ─────────────────────────────

@patch("publish_guide.check_tool")
@patch("publish_guide.check_dist")
def test_main_runs_without_error(mock_dist, mock_tool):
    """The main function should run without raising exceptions.

    WHY: The guide is meant to be run interactively. If it crashes due
    to an unhandled exception, the user sees a traceback instead of
    helpful instructions.
    """
    mock_tool.return_value = True
    mock_dist.return_value = ["fake.whl"]

    # Mock subprocess for the build tool check.
    with patch("publish_guide.subprocess.run"):
        from publish_guide import main
        # Should not raise any exceptions.
        main()
