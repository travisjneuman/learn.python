# Level 2 Mini Capstone: Data Pipeline — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone ties together everything from Level 2, so spend at least 30 minutes attempting it independently.

## Thinking Process

A data pipeline is a sequence of steps where each step takes input from the previous one. Before writing any code, sketch the five stages on paper: Load -> Clean -> Validate -> Analyse -> Report. Each stage is a separate function. This matters because if validation changes, you only edit the validation function -- everything else stays untouched.

Ask yourself: what does each stage receive, and what does it produce? `load_csv` receives a file path and produces raw records. `clean_records` receives raw records and produces cleaned records. `validate_batch` receives cleaned records and splits them into valid and invalid. Draw this data flow on paper before coding -- the implementation becomes a matter of filling in each box.

The capstone also asks you to think about failure modes. What if there are zero records? What if every record is invalid? What if there is no numeric column for anomaly detection? These are not exotic edge cases -- they happen every day in real data pipelines. Planning for them up front is what separates a script that works from one that works reliably.

## Step 1: Load and Parse the CSV

**What to do:** Write a function that reads a CSV file, skips comment lines (starting with `#`), and returns headers plus a list of record dicts.

**Why:** This is the foundation of the pipeline. Every other stage depends on getting structured data out of the file.

```python
def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [l.strip() for l in lines if l.strip() and not l.startswith("#")]

    if not lines:
        return [], []

    headers = [h.strip() for h in lines[0].split(",")]
    records = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        while len(values) < len(headers):
            values.append("")
        records.append(dict(zip(headers, values)))

    return headers, records
```

**Predict:** What happens when the file has only a header row and no data rows? Trace through the code -- what do `headers` and `records` look like?

## Step 2: Clean the Records

**What to do:** Write a cleaning function that strips whitespace and normalizes emails to lowercase.

**Why:** Raw data is messy. Cleaning is always the second step because validation (Step 3) should operate on normalized data, not raw data. If you validate first, you might reject `" alice@EXAMPLE.com "` even though it is a perfectly valid email after cleaning.

```python
def clean_record(record: dict[str, str]) -> dict[str, str]:
    cleaned = {}
    for key, value in record.items():
        value = value.strip()
        if "email" in key.lower():
            value = value.lower()
        cleaned[key] = value
    return cleaned

def clean_records(records):
    return [clean_record(r) for r in records]
```

**Predict:** Why lowercase only email fields and not everything? What would happen if you lowercased the "name" field?

## Step 3: Validate Against Rules

**What to do:** Write a validation function that checks required fields, email format, and numeric ranges against a configurable rules dictionary.

**Why:** Separating rules from logic means you can change what gets validated (e.g., add a new required field) without modifying the validation code itself. The rules dict acts as configuration.

```python
DEFAULT_RULES = {
    "required": ["name", "email"],
    "email_field": "email",
    "ranges": {
        "age": {"min": 0, "max": 150},
        "salary": {"min": 0, "max": 1000000},
    },
}

def validate_record(record, rules):
    errors = []
    for field in rules.get("required", []):
        if not record.get(field, "").strip():
            errors.append(f"Missing required field: {field}")

    email_field = rules.get("email_field")
    if email_field and record.get(email_field):
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", record[email_field]):
            errors.append(f"Invalid email: {record[email_field]}")

    for field, bounds in rules.get("ranges", {}).items():
        value = record.get(field, "")
        try:
            num = float(value)
            if num < bounds["min"] or num > bounds["max"]:
                errors.append(f"{field} out of range: {num}")
        except (ValueError, TypeError):
            if value:
                errors.append(f"{field} is not numeric: {value}")

    return {"valid": len(errors) == 0, "errors": errors}
```

Notice the **accumulate errors** pattern: each check adds to the `errors` list. A record is valid only if the list is empty. This gives the user all the problems at once, rather than fixing one and discovering the next.

**Predict:** Looking at a record like `,bad-email,-5,50000` -- how many errors will it accumulate? Name each one.

## Step 4: Detect Anomalies with Z-Scores

**What to do:** Write a function that finds outliers in a numeric field using z-scores (how many standard deviations a value is from the mean).

**Why:** Anomaly detection catches data that is technically valid (passes all rules) but is statistically unusual. A salary of 999999 might pass the range check but still be an outlier worth flagging.

```python
def detect_anomalies(records, field, threshold=2.0):
    values = []
    for r in records:
        try:
            values.append(float(r.get(field, "")))
        except (ValueError, TypeError):
            pass

    if len(values) < 2:
        return []

    avg = sum(values) / len(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    sd = math.sqrt(variance) if variance > 0 else 0

    if sd == 0:
        return []  # All values identical -- no anomalies possible
```

A **z-score** measures how far a value is from the average: `z = (value - mean) / standard_deviation`. Values with `|z| > threshold` (default 2.0) are flagged.

**Predict:** If all salaries are exactly the same (e.g., 50000), what is the standard deviation? What does the function return, and why is that the correct behavior?

## Step 5: Generate the Report

**What to do:** Write a function that assembles the results from all stages into a formatted text report.

**Why:** The report is the human-readable output that makes the pipeline useful. It summarizes what the pipeline found at every stage.

```python
def generate_report(total, valid, invalid, anomalies, numeric_field):
    lines = [
        "=" * 60,
        "  DATA PIPELINE REPORT",
        "=" * 60,
        f"Records loaded:    {total}",
        f"Records valid:     {len(valid)}",
        f"Records invalid:   {len(invalid)}",
        f"Anomalies found:   {len(anomalies)}",
        f"Pass rate:         {round(len(valid) / total * 100, 1) if total else 0}%",
    ]
    return "\n".join(lines)
```

**Predict:** What happens if `total` is 0? Why is the `if total else 0` guard necessary in the pass rate calculation?

## Step 6: Wire the Pipeline Together

**What to do:** Write a `run_pipeline()` function that calls each stage in order, passing outputs to inputs.

**Why:** This orchestrator function is the backbone. Notice how each stage is a clean function call -- no global state, no side effects between stages.

```python
def run_pipeline(input_path, rules, numeric_field, anomaly_threshold=2.0):
    headers, raw_records = load_csv(input_path)
    cleaned = clean_records(raw_records)
    valid, invalid = validate_batch(cleaned, rules)
    anomalies = detect_anomalies(valid, numeric_field, threshold=anomaly_threshold)
    report = generate_report(len(raw_records), valid, invalid, anomalies, numeric_field)
    return {"report": report, "valid_records": valid, ...}
```

Notice that anomaly detection runs on **valid** records only. Invalid records were already filtered out. This prevents bad data from skewing the statistics.

**Predict:** What would go wrong if you ran anomaly detection on all records, including invalid ones?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Division by zero in pass rate | Zero records loaded from an empty file | Guard with `if total else 0` |
| Anomaly detection crashes on non-numeric fields | `float()` on text values | Wrap in `try/except`, skip non-parseable values |
| Standard deviation is 0 | All values are identical | Check `if sd == 0` and return no anomalies |
| Validating before cleaning | Running stages out of order | Always clean first, then validate |
| One giant function | Tempting to write all logic in `main()` | Separate stages make testing and debugging possible |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
10 passed
```

Test with different options:

```bash
python project.py data/sample_input.txt
python project.py data/sample_input.txt --numeric-field salary --threshold 2.0
python project.py data/sample_input.txt --json
```

## What You Learned

- **Pipeline architecture** (Load -> Clean -> Validate -> Analyse -> Report) is the standard pattern for data processing. Each stage has a single responsibility.
- **Separating rules from logic** (the `rules` dict vs the `validate_record` function) means you can add new validation checks without touching the code that applies them.
- **Z-score anomaly detection** is a simple but effective way to find outliers: any value more than 2 standard deviations from the mean is flagged. This technique is used in monitoring, fraud detection, and quality control.
