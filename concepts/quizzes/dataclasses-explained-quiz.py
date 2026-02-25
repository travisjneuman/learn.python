"""
Quiz: Dataclasses Explained
Review: concepts/dataclasses-explained.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Dataclasses Explained")
    print("  Review: concepts/dataclasses-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1 — basic understanding
    print("Question 1/7: What does the @dataclass decorator do?")
    print()
    print("  a) Makes the class faster")
    print("  b) Automatically generates __init__, __repr__, and __eq__")
    print("  c) Makes all attributes private")
    print("  d) Converts the class to a dictionary")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! @dataclass generates __init__, __repr__,")
        print("and __eq__ from your field definitions.")
    else:
        print("Incorrect. The answer is b).")
        print("@dataclass auto-generates __init__, __repr__, and __eq__")
        print("so you do not have to write them yourself.")
    print()

    # Question 2 — code prediction
    print("Question 2/7: What does this code print?")
    print()
    print("  from dataclasses import dataclass")
    print()
    print("  @dataclass")
    print("  class Point:")
    print("      x: int")
    print("      y: int")
    print()
    print("  p1 = Point(3, 4)")
    print("  p2 = Point(3, 4)")
    print("  print(p1 == p2)")
    print()
    print("  a) True")
    print("  b) False")
    print("  c) Error")
    print("  d) Point(3, 4)")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "a":
        score += 1
        print("Correct! Dataclasses generate __eq__ that compares")
        print("all fields. Both have x=3 and y=4, so they are equal.")
    else:
        print("Incorrect. The answer is a) True.")
        print("Unlike plain classes, dataclasses compare by field values,")
        print("not by identity (memory address).")
    print()

    # Question 3 — mutable defaults
    print("Question 3/7: Why does this code raise an error?")
    print()
    print("  @dataclass")
    print("  class Team:")
    print("      name: str")
    print("      members: list[str] = []")
    print()
    print("  a) list[str] is invalid syntax")
    print("  b) Mutable defaults are forbidden — use field(default_factory=list)")
    print("  c) name must have a default value too")
    print("  d) Dataclasses cannot have list fields")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Mutable defaults like [] would be shared")
        print("between instances. Use field(default_factory=list) instead.")
    else:
        print("Incorrect. The answer is b).")
        print("Use field(default_factory=list) for mutable defaults.")
        print("This ensures each instance gets its own list.")
    print()

    # Question 4 — frozen
    print("Question 4/7: What does frozen=True do?")
    print()
    print("  @dataclass(frozen=True)")
    print("  class Color:")
    print("      r: int")
    print("      g: int")
    print("      b: int")
    print()
    print("  a) Improves performance")
    print("  b) Makes the instance immutable (read-only)")
    print("  c) Prevents creating new instances")
    print("  d) Freezes the class so no subclasses can be created")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! frozen=True makes instances immutable.")
        print("Trying to change a field raises FrozenInstanceError.")
    else:
        print("Incorrect. The answer is b).")
        print("frozen=True prevents modification after creation.")
        print("This also makes instances hashable (usable as dict keys).")
    print()

    # Question 5 — __post_init__
    print("Question 5/7: When does __post_init__ run?")
    print()
    print("  a) Before __init__")
    print("  b) Immediately after __init__ finishes")
    print("  c) When you call it manually")
    print("  d) When the object is garbage collected")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! __post_init__ runs right after the generated")
        print("__init__ sets all field values.")
    else:
        print("Incorrect. The answer is b).")
        print("__post_init__ is called automatically after __init__.")
        print("Use it to compute derived values from the fields.")
    print()

    # Question 6 — field ordering
    print("Question 6/7: Why does this code fail?")
    print()
    print("  @dataclass")
    print("  class User:")
    print('      role: str = "viewer"')
    print("      name: str")
    print()
    print("  a) role cannot have a default value")
    print("  b) Fields without defaults must come before fields with defaults")
    print("  c) Dataclasses cannot have string fields")
    print("  d) name needs a type hint")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Just like function parameters, fields without")
        print("defaults must come before fields with defaults.")
    else:
        print("Incorrect. The answer is b).")
        print("Put required fields (no default) first, then optional")
        print("fields (with defaults). Same rule as function arguments.")
    print()

    # Question 7 — dataclass vs plain class
    print("Question 7/7: When should you prefer a dataclass over")
    print("a plain class?")
    print()
    print("  a) Always — dataclasses are better in every way")
    print("  b) When your class is mainly about storing data")
    print("  c) Only for small classes with fewer than 3 fields")
    print("  d) Only when you need frozen instances")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Dataclasses shine when a class is primarily")
        print("a container for data. Use plain classes for complex behavior.")
    else:
        print("Incorrect. The answer is b).")
        print("Dataclasses are ideal for data containers. Plain classes")
        print("are better when you need complex initialization or behavior.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect score! You understand dataclasses well.")
    elif pct >= 70:
        print("  Good work! Review any questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/dataclasses-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
