"""
Quiz: Testing Strategies
Review: concepts/testing-strategies.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Testing Strategies")
    print("  Review: concepts/testing-strategies.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: In the test pyramid, which type of test should")
    print("you have the most of?")
    print()
    print("  a) End-to-end tests")
    print("  b) Integration tests")
    print("  c) Unit tests")
    print("  d) Manual tests")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Unit tests are fast, cheap, and focused. They form")
        print("the base of the pyramid — write lots of them.")
    else:
        print("Incorrect. The answer is c) unit tests.")
        print("Many unit tests, some integration tests, few E2E tests.")
    print()

    # Question 2
    print("Question 2/12: What does pytest.raises() test?")
    print()
    print("  with pytest.raises(ValueError):")
    print("      divide(10, 0)")
    print()
    print("  a) That the function returns a ValueError")
    print("  b) That the function raises a ValueError exception")
    print("  c) That the function does NOT raise an error")
    print("  d) That the error message is printed")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! pytest.raises verifies that the expected exception")
        print("is raised. The test fails if no exception occurs.")
    else:
        print("Incorrect. The answer is b).")
        print("pytest.raises checks that a specific exception is thrown.")
    print()

    # Question 3
    print("Question 3/12: What does @pytest.mark.parametrize do?")
    print()
    print("  a) Makes tests run in parallel")
    print("  b) Runs the same test function with multiple sets of inputs")
    print("  c) Parameterizes the test fixture")
    print("  d) Skips tests based on parameters")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! parametrize lets you test many input/output pairs")
        print("with a single test function. Each runs independently.")
    else:
        print("Incorrect. The answer is b).")
        print("One function, many test cases — each reported separately.")
    print()

    # Question 4
    print("Question 4/12: What is a pytest fixture?")
    print()
    print("  a) A broken test")
    print("  b) Reusable setup/teardown code that provides test dependencies")
    print("  c) A test configuration file")
    print("  d) A test report format")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Fixtures set up resources (databases, files, etc.)")
        print("and clean them up after. Each test gets a fresh instance.")
    else:
        print("Incorrect. The answer is b).")
        print("Fixtures use @pytest.fixture and yield for setup/teardown.")
    print()

    # Question 5
    print("Question 5/12: What is the purpose of mocking in tests?")
    print()
    print("  a) To make fun of bad code")
    print("  b) To replace external dependencies (APIs, databases) with")
    print("     controlled substitutes")
    print("  c) To skip tests that are too slow")
    print("  d) To create fake data")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Mocking replaces real dependencies with test doubles")
        print("so you can test your code in isolation.")
    else:
        print("Incorrect. The answer is b).")
        print("Mocking isolates the code under test from external systems.")
    print()

    # Question 6
    print("Question 6/12: What are the three steps of TDD?")
    print()
    print("  a) Plan, Code, Deploy")
    print("  b) Red (failing test), Green (make it pass), Refactor (clean up)")
    print("  c) Write, Run, Fix")
    print("  d) Test, Build, Ship")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Red-Green-Refactor: write a failing test, make it")
        print("pass with minimal code, then clean up.")
    else:
        print("Incorrect. The answer is b) Red, Green, Refactor.")
        print("Write the test FIRST, then the code to pass it.")
    print()

    # Question 7
    print("Question 7/12: What does code coverage measure?")
    print()
    print("  a) How fast tests run")
    print("  b) What percentage of your code is executed by tests")
    print("  c) How many tests you have")
    print("  d) How many bugs your tests found")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Coverage shows which lines your tests exercise.")
        print("100% coverage does not mean zero bugs — just that every line ran.")
    else:
        print("Incorrect. The answer is b).")
        print("Use pytest --cov to see coverage. Aim for 80%+ on critical code.")
    print()

    # Question 8
    print("Question 8/12: Why should tests be independent of each other?")
    print()
    print("  a) It makes them faster")
    print("  b) So one failing test does not cascade failures, and tests")
    print("     can run in any order")
    print("  c) It reduces code duplication")
    print("  d) It is a Python requirement")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Each test should set up its own data. Tests that")
        print("depend on each other are fragile and hard to debug.")
    else:
        print("Incorrect. The answer is b).")
        print("Independent tests are reliable regardless of execution order.")
    print()

    # Question 9
    print("Question 9/12: What is wrong with this test approach?")
    print()
    print("  def fizzbuzz(n):")
    print("      if n == 3: return 'Fizz'")
    print("      if n == 5: return 'Buzz'")
    print("      return str(n)")
    print()
    print("  a) Nothing — it passes the tests")
    print("  b) It hard-codes values to match test inputs instead of")
    print("     implementing real logic (n == 3 vs n % 3 == 0)")
    print("  c) It uses strings instead of numbers")
    print("  d) The function name is wrong")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! This only works for 3 and 5, not 6, 9, 10, 15, etc.")
        print("The real logic should use modulo: n % 3 == 0.")
    else:
        print("Incorrect. The answer is b).")
        print("Solutions must implement real logic, not pattern-match test inputs.")
    print()

    # Question 10
    print("Question 10/12: What should you test beyond the happy path?")
    print()
    print("  a) Only the most common inputs")
    print("  b) Edge cases: empty input, zero, negative numbers, None,")
    print("     very large values, boundary conditions")
    print("  c) Only inputs that users are likely to enter")
    print("  d) Only inputs that cause errors")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Edge cases are where bugs hide. Always test empty,")
        print("zero, negative, None, large values, and boundary conditions.")
    else:
        print("Incorrect. The answer is b).")
        print("Edge cases find the most bugs. Test the boundaries.")
    print()

    # Question 11
    print("Question 11/12: What should you test: behavior or implementation?")
    print()
    print("  a) Implementation details (internal data structures)")
    print("  b) Behavior (what the function does, not how)")
    print("  c) Both equally")
    print("  d) Neither — just check for errors")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Test what the code does (user.name == 'Alice'), not")
        print("how it stores data (user._data['name']). This lets you refactor")
        print("without breaking tests.")
    else:
        print("Incorrect. The answer is b) behavior.")
        print("Testing behavior makes tests resilient to refactoring.")
    print()

    # Question 12
    print("Question 12/12: What does monkeypatch do in pytest?")
    print()
    print("  a) Patches security vulnerabilities")
    print("  b) Temporarily replaces attributes, functions, or environment")
    print("     variables during a test")
    print("  c) Runs tests on multiple Python versions")
    print("  d) Patches broken tests automatically")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! monkeypatch lets you replace functions, attributes,")
        print("and env vars for the duration of a test, automatically reverting")
        print("them afterward.")
    else:
        print("Incorrect. The answer is b).")
        print("monkeypatch.setattr() is pytest's way to mock/stub dependencies.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand testing strategies well.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/testing-strategies.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
