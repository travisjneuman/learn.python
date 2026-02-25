"""Tests for Basic Expense Tracker."""

from pathlib import Path

import pytest

from project import (
    load_expenses,
    overall_stats,
    parse_expense,
    top_expenses,
    total_by_category,
)


def test_parse_expense_valid() -> None:
    row = {"date": "2024-01-15", "category": "Food", "amount": "12.50", "description": "Lunch"}
    exp = parse_expense(row)
    assert exp["category"] == "food"
    assert exp["amount"] == 12.50


def test_parse_expense_missing_field() -> None:
    row = {"date": "2024-01-15", "category": "", "amount": "10", "description": "X"}
    with pytest.raises(ValueError, match="Missing required field"):
        parse_expense(row)


def test_parse_expense_negative_amount() -> None:
    row = {"date": "2024-01-15", "category": "Food", "amount": "-5", "description": "Refund"}
    with pytest.raises(ValueError, match="Negative amount"):
        parse_expense(row)


def test_total_by_category() -> None:
    expenses = [
        {"category": "food", "amount": 10.0},
        {"category": "transport", "amount": 5.0},
        {"category": "food", "amount": 8.0},
    ]
    totals = total_by_category(expenses)
    assert totals["food"] == 18.0
    assert totals["transport"] == 5.0


def test_overall_stats() -> None:
    expenses = [{"amount": 10.0}, {"amount": 20.0}, {"amount": 30.0}]
    stats = overall_stats(expenses)
    assert stats["total"] == 60.0
    assert stats["average"] == 20.0
    assert stats["min"] == 10.0
    assert stats["max"] == 30.0


def test_overall_stats_empty() -> None:
    stats = overall_stats([])
    assert stats["total"] == 0.0
    assert stats["count"] == 0


def test_top_expenses() -> None:
    expenses = [
        {"amount": 5.0, "description": "small"},
        {"amount": 50.0, "description": "big"},
        {"amount": 25.0, "description": "medium"},
    ]
    top = top_expenses(expenses, n=2)
    assert len(top) == 2
    assert top[0]["amount"] == 50.0


def test_load_expenses_from_csv(tmp_path: Path) -> None:
    csv_file = tmp_path / "expenses.csv"
    csv_file.write_text(
        "date,category,amount,description\n"
        "2024-01-01,Food,15.00,Groceries\n"
        "2024-01-02,Transport,8.50,Bus fare\n",
        encoding="utf-8",
    )
    expenses = load_expenses(csv_file)
    assert len(expenses) == 2
    assert expenses[0]["category"] == "food"
    assert expenses[1]["amount"] == 8.50
