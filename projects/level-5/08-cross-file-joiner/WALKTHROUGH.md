# Cross-File Joiner — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 30 minutes attempting it independently.

## Thinking Process

Joining data across multiple files is one of the most important operations in data processing. If you have an `employees.csv` with columns `name, dept_id, role` and a `departments.csv` with `dept_id, dept_name, location`, you want to combine them so each employee row includes their department name and location. This is exactly what SQL `JOIN` does, and this project builds it in pure Python.

Before coding, understand the three join types. **Inner join** keeps only rows where the key exists in both files (employees without a department are dropped). **Left join** keeps all left-side rows, filling in right-side data where available (employees without a matching department keep their employee data but have no department info). **Full outer join** keeps everything from both sides.

The critical performance insight is **indexing**. The naive approach (for each left row, scan all right rows for a match) is O(n*m). Building a dictionary keyed by the join column first, then looking up each left row in O(1) time, reduces this to O(n+m). This is the same optimization databases use with hash joins.

## Step 1: Load CSV and JSON Files

**What to do:** Write a function that loads either CSV or JSON files into a list of dicts, determined by file extension.

**Why:** Real data comes in multiple formats. Supporting both means your joiner is more versatile. The function dispatches based on the file extension, which is a simple but effective pattern.

```python
import csv

def load_file(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"JSON file must contain an array: {path}")
        return data

    # Default: treat as CSV
    text = path.read_text(encoding="utf-8")
    return list(csv.DictReader(text.splitlines()))
```

**Predict:** What happens if someone passes a `.txt` file? Does the function crash, or does it try to parse it as CSV? Is that reasonable behavior?

## Step 2: Validate the Join Key

**What to do:** Write a function that checks whether the join key exists in the loaded records before attempting the join.

**Why:** If the key field does not exist in one of the files, the join would produce zero results without explanation. Validating up front gives the user a clear error message with the available column names, so they can fix the command.

```python
def validate_key_exists(records: list[dict], key: str, source_name: str) -> None:
    if records and not any(key in r for r in records):
        available = sorted(records[0].keys()) if records else []
        raise ValueError(
            f"Join key '{key}' not found in {source_name}. "
            f"Available columns: {available}"
        )
```

**Predict:** Why does the function check `any(key in r for r in records)` instead of just checking the first record? When might keys be present in some records but not others?

## Step 3: Build the Index

**What to do:** Write an `index_by_key()` function that builds a dictionary mapping key values to their records.

**Why:** This is the performance optimization that makes joins fast. Instead of scanning the right-side data for every left-side row, you build a lookup table once, then do O(1) lookups for each join.

```python
def index_by_key(records: list[dict], key: str) -> dict[str, dict]:
    index: dict[str, dict] = {}
    duplicates = 0

    for record in records:
        key_value = str(record.get(key, "")).strip()
        if not key_value:
            continue
        if key_value in index:
            duplicates += 1
        index[key_value] = record

    if duplicates:
        logging.warning("Found %d duplicate key values (last-wins policy)", duplicates)

    return index
```

Two things to notice:

- **Last-wins for duplicates**: If two departments have the same `dept_id`, the last one overwrites the first. The function logs a warning so the user knows this happened.
- **Empty keys are skipped**: A row with no value for the join column cannot participate in the join.

**Predict:** What happens if `employees.csv` has three rows with `dept_id=101`? After indexing, how many entries are in the index for key "101"?

## Step 4: Implement the Three Join Strategies

**What to do:** Write `join_inner()`, `join_left()`, and `join_full()` functions that combine two indexed datasets.

**Why:** Each join type serves a different use case. Inner join is for "show me only complete data." Left join is for "show me everything from the primary source with supplemental data where available." Full join is for "show me everything from both sources."

```python
def join_inner(left, right):
    result = []
    for key in left:
        if key in right:
            result.append({**left[key], **right[key]})
    return result

def join_left(left, right):
    result = []
    for key, row in left.items():
        if key in right:
            result.append({**row, **right[key]})
        else:
            result.append(dict(row))
    return result

def join_full(left, right):
    all_keys = sorted(set(left.keys()) | set(right.keys()))
    result = []
    for key in all_keys:
        merged = {}
        if key in left:
            merged.update(left[key])
        if key in right:
            merged.update(right[key])
        result.append(merged)
    return result
```

The `{**left[key], **right[key]}` syntax merges two dicts. If both dicts have the same key (like `dept_id`), the right-side value wins. For the full join, `set(left.keys()) | set(right.keys())` uses set union to get all keys from both sides.

**Predict:** If the left side has employees with `dept_id` values [101, 102, 103] and the right side has departments with `dept_id` values [102, 103, 104], how many rows does each join type produce?

## Step 5: Use a Strategy Map for Dispatch

**What to do:** Create a dictionary mapping strategy names to functions, and use it to select the right join function at runtime.

**Why:** This eliminates `if/elif` chains. Adding a new join type (e.g., `"right"`) is a one-line addition to the map plus one new function. The CLI just needs to add the new option to the choices list.

```python
JOIN_STRATEGIES = {
    "inner": join_inner,
    "left": join_left,
    "full": join_full,
}

# Usage:
join_func = JOIN_STRATEGIES.get(strategy, join_inner)
joined = join_func(left_idx, right_idx)
```

**Predict:** What happens if someone passes `strategy="right"` and it is not in the map? The `.get()` call falls back to `join_inner`. Is that the right default behavior, or should it raise an error?

## Step 6: Run the Full Pipeline

**What to do:** Write a `run()` function that loads both files, validates keys, indexes, joins, computes match statistics, and writes the output.

**Why:** The pipeline orchestrator ties everything together and also computes useful statistics (how many keys matched, how many were left-only or right-only) that help the user understand the join results.

```python
def run(left_path, right_path, output_path, key, strategy="inner"):
    left_data = load_file(left_path)
    right_data = load_file(right_path)

    validate_key_exists(left_data, key, str(left_path))
    validate_key_exists(right_data, key, str(right_path))

    left_idx = index_by_key(left_data, key)
    right_idx = index_by_key(right_data, key)

    join_func = JOIN_STRATEGIES.get(strategy, join_inner)
    joined = join_func(left_idx, right_idx)

    matched_keys = set(left_idx.keys()) & set(right_idx.keys())
    left_only = set(left_idx.keys()) - set(right_idx.keys())
    right_only = set(right_idx.keys()) - set(left_idx.keys())

    report = {
        "joined_records": len(joined),
        "strategy": strategy,
        "matched_keys": len(matched_keys),
        "left_only_keys": len(left_only),
        "right_only_keys": len(right_only),
        "data": joined,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
```

**Predict:** The statistics use set intersection (`&`) and set difference (`-`). What do `left_only` and `right_only` represent in business terms? (E.g., "employees in departments that do not exist in the departments file.")

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| O(n*m) nested loop instead of indexing | Not building the index first | Index both sides into dicts, then join using dict lookups |
| Join key not found silently | Key column has different names in the two files | `validate_key_exists` with helpful error message listing available columns |
| Duplicate keys produce unexpected results | Multiple rows share the same key value | Log a warning and document the last-wins policy |
| Right-side fields overwrite left-side fields | Both dicts have a column with the same name | Be aware of `{**left, **right}` -- right side wins on conflicts |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
5 passed
```

Test from the command line with different join types:

```bash
python project.py --left data/employees.csv --right data/departments.csv --key dept_id --join inner --output data/joined.json
python project.py --left data/employees.csv --right data/departments.csv --key dept_id --join left --output data/joined.json
python project.py --left data/employees.csv --right data/departments.csv --key dept_id --join full --output data/joined.json
```

Compare the row counts across the three join types to verify your understanding.

## What You Learned

- **Dictionary-based indexing** turns O(n*m) joins into O(n+m) joins. This is the same technique databases use with hash joins, and understanding it demystifies how SQL JOIN works under the hood.
- **Join strategies** (inner, left, full) serve different analytical needs. Inner for complete data only, left for primary-source completeness, full for comprehensive views.
- **Strategy pattern** (mapping names to functions in a dict) replaces `if/elif` chains and makes the code extensible without modification.
