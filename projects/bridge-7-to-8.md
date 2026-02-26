# Bridge Exercise: Level 7 to Level 8

You have completed Level 7. You can build API clients, implement caching, handle rate limiting, and work with pagination. Level 8 introduces **dashboards**, **data visualization**, **report generation**, and **monitoring**. This bridge exercise connects API data fetching with structured display and reporting.

---

## What Changes in Level 8

In Level 7, you fetched and stored data. In Level 8, you will:
- Build **text-based dashboards** that display live data
- Generate **reports** in multiple formats (text, CSV, JSON)
- Create **summary statistics** from raw data
- Design **monitoring views** that highlight important changes

---

## Part 1: Data Aggregation

### Exercise

Build functions that take raw API-style data and produce dashboard-ready summaries.

Create `bridge_7_to_8.py`:

```python
from collections import Counter, defaultdict
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def compute_stats(records, value_key="value"):
    """Compute summary statistics for a list of records.

    Returns: dict with count, total, average, min, max, and distribution.
    """
    if not records:
        return {"count": 0, "total": 0, "average": 0, "min": 0, "max": 0}

    values = [r[value_key] for r in records if value_key in r]
    if not values:
        return {"count": 0, "total": 0, "average": 0, "min": 0, "max": 0}

    return {
        "count": len(values),
        "total": sum(values),
        "average": round(sum(values) / len(values), 2),
        "min": min(values),
        "max": max(values),
    }


def group_and_summarize(records, group_key, value_key="value"):
    """Group records by a key and compute stats for each group.

    Returns: dict of {group_name: stats_dict}
    """
    groups = defaultdict(list)
    for record in records:
        if group_key in record:
            groups[record[group_key]].append(record)

    return {
        name: compute_stats(group_records, value_key)
        for name, group_records in sorted(groups.items())
    }
```

**New concepts introduced:**
- **Aggregation**: turning many data points into summary numbers.
- `defaultdict(list)` for grouping — each key gets an empty list to append to.
- Dict comprehension to build the summary in one expression.

---

## Part 2: Text Dashboard

### Exercise

Build a text-based dashboard that formats data for terminal display.

Add to `bridge_7_to_8.py`:

```python
def format_dashboard(title, grouped_stats, width=60):
    """Format grouped statistics as a text dashboard.

    Returns a multi-line string ready to print.
    """
    lines = []
    lines.append("=" * width)
    lines.append(f" {title}".center(width))
    lines.append("=" * width)
    lines.append("")

    for group_name, stats in grouped_stats.items():
        lines.append(f"  {group_name}")
        lines.append(f"  {'-' * (width - 4)}")
        lines.append(f"    Count:   {stats['count']}")
        lines.append(f"    Total:   {stats['total']:,.2f}")
        lines.append(f"    Average: {stats['average']:,.2f}")
        lines.append(f"    Min:     {stats['min']:,.2f}")
        lines.append(f"    Max:     {stats['max']:,.2f}")

        # Simple bar chart
        if stats["max"] > 0:
            bar_length = int(30 * stats["average"] / stats["max"])
            bar = "#" * bar_length
            lines.append(f"    Avg bar: [{bar:<30}]")
        lines.append("")

    lines.append("=" * width)
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * width)

    return "\n".join(lines)


def generate_report(records, group_key, value_key="value", format="text"):
    """Generate a report in the specified format.

    Formats: 'text' (dashboard), 'json' (structured), 'csv' (tabular)
    """
    grouped = group_and_summarize(records, group_key, value_key)

    if format == "json":
        return json.dumps(grouped, indent=2)

    elif format == "csv":
        lines = ["group,count,total,average,min,max"]
        for name, stats in grouped.items():
            lines.append(
                f"{name},{stats['count']},{stats['total']},"
                f"{stats['average']},{stats['min']},{stats['max']}"
            )
        return "\n".join(lines)

    else:  # text
        return format_dashboard("Data Report", grouped)
```

**New concepts introduced:**
- **Text formatting** with f-strings: `:,.2f` for thousands separator and 2 decimals.
- **String alignment**: `.center(width)`, `:<30` for left-align in 30 chars.
- **Multi-format output**: same data rendered as text, JSON, or CSV.
- Simple **ASCII bar charts** built from `#` characters.

---

## Part 3: Tests

Create `test_bridge_7_to_8.py`:

```python
import json
import pytest
from bridge_7_to_8 import compute_stats, group_and_summarize, generate_report


@pytest.fixture
def sales_data():
    return [
        {"region": "North", "value": 100},
        {"region": "North", "value": 200},
        {"region": "South", "value": 150},
        {"region": "South", "value": 50},
        {"region": "South", "value": 300},
        {"region": "East", "value": 175},
    ]


def test_compute_stats_basic():
    records = [{"value": 10}, {"value": 20}, {"value": 30}]
    stats = compute_stats(records)
    assert stats["count"] == 3
    assert stats["total"] == 60
    assert stats["average"] == 20.0
    assert stats["min"] == 10
    assert stats["max"] == 30


def test_compute_stats_empty():
    stats = compute_stats([])
    assert stats["count"] == 0


def test_group_and_summarize(sales_data):
    grouped = group_and_summarize(sales_data, "region")
    assert "North" in grouped
    assert "South" in grouped
    assert grouped["North"]["count"] == 2
    assert grouped["South"]["count"] == 3
    assert grouped["North"]["average"] == 150.0


def test_report_json(sales_data):
    report = generate_report(sales_data, "region", format="json")
    parsed = json.loads(report)
    assert "North" in parsed
    assert parsed["East"]["count"] == 1


def test_report_csv(sales_data):
    report = generate_report(sales_data, "region", format="csv")
    lines = report.strip().split("\n")
    assert lines[0] == "group,count,total,average,min,max"
    assert len(lines) == 4  # header + 3 regions


def test_report_text(sales_data):
    report = generate_report(sales_data, "region", format="text")
    assert "Data Report" in report
    assert "North" in report
    assert "South" in report
```

Run: `pytest test_bridge_7_to_8.py -v`

---

## You Are Ready

If you can aggregate data into summary statistics, group records by category, format output for terminal display, and generate reports in multiple formats, you are ready for Level 8.

---

| [Level 7 Projects](level-7/README.md) | [Home](../README.md) | [Level 8 Projects](level-8/README.md) |
|:---|:---:|---:|
