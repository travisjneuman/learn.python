"""Tests for Refactor Monolith Drill.

Each decomposed function is tested independently.
"""

from pathlib import Path

import pytest

from project import (
    CompanyReport,
    DepartmentStats,
    Employee,
    build_report,
    compute_department_stats,
    format_report_text,
    group_by_department,
    load_employees,
    parse_csv,
)


CSV_DATA = """\
name,department,salary,years
Alice,Engineering,95000,5
Bob,Engineering,105000,8
Carol,Marketing,72000,3
Dave,Marketing,68000,2
Eve,Engineering,88000,1
"""


def test_parse_csv() -> None:
    """CSV parsing should produce Employee dataclasses."""
    employees = parse_csv(CSV_DATA)
    assert len(employees) == 5
    assert employees[0].name == "Alice"
    assert employees[0].salary == 95000.0
    assert employees[0].department == "Engineering"


def test_parse_csv_bad_row() -> None:
    """Bad rows should be skipped, not crash."""
    bad = "name,department,salary,years\nBad,Data,notanumber,x\n"
    employees = parse_csv(bad)
    assert len(employees) == 0


def test_load_employees(tmp_path: Path) -> None:
    """Should load from a real file."""
    f = tmp_path / "data.csv"
    f.write_text(CSV_DATA, encoding="utf-8")
    employees = load_employees(f)
    assert len(employees) == 5


def test_load_employees_missing(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_employees(tmp_path / "nope.csv")


def test_group_by_department() -> None:
    """Employees should group by department name."""
    employees = parse_csv(CSV_DATA)
    groups = group_by_department(employees)
    assert "Engineering" in groups
    assert "Marketing" in groups
    assert len(groups["Engineering"]) == 3
    assert len(groups["Marketing"]) == 2


def test_compute_department_stats() -> None:
    """Stats should compute correct aggregates."""
    emps = [
        Employee("A", "Eng", 80000, 2),
        Employee("B", "Eng", 100000, 6),
    ]
    stats = compute_department_stats("Eng", emps)
    assert stats.headcount == 2
    assert stats.avg_salary == 90000.0
    assert stats.min_salary == 80000
    assert stats.max_salary == 100000
    assert stats.avg_tenure == 4.0


def test_build_report() -> None:
    """Full report should have correct totals."""
    employees = parse_csv(CSV_DATA)
    report = build_report(employees)
    assert report.total_employees == 5
    assert len(report.departments) == 2
    assert report.total_payroll == 428000.0


def test_format_report_text() -> None:
    """Text format should contain key information."""
    report = CompanyReport(
        total_employees=2,
        total_payroll=100000,
        departments=[DepartmentStats("Eng", 2, 100000, 50000, 40000, 60000, 3.0)],
    )
    text = format_report_text(report)
    assert "Eng" in text
    assert "100,000" in text
