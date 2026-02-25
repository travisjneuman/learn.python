"""
Quiz: Match/Case Explained
Review: concepts/match-case-explained.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Match/Case Explained")
    print("  Review: concepts/match-case-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1 — basic understanding
    print("Question 1/7: What Python version introduced match/case?")
    print()
    print("  a) Python 3.8")
    print("  b) Python 3.9")
    print("  c) Python 3.10")
    print("  d) Python 3.12")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Structural pattern matching was introduced")
        print("in Python 3.10 (PEP 634).")
    else:
        print("Incorrect. The answer is c) Python 3.10.")
        print("match/case is available from Python 3.10 onward.")
    print()

    # Question 2 — wildcard pattern
    print("Question 2/7: What does case _: do in a match statement?")
    print()
    print("  a) Matches only the underscore character")
    print("  b) Matches anything (like 'else' in if/elif)")
    print("  c) Raises an error")
    print("  d) Skips the current iteration")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The underscore _ is a wildcard pattern.")
        print("It matches anything, like a catch-all 'else' branch.")
    else:
        print("Incorrect. The answer is b).")
        print("case _: is the wildcard — it matches any value,")
        print("similar to the 'else' clause in if/elif/else.")
    print()

    # Question 3 — OR patterns
    print("Question 3/7: How do you match multiple values in one case?")
    print()
    print("  a) case 'a' and 'b':")
    print("  b) case 'a', 'b':")
    print("  c) case 'a' | 'b':")
    print("  d) case 'a' or 'b':")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! The pipe | operator combines patterns.")
        print("case 'a' | 'b': matches either 'a' or 'b'.")
    else:
        print("Incorrect. The answer is c) case 'a' | 'b':")
        print("Use the | operator to create OR patterns.")
    print()

    # Question 4 — capture pattern
    print("Question 4/7: What does x capture in this pattern?")
    print()
    print("  match point:")
    print("      case (x, 0):")
    print("          print(f'On x-axis at {x}')")
    print()
    print("  a) The literal character 'x'")
    print("  b) The first element of the tuple")
    print("  c) The entire tuple")
    print("  d) Nothing — x must be defined beforehand")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! x captures the first element of the tuple.")
        print("The pattern matches any tuple where the second element is 0.")
    else:
        print("Incorrect. The answer is b).")
        print("Bare names in patterns are capture variables. x gets")
        print("the value of the first tuple element.")
    print()

    # Question 5 — guard clause
    print("Question 5/7: What is the guard clause in this pattern?")
    print()
    print("  match age:")
    print("      case n if n < 0:")
    print("          print('Invalid')")
    print()
    print("  a) case n")
    print("  b) if n < 0")
    print("  c) print('Invalid')")
    print("  d) match age")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The 'if n < 0' part is the guard clause.")
        print("It adds an extra condition to the pattern match.")
    else:
        print("Incorrect. The answer is b) if n < 0.")
        print("A guard clause adds a condition after the pattern.")
        print("The case only matches if both the pattern and guard are true.")
    print()

    # Question 6 — variable name trap
    print("Question 6/7: What is wrong with this code?")
    print()
    print("  STATUS_OK = 200")
    print()
    print("  match code:")
    print("      case STATUS_OK:")
    print("          print('OK')")
    print()
    print("  a) Nothing — it correctly matches code == 200")
    print("  b) STATUS_OK becomes a capture variable, not a comparison")
    print("  c) Constants cannot be used in match statements")
    print("  d) case needs parentheses around STATUS_OK")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Bare names in patterns are capture variables.")
        print("STATUS_OK captures the value of code instead of comparing.")
        print("Use a literal (case 200:) or dotted name instead.")
    else:
        print("Incorrect. The answer is b).")
        print("Bare names are ALWAYS capture variables in patterns.")
        print("To match a constant, use the literal value: case 200:")
    print()

    # Question 7 — when to use
    print("Question 7/7: When is match/case most useful?")
    print()
    print("  a) For all conditional logic — always use it instead of if/elif")
    print("  b) For matching the structure and shape of data")
    print("  c) Only for matching strings")
    print("  d) Only when you have exactly two possible cases")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! match/case excels at structural pattern matching —")
        print("matching the shape of tuples, dicts, and class instances.")
    else:
        print("Incorrect. The answer is b).")
        print("match/case is designed for structural matching. For simple")
        print("value comparisons, if/elif is often clearer.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect score! You understand match/case well.")
    elif pct >= 70:
        print("  Good work! Review any questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/match-case-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
