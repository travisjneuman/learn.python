"""Tests for Simple Gradebook Engine."""

from project import calculate_average, class_summary, letter_grade, parse_student_row


def test_letter_grade_boundaries() -> None:
    assert letter_grade(95) == "A"
    assert letter_grade(85) == "B"
    assert letter_grade(75) == "C"
    assert letter_grade(65) == "D"
    assert letter_grade(50) == "F"


def test_calculate_average() -> None:
    assert calculate_average([80, 90, 100]) == 90.0
    assert calculate_average([]) == 0.0


def test_parse_student_row() -> None:
    row = {"student": "Alice", "score1": "90", "score2": "80", "score3": "70"}
    result = parse_student_row(row)
    assert result["student"] == "Alice"
    assert result["average"] == 80.0
    assert result["letter_grade"] == "B"
    assert result["passed"] is True


def test_class_summary() -> None:
    students = [
        {"average": 90, "passed": True},
        {"average": 50, "passed": False},
    ]
    summary = class_summary(students)
    assert summary["total_students"] == 2
    assert summary["passed"] == 1
    assert summary["class_average"] == 70.0
