# Solution: Level 1 / Project 03 - Unit Price Calculator

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Unit Price Calculator.

Compare unit prices across different package sizes from a CSV file.
Find the best deal by calculating price-per-unit for each product.

Concepts: csv module, float arithmetic, rounding, sorting, file I/O.
"""


import argparse
import csv
import json
from pathlib import Path


# WHY calculate_unit_price: This is the core calculation — dividing
# total price by quantity to get cost per unit.  Isolating it in its
# own function makes it easy to test with known values.
def calculate_unit_price(total_price: float, quantity: float) -> float:
    """Calculate price per unit, rounded to 4 decimal places.

    WHY round? -- Floating-point math can produce results like
    3.3333333333333335.  Rounding keeps the output readable.
    """
    # WHY raise ValueError: Division by zero would crash with a
    # confusing ZeroDivisionError.  Raising ValueError with a clear
    # message tells the caller exactly what went wrong.
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    # WHY round to 4: Currency calculations need precision, but
    # displaying 16 decimal places is noise.  4 places is enough
    # to distinguish similar unit prices.
    return round(total_price / quantity, 4)


# WHY parse_product_row: CSV data arrives as strings.  This function
# converts strings to proper types (float) and handles conversion
# errors gracefully, returning an error dict instead of crashing.
def parse_product_row(row: dict) -> dict:
    """Parse a CSV row into a product dict with unit price."""
    # WHY try/except for float conversion: CSV values are always
    # strings.  If someone puts "N/A" in the price column, float()
    # would raise ValueError.  Catching it lets us skip bad rows
    # instead of crashing the whole program.
    try:
        price = float(row["price"])
        quantity = float(row["quantity"])
    except (ValueError, KeyError) as err:
        # WHY return error dict: Returning {"error": ...} instead of
        # raising lets the caller decide what to do with bad rows
        # (skip them, log them, etc.).
        return {"raw": str(row), "error": str(err)}

    if quantity <= 0:
        return {"raw": str(row), "error": "Quantity must be positive"}

    unit_price = calculate_unit_price(price, quantity)

    return {
        "product": row.get("product", "").strip(),
        "price": price,
        "quantity": quantity,
        # WHY .get with default: If the CSV is missing a "unit" column,
        # we default to "unit" rather than crashing on a KeyError.
        "unit": row.get("unit", "unit").strip(),
        "unit_price": unit_price,
    }


# WHY load_products: Separating CSV reading from price calculation
# means parse_product_row() can be tested with plain dicts, and
# the file I/O is isolated in one function.
def load_products(path: Path) -> list[dict]:
    """Load products from a CSV file and compute unit prices."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    products = []
    # WHY newline="": Python's csv module handles line endings itself.
    # Passing newline="" prevents the system from double-interpreting
    # carriage returns, which can cause blank-row bugs on Windows.
    with open(path, encoding="utf-8", newline="") as f:
        # WHY DictReader: It uses the first row as column names, so
        # each row becomes a dict like {"product": "Rice", "price": "8.99"}.
        # This is more readable than accessing columns by index.
        reader = csv.DictReader(f)
        for row in reader:
            products.append(parse_product_row(row))

    return products


# WHY find_best_deal: Identifying the lowest unit price is the primary
# use case — the whole point of comparing prices.
def find_best_deal(products: list[dict]) -> dict | None:
    """Find the product with the lowest unit price.

    WHY filter errors first? -- Products with parse errors have no
    unit_price, so including them would crash the comparison.
    """
    # WHY filter: Products with "error" keys have no unit_price field.
    # Trying to access it would raise KeyError.
    valid = [p for p in products if "error" not in p]
    if not valid:
        return None

    # WHY manual loop instead of min(): At Level 1, an explicit loop
    # is easier to follow.  The alternative section shows the min() version.
    best = valid[0]
    for product in valid[1:]:
        if product["unit_price"] < best["unit_price"]:
            best = product

    return best


# WHY rank_products: Sorting by unit price gives a ranked comparison
# from best to worst deal, which is how shoppers think about value.
def rank_products(products: list[dict]) -> list[dict]:
    """Sort valid products by unit price (cheapest first)."""
    valid = [p for p in products if "error" not in p]
    # WHY lambda: sorted() needs to know which value to compare.
    # The lambda extracts unit_price from each product dict.
    return sorted(valid, key=lambda p: p["unit_price"])


# WHY parse_args: argparse makes the script flexible — users can
# point it at different CSV files without editing code.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Unit Price Calculator")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Wrapping orchestration in main() keeps the module
# importable.  Tests can import calculate_unit_price() without
# triggering file reads or prints.
def main() -> None:
    args = parse_args()
    products = load_products(Path(args.input))
    ranked = rank_products(products)
    best = find_best_deal(products)

    print("=== Unit Price Comparison ===\n")
    print(f"  {'Product':<25} {'Price':>8} {'Qty':>8} {'Unit':>6} {'$/Unit':>10}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*6} {'-'*10}")

    for p in ranked:
        print(f"  {p['product']:<25} ${p['price']:>7.2f} {p['quantity']:>8.1f} {p['unit']:>6} ${p['unit_price']:>9.4f}")

    if best:
        print(f"\n  Best deal: {best['product']} at ${best['unit_price']:.4f}/{best['unit']}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"ranked": ranked, "best": best}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Round to 4 decimal places | Enough precision to distinguish similar prices without cluttering output with floating-point noise | Round to 2 — loses precision when comparing very similar unit prices (e.g., $0.0312 vs $0.0318) |
| Error dicts instead of exceptions in `parse_product_row()` | Lets the program continue processing valid rows instead of stopping at the first bad row | Raise ValueError — would require try/except in the caller and stop on first error |
| `csv.DictReader` instead of `csv.reader` | Column access by name (`row["price"]`) is self-documenting; column reordering does not break the code | `csv.reader` with index access (`row[1]`) — fragile if CSV columns are reordered |
| Separate `find_best_deal` and `rank_products` | Different use cases: quick answer ("what is cheapest?") vs full comparison table | One function that sorts and returns `sorted[0]` — conflates two concerns |

## Alternative approaches

### Approach B: Using `min()` with a key function

```python
def find_best_deal_min(products: list[dict]) -> dict | None:
    """Find the cheapest product using min() with a key function."""
    valid = [p for p in products if "error" not in p]
    if not valid:
        return None
    # WHY min with key: min() iterates the list once and returns the
    # item with the smallest unit_price.  The key function tells min()
    # which value to compare.
    return min(valid, key=lambda p: p["unit_price"])
```

**Trade-off:** The `min()` approach is more concise and more Pythonic. It does the same work as the manual loop in one line. The manual loop version is better for learning because you can see exactly how the comparison works step by step. Once you are comfortable with `lambda` and `key` functions, prefer `min()`.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| CSV row has quantity of 0 | `calculate_unit_price()` raises `ValueError("Quantity must be positive")`, caught by `parse_product_row()` which returns an error dict | The guard clause is already in place; the zero-quantity row is skipped in ranking |
| Price column contains text like `"N/A"` | `float("N/A")` raises ValueError, caught by the try/except in `parse_product_row()` | Error is captured in the result dict; valid rows still process normally |
| CSV file has no data rows (headers only) | `load_products()` returns `[]`, `find_best_deal()` returns `None`, `rank_products()` returns `[]` | All functions handle empty lists gracefully; output shows an empty comparison table |
| Floating-point precision (e.g., `7.99 / 3`) | Without rounding, result would be `2.6633333333333336`; with `round(..., 4)` it becomes `2.6633` | Rounding is built into `calculate_unit_price()` |

## Key takeaways

1. **CSV data is always strings.** Every value from `csv.DictReader` is a string — you must convert to `float()` or `int()` explicitly, and handle conversion failures. This is true for all external data sources (files, APIs, databases).
2. **`sorted()` with `key=lambda` is how Python sorts complex data.** You will use this pattern constantly: `sorted(items, key=lambda x: x["field"])`. The `key` function tells Python what value to compare.
3. **This project connects to real-world price comparison engines.** Grocery apps, procurement systems, and e-commerce platforms all compute unit prices to help users find the best deal. The same CSV-parse-compute-sort pipeline applies to any tabular data analysis.
