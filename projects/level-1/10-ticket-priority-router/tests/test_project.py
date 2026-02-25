"""Tests for Ticket Priority Router."""

from project import classify_ticket, group_by_priority, route_ticket


def test_classify_critical() -> None:
    assert classify_ticket("Website is down, total outage") == "critical"


def test_classify_high() -> None:
    assert classify_ticket("Login page is broken for all users") == "high"


def test_classify_medium() -> None:
    assert classify_ticket("Dashboard is loading slow") == "medium"


def test_classify_default_low() -> None:
    assert classify_ticket("Can you change the button color?") == "low"


def test_route_ticket_structure() -> None:
    result = route_ticket(42, "Server crash at 3am")
    assert result["id"] == 42
    assert result["priority"] == "critical"


def test_group_by_priority() -> None:
    tickets = [
        {"priority": "high", "id": 1},
        {"priority": "low", "id": 2},
        {"priority": "high", "id": 3},
    ]
    groups = group_by_priority(tickets)
    assert len(groups["high"]) == 2
    assert len(groups["low"]) == 1
