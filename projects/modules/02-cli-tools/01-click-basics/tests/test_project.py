"""Tests for Module 02 / Project 01 — Click Basics.

These tests use Click's built-in test runner (CliRunner) to invoke the
CLI command without starting a real process. CliRunner simulates command-line
arguments and captures the output, making it easy to assert on results.

WHY use CliRunner?
- It runs the CLI in-process, so tests are fast and don't fork a subprocess.
- It captures stdout so you can assert on the output text.
- It provides the exit_code so you can check for success (0) or failure.
"""

import sys
import os

import pytest
from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import greet


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_greet_with_name():
    """Passing a name argument should produce 'Hello, <name>!' output.

    The default greeting word is 'Hello', so 'World' should give 'Hello, World!'.
    """
    runner = CliRunner()
    result = runner.invoke(greet, ["World"])

    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_greet_custom_greeting():
    """The --greeting option should replace the default 'Hello' word.

    'python project.py World --greeting Hi' should output 'Hi, World!'.
    """
    runner = CliRunner()
    result = runner.invoke(greet, ["World", "--greeting", "Hi"])

    assert result.exit_code == 0
    assert "Hi, World!" in result.output


def test_greet_shout_flag():
    """The --shout flag should convert the output to uppercase.

    'python project.py World --shout' should produce 'HELLO, WORLD!'.
    """
    runner = CliRunner()
    result = runner.invoke(greet, ["World", "--shout"])

    assert result.exit_code == 0
    assert "HELLO, WORLD!" in result.output


def test_greet_custom_greeting_with_shout():
    """--greeting and --shout should work together.

    'python project.py Alice --greeting Howdy --shout' -> 'HOWDY, ALICE!'
    """
    runner = CliRunner()
    result = runner.invoke(greet, ["Alice", "--greeting", "Howdy", "--shout"])

    assert result.exit_code == 0
    assert "HOWDY, ALICE!" in result.output


def test_greet_missing_name():
    """Invoking greet without a NAME argument should produce an error.

    Click requires the NAME argument. Without it, Click prints a usage
    message and exits with a non-zero code.
    """
    runner = CliRunner()
    result = runner.invoke(greet, [])

    assert result.exit_code != 0


def test_greet_help_flag():
    """The --help flag should display the command's docstring and options.

    Click generates help text automatically from the function's docstring
    and the option/argument decorators.
    """
    runner = CliRunner()
    result = runner.invoke(greet, ["--help"])

    assert result.exit_code == 0
    assert "Greet someone by name" in result.output
    assert "--greeting" in result.output
    assert "--shout" in result.output
