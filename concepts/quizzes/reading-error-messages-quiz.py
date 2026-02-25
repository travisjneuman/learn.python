"""
Quiz: Reading Error Messages
Review: concepts/reading-error-messages.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Reading Error Messages")
    print("  Review: concepts/reading-error-messages.md")
    print("=" * 60)
    print()

    score = 0
    total = 8

    # Question 1
    print("Question 1/8: When reading a Python traceback, which direction")
    print("should you read it?")
    print()
    print("  a) Top to bottom")
    print("  b) Bottom to top")
    print("  c) Only the middle matters")
    print("  d) Left to right")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The last line tells you what went wrong.")
        print("The frames above show how Python got there.")
    else:
        print("Incorrect. The answer is b).")
        print("Always start at the bottom -- that is the actual error.")
    print()

    # Question 2
    print("Question 2/8: What does this error mean?")
    print()
    print("  NameError: name 'user_name' is not defined")
    print()
    print("  a) The variable 'user_name' has the wrong value")
    print("  b) The variable 'user_name' does not exist in this scope")
    print("  c) The variable 'user_name' is the wrong type")
    print("  d) The file 'user_name' was not found")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! NameError means the name has never been defined.")
        print("Check for typos or make sure you defined it before using it.")
    else:
        print("Incorrect. The answer is b).")
        print("NameError means Python has never seen that name.")
    print()

    # Question 3
    print("Question 3/8: What kind of error is this?")
    print()
    print("  if x > 5")
    print('      print("big")')
    print()
    print("  a) NameError")
    print("  b) IndentationError")
    print("  c) SyntaxError -- missing colon after 'if x > 5'")
    print("  d) TypeError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! The colon after the condition is required.")
        print("SyntaxError means Python could not even parse the code.")
    else:
        print("Incorrect. The answer is c).")
        print("if/for/while/def lines need a colon at the end.")
    print()

    # Question 4
    print("Question 4/8: What does this error tell you?")
    print()
    print("  TypeError: unsupported operand type(s) for +: 'int' and 'str'")
    print()
    print("  a) You used the wrong variable name")
    print("  b) You tried to add an integer and a string together")
    print("  c) The file was not found")
    print("  d) The list index is out of range")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! You cannot add numbers and text directly.")
        print("Convert one to match the other: str(num) or int(text).")
    else:
        print("Incorrect. The answer is b).")
        print("TypeError means the types do not support the operation.")
    print()

    # Question 5
    print("Question 5/8: What error does int('3.14') produce?")
    print()
    print("  a) TypeError")
    print("  b) SyntaxError")
    print("  c) ValueError -- cannot convert '3.14' to int directly")
    print("  d) No error -- it returns 3")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! int() cannot convert a float string directly.")
        print("Use int(float('3.14')) to go string -> float -> int.")
    else:
        print("Incorrect. The answer is c).")
        print("int('3.14') raises ValueError because the string contains a decimal.")
    print()

    # Question 6
    print("Question 6/8: Given this traceback, which line actually caused")
    print("the error?")
    print()
    print('  Traceback (most recent call last):')
    print('    File "main.py", line 10, in run')
    print('      total = add_prices(items)')
    print('    File "main.py", line 5, in add_prices')
    print('      total += item["price"]')
    print("  KeyError: 'price'")
    print()
    print("  a) Line 10")
    print("  b) Line 5")
    print("  c) Both lines")
    print("  d) Cannot tell from the traceback")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The bottom frame (line 5) is where it actually broke.")
        print("Line 10 called the function, but line 5 is the failing line.")
    else:
        print("Incorrect. The answer is b).")
        print("The bottom-most frame in a traceback is where the error happened.")
    print()

    # Question 7
    print("Question 7/8: What is the difference between KeyError and")
    print("IndexError?")
    print()
    print("  a) They are the same thing")
    print("  b) KeyError is for dicts, IndexError is for lists")
    print("  c) KeyError is for lists, IndexError is for dicts")
    print("  d) Both are for lists")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! KeyError means a dict key is missing.")
        print("IndexError means a list/tuple position is out of range.")
    else:
        print("Incorrect. The answer is b).")
        print("Dicts use keys (KeyError), lists use indexes (IndexError).")
    print()

    # Question 8
    print("Question 8/8: What does AttributeError usually mean?")
    print()
    print("  a) You used the wrong file name")
    print("  b) You called a method on an object that does not have it")
    print("  c) You forgot to install a package")
    print("  d) Your indentation is wrong")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! AttributeError means the object does not have")
        print("that method or property. Often caused by calling .method()")
        print("on None.")
    else:
        print("Incorrect. The answer is b).")
        print("Check that the object is the type you expect. A common")
        print("cause is calling methods on None.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You can decode any Python traceback.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/reading-error-messages.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
