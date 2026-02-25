"""Tests for Mini Inventory Engine.

Covers:
- Adding items (new and existing)
- Removing stock (success and failure)
- Search by pattern
- Low-stock alerts
- Inventory valuation
- File loading
"""

from pathlib import Path

import pytest

from project import (
    add_item,
    create_inventory,
    get_low_stock,
    inventory_value,
    load_inventory,
    remove_stock,
    search_items,
)


@pytest.fixture
def sample_inventory() -> dict[str, dict]:
    """Build a small inventory for testing."""
    inv = create_inventory()
    add_item(inv, "Widget", 100, 9.99, "hardware")
    add_item(inv, "Gadget", 3, 49.99, "electronics", min_stock=5)
    add_item(inv, "Gizmo", 50, 19.99, "electronics")
    return inv


def test_add_new_item() -> None:
    """Adding a new item should create it in inventory."""
    inv = create_inventory()
    add_item(inv, "Test Item", 10, 5.00)
    assert "test item" in inv
    assert inv["test item"]["quantity"] == 10


def test_add_existing_item_increases_quantity() -> None:
    """Adding an existing item should increase its quantity."""
    inv = create_inventory()
    add_item(inv, "Widget", 10, 5.00)
    add_item(inv, "widget", 5, 5.00)  # same item, different case
    assert inv["widget"]["quantity"] == 15


def test_remove_stock_success(sample_inventory: dict) -> None:
    """Removing available stock should succeed."""
    result = remove_stock(sample_inventory, "Widget", 10)
    assert result["success"] is True
    assert result["remaining"] == 90


def test_remove_stock_insufficient(sample_inventory: dict) -> None:
    """Removing more than available should fail with error."""
    result = remove_stock(sample_inventory, "Gadget", 100)
    assert result["success"] is False
    assert "Cannot remove" in result["error"]


def test_remove_stock_missing_item(sample_inventory: dict) -> None:
    """Removing from non-existent item should fail."""
    result = remove_stock(sample_inventory, "Nonexistent", 1)
    assert result["success"] is False


def test_search_items(sample_inventory: dict) -> None:
    """Search should find items matching the pattern."""
    results = search_items(sample_inventory, "g.*t")
    names = [name for name, _ in results]
    assert "gadget" in names


@pytest.mark.parametrize(
    "pattern,expected_count",
    [("widget", 1), ("g", 2), ("zzz", 0), (".*", 3)],
)
def test_search_patterns(
    sample_inventory: dict, pattern: str, expected_count: int
) -> None:
    """Different patterns should match different counts."""
    results = search_items(sample_inventory, pattern)
    assert len(results) == expected_count


def test_get_low_stock(sample_inventory: dict) -> None:
    """Gadget (qty=3, min=5) should appear in low stock."""
    low = get_low_stock(sample_inventory)
    low_names = [name for name, _ in low]
    assert "gadget" in low_names


def test_inventory_value(sample_inventory: dict) -> None:
    """Total value should be sum of qty * price for all items."""
    val = inventory_value(sample_inventory)
    expected = (100 * 9.99) + (3 * 49.99) + (50 * 19.99)
    assert abs(val["total_value"] - expected) < 0.01


def test_load_inventory(tmp_path: Path) -> None:
    """Loading from CSV should populate inventory."""
    p = tmp_path / "inv.csv"
    p.write_text(
        "name,quantity,price,category,min_stock\n"
        "Bolt,200,0.50,hardware,20\n"
        "Nut,150,0.25,hardware,10\n",
        encoding="utf-8",
    )
    inv = load_inventory(p)
    assert len(inv) == 2
    assert inv["bolt"]["quantity"] == 200
