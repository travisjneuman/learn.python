"""
Quiz: Enums Explained
Review: concepts/enums-explained.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Enums Explained")
    print("  Review: concepts/enums-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 11

    # Question 1
    print("Question 1/11: What is the main purpose of an enum?")
    print()
    print("  a) To create loops")
    print("  b) To define a set of named constants")
    print("  c) To sort data")
    print("  d) To create classes")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Enums define a fixed set of named constants,")
        print("replacing magic strings and numbers.")
    else:
        print("Incorrect. The answer is b) define a set of named constants.")
    print()

    # Question 2
    print("Question 2/11: What attributes does an enum member have?")
    print()
    print("  class Color(Enum):")
    print("      RED = 'red'")
    print()
    print("  a) .key and .val")
    print("  b) .name and .value")
    print("  c) .label and .data")
    print("  d) .id and .text")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Color.RED.name is 'RED', Color.RED.value is 'red'.")
    else:
        print("Incorrect. The answer is b) .name and .value.")
    print()

    # Question 3
    print("Question 3/11: Does Color.RED == 'red' evaluate to True?")
    print("(Color is a regular Enum, not StrEnum)")
    print()
    print("  a) Yes")
    print("  b) No — regular Enum members are not equal to their values")
    print("  c) It raises an error")
    print("  d) Only if you use ==, not is")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Regular Enum members are not equal to their values.")
        print("Use Color.RED.value == 'red' or switch to StrEnum.")
    else:
        print("Incorrect. The answer is b).")
        print("Color.RED == 'red' is False for regular Enum. Use StrEnum for")
        print("string equality.")
    print()

    # Question 4
    print("Question 4/11: What does IntEnum allow that regular Enum does not?")
    print()
    print("  a) String comparisons")
    print("  b) Comparison with integers and use in math")
    print("  c) More than 10 members")
    print("  d) Dynamic member creation")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! IntEnum members behave like integers — you can")
        print("compare them with numbers, sort them, and use them in math.")
    else:
        print("Incorrect. The answer is b).")
        print("Priority.HIGH == 3 is True with IntEnum, False with regular Enum.")
    print()

    # Question 5
    print("Question 5/11: What does auto() do?")
    print()
    print("  class Direction(Enum):")
    print("      NORTH = auto()")
    print("      SOUTH = auto()")
    print()
    print("  a) Creates random values")
    print("  b) Assigns incrementing integers starting from 1")
    print("  c) Assigns string values matching the name")
    print("  d) Raises an error")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! auto() assigns 1, 2, 3, ... automatically.")
        print("Useful when you care about the name, not the value.")
    else:
        print("Incorrect. The answer is b).")
        print("auto() auto-generates incrementing integers starting from 1.")
    print()

    # Question 6
    print("Question 6/11: What is StrEnum (Python 3.11+)?")
    print()
    print("  a) An enum that only allows single characters")
    print("  b) An enum whose members behave like strings")
    print("  c) A string that has enum methods")
    print("  d) A deprecated enum type")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! StrEnum members work like strings — ")
        print("Status.ACTIVE == 'active' is True.")
    else:
        print("Incorrect. The answer is b).")
        print("StrEnum members can be compared to strings directly.")
    print()

    # Question 7
    print("Question 7/11: How do you look up an enum member by its value?")
    print()
    print("  class Color(Enum):")
    print("      RED = 'red'")
    print()
    print("  a) Color.get('red')")
    print("  b) Color('red')")
    print("  c) Color.find('red')")
    print("  d) Color.from_value('red')")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Color('red') returns Color.RED.")
        print("Color['RED'] looks up by name instead.")
    else:
        print("Incorrect. The answer is b) Color('red').")
        print("Call the enum class with a value to look up the member.")
    print()

    # Question 8
    print("Question 8/11: Can you modify an enum member's value?")
    print()
    print("  Color.RED = 'crimson'")
    print()
    print("  a) Yes, it updates the value")
    print("  b) No, it raises an AttributeError because enums are immutable")
    print("  c) Yes, but only for StrEnum")
    print("  d) It silently does nothing")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Enum members are immutable — you cannot change")
        print("their values after definition.")
    else:
        print("Incorrect. The answer is b) AttributeError.")
        print("Enums are immutable by design.")
    print()

    # Question 9
    print("Question 9/11: How do you iterate over all members of an enum?")
    print()
    print("  a) Color.all()")
    print("  b) for color in Color:")
    print("  c) Color.members()")
    print("  d) list(Color.values())")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Enums are iterable — 'for member in MyEnum:' works.")
    else:
        print("Incorrect. The answer is b) for color in Color:")
        print("You can loop directly over an enum class.")
    print()

    # Question 10
    print("Question 10/11: Why are enums better than magic strings?")
    print()
    print("  a) They use less memory")
    print("  b) Typos are caught immediately as AttributeError instead of")
    print("     silently producing wrong behavior")
    print("  c) They run faster")
    print("  d) They support more characters")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Status.ACTVE raises AttributeError immediately.")
        print("The string 'actve' would silently pass through undetected.")
    else:
        print("Incorrect. The answer is b).")
        print("Enums provide typo protection — misspelled names fail loudly.")
    print()

    # Question 11
    print("Question 11/11: What Python version is needed for StrEnum?")
    print()
    print("  a) 3.8+")
    print("  b) 3.9+")
    print("  c) 3.10+")
    print("  d) 3.11+")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "d":
        score += 1
        print("Correct! StrEnum was added in Python 3.11.")
        print("For earlier versions, use class Status(str, Enum) instead.")
    else:
        print("Incorrect. The answer is d) 3.11+.")
        print("Use class MyEnum(str, Enum) on older Python versions.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand enums well.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/enums-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
