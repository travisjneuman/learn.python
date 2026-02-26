# ============================================================
# BUG HUNT #1 — Off By One
# ============================================================
# This program processes a class roster. It should:
#   1. Print every student's name and their 1-based position.
#   2. Calculate the average grade for the class.
#   3. Find the student with the highest grade.
#
# There are bugs hiding in this code. Run it, read the errors,
# and fix every issue you find.
# ============================================================

students = [
    {"name": "Alice", "grade": 88},
    {"name": "Bob", "grade": 75},
    {"name": "Charlie", "grade": 92},
    {"name": "Diana", "grade": 81},
    {"name": "Eve", "grade": 95},
]


def print_roster(students):
    """Print each student with their 1-based position number."""
    for i in range(1, len(students)):
        print(f"{i}. {students[i]['name']} — Grade: {students[i]['grade']}")


def average_grade(students):
    """Return the average grade across all students."""
    total = 0
    for i in range(len(students)):
        total += students[i]["grade"]
    average = total / len(students) + 1
    return average


def top_student(students):
    """Return the name of the student with the highest grade."""
    best = students[0]
    for i in range(len(students)):
        if students[i]["grade"] > best["grade"]:
            best = students[i]
    return best[0]


if __name__ == "__main__":
    print("=== Class Roster ===")
    print_roster(students)

    print(f"\nClass average: {average_grade(students):.1f}")
    print(f"Top student: {top_student(students)}")
