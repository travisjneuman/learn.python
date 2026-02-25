"""
Quiz: Decorators Explained
Review: concepts/decorators-explained.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Decorators Explained")
    print("  Review: concepts/decorators-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 6

    # Question 1
    print("Question 1/6: What does a decorator do?")
    print()
    print("  a) Deletes a function")
    print("  b) Wraps a function to add extra behavior")
    print("  c) Makes a function run faster")
    print("  d) Converts a function to a class")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! A decorator takes a function, wraps it with")
        print("additional behavior, and returns the new version.")
    else:
        print("Incorrect. The answer is b).")
        print("Decorators wrap functions to add behavior like logging,")
        print("timing, or route registration.")
    print()

    # Question 2
    print("Question 2/6: What is @shout equivalent to?")
    print()
    print("  @shout")
    print("  def greet():")
    print('      return "hello"')
    print()
    print("  a) greet = shout()")
    print("  b) greet = shout(greet)")
    print("  c) shout = greet(shout)")
    print("  d) shout(greet())")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! @shout is syntactic sugar for greet = shout(greet).")
        print("The decorator receives the function and returns a new one.")
    else:
        print("Incorrect. The answer is b) greet = shout(greet).")
        print("The @ syntax passes the function to the decorator and")
        print("replaces it with whatever the decorator returns.")
    print()

    # Question 3
    print("Question 3/6: When multiple decorators are stacked, in what")
    print("order are they applied?")
    print()
    print("  @decorator_a")
    print("  @decorator_b")
    print("  def func(): pass")
    print()
    print("  a) Top to bottom: decorator_a first, then decorator_b")
    print("  b) Bottom to top: decorator_b first, then decorator_a")
    print("  c) They run at the same time")
    print("  d) Only the top one runs")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Decorators apply bottom-up. This is equivalent to:")
        print("func = decorator_a(decorator_b(func))")
    else:
        print("Incorrect. The answer is b) bottom to top.")
        print("The closest decorator to the function runs first.")
    print()

    # Question 4
    print("Question 4/6: Why should you use @functools.wraps in a")
    print("decorator?")
    print()
    print("  a) To make the decorator run faster")
    print("  b) To preserve the original function's name and docstring")
    print("  c) To allow the decorator to take arguments")
    print("  d) It is required — decorators do not work without it")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Without @wraps, the decorated function loses its")
        print("original __name__ and __doc__, making debugging harder.")
    else:
        print("Incorrect. The answer is b).")
        print("@wraps copies the original function's metadata to the wrapper,")
        print("so debugging and introspection still work properly.")
    print()

    # Question 5
    print("Question 5/6: Why does the wrapper function need *args and")
    print("**kwargs?")
    print()
    print("  def log_call(func):")
    print("      def wrapper(*args, **kwargs):")
    print("          print(f'Calling {func.__name__}')")
    print("          return func(*args, **kwargs)")
    print("      return wrapper")
    print()
    print("  a) They are required Python syntax")
    print("  b) So the wrapper can accept and forward any arguments")
    print("     the original function expects")
    print("  c) They make the function faster")
    print("  d) They are only needed for methods")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! *args and **kwargs let the wrapper accept any")
        print("combination of arguments and pass them through to the")
        print("original function.")
    else:
        print("Incorrect. The answer is b).")
        print("Without *args and **kwargs, the wrapper could not handle")
        print("functions with different parameter signatures.")
    print()

    # Question 6
    print("Question 6/6: Which of these is a real-world use of decorators?")
    print()
    print("  a) @app.get('/') in FastAPI to register a route")
    print("  b) @pytest.mark.parametrize to run a test with multiple inputs")
    print("  c) @click.command() to create a CLI command")
    print("  d) All of the above")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "d":
        score += 1
        print("Correct! Decorators are used heavily in web frameworks,")
        print("testing, CLI tools, and many other Python libraries.")
    else:
        print("Incorrect. The answer is d) all of the above.")
        print("Decorators are one of the most widely used patterns")
        print("in the Python ecosystem.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand decorators thoroughly.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/decorators-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
