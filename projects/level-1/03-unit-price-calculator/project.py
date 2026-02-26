"""Level 1 project: Unit Price Calculator.

Compare unit prices across different package sizes from a CSV file.
Find the best deal by calculating price-per-unit for each product.

Concepts: csv module, float arithmetic, rounding, sorting, file I/O.
"""


import argparse
import csv
import json
from pathlib import Path


def calculate_unit_price(total_price: float, quantity: float) -> float:
    """Calculate price per unit, rounded to 4 decimal places.

    WHY round? -- Floating-point math can produce results like
    3.3333333333333335.  Rounding keeps the output readable.
    """
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    return round(total_price / quantity, 4)


def parse_product_row(row: dict) -> dict:
    """Parse a CSV row into a product dict with unit price.

    Expected CSV columns: product, price, quantity, unit
    """
    try:
        price = float(row["price"])
        quantity = float(row["quantity"])
    except (ValueError, KeyError) as err:
        return {"raw": str(row), "error": str(err)}

    if quantity <= 0:
        return {"raw": str(row), "error": "Quantity must be positive"}

    unit_price = calculate_unit_price(price, quantity)

    return {
        "product": row.get("product", "").strip(),
        "price": price,
        "quantity": quantity,
        "unit": row.get("unit", "unit").strip(),
        "unit_price": unit_price,
    }


def load_products(path: Path) -> list[dict]:
    """Load products from a CSV file and compute unit prices."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    products = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(parse_product_row(row))

    return products


def find_best_deal(products: list[dict]) -> dict | None:
    """Find the product with the lowest unit price.

    WHY filter errors first? -- Products with parse errors have no
    unit_price, so including them would crash the comparison.
    """
    valid = [p for p in products if "error" not in p]
    if not valid:
        return None

    best = valid[0]
    for product in valid[1:]:
        if product["unit_price"] < best["unit_price"]:
            best = product

    return best


def rank_products(products: list[dict]) -> list[dict]:
    """Sort valid products by unit price (cheapest first)."""
    valid = [p for p in products if "error" not in p]
    return sorted(valid, key=lambda p: p["unit_price"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Unit Price Calculator")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


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
