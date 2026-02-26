# Solution: Level 1 / Project 06 - Simple Gradebook Engine

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Simple Gradebook Engine.

Manage student grades from a CSV file: calculate averages,
assign letter grades, and generate a class report.

Concepts: csv, dictionaries, arithmetic, grade bands, sorting.
"""


import argparse
import csv
from pathlib import Path


# WHY letter_grade: Converting numeric averages to letter grades is a
# classic threshold-mapping problem.  Isolating it in its own function
# makes it reusable and easy to test with specific boundary values.
def letter_grade(average: float) -> str:
    """Convert a numeric average to a letter grade.

    WHY if/elif chains? -- Grade bands are ranges, not exact values.
    Each condition checks a threshold from highest to lowest.
    """
    # WHY descending order: Checking 90 first means that a score of 95
    # hits the first condition and returns "A" immediately.  If we
    # checked 60 first, a score of 95 would match the D threshold
    # (>= 60) and return the wrong grade.
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


# WHY calculate_average: Average computation is used in two places
# (individual students and class-wide), so extracting it prevents
# duplicating the sum/len/round logic.
def calculate_average(scores: list[float]) -> float:
    """Calculate the arithmetic mean of a list of scores.

    WHY guard against empty? -- Dividing by zero would crash.
    """
    # WHY return 0.0 for empty: A student with no scores gets an
    # average of 0 rather than crashing.  This is a safe default
    # that downstream code can handle.
    if not scores:
        return 0.0
    # WHY round to 2: Grade averages displayed to teachers should be
    # clean numbers like 87.33, not 87.33333333333333.
    return round(sum(scores) / len(scores), 2)


# WHY parse_student_row: This function bridges CSV data (all strings)
# and the structured student record (with floats and computed fields).
# It handles conversion errors so one bad row does not crash the
# entire gradebook.
def parse_student_row(row: dict) -> dict:
    """Parse a CSV row into a student record with computed fields.

    Expected columns: student, score1, score2, score3, ...
    Any column starting with 'score' is treated as a grade.
    """
    name = row.get("student", "Unknown").strip()

    # WHY iterate keys starting with "score": This is flexible — the
    # CSV can have score1, score2, score3 or score1 through score10,
    # and the code adapts without changes.
    scores = []
    for key, value in row.items():
        if key.startswith("score"):
            try:
                scores.append(float(value.strip()))
            except ValueError:
                # WHY continue: A non-numeric score like "A" is skipped
                # rather than crashing.  The student's average is
                # computed from whichever scores are valid.
                continue

    avg = calculate_average(scores)

    return {
        "student": name,
        "scores": scores,
        "average": avg,
        "letter_grade": letter_grade(avg),
        # WHY passed field: A boolean "passed/failed" flag is easier
        # to count and filter than checking the average each time.
        "passed": avg >= 60,
    }


# WHY load_gradebook: Separates file I/O from grade computation.
# parse_student_row() can be tested with a plain dict, and this
# function handles the filesystem.
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


# WHY class_summary: Teachers need class-wide metrics (average, pass
# rate) in addition to individual grades.  This function computes
# aggregate statistics from the per-student data.
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


# WHY format_report: A formatted plain-text report is easy to read in
# a terminal, paste into an email, or print on paper.  Structured
# output (JSON) is for machines; formatted text is for humans.
def format_report(students: list[dict], summary: dict) -> str:
    """Format the gradebook as a plain-text table report."""
    lines = [
        "GRADEBOOK REPORT",
        "=" * 52,
        # WHY format specifiers: :<20 left-aligns in a 20-char field,
        # :>8 right-aligns in an 8-char field.  This creates neat columns.
        f"  {'Student':<20} {'Average':>8} {'Grade':>6} {'Status':>8}",
        f"  {'-'*20} {'-'*8} {'-'*6} {'-'*8}",
    ]

    # WHY sort by average descending: Showing the best students first
    # is the natural ordering for a grade report.
    for s in sorted(students, key=lambda x: x["average"], reverse=True):
        status = "PASS" if s["passed"] else "FAIL"
        lines.append(f"  {s['student']:<20} {s['average']:>8.2f} {s['letter_grade']:>6} {status:>8}")

    lines.append("")
    lines.append("-" * 52)
    lines.append(f"  Class average: {summary['class_average']}")
    lines.append(f"  Passed: {summary['passed']}/{summary['total_students']}")
    lines.append(f"  Failed: {summary['failed']}/{summary['total_students']}")
    lines.append("=" * 52)

    return "\n".join(lines)


# WHY parse_args: Standard argparse pattern for flexible file paths.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple Gradebook Engine")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/report.txt")
    return parser.parse_args()


# WHY main: Orchestrates the full workflow and keeps the module
# importable for testing.
def main() -> None:
    args = parse_args()
    students = load_gradebook(Path(args.input))
    summary = class_summary(students)

    report = format_report(students, summary)
    print(report)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved to {output_path}")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| If/elif chain with descending thresholds for grades | Order matters: checking highest first ensures 95 gets "A", not "D" (which 95 also satisfies since 95 >= 60) | Dict mapping of ranges — more flexible but harder to read at Level 1 |
| Dynamic score column detection (`key.startswith("score")`) | Works with any number of score columns without code changes | Hardcode column names like `score1, score2, score3` — breaks if the CSV adds `score4` |
| Skip non-numeric scores with `continue` | One bad cell in a row does not crash the entire gradebook; the student's average is computed from valid scores | Raise ValueError — would lose all students after the first bad row |
| Separate `class_summary()` from individual grades | Class-wide stats are a different concern from individual grades; separating them makes each function simpler and independently testable | Compute class stats inside `format_report()` — mixes computation with presentation |

## Alternative approaches

### Approach B: Using a lookup list for grade thresholds

```python
# WHY a list of tuples: This approach makes it easy to add new grade
# bands (like A+, B+) without modifying if/elif logic.  Just add a
# tuple to the list.
GRADE_BANDS = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
    (0, "F"),
]

def letter_grade_lookup(average: float) -> str:
    """Map average to letter grade using a lookup table."""
    for threshold, grade in GRADE_BANDS:
        if average >= threshold:
            return grade
    return "F"
```

**Trade-off:** The lookup-table approach is more data-driven and easier to extend (adding A+/A- is just adding tuples). The if/elif approach is more explicit and easier to read when there are only 5 grades. Use the lookup approach when you have many thresholds or need to load them from configuration.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Student with no scores (just a name) | `calculate_average([])` returns `0.0`; student gets grade "F" and `passed: False` | The empty-list guard in `calculate_average()` prevents ZeroDivisionError |
| Non-numeric score like `"A"` in CSV | `float("A")` raises ValueError, caught by the try/except, score is skipped; average computed from remaining valid scores | The `continue` in the except block handles this gracefully |
| Score above 100 (e.g., extra credit) | `letter_grade(105)` correctly returns "A" because 105 >= 90 | The if/elif chain handles any value; no upper bound check needed for basic grading |
| Empty CSV (headers only) | `load_gradebook()` returns `[]`, `class_summary()` returns `{"total": 0}`, report shows no students | The `if not students` guard in `class_summary()` prevents division by zero |

## Key takeaways

1. **If/elif order matters for threshold checking.** Always check from highest to lowest when mapping values to ranges. If you check `>= 60` before `>= 90`, every passing score would be labeled "D". This is a common bug in range-based logic.
2. **Separating computation from presentation makes code testable.** `calculate_average()` and `letter_grade()` can be tested with simple values; `format_report()` only handles formatting. This separation of concerns is a fundamental software design principle.
3. **This pattern connects to Learning Management Systems (LMS) like Canvas, Blackboard, and Google Classroom.** The same grade computation, threshold mapping, and class statistics you built here exist in every school administration system, just at larger scale.
