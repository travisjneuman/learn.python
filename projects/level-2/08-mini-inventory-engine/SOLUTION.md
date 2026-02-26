# Mini Inventory Engine — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Mini Inventory Engine — complete annotated solution."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def create_inventory() -> dict[str, dict]:
    """Create an empty inventory structure."""
    # WHY: A factory function for the inventory makes it clear what shape
    # the data takes and provides a single place to change the structure later.
    return {}


def add_item(
    inventory: dict[str, dict],
    name: str,
    quantity: int,
    price: float,
    category: str = "general",
    min_stock: int = 5,
) -> dict[str, dict]:
    """Add a new item or increase stock of an existing item."""
    # WHY: Normalise to lowercase so "Widget" and "widget" map to the same
    # inventory slot. Inconsistent casing is the #1 source of phantom duplicates.
    key = name.strip().lower()

    if key in inventory:
        # WHY: Adding to existing quantity instead of replacing it models
        # real inventory — receiving a shipment of 50 bolts adds to what
        # you already have, it does not reset the count.
        inventory[key]["quantity"] += quantity
        inventory[key]["price"] = price
        inventory[key]["category"] = category
    else:
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
    """Remove stock from an existing item. Returns a result dict, never raises."""
    key = name.strip().lower()

    if key not in inventory:
        return {"success": False, "error": f"Item '{name}' not found"}

    current = inventory[key]["quantity"]

    # WHY: Prevent negative inventory. Real warehouses cannot ship items
    # they do not have. Returning an error dict instead of raising an
    # exception lets the caller decide how to handle the problem.
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
    """Search inventory by name using a regex pattern."""
    try:
        # WHY: re.IGNORECASE makes searches user-friendly. Nobody wants
        # to remember whether they capitalised "widget" when adding it.
        compiled = re.compile(pattern, re.IGNORECASE)
    except re.error:
        # WHY: Invalid regex (like "[unclosed") would crash without this guard.
        # Returning empty results is safer than crashing the whole application.
        return []

    return [
        (name, info)
        for name, info in inventory.items()
        if compiled.search(name)
    ]


def get_low_stock(inventory: dict[str, dict]) -> list[tuple[str, dict]]:
    """Find items at or below minimum stock level, sorted by urgency."""
    low = [
        (name, info)
        for name, info in inventory.items()
        if info["quantity"] <= info["min_stock"]
    ]
    # WHY: Sorting by quantity ascending puts the most urgent items first.
    # An item with 0 remaining is more urgent than one with 4.
    return sorted(low, key=lambda pair: pair[1]["quantity"])


def inventory_value(inventory: dict[str, dict]) -> dict:
    """Calculate total inventory value with per-category breakdown."""
    # WHY: Generator expression inside sum() avoids creating an intermediate list.
    # For large inventories this saves memory.
    total = sum(
        info["quantity"] * info["price"] for info in inventory.values()
    )

    # WHY: Grouping by category with dict.get(key, 0) + value is the
    # accumulator pattern — simpler than defaultdict for small cases.
    categories: dict[str, float] = {}
    for info in inventory.values():
        cat = info["category"]
        val = info["quantity"] * info["price"]
        categories[cat] = categories.get(cat, 0) + val

    # WHY: Sorting by value descending shows the most valuable categories first.
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
    """Load inventory from a CSV file."""
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
            # WHY: Reusing add_item() for loading ensures the same normalisation
            # and duplicate-handling logic applies during file loading as during
            # runtime additions. DRY principle.
            add_item(inventory, name, qty, price, category, min_stock)
        except (ValueError, IndexError):
            # WHY: Skipping bad rows instead of crashing lets us load partial
            # data from messy CSV files. Log a warning in production.
            continue

    return inventory


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Mini inventory engine")
    parser.add_argument(
        "--inventory", default="data/sample_input.txt",
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

    print(f"Inventory ({len(inventory)} products):")
    for name, info in sorted(inventory.items()):
        print(f"  {name}: qty={info['quantity']}, ${info['price']:.2f}, {info['category']}")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Dict-of-dicts for inventory | Each item needs multiple attributes (quantity, price, category). A dict-of-dicts gives O(1) lookup by name and naturally groups related data. This is the same pattern as a database table with a primary key. |
| Mutating the inventory in place | `add_item` and `remove_stock` modify the inventory dict directly and return it. This avoids creating copies on every operation, which matters when the inventory is large. |
| Result dicts from `remove_stock` | Returning `{"success": False, "error": "..."}` instead of raising exceptions puts the caller in control. In a web API, you would return this as a JSON response; in a CLI, you would print it. |
| `min_stock` per item | Different items have different urgency thresholds. A warehouse with 3 laptops left is in trouble, but 3 screws is fine. Per-item thresholds make low-stock alerts meaningful. |
| Regex search with `re.IGNORECASE` | Users searching for "bolt" should find "Bolt" and "BOLT". Case-insensitive regex is the simplest way to achieve this while also supporting patterns like `"key.*board"`. |

## Alternative Approaches

### Using a class instead of plain dicts

```python
class InventoryItem:
    def __init__(self, name, quantity, price, category="general", min_stock=5):
        self.name = name.strip().lower()
        self.quantity = quantity
        self.price = price
        self.category = category
        self.min_stock = min_stock

    @property
    def value(self):
        return self.quantity * self.price

    @property
    def is_low_stock(self):
        return self.quantity <= self.min_stock
```

A class encapsulates behavior with data (e.g., `item.is_low_stock` instead of `item["quantity"] <= item["min_stock"]`). This project uses plain dicts because classes are covered in later levels. The class approach becomes preferable as the system grows more complex.

### Using `dataclasses` for structured inventory items

```python
from dataclasses import dataclass

@dataclass
class Item:
    quantity: int
    price: float
    category: str = "general"
    min_stock: int = 5
```

Dataclasses provide type safety, default values, and `__repr__` for free. They are the modern Python approach for structured data but require understanding decorators and type hints, which come in later levels.

## Common Pitfalls

1. **Allowing negative quantities** — Without validation, `add_item(inv, "bolt", -50, 0.50)` would reduce stock through the "add" path, bypassing `remove_stock` checks. Production code should validate that quantity is non-negative in `add_item`.

2. **Floating-point price arithmetic** — `0.10 + 0.20 = 0.30000000000000004` in floating-point. For financial calculations, use `decimal.Decimal` or store prices in cents as integers. The `round()` calls in `inventory_value` mitigate this but do not eliminate it.

3. **Concurrent modification** — If two processes modify the same inventory simultaneously (e.g., two warehouse workers scanning items), data can become inconsistent. Real inventory systems use database transactions with locking. This single-process version does not need to worry about concurrency.
