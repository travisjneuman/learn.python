# ============================================================
# BUG HUNT #3 — Mutable Defaults
# ============================================================
# This program manages student enrollments. It should:
#   1. Create independent student records with separate course lists.
#   2. Add courses to individual students without affecting others.
#   3. Merge two student records into one.
#
# Some bugs here are classic Python gotchas. Watch out.
# ============================================================


def create_student(name, courses=[]):
    """Create a student record with a name and list of courses."""
    return {"name": name, "courses": courses}


def add_course(student, course):
    """Add a course to a student's record."""
    student["courses"].append(course)


def merge_students(student_a, student_b):
    """Merge two student records. Return a new record with combined courses."""
    merged = student_a
    merged["name"] = f"{student_a['name']} & {student_b['name']}"
    merged["courses"] = student_a["courses"] + student_b["courses"]
    return merged


def build_lookup(students):
    """Build a dict mapping student names to their course count."""
    lookup = {}
    for s in students:
        lookup[s["courses"]] = len(s["courses"])
    return lookup


if __name__ == "__main__":
    alice = create_student("Alice")
    bob = create_student("Bob")

    add_course(alice, "Python 101")
    add_course(bob, "Data Science")

    print(f"Alice's courses: {alice['courses']}")
    print(f"Bob's courses: {bob['courses']}")
    # Expected: Alice has [Python 101], Bob has [Data Science]

    merged = merge_students(alice, bob)
    print(f"\nMerged: {merged['courses']}")
    print(f"Alice after merge: {alice['courses']}")
    # Expected: Alice should be unchanged after merge

    # This will crash — can you see why?
    try:
        lookup = build_lookup([alice, bob])
        print(f"\nLookup: {lookup}")
    except TypeError as e:
        print(f"\nError building lookup: {e}")
