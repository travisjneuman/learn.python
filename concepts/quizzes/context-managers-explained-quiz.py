"""
Quiz: Context Managers Explained
Review: concepts/context-managers-explained.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Context Managers Explained")
    print("  Review: concepts/context-managers-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 11

    # Question 1
    print("Question 1/11: What does the 'with' statement guarantee?")
    print()
    print("  a) The code inside runs faster")
    print("  b) Resources are cleaned up when the block exits, even on errors")
    print("  c) No exceptions can occur inside the block")
    print("  d) The file is opened in read-only mode")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The with statement guarantees cleanup (__exit__)")
        print("runs even if an exception occurs inside the block.")
    else:
        print("Incorrect. The answer is b).")
        print("The key benefit of 'with' is guaranteed cleanup.")
    print()

    # Question 2
    print("Question 2/11: Which two special methods must a class implement")
    print("to be a context manager?")
    print()
    print("  a) __init__ and __del__")
    print("  b) __enter__ and __exit__")
    print("  c) __open__ and __close__")
    print("  d) __start__ and __stop__")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! __enter__ runs when entering the with block,")
        print("__exit__ runs when leaving it.")
    else:
        print("Incorrect. The answer is b) __enter__ and __exit__.")
    print()

    # Question 3
    print("Question 3/11: What does __enter__ return?")
    print()
    print("  with open('file.txt') as f:")
    print("      ...")
    print()
    print("  a) Nothing")
    print("  b) The value assigned to the 'as' variable")
    print("  c) True or False")
    print("  d) The filename")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Whatever __enter__ returns is bound to the 'as' variable.")
    else:
        print("Incorrect. The answer is b).")
        print("__enter__'s return value becomes the variable after 'as'.")
    print()

    # Question 4
    print("Question 4/11: What happens if __exit__ returns True?")
    print()
    print("  a) The context manager is reusable")
    print("  b) The exception (if any) is suppressed silently")
    print("  c) The exception is re-raised")
    print("  d) The program exits")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Returning True from __exit__ suppresses the exception.")
        print("Almost always return False to let exceptions propagate.")
    else:
        print("Incorrect. The answer is b).")
        print("True = suppress the exception. False = let it propagate.")
        print("You should almost always return False.")
    print()

    # Question 5
    print("Question 5/11: What three arguments does __exit__ receive?")
    print()
    print("  a) filename, mode, encoding")
    print("  b) exc_type, exc_val, exc_tb")
    print("  c) self, args, kwargs")
    print("  d) error, message, code")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! __exit__ receives the exception type, value, and")
        print("traceback. All three are None if no exception occurred.")
    else:
        print("Incorrect. The answer is b) exc_type, exc_val, exc_tb.")
        print("These describe any exception that occurred in the block.")
    print()

    # Question 6
    print("Question 6/11: What does @contextmanager from contextlib do?")
    print()
    print("  a) Makes any function a context manager")
    print("  b) Turns a generator function (with yield) into a context manager")
    print("  c) Adds __enter__ and __exit__ to any class")
    print("  d) Automatically closes files")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! @contextmanager turns a generator function into a")
        print("context manager. Code before yield = setup, after yield = cleanup.")
    else:
        print("Incorrect. The answer is b).")
        print("The function must use yield. Before yield is __enter__,")
        print("after yield is __exit__.")
    print()

    # Question 7
    print("Question 7/11: In a @contextmanager function, what does the")
    print("yielded value represent?")
    print()
    print("  a) The return value of the function")
    print("  b) The value assigned to the 'as' variable in the with block")
    print("  c) A signal that cleanup should start")
    print("  d) The exception that occurred")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The yielded value becomes what follows 'as' in")
        print("the with statement.")
    else:
        print("Incorrect. The answer is b).")
        print("'with managed_resource() as x:' — x gets the yielded value.")
    print()

    # Question 8
    print("Question 8/11: What does contextlib.suppress do?")
    print()
    print("  from contextlib import suppress")
    print("  with suppress(FileNotFoundError):")
    print("      os.remove('temp.txt')")
    print()
    print("  a) Prevents the file from being deleted")
    print("  b) Silently catches FileNotFoundError if the file does not exist")
    print("  c) Logs the error to a file")
    print("  d) Retries the operation")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! suppress catches the specified exception and does")
        print("nothing — a cleaner alternative to try/except/pass.")
    else:
        print("Incorrect. The answer is b).")
        print("suppress is equivalent to try: ... except XError: pass.")
    print()

    # Question 9
    print("Question 9/11: What happens if you try to use a file outside")
    print("its with block?")
    print()
    print("  with open('data.txt') as f:")
    print("      pass")
    print("  f.read()")
    print()
    print("  a) It works normally")
    print("  b) ValueError — I/O operation on closed file")
    print("  c) The file is reopened automatically")
    print("  d) Returns an empty string")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The file is closed when the with block exits.")
        print("Reading a closed file raises ValueError.")
    else:
        print("Incorrect. The answer is b) ValueError.")
        print("The resource is only valid inside the with block.")
    print()

    # Question 10
    print("Question 10/11: How can you use multiple context managers at once")
    print("in Python 3.10+?")
    print()
    print("  a) with open('a') as a; open('b') as b:")
    print("  b) with (open('a') as a, open('b') as b):")
    print("  c) with open('a') as a and open('b') as b:")
    print("  d) with [open('a') as a, open('b') as b]:")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Python 3.10+ supports parenthesized context managers")
        print("for cleaner multi-line with statements.")
    else:
        print("Incorrect. The answer is b).")
        print("Parenthesized context managers: with (cm1 as a, cm2 as b):")
    print()

    # Question 11
    print("Question 11/11: Why should cleanup code in a @contextmanager")
    print("function be inside a 'finally' block?")
    print()
    print("  @contextmanager")
    print("  def managed(name):")
    print("      f = open(name)")
    print("      try:")
    print("          yield f")
    print("      finally:")
    print("          f.close()")
    print()
    print("  a) finally is required by the decorator")
    print("  b) It ensures cleanup runs even if the with block raises an exception")
    print("  c) It makes the function faster")
    print("  d) It prevents the file from being opened")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Without try/finally, an exception in the with block")
        print("would skip the cleanup code after yield.")
    else:
        print("Incorrect. The answer is b).")
        print("finally guarantees cleanup runs regardless of exceptions.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand context managers thoroughly.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/context-managers-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
