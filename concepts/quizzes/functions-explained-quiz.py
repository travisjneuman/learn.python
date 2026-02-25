"""
Quiz: Functions Explained
Review: concepts/functions-explained.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Functions Explained")
    print("  Review: concepts/functions-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print("Question 1/7: What keyword defines a function in Python?")
    print()
    print("  a) function")
    print("  b) func")
    print("  c) def")
    print("  d) define")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! The 'def' keyword is used to define functions.")
    else:
        print("Incorrect. The answer is c) def.")
        print("Python uses 'def' (short for define) to create functions.")
    print()

    # Question 2
    print("Question 2/7: What will this code print?")
    print()
    print("  def add(a, b):")
    print("      result = a + b")
    print()
    print("  total = add(3, 5)")
    print("  print(total)")
    print()
    print("  a) 8")
    print("  b) None")
    print("  c) Error")
    print("  d) 0")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! The function calculates the result but never")
        print("returns it. Without a return statement, functions return None.")
    else:
        print("Incorrect. The answer is b) None.")
        print("The function is missing 'return result'. Without return,")
        print("Python returns None by default.")
    print()

    # Question 3
    print("Question 3/7: In this function definition, what is 'name'?")
    print()
    print("  def greet(name):")
    print('      return f"Hello, {name}!"')
    print()
    print("  a) An argument")
    print("  b) A parameter")
    print("  c) A variable")
    print("  d) A string")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Parameters are the names in the function definition.")
        print("Arguments are the values you pass when calling the function.")
    else:
        print("Incorrect. The answer is b) parameter.")
        print("In the definition, it is a parameter. When you call")
        print("greet('Alice'), 'Alice' is the argument.")
    print()

    # Question 4
    print("Question 4/7: What will this code print?")
    print()
    print('  def greet(name, greeting="Hello"):')
    print('      return f"{greeting}, {name}!"')
    print()
    print('  print(greet("Alice"))')
    print()
    print('  a) Error — missing argument')
    print('  b) Hello, Alice!')
    print('  c) None, Alice!')
    print('  d) Alice')
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! greeting has a default value of 'Hello', so you")
        print("can call the function with just one argument.")
    else:
        print("Incorrect. The answer is b) Hello, Alice!")
        print("The greeting parameter has a default value, so it is optional.")
    print()

    # Question 5
    print("Question 5/7: What is wrong with this code?")
    print()
    print('  greet("Alice")')
    print()
    print("  def greet(name):")
    print('      return f"Hello, {name}!"')
    print()
    print("  a) Nothing — it works fine")
    print("  b) NameError — greet is called before it is defined")
    print("  c) SyntaxError — wrong order")
    print("  d) TypeError — wrong argument type")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Functions must be defined before they are called.")
        print("Python reads top to bottom.")
    else:
        print("Incorrect. The answer is b) NameError.")
        print("You must define a function before calling it.")
    print()

    # Question 6
    print("Question 6/7: What is the difference between these two lines?")
    print()
    print("  greet")
    print('  greet("Alice")')
    print()
    print("  a) They are the same")
    print("  b) greet is the function object; greet('Alice') calls it")
    print("  c) greet prints the function; greet('Alice') runs it")
    print("  d) Both call the function")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Without parentheses, you are referencing the")
        print("function object itself. With parentheses, you call it.")
    else:
        print("Incorrect. The answer is b).")
        print("Parentheses () are what actually call the function.")
    print()

    # Question 7
    print("Question 7/7: Why are functions useful? (Pick the best answer)")
    print()
    print("  a) They make code run faster")
    print("  b) They let you reuse code, organize logic, and test pieces")
    print("     independently")
    print("  c) Python requires them")
    print("  d) They use less memory")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Functions enable reuse, organization, testability,")
        print("and readability.")
    else:
        print("Incorrect. The answer is b).")
        print("Functions help with reuse, organization, testing, and clarity.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand functions well.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/functions-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
