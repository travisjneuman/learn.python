"""Level 3 project: Refactor Monolith Drill.

Starts with one large function that does everything (the "monolith"),
then refactors into small, testable, single-responsibility functions.

Skills practiced: refactoring, function decomposition, logging,
dataclasses, typing basics, separation of concerns.
"""

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


# ── Step 1: Parse ──────────────────────────────────────────────

def parse_csv(text: str) -> list[Employee]:
    """Parse CSV text into Employee records.

    Expected columns: name, department, salary, years
    """
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
            logger.warning("Skipping bad row %r: %s", row, exc)

    logger.info("Parsed %d employees", len(employees))
    return employees


def load_employees(path: Path) -> list[Employee]:
    """Load employees from a CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    return parse_csv(text)


# ── Step 2: Group ──────────────────────────────────────────────

def group_by_department(employees: list[Employee]) -> dict[str, list[Employee]]:
    """Group employees by department name."""
    groups: dict[str, list[Employee]] = {}
    for emp in employees:
        groups.setdefault(emp.department, []).append(emp)
    return groups


# ── Step 3: Compute stats ─────────────────────────────────────

def compute_department_stats(name: str, employees: list[Employee]) -> DepartmentStats:
    """Compute statistics for a single department."""
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


# ── Step 4: Build report ──────────────────────────────────────

def build_report(employees: list[Employee]) -> CompanyReport:
    """Build a full company report from employee records.

    This is the 'orchestrator' that ties the decomposed steps together.
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


# ── Step 5: Format output ─────────────────────────────────────

def format_report_text(report: CompanyReport) -> str:
    """Format a CompanyReport as human-readable text."""
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
