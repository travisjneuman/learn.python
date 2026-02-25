"""
Quiz: Type Hints Explained
Review: concepts/type-hints-explained.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Type Hints Explained")
    print("  Review: concepts/type-hints-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1 — basic understanding
    print("Question 1/7: What do type hints do at runtime?")
    print()
    print("  a) They make Python reject wrong types with an error")
    print("  b) They speed up code by telling Python the type")
    print("  c) Nothing — Python ignores them at runtime")
    print("  d) They convert values to the specified type")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Type hints are for humans and tools (editors,")
        print("mypy). Python itself ignores them when running code.")
    else:
        print("Incorrect. The answer is c).")
        print("Python ignores type hints at runtime. They help editors")
        print("and type checkers catch mistakes before you run the code.")
    print()

    # Question 2 — function annotation syntax
    print("Question 2/7: What does -> str mean in this function?")
    print()
    print("  def greet(name: str) -> str:")
    print('      return f"Hello, {name}"')
    print()
    print("  a) The function takes a string argument")
    print("  b) The function returns a string")
    print("  c) The function converts the result to a string")
    print("  d) The function prints a string")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The -> str annotation says this function")
        print("returns a string value.")
    else:
        print("Incorrect. The answer is b).")
        print("-> str is the return type annotation. name: str is the")
        print("parameter annotation.")
    print()

    # Question 3 — collection types
    print("Question 3/7: How do you annotate a list of integers?")
    print()
    print("  a) list(int)")
    print("  b) List[int]")
    print("  c) list[int]")
    print("  d) Both b and c work")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "d":
        score += 1
        print("Correct! list[int] works in Python 3.9+. List[int]")
        print("(from typing) works in older versions too.")
    else:
        print("Incorrect. The answer is d).")
        print("list[int] (lowercase) works in 3.9+. List[int] (from")
        print("typing import List) works in all Python 3 versions.")
    print()

    # Question 4 — Optional
    print("Question 4/7: What does Optional[str] mean?")
    print()
    print("  a) The parameter is optional and can be omitted")
    print("  b) The value can be a string or None")
    print("  c) The string might be empty")
    print("  d) The value defaults to an empty string")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Optional[str] means str | None — the value")
        print("is either a string or None.")
    else:
        print("Incorrect. The answer is b).")
        print("Optional[str] is shorthand for str | None. It means")
        print("the value could be a string or could be None.")
    print()

    # Question 5 — code prediction
    print("Question 5/7: What is wrong with this code?")
    print()
    print("  def find_user(name: str) -> Optional[dict]:")
    print("      user = database.get(name)")
    print("      return user")
    print()
    print("  result = find_user('Alice')")
    print("  print(result['email'])")
    print()
    print("  a) Nothing is wrong")
    print("  b) result might be None, causing a TypeError on ['email']")
    print("  c) Optional[dict] is invalid syntax")
    print("  d) find_user should return a string, not a dict")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Since the function returns Optional[dict],")
        print("result could be None. You must check before accessing keys.")
    else:
        print("Incorrect. The answer is b).")
        print("Optional[dict] means the function might return None.")
        print("Accessing ['email'] on None would crash.")
    print()

    # Question 6 — Union types
    print("Question 6/7: In Python 3.10+, how do you say a value")
    print("can be a string or an integer?")
    print()
    print("  a) str & int")
    print("  b) str + int")
    print("  c) str | int")
    print("  d) str, int")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! The | operator creates a union type.")
        print("str | int means 'either a string or an integer.'")
    else:
        print("Incorrect. The answer is c) str | int.")
        print("The pipe operator | creates union types in Python 3.10+.")
    print()

    # Question 7 — Protocol
    print("Question 7/7: What is a Protocol in Python typing?")
    print()
    print("  a) A network communication standard")
    print("  b) A way to define required methods without inheritance")
    print("  c) A special base class all classes must inherit from")
    print("  d) A way to enforce type hints at runtime")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! A Protocol defines what methods an object must")
        print("have. Any class with those methods matches, no inheritance needed.")
    else:
        print("Incorrect. The answer is b).")
        print("Protocol is structural typing — it checks that an object")
        print("has the right methods, regardless of its class hierarchy.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect score! You understand Python type hints well.")
    elif pct >= 70:
        print("  Good work! Review any questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/type-hints-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
