"""
Quiz: Types and Conversions
Review: concepts/types-and-conversions.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Types and Conversions")
    print("  Review: concepts/types-and-conversions.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print('Question 1/7: What is the type of "42" (with quotes)?')
    print()
    print("  a) int")
    print("  b) float")
    print("  c) str")
    print("  d) bool")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Anything in quotes is a string, even if it")
        print("looks like a number.")
    else:
        print("Incorrect. The answer is c) str.")
        print('Quotes make it a string. "42" is text, not a number.')
    print()

    # Question 2
    print("Question 2/7: What does input() always return?")
    print()
    print("  a) An integer")
    print("  b) Whatever type the user types")
    print("  c) A string")
    print("  d) None")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! input() always returns a string.")
        print("You must convert it with int() or float() for math.")
    else:
        print("Incorrect. The answer is c) a string.")
        print("Even if the user types 42, input() returns '42' as text.")
    print()

    # Question 3
    print('Question 3/7: What does "5" == 5 evaluate to?')
    print()
    print("  a) True")
    print("  b) False")
    print("  c) Error")
    print('  d) "5"')
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! A string and an integer are never equal in Python,")
        print("even if they look the same.")
    else:
        print("Incorrect. The answer is b) False.")
        print('The string "5" and the integer 5 are different types.')
    print()

    # Question 4
    print("Question 4/7: Which of these values is 'falsy' in Python?")
    print()
    print('  a) "hello"')
    print("  b) 1")
    print("  c) [1, 2, 3]")
    print("  d) 0")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "d":
        score += 1
        print("Correct! 0 is falsy. Other falsy values include: False,")
        print('None, "", [], and {}.')
    else:
        print("Incorrect. The answer is d) 0.")
        print("Zero, empty strings, empty collections, None, and False")
        print("are all falsy.")
    print()

    # Question 5
    print('Question 5/7: What does int("3.14") produce?')
    print()
    print("  a) 3")
    print("  b) 3.14")
    print("  c) ValueError")
    print('  d) "3"')
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! int() cannot convert a float-format string directly.")
        print("You would need int(float('3.14')) to get 3.")
    else:
        print("Incorrect. The answer is c) ValueError.")
        print("int() cannot parse a decimal string. Use float() first,")
        print("then int().")
    print()

    # Question 6
    print("Question 6/7: What does bool([]) return?")
    print()
    print("  a) True")
    print("  b) False")
    print("  c) None")
    print("  d) Error")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! An empty list is falsy. bool([]) returns False.")
        print("A non-empty list like [1] would return True.")
    else:
        print("Incorrect. The answer is b) False.")
        print("Empty collections are falsy in Python.")
    print()

    # Question 7
    print("Question 7/7: What will this code print?")
    print()
    print("  x = 10")
    print("  y = 3")
    print("  print(type(x / y))")
    print()
    print("  a) <class 'int'>")
    print("  b) <class 'float'>")
    print("  c) <class 'str'>")
    print("  d) Error")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Division with / always returns a float in Python,")
        print("even when dividing two integers. Use // for integer division.")
    else:
        print("Incorrect. The answer is b) <class 'float'>.")
        print("The / operator always produces a float. 10 / 3 = 3.333...")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand Python types and conversions.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/types-and-conversions.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
