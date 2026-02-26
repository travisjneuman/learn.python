"""
Quiz: Debugging Methodology
Review: concepts/debugging-methodology.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Debugging Methodology")
    print("  Review: concepts/debugging-methodology.md")
    print("=" * 60)
    print()

    score = 0
    total = 11

    # Question 1
    print("Question 1/11: What is the first step of the 7-step debugging")
    print("method?")
    print()
    print("  a) Fix the bug")
    print("  b) Reproduce — make the bug happen reliably")
    print("  c) Hypothesize — guess what is wrong")
    print("  d) Read the error message")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! You must be able to reproduce the bug reliably before")
        print("you can verify you have fixed it.")
    else:
        print("Incorrect. The answer is b) Reproduce.")
        print("If you cannot reproduce the bug, you cannot verify the fix.")
    print()

    # Question 2
    print("Question 2/11: What is the 'binary search' method for isolating")
    print("a bug?")
    print()
    print("  a) Search for the error message on Google")
    print("  b) Add a print halfway through, check if data is correct,")
    print("     then repeat in the half that has the bug")
    print("  c) Delete half the code and see if the bug goes away")
    print("  d) Run the program twice and compare output")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Add prints at the midpoint to narrow down which half")
        print("of the code contains the bug, then repeat.")
    else:
        print("Incorrect. The answer is b).")
        print("Binary search narrows the bug's location by checking if data")
        print("is correct at the midpoint, halving the search space each time.")
    print()

    # Question 3
    print("Question 3/11: Why should you NOT start changing code randomly")
    print("when you find a bug?")
    print()
    print("  a) It is slower than rewriting everything")
    print("  b) Random changes waste time and can introduce new bugs")
    print("  c) Python does not allow it")
    print("  d) The linter will catch it anyway")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Always form a hypothesis first. Random changes can")
        print("introduce new bugs and obscure the original problem.")
    else:
        print("Incorrect. The answer is b).")
        print("Methodical debugging (hypothesize, test, fix) is far more")
        print("effective than random changes.")
    print()

    # Question 4
    print("Question 4/11: What does the f-string = shorthand do?")
    print()
    print("  x = 42")
    print("  print(f'{x=}')")
    print()
    print("  a) Prints '42'")
    print("  b) Prints 'x=42'")
    print("  c) Prints 'x'")
    print("  d) Raises a SyntaxError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! f'{x=}' prints both the variable name and its value.")
        print("Very useful for quick debug output.")
    else:
        print("Incorrect. The answer is b) 'x=42'.")
        print("The = inside an f-string shows the expression and its value.")
    print()

    # Question 5
    print("Question 5/11: What does breakpoint() do?")
    print()
    print("  a) Stops the program permanently")
    print("  b) Pauses execution and opens an interactive debugger (pdb)")
    print("  c) Prints the current line number")
    print("  d) Creates a code comment")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! breakpoint() pauses execution and drops you into")
        print("pdb where you can inspect variables and step through code.")
    else:
        print("Incorrect. The answer is b).")
        print("breakpoint() opens the Python debugger at that line.")
    print()

    # Question 6
    print("Question 6/11: In pdb, what does the 'n' command do?")
    print()
    print("  a) Print a variable's value")
    print("  b) Execute the next line of code")
    print("  c) Quit the debugger")
    print("  d) Step into a function call")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! 'n' (next) executes the current line and moves to")
        print("the next one. Use 's' (step) to go inside function calls.")
    else:
        print("Incorrect. The answer is b) execute the next line.")
        print("'n' = next line, 's' = step into, 'c' = continue, 'p' = print.")
    print()

    # Question 7
    print("Question 7/11: When you see a TypeError, what should you check?")
    print()
    print("  a) The file encoding")
    print("  b) The types of all arguments being passed")
    print("  c) The network connection")
    print("  d) The Python version")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! TypeError usually means you passed the wrong type.")
        print("Print type(x) for each argument to find the mismatch.")
    else:
        print("Incorrect. The answer is b).")
        print("TypeError means wrong types. Use print(f'{type(x)=}') to check.")
    print()

    # Question 8
    print("Question 8/11: How should you read a Python traceback?")
    print()
    print("  a) Top to bottom — the first line is the error")
    print("  b) Bottom to top — the last line is where the error occurred")
    print("  c) Only the first line matters")
    print("  d) Only the last line matters")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Read from the bottom — the last line shows the error.")
        print("The lines above show the call chain that led to it.")
    else:
        print("Incorrect. The answer is b) bottom to top.")
        print("The actual error is at the bottom. Lines above show the")
        print("chain of function calls that led to the error.")
    print()

    # Question 9
    print("Question 9/11: What is the purpose of step 7 (Prevent) in the")
    print("debugging method?")
    print()
    print("  a) Prevent the program from running")
    print("  b) Write a test that catches this specific bug so it never returns")
    print("  c) Add more print statements")
    print("  d) Refactor the entire codebase")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Writing a regression test ensures the same bug")
        print("cannot come back without being detected.")
    else:
        print("Incorrect. The answer is b).")
        print("A regression test catches the bug if it ever reappears.")
    print()

    # Question 10
    print("Question 10/11: What debugging tool automatically prints variable")
    print("names with their values, replacing manual print(f'{x=}')?")
    print()
    print("  a) pdb")
    print("  b) icecream (ic)")
    print("  c) pytest")
    print("  d) ruff")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! icecream's ic() function automatically shows the")
        print("variable name and value: ic(x) prints 'ic| x: 42'.")
    else:
        print("Incorrect. The answer is b) icecream (ic).")
        print("ic(x) automatically formats as 'ic| x: 42' — cleaner than print.")
    print()

    # Question 11
    print("Question 11/11: When debugging a logic error (wrong output,")
    print("no crash), what technique helps check your assumptions?")
    print()
    print("  a) Use try/except blocks")
    print("  b) Add assertions that verify expected conditions")
    print("  c) Restart the computer")
    print("  d) Rewrite the code from scratch")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Assertions like assert len(results) > 0 make your")
        print("assumptions explicit and fail loudly when they are wrong.")
    else:
        print("Incorrect. The answer is b) add assertions.")
        print("Assertions document and verify your assumptions at runtime.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You have a solid debugging methodology.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/debugging-methodology.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
