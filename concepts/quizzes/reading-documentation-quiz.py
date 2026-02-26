"""
Quiz: Reading Documentation
Review: concepts/reading-documentation.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Reading Documentation")
    print("  Review: concepts/reading-documentation.md")
    print("=" * 60)
    print()

    score = 0
    total = 10

    # Question 1
    print("Question 1/10: Which section of the Python docs will you use")
    print("most often?")
    print()
    print("  a) The Tutorial")
    print("  b) The Library Reference")
    print("  c) The Language Reference")
    print("  d) The FAQ")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The Library Reference documents every module in the")
        print("standard library — functions, classes, and their parameters.")
    else:
        print("Incorrect. The answer is b) The Library Reference.")
        print("It is the go-to resource for looking up specific functions.")
    print()

    # Question 2
    print("Question 2/10: In the signature str.split(sep=None, maxsplit=-1),")
    print("what does sep=None mean?")
    print()
    print("  a) sep is required")
    print("  b) sep defaults to None (splits on whitespace)")
    print("  c) sep must be None")
    print("  d) sep is not used")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! sep=None means the parameter is optional and defaults")
        print("to None, which splits on any whitespace.")
    else:
        print("Incorrect. The answer is b).")
        print("Default values (like =None) mean the parameter is optional.")
    print()

    # Question 3
    print("Question 3/10: What does -> Any mean in a function signature?")
    print()
    print("  json.loads(s: str) -> Any")
    print()
    print("  a) The function accepts any type")
    print("  b) The function returns a value of type Any (varies)")
    print("  c) The function has no return value")
    print("  d) The function raises any exception")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! -> indicates the return type. Any means the return")
        print("type depends on the input (could be dict, list, str, etc.).")
    else:
        print("Incorrect. The answer is b).")
        print("The -> annotation shows the return type of the function.")
    print()

    # Question 4
    print("Question 4/10: What does the * in a function signature mean?")
    print()
    print("  json.loads(s, *, cls=None, ...)")
    print()
    print("  a) The function accepts *args")
    print("  b) Everything after * must be passed as keyword arguments")
    print("  c) The parameter is required")
    print("  d) The function is deprecated")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! A bare * means all following parameters are")
        print("keyword-only. You must use cls=MyClass, not just pass MyClass.")
    else:
        print("Incorrect. The answer is b).")
        print("Parameters after * must be passed by name (keyword-only).")
    print()

    # Question 5
    print("Question 5/10: What Python built-in function shows documentation")
    print("in the REPL?")
    print()
    print("  a) docs()")
    print("  b) help()")
    print("  c) info()")
    print("  d) man()")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! help(str.split) shows the docstring right in your")
        print("terminal. Use dir(obj) to list all available methods.")
    else:
        print("Incorrect. The answer is b) help().")
        print("help(function) shows its documentation in the REPL.")
    print()

    # Question 6
    print("Question 6/10: What does dir(str) show?")
    print()
    print("  a) The directory where str is defined")
    print("  b) A list of all attributes and methods available on str objects")
    print("  c) The source code of the str class")
    print("  d) Documentation for str")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! dir() lists all attributes and methods. Use it to")
        print("discover what you can do with an object, then use help() to")
        print("learn about specific methods.")
    else:
        print("Incorrect. The answer is b).")
        print("dir() shows available methods. help() shows details for each.")
    print()

    # Question 7
    print("Question 7/10: What type annotation means 'a string or None'?")
    print()
    print("  a) str[]")
    print("  b) str | None (or Optional[str])")
    print("  c) str?")
    print("  d) Nullable[str]")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! str | None (Python 3.10+) and Optional[str] both")
        print("mean the value can be a string or None.")
    else:
        print("Incorrect. The answer is b) str | None or Optional[str].")
    print()

    # Question 8
    print("Question 8/10: Why is it important to read the 'Raises' section")
    print("of a function's documentation?")
    print()
    print("  a) It tells you how to format your code")
    print("  b) It tells you which exceptions the function can raise,")
    print("     so you know what errors to handle")
    print("  c) It lists deprecated features")
    print("  d) It shows performance benchmarks")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The Raises section tells you what can go wrong.")
        print("For example, str.index() raises ValueError when not found.")
    else:
        print("Incorrect. The answer is b).")
        print("Knowing which exceptions a function raises helps you write")
        print("proper error handling.")
    print()

    # Question 9
    print("Question 9/10: Where do you find documentation for third-party")
    print("packages like requests or FastAPI?")
    print()
    print("  a) docs.python.org")
    print("  b) Each package has its own documentation site")
    print("  c) The Python FAQ")
    print("  d) The Language Reference")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Third-party packages have their own docs sites.")
        print("requests -> docs.python-requests.org, FastAPI -> fastapi.tiangolo.com, etc.")
    else:
        print("Incorrect. The answer is b).")
        print("docs.python.org covers the standard library only.")
        print("Third-party packages maintain their own documentation.")
    print()

    # Question 10
    print("Question 10/10: What is the best strategy for reading a module")
    print("documentation page?")
    print()
    print("  a) Read the entire page from top to bottom")
    print("  b) Read the module description, scan the function list, then")
    print("     read the specific function you need")
    print("  c) Only read the examples section")
    print("  d) Skip to the FAQ at the bottom")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Start with the overview, scan for what you need,")
        print("then read that specific entry. Do not try to read everything.")
    else:
        print("Incorrect. The answer is b).")
        print("Read strategically: overview -> scan -> targeted reading.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You know how to navigate Python documentation.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/reading-documentation.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
