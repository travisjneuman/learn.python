"""
Quiz: Errors and Debugging
Review: concepts/errors-and-debugging.md
"""

from _quiz_helpers import normalize_answer, ask_true_false, ask_code_completion


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Errors and Debugging")
    print("  Review: concepts/errors-and-debugging.md")
    print("=" * 60)
    print()

    score = 0
    total = 9

    # Question 1
    print("Question 1/9: When reading a Python error message (traceback),")
    print("where should you look first?")
    print()
    print("  a) The very top line")
    print("  b) The middle of the message")
    print("  c) The last line — it says what went wrong")
    print("  d) It does not matter")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Read tracebacks bottom-up. The last line tells")
        print("you the error type and message.")
    else:
        print("Incorrect. The answer is c).")
        print("The last line has the error type and description.")
        print("Then look at the line number above it.")
    print()

    # Question 2
    print("Question 2/9: What error do you get if you use a variable")
    print("that has not been created yet?")
    print()
    print("  a) SyntaxError")
    print("  b) TypeError")
    print("  c) NameError")
    print("  d) ValueError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! NameError means Python cannot find a variable")
        print("with that name. Usually a typo or using it before defining it.")
    else:
        print("Incorrect. The answer is c) NameError.")
        print("This means the name does not exist in the current scope.")
    print()

    # Question 3
    print("Question 3/9: What error does this code produce?")
    print()
    print('  age = 30')
    print('  print("I am " + age)')
    print()
    print("  a) NameError")
    print("  b) TypeError — cannot add string and integer")
    print("  c) ValueError")
    print("  d) No error — it prints 'I am 30'")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! You cannot concatenate a string and an int.")
        print('Use str(age) or f"I am {age}" instead.')
    else:
        print("Incorrect. The answer is b) TypeError.")
        print("Python cannot add a string and an integer together.")
    print()

    # Question 4
    print("Question 4/9: What error does int('hello') produce?")
    print()
    print("  a) TypeError")
    print("  b) NameError")
    print("  c) ValueError — 'hello' is not a valid number")
    print("  d) SyntaxError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! The type is right (it is a string), but the value")
        print("cannot be converted to an integer.")
    else:
        print("Incorrect. The answer is c) ValueError.")
        print("ValueError means the type is correct but the value is wrong.")
    print()

    # Question 5
    print("Question 5/9: What is the simplest debugging technique?")
    print()
    print("  a) Using a professional debugger")
    print("  b) Rewriting the code from scratch")
    print("  c) Adding print() statements to see variable values")
    print("  d) Asking someone else to fix it")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! print() debugging is simple and effective.")
        print("Print variable values and types before the error line.")
    else:
        print("Incorrect. The answer is c).")
        print("Adding print() calls to inspect values is the most")
        print("accessible debugging technique for beginners.")
    print()

    # Question 6
    print("Question 6/9: What is wrong with this code?")
    print()
    print("  if x > 5")
    print('      print("big")')
    print()
    print("  a) NameError — x is not defined")
    print("  b) SyntaxError — missing colon after the condition")
    print("  c) IndentationError")
    print("  d) TypeError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! if statements require a colon at the end.")
        print("It should be: if x > 5:")
    else:
        print("Incorrect. The answer is b) SyntaxError.")
        print("Python needs a colon after if, for, while, and def lines.")
    print()

    # Question 7
    print("Question 7/9: What error occurs here?")
    print()
    print("  my_list = [10, 20, 30]")
    print("  print(my_list[5])")
    print()
    print("  a) ValueError")
    print("  b) KeyError")
    print("  c) IndexError — index out of range")
    print("  d) TypeError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! The list only has indexes 0, 1, 2.")
        print("Index 5 does not exist, so Python raises IndexError.")
    else:
        print("Incorrect. The answer is c) IndexError.")
        print("The list has 3 items (indexes 0-2). Index 5 is out of range.")
    print()

    # Question 8 — true/false
    if ask_true_false(
        question_num=8,
        total=total,
        statement="A SyntaxError means your code ran but produced the wrong result.",
        correct=False,
        explanation_correct="SyntaxError means Python could not even parse your code. It never runs.",
        explanation_incorrect="SyntaxError happens before your code runs. Python cannot understand the structure, so it stops immediately.",
    ):
        score += 1

    # Question 9 — code completion
    if ask_code_completion(
        question_num=9,
        total=total,
        prompt="Complete the try/except block to catch a ValueError:",
        code_lines=[
            "try:",
            '    number = int(input("Enter a number: "))',
            "____ ValueError:",
            '    print("That is not a valid number.")',
        ],
        correct_answers=["except"],
        explanation_correct="except catches the specified error type so the program can handle it gracefully.",
        explanation_incorrect="The except keyword follows a try block to catch specific error types.",
        case_sensitive=True,
    ):
        score += 1

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You can read errors like a pro.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/errors-and-debugging.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
