"""Tests for Unit Price Calculator."""

import pytest

from project import calculate_unit_price, find_best_deal, parse_product_row


def test_calculate_unit_price() -> None:
    assert calculate_unit_price(10.0, 5) == 2.0
    assert calculate_unit_price(7.99, 3) == 2.6633


def test_calculate_unit_price_zero_quantity() -> None:
    with pytest.raises(ValueError, match="Quantity must be positive"):
        calculate_unit_price(10, 0)


def test_parse_product_row_valid() -> None:
    row = {"product": "Rice 5lb", "price": "8.99", "quantity": "5", "unit": "lb"}
    result = parse_product_row(row)
    assert result["unit_price"] == 1.798
    assert "error" not in result


def test_parse_product_row_bad_price() -> None:
    row = {"product": "Bad", "price": "abc", "quantity": "5", "unit": "lb"}
    result = parse_product_row(row)
    assert "error" in result


def test_find_best_deal() -> None:
    products = [
        {"product": "A", "unit_price": 2.50},
        {"product": "B", "unit_price": 1.25},
        {"product": "C", "unit_price": 3.00},
    ]
    best = find_best_deal(products)
    assert best["product"] == "B"
