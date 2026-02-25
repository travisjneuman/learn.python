"""Level 3 project: Mini Capstone — Project Health Dashboard.

Combines Level 3 skills into a junior-level production tool that
scans a project directory and generates a health report: file counts,
code quality metrics, structure validation, and a summary dashboard.

Skills practiced: dataclasses, typing, logging, argparse subcommands,
pathlib, JSON output, function composition, error handling.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# ── Data models ───────────────────────────────────────────────

@dataclass
class FileMetrics:
    """Metrics for a single file."""
    name: str
    path: str
    lines: int
    blank_lines: int
    comment_lines: int
    code_lines: int
    functions: int
    classes: int


@dataclass
class DirectoryMetrics:
    """Metrics for a directory."""
    name: str
    total_files: int
    total_lines: int
    total_code_lines: int
    total_functions: int
    total_classes: int
    avg_file_size: float
    files: list[FileMetrics] = field(default_factory=list)


@dataclass
class HealthIssue:
    """A potential issue found during health check."""
    severity: str  # "error", "warning", "info"
    category: str
    message: str
    file: str = ""


@dataclass
class HealthReport:
    """Full project health report."""
    project_path: str
    metrics: DirectoryMetrics
    issues: list[HealthIssue] = field(default_factory=list)
    score: int = 100  # 0-100 health score
    grade: str = "A"


# ── File analysis ─────────────────────────────────────────────

def analyse_python_file(path: Path) -> FileMetrics:
    """Analyse a single Python file for metrics."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    blank = sum(1 for l in lines if not l.strip())
    comments = sum(1 for l in lines if l.strip().startswith("#"))
    code = len(lines) - blank - comments

    functions = sum(1 for l in lines if l.strip().startswith("def "))
    classes = sum(1 for l in lines if l.strip().startswith("class "))

    return FileMetrics(
        name=path.name,
        path=str(path),
        lines=len(lines),
        blank_lines=blank,
        comment_lines=comments,
        code_lines=code,
        functions=functions,
        classes=classes,
    )


def analyse_directory(root: Path, pattern: str = "*.py") -> DirectoryMetrics:
    """Analyse all matching files in a directory."""
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    files: list[FileMetrics] = []
    for path in sorted(root.rglob(pattern)):
        if path.is_file():
            try:
                metrics = analyse_python_file(path)
                files.append(metrics)
            except Exception as exc:
                logger.warning("Could not analyse %s: %s", path, exc)

    total_lines = sum(f.lines for f in files)
    total_code = sum(f.code_lines for f in files)
    total_funcs = sum(f.functions for f in files)
    total_classes = sum(f.classes for f in files)

    return DirectoryMetrics(
        name=root.name,
        total_files=len(files),
        total_lines=total_lines,
        total_code_lines=total_code,
        total_functions=total_funcs,
        total_classes=total_classes,
        avg_file_size=round(total_lines / len(files), 1) if files else 0,
        files=files,
    )


# ── Health checks ─────────────────────────────────────────────

def check_large_files(files: list[FileMetrics], max_lines: int = 300) -> list[HealthIssue]:
    """Flag files over the line limit."""
    return [
        HealthIssue("warning", "size", f"{f.name} has {f.lines} lines (limit: {max_lines})", f.name)
        for f in files if f.lines > max_lines
    ]


def check_missing_readme(root: Path) -> list[HealthIssue]:
    """Check for README file."""
    readme_names = ["README.md", "README.txt", "README.rst", "readme.md"]
    for name in readme_names:
        if (root / name).exists():
            return []
    return [HealthIssue("warning", "documentation", "No README file found")]


def check_missing_tests(root: Path) -> list[HealthIssue]:
    """Check for test files."""
    test_files = list(root.rglob("test_*.py")) + list(root.rglob("*_test.py"))
    if not test_files:
        return [HealthIssue("warning", "testing", "No test files found")]
    return []


def check_long_functions(files: list[FileMetrics], max_funcs: int = 20) -> list[HealthIssue]:
    """Flag files with too many functions (likely needs splitting)."""
    return [
        HealthIssue("info", "complexity", f"{f.name} has {f.functions} functions", f.name)
        for f in files if f.functions > max_funcs
    ]


def calculate_score(issues: list[HealthIssue]) -> tuple[int, str]:
    """Calculate health score from issues."""
    score = 100
    for issue in issues:
        if issue.severity == "error":
            score -= 20
        elif issue.severity == "warning":
            score -= 10
        elif issue.severity == "info":
            score -= 2

    score = max(0, min(100, score))

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    return score, grade


# ── Report generation ─────────────────────────────────────────

def generate_report(root: Path) -> HealthReport:
    """Generate a full health report for a project directory."""
    metrics = analyse_directory(root)

    issues: list[HealthIssue] = []
    issues.extend(check_large_files(metrics.files))
    issues.extend(check_missing_readme(root))
    issues.extend(check_missing_tests(root))
    issues.extend(check_long_functions(metrics.files))

    score, grade = calculate_score(issues)

    return HealthReport(
        project_path=str(root),
        metrics=metrics,
        issues=issues,
        score=score,
        grade=grade,
    )


def format_report_text(report: HealthReport) -> str:
    """Format a health report as human-readable text."""
    lines = [
        f"Project Health: {report.metrics.name}",
        f"Score: {report.score}/100 (Grade: {report.grade})",
        "=" * 50,
        f"Files: {report.metrics.total_files}",
        f"Total lines: {report.metrics.total_lines:,}",
        f"Code lines: {report.metrics.total_code_lines:,}",
        f"Functions: {report.metrics.total_functions}",
        f"Classes: {report.metrics.total_classes}",
        f"Avg file size: {report.metrics.avg_file_size:.0f} lines",
    ]

    if report.issues:
        lines.append(f"\nIssues ({len(report.issues)}):")
        for issue in report.issues:
            prefix = f"[{issue.severity.upper():7s}]"
            lines.append(f"  {prefix} {issue.message}")
    else:
        lines.append("\nNo issues found.")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Project health dashboard")

    sub = parser.add_subparsers(dest="command")

    report = sub.add_parser("report", help="Generate health report")
    report.add_argument("directory", help="Project directory to analyse")
    report.add_argument("--json", action="store_true")

    scan = sub.add_parser("scan", help="Scan files and show metrics")
    scan.add_argument("directory", help="Directory to scan")
    scan.add_argument("--pattern", default="*.py")

    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    """Entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "report":
        report = generate_report(Path(args.directory))
        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            print(format_report_text(report))

    elif args.command == "scan":
        metrics = analyse_directory(Path(args.directory), args.pattern)
        for f in metrics.files:
            print(f"{f.lines:>6} lines  {f.functions:>3} funcs  {f.name}")
        print(f"\nTotal: {metrics.total_files} files, {metrics.total_lines:,} lines")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
