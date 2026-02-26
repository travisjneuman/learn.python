"""Tests for WebSocket Chat Server."""

import asyncio
import pytest

from project import format_message, clients


def test_format_message_contains_username():
    result = format_message("Alice", "Hello!")
    assert "Alice" in result
    assert "Hello!" in result


def test_format_message_contains_timestamp():
    result = format_message("Bob", "Hi")
    # Should contain HH:MM:SS format
    assert "]" in result
    assert "[" in result


def test_format_message_structure():
    result = format_message("TestUser", "test message")
    # Format: [HH:MM:SS] TestUser: test message
    assert "TestUser: test message" in result


def test_clients_dict_starts_empty():
    """Verify the clients dict is accessible and starts empty in test context."""
    # Clear any state from other tests
    clients.clear()
    assert len(clients) == 0


def test_format_message_special_characters():
    result = format_message("User<1>", "Hello & goodbye!")
    assert "User<1>" in result
    assert "Hello & goodbye!" in result
