"""Level 2 project: Mini Inventory Engine.

Heavily commented beginner-friendly script:
- track inventory items with quantities and prices,
- add stock, remove stock, search items,
- generate low-stock alerts and inventory reports.

Skills practiced: nested dicts, dict/list comprehensions, try/except,
sets, enumerate, sorting with key functions, re for search.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def create_inventory() -> dict[str, dict]:
    """Create an empty inventory structure.

    Each item is stored as:
        {"quantity": int, "price": float, "category": str, "min_stock": int}
    """
    return {}


def add_item(
    inventory: dict[str, dict],
    name: str,
    quantity: int,
    price: float,
    category: str = "general",
    min_stock: int = 5,
) -> dict[str, dict]:
    """Add a new item or increase stock of an existing item.

    If the item already exists, quantity is ADDED to current stock.
    Price and category are updated to the new values.
    """
    # Normalise item name to lowercase for consistent lookups.
    key = name.strip().lower()

    if key in inventory:
        # Item exists — increase quantity.
        inventory[key]["quantity"] += quantity
        inventory[key]["price"] = price
        inventory[key]["category"] = category
    else:
        # New item — create the record.
        inventory[key] = {
            "quantity": quantity,
            "price": price,
            "category": category,
            "min_stock": min_stock,
        }

    return inventory


def remove_stock(
    inventory: dict[str, dict], name: str, quantity: int
) -> dict:
    """Remove stock from an existing item.

    Returns a result dict with success status and remaining quantity.
    Raises no exception — returns error info in the dict instead.
    """
    key = name.strip().lower()

    if key not in inventory:
        return {"success": False, "error": f"Item '{name}' not found"}

    current = inventory[key]["quantity"]

    if quantity > current:
        return {
            "success": False,
            "error": f"Cannot remove {quantity} — only {current} in stock",
        }

    inventory[key]["quantity"] -= quantity

    return {
        "success": True,
        "item": key,
        "removed": quantity,
        "remaining": inventory[key]["quantity"],
    }


def search_items(
    inventory: dict[str, dict], pattern: str
) -> list[tuple[str, dict]]:
    """Search inventory by name using a regex pattern.

    Returns a list of (name, item_dict) tuples matching the pattern.
    Case-insensitive by default.
    """
    try:
        compiled = re.compile(pattern, re.IGNORECASE)
    except re.error:
        return []

    # List comprehension filtering items whose names match the pattern.
    return [
        (name, info)
        for name, info in inventory.items()
        if compiled.search(name)
    ]


def get_low_stock(inventory: dict[str, dict]) -> list[tuple[str, dict]]:
    """Find items where quantity is at or below the minimum stock level.

    Sorted by quantity (lowest first) so the most urgent items show first.
    """
    low = [
        (name, info)
        for name, info in inventory.items()
        if info["quantity"] <= info["min_stock"]
    ]
    # Sort by quantity ascending using a key function.
    return sorted(low, key=lambda pair: pair[1]["quantity"])


def inventory_value(inventory: dict[str, dict]) -> dict:
    """Calculate the total inventory value and per-category breakdown.

    Uses dict comprehension for category grouping.
    """
    total = sum(
        info["quantity"] * info["price"] for info in inventory.values()
    )

    # Group by category.
    categories: dict[str, float] = {}
    for info in inventory.values():
        cat = info["category"]
        val = info["quantity"] * info["price"]
        categories[cat] = categories.get(cat, 0) + val

    # Sort categories by value (highest first).
    sorted_cats = dict(
        sorted(categories.items(), key=lambda pair: pair[1], reverse=True)
    )

    return {
        "total_value": round(total, 2),
        "total_items": sum(info["quantity"] for info in inventory.values()),
        "unique_products": len(inventory),
        "by_category": {k: round(v, 2) for k, v in sorted_cats.items()},
    }


def load_inventory(path: Path) -> dict[str, dict]:
    """Load inventory from a CSV file.

    Expected format: name,quantity,price,category,min_stock
    First line is header.
    """
    if not path.exists():
        raise FileNotFoundError(f"Inventory file not found: {path}")

    inventory = create_inventory()
    lines = path.read_text(encoding="utf-8").splitlines()

    for line in lines[1:]:  # Skip header.
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        try:
            name = parts[0]
            qty = int(parts[1])
            price = float(parts[2])
            category = parts[3] if len(parts) > 3 else "general"
            min_stock = int(parts[4]) if len(parts) > 4 else 5
            add_item(inventory, name, qty, price, category, min_stock)
        except (ValueError, IndexError):
            continue

    return inventory


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Mini inventory engine")
    parser.add_argument(
        "--inventory",
        default="data/sample_input.txt",
        help="Path to inventory CSV file",
    )
    parser.add_argument("--search", default=None, help="Search pattern")
    parser.add_argument("--low-stock", action="store_true", help="Show low-stock alerts")
    parser.add_argument("--value", action="store_true", help="Show inventory value")
    return parser.parse_args()


def main() -> None:
    """Entry point: load inventory and run requested operations."""
    args = parse_args()
    inventory = load_inventory(Path(args.inventory))

    if args.search:
        results = search_items(inventory, args.search)
        print(f"Search results for '{args.search}':")
        for name, info in results:
            print(f"  {name}: qty={info['quantity']}, price=${info['price']:.2f}")
        return

    if args.low_stock:
        low = get_low_stock(inventory)
        if low:
            print("LOW STOCK ALERTS:")
            for name, info in low:
                print(f"  {name}: {info['quantity']} remaining (min: {info['min_stock']})")
        else:
            print("All items are above minimum stock levels.")
        return

    if args.value:
        val = inventory_value(inventory)
        print("=== Inventory Value Report ===")
        print(f"  {'Category':<20} {'Value':>12}")
        print(f"  {'-'*20} {'-'*12}")
        for cat, amount in sorted(val.get("by_category", {}).items(),
                                   key=lambda x: x[1], reverse=True):
            print(f"  {cat:<20} ${amount:>10.2f}")
        print(f"  {'-'*20} {'-'*12}")
        print(f"  {'TOTAL':<20} ${val.get('total', 0):>10.2f}")
        return

    # Default: show full inventory.
    print(f"Inventory ({len(inventory)} products):")
    for name, info in sorted(inventory.items()):
        print(f"  {name}: qty={info['quantity']}, ${info['price']:.2f}, {info['category']}")


if __name__ == "__main__":
    main()
