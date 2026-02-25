"""
Quiz: What is a Variable?
Review: concepts/what-is-a-variable.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: What is a Variable?")
    print("  Review: concepts/what-is-a-variable.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1 — multiple choice
    print("Question 1/7: Which of these is a valid Python variable name?")
    print()
    print("  a) 2nd_place")
    print("  b) second-place")
    print("  c) second_place")
    print("  d) second place")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Variable names can contain letters, numbers, and")
        print("underscores, but must start with a letter or underscore.")
    else:
        print("Incorrect. The answer is c) second_place.")
        print("Names must start with a letter or underscore. No hyphens or spaces.")
    print()

    # Question 2 — code prediction
    print("Question 2/7: What will this code print?")
    print()
    print('  name = "Alice"')
    print('  name = "Bob"')
    print("  print(name)")
    print()
    print("  a) Alice")
    print("  b) Bob")
    print("  c) AliceBob")
    print("  d) Error")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Assigning a new value replaces the old one.")
        print("The variable now holds 'Bob'.")
    else:
        print("Incorrect. The answer is b) Bob.")
        print("The second assignment replaces 'Alice' with 'Bob'.")
    print()

    # Question 3 — understanding = vs ==
    print("Question 3/7: What is the difference between = and == in Python?")
    print()
    print("  a) They do the same thing")
    print("  b) = assigns a value, == checks equality")
    print("  c) = checks equality, == assigns a value")
    print("  d) == is used for strings, = is used for numbers")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! x = 5 stores 5 in x. x == 5 checks if x equals 5.")
    else:
        print("Incorrect. The answer is b).")
        print("= is assignment (store a value). == is comparison (check equality).")
    print()

    # Question 4 — case sensitivity
    print("Question 4/7: Are 'Score' and 'score' the same variable in Python?")
    print()
    print("  a) Yes, Python ignores case")
    print("  b) No, Python is case-sensitive")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Python is case-sensitive. Score and score are")
        print("two completely different variables.")
    else:
        print("Incorrect. The answer is b).")
        print("Python treats uppercase and lowercase letters as different.")
    print()

    # Question 5 — code prediction
    print("Question 5/7: What happens when you run this code?")
    print()
    print("  print(score)")
    print("  score = 100")
    print()
    print("  a) Prints 100")
    print("  b) Prints None")
    print("  c) NameError — score is not defined yet")
    print("  d) Prints 0")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! You cannot use a variable before creating it.")
        print("Python reads top to bottom, so score does not exist at line 1.")
    else:
        print("Incorrect. The answer is c) NameError.")
        print("The variable must be created before it is used.")
    print()

    # Question 6 — naming convention
    print("Question 6/7: What naming convention does Python recommend")
    print("for variables?")
    print()
    print("  a) camelCase (studentCount)")
    print("  b) PascalCase (StudentCount)")
    print("  c) snake_case (student_count)")
    print("  d) UPPER_CASE (STUDENT_COUNT)")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Python convention is snake_case for variables:")
        print("lowercase_with_underscores.")
    else:
        print("Incorrect. The answer is c) snake_case.")
        print("Python uses lowercase_with_underscores for variable names.")
    print()

    # Question 7 — short answer
    print("Question 7/7: What will this code print?")
    print()
    print("  age = 25")
    print("  next_year = age + 1")
    print("  print(next_year)")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "26":
        score += 1
        print("Correct! age holds 25, so age + 1 is 26, which gets")
        print("stored in next_year.")
    else:
        print("Incorrect. The answer is 26.")
        print("age is 25, and 25 + 1 = 26.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect score! You have a solid grasp of variables.")
    elif pct >= 70:
        print("  Good work! Review any questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/what-is-a-variable.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
