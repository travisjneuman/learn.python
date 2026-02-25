"""Level 1 project: Simple Gradebook Engine.

Manage student grades from a CSV file: calculate averages,
assign letter grades, and generate a class report.

Concepts: csv, dictionaries, arithmetic, grade bands, sorting.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def letter_grade(average: float) -> str:
    """Convert a numeric average to a letter grade.

    WHY if/elif chains? -- Grade bands are ranges, not exact values.
    Each condition checks a threshold from highest to lowest.
    """
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def calculate_average(scores: list[float]) -> float:
    """Calculate the arithmetic mean of a list of scores.

    WHY guard against empty? -- Dividing by zero would crash.
    """
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def parse_student_row(row: dict) -> dict:
    """Parse a CSV row into a student record with computed fields.

    Expected columns: student, score1, score2, score3, ...
    Any column starting with 'score' is treated as a grade.
    """
    name = row.get("student", "Unknown").strip()

    scores = []
    for key, value in row.items():
        if key.startswith("score"):
            try:
                scores.append(float(value.strip()))
            except ValueError:
                continue

    avg = calculate_average(scores)

    return {
        "student": name,
        "scores": scores,
        "average": avg,
        "letter_grade": letter_grade(avg),
        "passed": avg >= 60,
    }


def load_gradebook(path: Path) -> list[dict]:
    """Load students and their grades from a CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"Gradebook file not found: {path}")

    students = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(parse_student_row(row))
    return students


def class_summary(students: list[dict]) -> dict:
    """Compute class-wide statistics."""
    if not students:
        return {"total": 0}

    averages = [s["average"] for s in students]
    passed = sum(1 for s in students if s["passed"])

    return {
        "total_students": len(students),
        "class_average": round(sum(averages) / len(averages), 2),
        "highest": max(averages),
        "lowest": min(averages),
        "passed": passed,
        "failed": len(students) - passed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple Gradebook Engine")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    students = load_gradebook(Path(args.input))
    summary = class_summary(students)

    print("=== Gradebook Report ===\n")
    print(f"  {'Student':<20} {'Average':>8} {'Grade':>6} {'Status':>8}")
    print(f"  {'-'*20} {'-'*8} {'-'*6} {'-'*8}")

    for s in sorted(students, key=lambda x: x["average"], reverse=True):
        status = "PASS" if s["passed"] else "FAIL"
        print(f"  {s['student']:<20} {s['average']:>8.2f} {s['letter_grade']:>6} {status:>8}")

    print(f"\n  Class average: {summary['class_average']}")
    print(f"  Passed: {summary['passed']}/{summary['total_students']}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"students": students, "summary": summary}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
