"""
Quiz: *args and **kwargs Explained
Review: concepts/args-kwargs-explained.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: *args and **kwargs Explained")
    print("  Review: concepts/args-kwargs-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: What type does *args collect extra positional")
    print("arguments into?")
    print()
    print("  a) list")
    print("  b) tuple")
    print("  c) dict")
    print("  d) set")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! *args collects extra positional arguments into a tuple.")
    else:
        print("Incorrect. The answer is b) tuple.")
        print("The * operator collects positional arguments into a tuple, not a list.")
    print()

    # Question 2
    print("Question 2/12: What type does **kwargs collect extra keyword")
    print("arguments into?")
    print()
    print("  a) list")
    print("  b) tuple")
    print("  c) dict")
    print("  d) set")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! **kwargs collects keyword arguments into a dictionary.")
    else:
        print("Incorrect. The answer is c) dict.")
        print("The ** operator collects keyword arguments into a dictionary.")
    print()

    # Question 3
    print("Question 3/12: What is the correct parameter order in a")
    print("function definition?")
    print()
    print("  a) **kwargs, *args, regular")
    print("  b) *args, regular, **kwargs")
    print("  c) regular, **kwargs, *args")
    print("  d) regular, *args, **kwargs")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "d":
        score += 1
        print("Correct! The order is: regular parameters, then *args, then **kwargs.")
    else:
        print("Incorrect. The answer is d) regular, *args, **kwargs.")
        print("Regular parameters come first, then *args, then **kwargs.")
    print()

    # Question 4
    print("Question 4/12: What will this code print?")
    print()
    print("  def show(*args):")
    print("      print(args)")
    print()
    print("  show(1, 2, 3)")
    print()
    print("  a) [1, 2, 3]")
    print("  b) (1, 2, 3)")
    print("  c) 1 2 3")
    print("  d) {1, 2, 3}")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! *args is a tuple, so printing it shows (1, 2, 3).")
    else:
        print("Incorrect. The answer is b) (1, 2, 3).")
        print("*args collects values into a tuple, which displays with parentheses.")
    print()

    # Question 5
    print("Question 5/12: What does the * operator do when used in a")
    print("function CALL (not definition)?")
    print()
    print("  def add(a, b, c):")
    print("      return a + b + c")
    print()
    print("  nums = [1, 2, 3]")
    print("  add(*nums)")
    print()
    print("  a) Passes the list as a single argument")
    print("  b) Unpacks the list into separate positional arguments")
    print("  c) Creates a tuple from the list")
    print("  d) Raises a TypeError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! *nums unpacks [1, 2, 3] into add(1, 2, 3).")
    else:
        print("Incorrect. The answer is b).")
        print("The * operator in a function call unpacks a sequence into")
        print("separate positional arguments.")
    print()

    # Question 6
    print("Question 6/12: What does a bare * in a parameter list do?")
    print()
    print("  def connect(host, port, *, timeout=30):")
    print("      pass")
    print()
    print("  a) Collects extra positional arguments")
    print("  b) Makes all parameters optional")
    print("  c) Forces everything after it to be keyword-only")
    print("  d) Raises a SyntaxError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! A bare * forces all following parameters to be")
        print("keyword-only. connect('host', 8080, 10) would be a TypeError.")
    else:
        print("Incorrect. The answer is c).")
        print("A bare * means everything after it must be passed as a")
        print("keyword argument, preventing positional mistakes.")
    print()

    # Question 7
    print("Question 7/12: What does the / in a parameter list do?")
    print()
    print("  def greet(name, /, greeting='Hello'):")
    print("      return f'{greeting}, {name}!'")
    print()
    print("  a) Separates required from optional parameters")
    print("  b) Everything before / must be positional-only")
    print("  c) Everything after / must be keyword-only")
    print("  d) It is not valid Python syntax")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Parameters before / are positional-only.")
        print("greet(name='Alice') would raise a TypeError.")
    else:
        print("Incorrect. The answer is b).")
        print("The / marker means parameters before it cannot be passed by name.")
    print()

    # Question 8
    print("Question 8/12: What happens with this code?")
    print()
    print("  def add(a, b):")
    print("      return a + b")
    print()
    print("  args = (1, 2)")
    print("  add(args)")
    print()
    print("  a) Returns 3")
    print("  b) Returns (1, 2)")
    print("  c) TypeError — missing argument")
    print("  d) TypeError — cannot add tuple")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! add(args) passes the tuple as a single argument,")
        print("so b is missing. You need add(*args) to unpack.")
    else:
        print("Incorrect. The answer is c) TypeError — missing argument.")
        print("Without *, the tuple is passed as one argument. Use add(*args).")
    print()

    # Question 9
    print("Question 9/12: What is the output?")
    print()
    print("  def f(name, *hobbies, **details):")
    print("      print(len(hobbies), len(details))")
    print()
    print('  f("Alice", "reading", "hiking", age=30, city="Portland")')
    print()
    print("  a) 2 2")
    print("  b) 3 2")
    print("  c) 2 3")
    print("  d) 1 4")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "a":
        score += 1
        print('Correct! hobbies captures ("reading", "hiking") — length 2.')
        print('details captures {"age": 30, "city": "Portland"} — length 2.')
    else:
        print("Incorrect. The answer is a) 2 2.")
        print("Two extra positional args go to hobbies, two keyword args to details.")
    print()

    # Question 10
    print("Question 10/12: What does ** do when merging dictionaries?")
    print()
    print("  defaults = {'color': 'blue', 'size': 'medium'}")
    print("  user = {'color': 'red'}")
    print("  merged = {**defaults, **user}")
    print()
    print("  a) {'color': 'blue', 'size': 'medium'}")
    print("  b) {'color': 'red', 'size': 'medium'}")
    print("  c) {'color': ['blue', 'red'], 'size': 'medium'}")
    print("  d) Raises a TypeError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Later values override earlier ones. user's 'red'")
        print("overrides defaults' 'blue'.")
    else:
        print("Incorrect. The answer is b).")
        print("When merging with **, later dictionaries override earlier ones.")
    print()

    # Question 11
    print("Question 11/12: Why is this default argument dangerous?")
    print()
    print("  def add_item(item, items=[]):")
    print("      items.append(item)")
    print("      return items")
    print()
    print("  a) Lists cannot be default arguments")
    print("  b) The default list is shared between all calls")
    print("  c) It causes a SyntaxError")
    print("  d) It only works once")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Mutable default arguments are shared between calls.")
        print("Use None as default and create a new list inside the function.")
    else:
        print("Incorrect. The answer is b).")
        print("The list is created once and reused, so items accumulate across calls.")
    print()

    # Question 12
    print("Question 12/12: Why are *args and **kwargs important for")
    print("writing decorators?")
    print()
    print("  a) Decorators require exactly these names")
    print("  b) They let the wrapper accept any arguments and forward them")
    print("     to the wrapped function")
    print("  c) They make the decorator run faster")
    print("  d) Python syntax requires them in decorators")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! *args and **kwargs let a decorator's wrapper function")
        print("accept and forward any arguments to the original function.")
    else:
        print("Incorrect. The answer is b).")
        print("Decorators use *args/**kwargs so the wrapper can handle any")
        print("function signature without knowing it in advance.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand *args and **kwargs thoroughly.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/args-kwargs-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
