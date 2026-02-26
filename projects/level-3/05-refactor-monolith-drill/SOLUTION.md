# Refactor Monolith Drill — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Refactor Monolith Drill."""

from __future__ import annotations

import argparse
import csv
import json
import logging
from dataclasses import dataclass, field, asdict
from io import StringIO
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# WHY: dataclasses give each entity a clear, typed shape.
# In the "monolith" version, employees would be plain dicts
# and you would never be sure which keys exist.
@dataclass
class Employee:
    """A single employee record."""
    name: str
    department: str
    salary: float
    years: int


@dataclass
class DepartmentStats:
    """Statistics for one department."""
    name: str
    headcount: int
    total_salary: float
    avg_salary: float
    min_salary: float
    max_salary: float
    avg_tenure: float


@dataclass
class CompanyReport:
    """Full company report with per-department breakdowns."""
    total_employees: int
    total_payroll: float
    departments: list[DepartmentStats] = field(default_factory=list)


# -- Step 1: Parse -------------------------------------------------------
# WHY: separating parsing from file I/O lets us test parse_csv()
# with a string, without ever touching the filesystem.

def parse_csv(text: str) -> list[Employee]:
    """Parse CSV text into Employee records."""
    # WHY: csv.DictReader handles header-row mapping automatically.
    # StringIO wraps a string so DictReader can read it like a file.
    reader = csv.DictReader(StringIO(text))
    employees: list[Employee] = []

    for row in reader:
        try:
            emp = Employee(
                name=row["name"].strip(),
                department=row["department"].strip(),
                salary=float(row["salary"]),
                years=int(row["years"]),
            )
            employees.append(emp)
        except (KeyError, ValueError) as exc:
            # WHY: log and skip bad rows instead of crashing.
            # One corrupt row should not prevent processing the
            # other 999 valid rows.
            logger.warning("Skipping bad row %r: %s", row, exc)

    logger.info("Parsed %d employees", len(employees))
    return employees


def load_employees(path: Path) -> list[Employee]:
    """Load employees from a CSV file.

    WHY: this thin wrapper is the ONLY place that touches the
    filesystem. parse_csv() is pure logic.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    return parse_csv(text)


# -- Step 2: Group -------------------------------------------------------

def group_by_department(employees: list[Employee]) -> dict[str, list[Employee]]:
    """Group employees by department name.

    WHY: setdefault() creates the list on first access, avoiding
    a separate "if key not in dict" check. Cleaner than defaultdict
    for simple cases.
    """
    groups: dict[str, list[Employee]] = {}
    for emp in employees:
        groups.setdefault(emp.department, []).append(emp)
    return groups


# -- Step 3: Compute stats -----------------------------------------------

def compute_department_stats(name: str, employees: list[Employee]) -> DepartmentStats:
    """Compute statistics for a single department.

    WHY: this function takes a NAME and a LIST — it knows nothing
    about how the grouping was done. That makes it independently
    testable: pass in any list of employees and get stats back.
    """
    salaries = [e.salary for e in employees]
    tenures = [e.years for e in employees]
    return DepartmentStats(
        name=name,
        headcount=len(employees),
        total_salary=round(sum(salaries), 2),
        avg_salary=round(sum(salaries) / len(salaries), 2),
        min_salary=min(salaries),
        max_salary=max(salaries),
        avg_tenure=round(sum(tenures) / len(tenures), 1),
    )


# -- Step 4: Build report ------------------------------------------------

def build_report(employees: list[Employee]) -> CompanyReport:
    """Build a full company report from employee records.

    WHY: this is the orchestrator that chains the decomposed steps.
    Each step is one line — easy to read, easy to debug, easy to
    insert a new step (e.g. "enrich" before "compute").
    """
    groups = group_by_department(employees)
    dept_stats = [
        compute_department_stats(name, emps)
        for name, emps in sorted(groups.items())
    ]

    return CompanyReport(
        total_employees=len(employees),
        total_payroll=round(sum(e.salary for e in employees), 2),
        departments=dept_stats,
    )


# -- Step 5: Format output -----------------------------------------------

def format_report_text(report: CompanyReport) -> str:
    """Format a CompanyReport as human-readable text.

    WHY: formatting is separate from computation. The same report
    data can be rendered as text, JSON, HTML, or CSV by writing
    different format functions — no business logic changes.
    """
    lines = [
        f"Company Report: {report.total_employees} employees, "
        f"${report.total_payroll:,.2f} total payroll",
        "=" * 60,
    ]

    for dept in report.departments:
        lines.append(f"\n{dept.name} ({dept.headcount} people)")
        lines.append(f"  Salary range: ${dept.min_salary:,.0f} - ${dept.max_salary:,.0f}")
        lines.append(f"  Average salary: ${dept.avg_salary:,.2f}")
        lines.append(f"  Average tenure: {dept.avg_tenure} years")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Refactor monolith drill")
    parser.add_argument("file", help="CSV file with employee data")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--department", help="Filter to one department")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    """Entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    employees = load_employees(Path(args.file))

    if args.department:
        employees = [e for e in employees if e.department == args.department]
        if not employees:
            print(f"No employees found in department: {args.department}")
            return

    report = build_report(employees)

    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(format_report_text(report))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| 5-step pipeline: parse -> group -> compute -> build -> format | Each step has a single responsibility and can be tested independently. The "monolith" alternative would be one 100-line function that is impossible to test or modify safely. |
| `parse_csv` takes a string, not a file path | Separating parsing from I/O means tests can pass CSV strings directly without creating temporary files. This is the core lesson of this project. |
| `csv.DictReader` instead of manual splitting | DictReader handles quoting, headers, and edge cases that `line.split(",")` misses. Use standard library tools when they exist. |
| Skip bad rows with logging, do not crash | In batch processing, one bad row should not kill the entire run. Log the problem, skip it, and let the user decide whether to fix the data. |
| `sorted(groups.items())` for department ordering | Alphabetical department order makes output deterministic and diffable across runs. |

## Alternative Approaches

### Using `pandas` for analysis

```python
import pandas as pd

def build_report_pandas(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)
    summary = df.groupby("department").agg(
        headcount=("name", "count"),
        avg_salary=("salary", "mean"),
        total_salary=("salary", "sum"),
    ).to_dict("index")
    return summary
```

**Trade-off:** Pandas is dramatically more concise for data aggregation and handles edge cases automatically. But it is a heavy dependency (100+ MB) and hides the mechanics that this project is designed to teach. Use pandas in production, but understand the manual approach first.

## Common Pitfalls

1. **Division by zero in stats** — If a department has zero employees (which should not happen after grouping, but could happen with a filter), `sum(salaries) / len(salaries)` crashes. Always guard division operations or ensure the list is non-empty before computing.

2. **Mutating the input list** — Writing `employees = [e for e in employees if ...]` creates a new list. If you used `employees.remove(e)` in a loop, you would skip elements because the list shifts under the iterator.

3. **Forgetting to strip CSV fields** — Raw CSV values often have trailing spaces or newlines. The `row["name"].strip()` calls are essential. Without them, "Engineering" and "Engineering " would be treated as different departments.
