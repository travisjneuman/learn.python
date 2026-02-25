"""
Quiz: How Imports Work
Review: concepts/how-imports-work.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: How Imports Work")
    print("  Review: concepts/how-imports-work.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print("Question 1/7: What is the difference between these two imports?")
    print()
    print("  import math")
    print("  from math import sqrt")
    print()
    print("  a) They do the same thing")
    print("  b) The first imports the whole module (use math.sqrt);")
    print("     the second imports just sqrt (use sqrt directly)")
    print("  c) The second is faster")
    print("  d) The first only works on Linux")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! 'import math' requires the math. prefix.")
        print("'from math import sqrt' lets you use sqrt() directly.")
    else:
        print("Incorrect. The answer is b).")
        print("import math -> math.sqrt(16)")
        print("from math import sqrt -> sqrt(16)")
    print()

    # Question 2
    print("Question 2/7: What file makes a folder into a Python package?")
    print()
    print("  a) main.py")
    print("  b) __init__.py")
    print("  c) setup.py")
    print("  d) package.json")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! __init__.py tells Python that the folder is a")
        print("package that can be imported.")
    else:
        print("Incorrect. The answer is b) __init__.py.")
        print("This file (even if empty) marks a folder as a Python package.")
    print()

    # Question 3
    print("Question 3/7: Why is 'from math import *' discouraged?")
    print()
    print("  a) It is slower")
    print("  b) It makes it hard to track where names came from")
    print("     and can overwrite existing names")
    print("  c) It does not work")
    print("  d) It only imports one function")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Star imports pollute your namespace.")
        print("You cannot tell where a function came from, and names")
        print("can silently overwrite each other.")
    else:
        print("Incorrect. The answer is b).")
        print("import * brings in everything, which makes your code")
        print("harder to understand and debug.")
    print()

    # Question 4
    print("Question 4/7: You name your file 'random.py' and then run")
    print("'import random'. What happens?")
    print()
    print("  a) Python imports the built-in random module")
    print("  b) Python imports YOUR random.py instead of the built-in")
    print("  c) Python imports both")
    print("  d) Error — duplicate names are not allowed")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Python searches the current directory first.")
        print("Your file shadows the built-in module. Rename your file.")
    else:
        print("Incorrect. The answer is b).")
        print("Python looks in the current directory before the standard")
        print("library, so your file takes priority.")
    print()

    # Question 5
    print("Question 5/7: What does 'import pandas as pd' do?")
    print()
    print("  a) Renames the pandas library permanently")
    print("  b) Creates an alias so you can write pd instead of pandas")
    print("  c) Installs pandas")
    print("  d) Imports only the 'pd' function from pandas")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! 'as pd' creates a shorter alias for the module.")
        print("You use pd.DataFrame() instead of pandas.DataFrame().")
    else:
        print("Incorrect. The answer is b).")
        print("The 'as' keyword creates an alias for convenience.")
    print()

    # Question 6
    print("Question 6/7: What is a circular import?")
    print()
    print("  a) Importing a module more than once")
    print("  b) Two files that import from each other, creating a loop")
    print("  c) Importing a module inside a loop")
    print("  d) Using import inside a function")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! When file_a imports file_b and file_b imports")
        print("file_a, Python gets stuck in a loop.")
    else:
        print("Incorrect. The answer is b).")
        print("Circular imports happen when two modules depend on each")
        print("other. Fix by restructuring or moving imports into functions.")
    print()

    # Question 7
    print("Question 7/7: In what order does Python search for modules?")
    print()
    print("  a) Standard library, installed packages, current directory")
    print("  b) Current directory, installed packages, standard library")
    print("  c) Installed packages, current directory, standard library")
    print("  d) Alphabetical order")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Python checks the current directory first,")
        print("then installed packages, then the standard library.")
    else:
        print("Incorrect. The answer is b).")
        print("Current directory comes first, which is why naming your")
        print("file after a standard module causes problems.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand Python's import system.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/how-imports-work.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
