"""
Quiz: Comprehensions Explained
Review: concepts/comprehensions-explained.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Comprehensions Explained")
    print("  Review: concepts/comprehensions-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: What does this list comprehension produce?")
    print()
    print("  [n ** 2 for n in range(1, 6)]")
    print()
    print("  a) [1, 2, 3, 4, 5]")
    print("  b) [1, 4, 9, 16, 25]")
    print("  c) [2, 4, 6, 8, 10]")
    print("  d) [0, 1, 4, 9, 16]")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! range(1, 6) gives 1-5, and squaring each gives")
        print("[1, 4, 9, 16, 25].")
    else:
        print("Incorrect. The answer is b) [1, 4, 9, 16, 25].")
        print("Each number from 1 to 5 is squared.")
    print()

    # Question 2
    print("Question 2/12: Where does the filter condition go in a list")
    print("comprehension?")
    print()
    print("  a) Before the expression: [if x > 5 x for x in items]")
    print("  b) After the for clause: [x for x in items if x > 5]")
    print("  c) Inside the expression: [x(if x > 5) for x in items]")
    print("  d) Before the for clause: [x if x > 5 for x in items]")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The filter goes at the end: [expr for var in iterable if cond].")
    else:
        print("Incorrect. The answer is b).")
        print("Filter conditions go after the for clause.")
    print()

    # Question 3
    print("Question 3/12: What is the syntax for a dictionary comprehension?")
    print()
    print("  a) [key: value for item in iterable]")
    print("  b) {key: value for item in iterable}")
    print("  c) dict(key, value for item in iterable)")
    print("  d) {key, value for item in iterable}")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Dict comprehensions use {key: value for ...}.")
    else:
        print("Incorrect. The answer is b) {key: value for item in iterable}.")
        print("Use curly braces with a colon for dict comprehensions.")
    print()

    # Question 4
    print("Question 4/12: What does {w.lower() for w in words} create?")
    print()
    print("  a) A list")
    print("  b) A dictionary")
    print("  c) A set")
    print("  d) A tuple")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Curly braces without a colon create a set comprehension.")
        print("Duplicates are automatically removed.")
    else:
        print("Incorrect. The answer is c) a set.")
        print("{expr for ...} without a colon is a set comprehension.")
    print()

    # Question 5
    print("Question 5/12: What is the difference between a list comprehension")
    print("and a generator expression?")
    print()
    print("  a) Generator expressions use [] and lists use ()")
    print("  b) List comprehensions use [] and build everything in memory;")
    print("     generator expressions use () and compute lazily")
    print("  c) There is no difference")
    print("  d) Generator expressions are faster at indexing")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! [x for x in items] builds the full list in memory.")
        print("(x for x in items) computes values one at a time.")
    else:
        print("Incorrect. The answer is b).")
        print("Generator expressions use () and are lazy — they compute")
        print("values on demand using almost no memory.")
    print()

    # Question 6
    print("Question 6/12: What is wrong with this code?")
    print()
    print("  [x if x > 5 for x in range(10)]")
    print()
    print("  a) Nothing, it filters values greater than 5")
    print("  b) SyntaxError — if/else before for needs an else clause")
    print("  c) It should use () instead of []")
    print("  d) range(10) is invalid")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! When if/else appears before 'for', it is a conditional")
        print("expression and needs an else. Use [x for x in range(10) if x > 5]")
        print("for filtering.")
    else:
        print("Incorrect. The answer is b) SyntaxError.")
        print("Filter if goes at the end: [x for x in range(10) if x > 5].")
        print("Conditional expression needs else: [x if x > 5 else 0 for x in ...].")
    print()

    # Question 7
    print("Question 7/12: How do you flatten a list of lists?")
    print()
    print("  matrix = [[1, 2], [3, 4], [5, 6]]")
    print()
    print("  a) [num for num in matrix]")
    print("  b) [num for row in matrix for num in row]")
    print("  c) [row for row in matrix for num in row]")
    print("  d) [matrix[row][num] for row, num in matrix]")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The nested comprehension reads like the equivalent")
        print("nested for loops: for row in matrix: for num in row.")
    else:
        print("Incorrect. The answer is b).")
        print("[num for row in matrix for num in row] flattens to [1, 2, 3, 4, 5, 6].")
    print()

    # Question 8
    print("Question 8/12: What does this produce?")
    print()
    print('  ["even" if n % 2 == 0 else "odd" for n in [1, 2, 3]]')
    print()
    print('  a) ["odd", "even", "odd"]')
    print('  b) ["even", "odd", "even"]')
    print("  c) [1, 2, 3]")
    print('  d) ["odd", "odd", "odd"]')
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "a":
        score += 1
        print('Correct! 1 is odd, 2 is even, 3 is odd: ["odd", "even", "odd"].')
    else:
        print('Incorrect. The answer is a) ["odd", "even", "odd"].')
        print("The conditional expression (if/else before for) transforms each value.")
    print()

    # Question 9
    print("Question 9/12: Why is this comprehension bad practice?")
    print()
    print("  [print(x) for x in range(10)]")
    print()
    print("  a) print() is not allowed in comprehensions")
    print("  b) It works but creates a useless list of None values")
    print("  c) It causes a SyntaxError")
    print("  d) It prints nothing")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! print() returns None, so this creates [None, None, ...].")
        print("Use a regular for loop for side effects.")
    else:
        print("Incorrect. The answer is b).")
        print("Comprehensions are for building data, not for side effects.")
        print("Use a for loop when you need print() or other side effects.")
    print()

    # Question 10
    print("Question 10/12: What is an empty set literal in Python?")
    print()
    print("  a) {}")
    print("  b) set()")
    print("  c) ()")
    print("  d) []")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! {} creates an empty dict, not a set.")
        print("Use set() for an empty set.")
    else:
        print("Incorrect. The answer is b) set().")
        print("{} is an empty dict. Python has no literal syntax for empty sets.")
    print()

    # Question 11
    print("Question 11/12: What does the walrus operator := do in a")
    print("comprehension?")
    print()
    print("  [(w, length) for w in data if (length := len(w)) > 2]")
    print()
    print("  a) Checks equality")
    print("  b) Assigns a value and uses it in the same expression")
    print("  c) Creates a new variable in the outer scope")
    print("  d) It is not valid syntax")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! := assigns len(w) to 'length' and uses it in both")
        print("the filter and the output expression, avoiding computing len() twice.")
    else:
        print("Incorrect. The answer is b).")
        print("The walrus operator := lets you assign and use a value in")
        print("the same expression, avoiding redundant computation.")
    print()

    # Question 12
    print("Question 12/12: When should you use a regular for loop instead")
    print("of a comprehension?")
    print()
    print("  a) When building a list from another list")
    print("  b) When you need side effects, complex logic, or readability suffers")
    print("  c) Never — comprehensions are always better")
    print("  d) When the iterable is a range")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Use loops for side effects (print, write files),")
        print("complex logic, or when the comprehension is hard to read.")
    else:
        print("Incorrect. The answer is b).")
        print("Comprehensions are for building data. Loops are better for")
        print("side effects and complex logic.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You have mastered comprehensions.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/comprehensions-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
