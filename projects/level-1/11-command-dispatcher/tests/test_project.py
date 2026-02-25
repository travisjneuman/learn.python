"""Tests for Command Dispatcher."""

from project import cmd_reverse, cmd_upper, dispatch, list_commands


def test_cmd_upper() -> None:
    assert cmd_upper("hello") == "HELLO"


def test_cmd_reverse() -> None:
    assert cmd_reverse("abc") == "cba"


def test_dispatch_valid_command() -> None:
    result = dispatch("upper", "hello world")
    assert result["result"] == "HELLO WORLD"
    assert "error" not in result


def test_dispatch_unknown_command() -> None:
    result = dispatch("fly", "to the moon")
    assert "error" in result
    assert "Unknown command" in result["error"]


def test_list_commands() -> None:
    commands = list_commands()
    assert "upper" in commands
    assert "reverse" in commands
    assert len(commands) >= 5
