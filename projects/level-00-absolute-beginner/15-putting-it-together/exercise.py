"""Learn to combine variables, functions, files, and loops into a complete program."""
# ============================================================
# Exercise 15: Putting It Together
# ============================================================
#
# This exercise combines everything from Exercises 01-14:
# - Variables and strings
# - User input
# - Conditions (if/else)
# - Lists and dictionaries
# - Loops
# - Functions
# - File reading
#
# It is a small but complete program: a student grade reporter.
#
# RUN THIS: python exercise.py
# ============================================================


def load_students(filename):
    """Read student data from a file and return a list of dictionaries."""
    students = []

    for line in open(filename):
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")
        name = parts[0]
        score = int(parts[1])

        # Each student is a dictionary with name and score
        student = {"name": name, "score": score}
        students.append(student)

    return students


def get_letter_grade(score):
    """Convert a numeric score to a letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def calculate_average(students):
    """Calculate the average score from a list of student dicts."""
    total = 0
    for student in students:
        total = total + student["score"]
    return total / len(students)


def print_report(students):
    """Print a formatted grade report for all students."""
    print("=" * 40)
    print("       STUDENT GRADE REPORT")
    print("=" * 40)
    print()

    for student in students:
        name = student["name"]
        score = student["score"]
        grade = get_letter_grade(score)
        print(f"  {name:<10} {score:>3}  ({grade})")

    print()
    print("-" * 40)

    average = calculate_average(students)
    print(f"  Class Average: {average:.1f}")
    print(f"  Highest: {max(s['score'] for s in students)}")
    print(f"  Lowest:  {min(s['score'] for s in students)}")
    print(f"  Students: {len(students)}")
    print("=" * 40)


# ---- Main program starts here ----

# Load data from file (reusing sample data from Exercise 14)
students = load_students("../14-reading-files/data/sample.txt")

# Print the report
print_report(students)

# Ask the user if they want to look up a specific student
print()
lookup = input("Look up a student by name (or press Enter to skip): ")

if lookup:
    found = False
    for student in students:
        if student["name"].lower() == lookup.lower():
            grade = get_letter_grade(student["score"])
            print(f"\n{student['name']} scored {student['score']} ({grade})")
            found = True

    if not found:
        print(f"\nNo student named '{lookup}' found.")

print("\nDone!")

# ============================================================
# WHAT YOU JUST BUILT:
#
# A program that reads data from a file, processes it, formats
# a report, and responds to user input. This is the foundation
# of every data processing tool you will build from here on.
#
# If you understood this exercise, you are ready for Level 0.
# ============================================================
