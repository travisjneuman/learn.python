# Bridge Exercise: Level 1 to Level 2

You have completed Level 1. You can read and write files (CSV, JSON, text), handle errors with try/except, and work with basic string formatting. Level 2 introduces **data structures** (nested dicts, sets, defaultdict), **data cleaning**, and **more complex testing**. This bridge exercise connects file I/O to data manipulation.

---

## What Changes in Level 2

In Level 1, you read files and processed them line by line. In Level 2, you will:
- Build **complex data structures** (lists of dicts, nested dicts, sets)
- **Clean and transform** messy real-world data
- Use **collections** like `defaultdict` and `Counter`
- Write tests that check **data transformations**, not just single values

---

## Part 1: From File to Data Structure

### Exercise

You have a CSV file of sales data. Read it and build a structured summary.

Create `bridge_1_to_2.py`:

```python
import csv
from collections import defaultdict
from pathlib import Path


def load_sales(filepath):
    """Read a CSV file and return a list of sale dicts.

    Expected columns: date, product, quantity, price
    Skips rows with missing or invalid data.
    """
    path = Path(filepath)
    sales = []

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                sale = {
                    "date": row["date"].strip(),
                    "product": row["product"].strip(),
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"]),
                }
                sales.append(sale)
            except (ValueError, KeyError):
                continue  # skip bad rows

    return sales


def summarize_by_product(sales):
    """Group sales by product and return totals.

    Returns a dict: {product_name: {"units": int, "revenue": float}}
    """
    summary = defaultdict(lambda: {"units": 0, "revenue": 0.0})

    for sale in sales:
        product = sale["product"]
        summary[product]["units"] += sale["quantity"]
        summary[product]["revenue"] += sale["quantity"] * sale["price"]

    return dict(summary)
```

**New concepts introduced:**
- `csv.DictReader` turns each CSV row into a dict (column headers become keys).
- `defaultdict` creates missing keys automatically with a default value.
- Building a nested data structure from flat file data.

### Try it

Create `sample_sales.csv`:

```csv
date,product,quantity,price
2024-01-15,Widget,10,4.99
2024-01-15,Gadget,3,19.99
2024-01-16,Widget,7,4.99
2024-01-16,Gadget,5,19.99
2024-01-17,Widget,bad,4.99
```

```python
from bridge_1_to_2 import load_sales, summarize_by_product

sales = load_sales("sample_sales.csv")
print(f"Loaded {len(sales)} valid sales")  # 4 (bad row skipped)

summary = summarize_by_product(sales)
for product, totals in summary.items():
    print(f"{product}: {totals['units']} units, ${totals['revenue']:.2f}")
```

---

## Part 2: Data Cleaning

### Exercise

Add a function that finds duplicate and anomalous records.

Add to `bridge_1_to_2.py`:

```python
def find_anomalies(sales):
    """Identify potential data quality issues.

    Returns a dict with:
    - 'duplicates': list of (date, product) pairs that appear more than once
    - 'high_quantity': sales where quantity > 100
    - 'unique_products': set of all product names
    """
    seen = defaultdict(int)
    duplicates = []
    high_quantity = []

    for sale in sales:
        key = (sale["date"], sale["product"])
        seen[key] += 1
        if sale["quantity"] > 100:
            high_quantity.append(sale)

    for key, count in seen.items():
        if count > 1:
            duplicates.append(key)

    unique_products = {sale["product"] for sale in sales}  # set comprehension

    return {
        "duplicates": duplicates,
        "high_quantity": high_quantity,
        "unique_products": unique_products,
    }
```

**New concepts introduced:**
- **Set comprehension** `{x for x in items}` — builds a set of unique values in one line.
- Using tuples as dict keys — `(date, product)` pairs are hashable, so they work as keys.
- Counting occurrences to find duplicates.

---

## Part 3: Tests

Create `test_bridge_1_to_2.py`:

```python
import pytest
from bridge_1_to_2 import load_sales, summarize_by_product, find_anomalies


@pytest.fixture
def sample_csv(tmp_path):
    f = tmp_path / "sales.csv"
    f.write_text(
        "date,product,quantity,price\n"
        "2024-01-15,Widget,10,4.99\n"
        "2024-01-15,Gadget,3,19.99\n"
        "2024-01-16,Widget,7,4.99\n"
    )
    return f


def test_load_sales(sample_csv):
    sales = load_sales(sample_csv)
    assert len(sales) == 3
    assert sales[0]["product"] == "Widget"
    assert sales[0]["quantity"] == 10


def test_load_skips_bad_rows(tmp_path):
    f = tmp_path / "bad.csv"
    f.write_text(
        "date,product,quantity,price\n"
        "2024-01-15,Widget,bad,4.99\n"
        "2024-01-15,Gadget,3,19.99\n"
    )
    sales = load_sales(f)
    assert len(sales) == 1


def test_summarize_by_product(sample_csv):
    sales = load_sales(sample_csv)
    summary = summarize_by_product(sales)
    assert summary["Widget"]["units"] == 17
    assert summary["Widget"]["revenue"] == pytest.approx(84.83)


def test_find_anomalies_unique_products(sample_csv):
    sales = load_sales(sample_csv)
    result = find_anomalies(sales)
    assert result["unique_products"] == {"Widget", "Gadget"}
```

Run: `pytest test_bridge_1_to_2.py -v`

---

## You Are Ready

If you can read a CSV into a list of dicts, group data with `defaultdict`, use set comprehensions, and test data transformations, you are ready for Level 2.

---

| [Level 1 Projects](level-1/README.md) | [Home](../README.md) | [Level 2 Projects](level-2/README.md) |
|:---|:---:|---:|
