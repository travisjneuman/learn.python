# Records Deduplicator — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 20 minutes attempting it independently.

## Thinking Process

Deduplication is one of the most common tasks in data processing. Before writing any code, ask yourself: what makes two records "the same"? It is not always every field -- maybe two customer records have the same email but different phone numbers. The user should be able to choose which fields define uniqueness.

Next, think about the data structure you need. You are going to iterate through records and ask "have I seen this combination of fields before?" That is a membership question, and Python sets answer membership questions in O(1) time -- constant time regardless of how many items are in the set. A list would require scanning every previous item, which gets slower as the data grows.

Finally, consider the "keep" strategy. If you keep the first occurrence, you skip later duplicates. If you keep the last, you need to replace what you stored earlier. These two strategies require slightly different logic, so plan for both before coding.

## Step 1: Parse the CSV into Records

**What to do:** Write a function that reads a CSV file and returns a list of header names plus a list of dicts (one per row).

**Why:** Everything downstream needs structured data. Converting CSV rows into dicts lets you access fields by name (`record["email"]`) instead of by position (`row[2]`), which is less error-prone.

```python
def parse_csv_records(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return [], []

    headers = [h.strip() for h in lines[0].split(",")]
    records = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        while len(values) < len(headers):
            values.append("")
        record = dict(zip(headers, values))
        records.append(record)

    return headers, records
```

**Predict:** What does `dict(zip(headers, values))` produce if `headers = ["name", "email"]` and `values = ["Alice", "alice@example.com"]`? What if there are more headers than values -- why does the `while` padding matter?

## Step 2: Build the Dedup Key

**What to do:** Write a function that creates a unique string from the fields that define "sameness."

**Why:** To check if two records are duplicates, you need a single comparable value. By joining the normalized field values with a separator, you get a string that uniquely represents the combination of those fields.

```python
def make_dedup_key(record: dict[str, str], key_fields: list[str]) -> str:
    parts = []
    for field in key_fields:
        value = record.get(field, "").strip().lower()
        parts.append(value)
    return "|".join(parts)
```

The `|` separator is critical. Without it, a record with name `"ab"` and email `"cd"` would have the same key as one with name `"a"` and email `"bcd"` (both would be `"abcd"`). The separator keeps field boundaries clear.

**Predict:** If you use `--keys email` instead of `--keys name email`, would records with `alice@example.com` and `ALICE@EXAMPLE.COM` still be detected as duplicates?

## Step 3: Deduplicate with "Keep First"

**What to do:** Write the core `deduplicate()` function using a set to track seen keys.

**Why:** This is where the set's O(1) lookup shines. For each record, you check `if dedup_key in seen` -- this is instant, no matter how large the dataset.

```python
def deduplicate(records, key_fields, keep="first"):
    seen: set[str] = set()
    key_to_record: dict[str, dict] = {}
    unique: list[dict] = []
    duplicates: list[dict] = []

    for idx, record in enumerate(records):
        dedup_key = make_dedup_key(record, key_fields)
        record_with_meta = {**record, "_original_index": idx, "_dedup_key": dedup_key}

        if dedup_key in seen:
            if keep == "first":
                duplicates.append(record_with_meta)
        else:
            seen.add(dedup_key)
            key_to_record[dedup_key] = record_with_meta
            if keep == "first":
                unique.append(record_with_meta)
```

**Predict:** What changes for `keep="last"` mode? Think about it: you want to keep the last occurrence of each key instead of the first. How would you modify the logic?

## Step 4: Handle "Keep Last" Mode

**What to do:** Extend the dedup logic so that when `keep="last"`, later records replace earlier ones.

**Why:** In "last" mode, when a duplicate arrives, the previously stored record becomes the duplicate and the new one takes its place. At the end, you sort by original index to restore file order.

```python
if dedup_key in seen:
    if keep == "last":
        old = key_to_record[dedup_key]
        duplicates.append(old)
        key_to_record[dedup_key] = record_with_meta

# After the loop, for "last" mode:
if keep == "last":
    unique = sorted(key_to_record.values(), key=lambda r: r["_original_index"])
```

**Predict:** Why do we need to sort by `_original_index` at the end? What would the order be without sorting?

## Step 5: Group Duplicates for Analysis

**What to do:** Write a `find_duplicate_groups()` function that groups all records sharing the same dedup key, then filters to only groups with more than one member.

**Why:** Sometimes you want to see which records are duplicates of each other, not just get the deduplicated list. This is useful for data auditing -- before deleting duplicates, you want to inspect them.

```python
def find_duplicate_groups(records, key_fields):
    groups: dict[str, list[dict]] = {}
    for record in records:
        key = make_dedup_key(record, key_fields)
        groups.setdefault(key, []).append(record)

    # Dict comprehension: keep only groups with actual duplicates
    return {k: v for k, v in groups.items() if len(v) > 1}
```

`dict.setdefault(key, [])` is a useful pattern: if the key exists, return its value; if not, set it to `[]` and return that. This avoids the `if key not in groups: groups[key] = []` boilerplate.

**Predict:** What would the output look like for a dataset where every record is unique? What about a dataset where every record is identical?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Using a list instead of a set for `seen` | Works but is slow for large data | Sets have O(1) lookup; lists have O(n) |
| Forgetting to normalize case | "Alice" and "alice" are treated as different | `.strip().lower()` in `make_dedup_key()` |
| No separator between key parts | `"ab" + "cd"` and `"a" + "bcd"` both produce `"abcd"` | Join with `"\|"` to keep fields distinct |
| `keep="last"` loses original order | Records come out in dict insertion order, not file order | Track `_original_index` and sort at the end |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
9 passed
```

Test from the command line with different modes:

```bash
python project.py data/sample_input.txt --keys name email
python project.py data/sample_input.txt --keys email --keep last
python project.py data/sample_input.txt --keys email --show-groups
```

## What You Learned

- **Sets provide O(1) membership testing**, making them the right choice any time you need to ask "have I seen this before?" across a large dataset.
- **Composite keys** (joining multiple fields with a separator) let you define uniqueness across any combination of columns, not just a single field.
- **The `keep="first"` vs `keep="last"` pattern** appears everywhere in data processing -- pandas has the same concept in `DataFrame.drop_duplicates(keep=...)`.
