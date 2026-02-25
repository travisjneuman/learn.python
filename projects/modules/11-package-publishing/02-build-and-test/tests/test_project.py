"""
Tests for Project 02 — Build and Test

This project's main file (build_and_test.py) is a workflow automation
script that runs shell commands (build, install, test). We test the
helper function run_command and verify the script's configuration.

Why test a build script?
    Build scripts are infrastructure code. If run_command mishandles
    errors (e.g., treats failure as success), the entire build pipeline
    silently passes when it should fail. Testing the helper catches these
    logic errors.

Run with: pytest tests/test_project.py -v
"""

import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

import pytest

from build_and_test import run_command, PACKAGE_DIR


# ── Test: run_command with successful command ──────────────────────────

@patch("build_and_test.subprocess.run")
def test_run_command_returns_true_on_success(mock_run):
    """run_command should return True when the command succeeds (exit code 0).

    WHY: The build script uses the return value to decide whether to
    continue or report an error. If it returns True for failures, broken
    builds would appear successful.
    """
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="Success output",
        stderr="",
    )

    result = run_command("Test step", [sys.executable, "--version"])

    assert result is True, "Should return True for exit code 0"


@patch("build_and_test.subprocess.run")
def test_run_command_returns_false_on_failure(mock_run):
    """run_command should return False when the command fails (non-zero exit code).

    WHY: A non-zero exit code means the command failed. The script should
    detect this and report it. Returning True would hide the failure.
    """
    mock_run.return_value = MagicMock(
        returncode=1,
        stdout="",
        stderr="Error: something went wrong",
    )

    result = run_command("Failing step", ["false"])

    assert result is False, "Should return False for non-zero exit code"


@patch("build_and_test.subprocess.run")
def test_run_command_passes_cwd(mock_run):
    """run_command should pass the cwd parameter to subprocess.run.

    WHY: Build commands must run in the correct directory (the package
    directory). If cwd is not passed, commands run in the wrong directory
    and fail with confusing errors.
    """
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

    custom_dir = "/custom/directory"
    run_command("Test step", ["echo"], cwd=custom_dir)

    # Verify subprocess.run was called with the custom cwd.
    call_kwargs = mock_run.call_args
    assert call_kwargs[1].get("cwd") == custom_dir or call_kwargs.kwargs.get("cwd") == custom_dir


@patch("build_and_test.subprocess.run")
def test_run_command_uses_package_dir_as_default_cwd(mock_run):
    """run_command without explicit cwd should use PACKAGE_DIR.

    WHY: The default cwd should be the package directory (../01-package-structure).
    If the default is wrong, all commands run in the wrong place.
    """
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

    run_command("Test step", ["echo"])

    call_kwargs = mock_run.call_args
    used_cwd = call_kwargs[1].get("cwd") or call_kwargs.kwargs.get("cwd")
    assert used_cwd == PACKAGE_DIR, f"Default cwd should be PACKAGE_DIR, got {used_cwd}"


# ── Test: PACKAGE_DIR points to correct location ──────────────────────

def test_package_dir_references_package_structure():
    """PACKAGE_DIR should point to the 01-package-structure directory.

    WHY: The build script operates on the package from project 01. If
    PACKAGE_DIR is wrong, every command runs against the wrong files.
    """
    assert "01-package-structure" in PACKAGE_DIR, (
        "PACKAGE_DIR should reference the 01-package-structure project"
    )


@patch("build_and_test.subprocess.run")
def test_run_command_captures_output(mock_run):
    """run_command should use capture_output=True to capture stdout/stderr.

    WHY: Without capture_output, command output goes directly to the
    terminal and cannot be displayed in the script's formatted output.
    """
    mock_run.return_value = MagicMock(returncode=0, stdout="captured", stderr="")

    run_command("Test", ["echo"])

    call_kwargs = mock_run.call_args
    assert call_kwargs[1].get("capture_output") is True or call_kwargs.kwargs.get("capture_output") is True
