"""
Quiz: Collections — Lists, Dicts, Sets, Tuples
Review: concepts/collections-explained.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Collections — Lists, Dicts, Sets, Tuples")
    print("  Review: concepts/collections-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 8

    # Question 1
    print("Question 1/8: What will this code print?")
    print()
    print("  x = [1, 2, 3]")
    print("  x.append(4)")
    print("  print(len(x))")
    print()
    print("  a) 3")
    print("  b) 4")
    print("  c) [1, 2, 3, 4]")
    print("  d) Error")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! append() adds one item, so the list now has")
        print("4 elements.")
    else:
        print("Incorrect. The answer is b) 4.")
        print("append() adds one element. len() counts the total items.")
    print()

    # Question 2
    print("Question 2/8: How do you access the value 'Denver' from this dict?")
    print()
    print('  person = {"name": "Alice", "city": "Denver"}')
    print()
    print('  a) person[1]')
    print('  b) person["city"]')
    print('  c) person.city')
    print('  d) person("city")')
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Dictionaries use keys in square brackets")
        print("to access values.")
    else:
        print('Incorrect. The answer is b) person["city"].')
        print("Dicts use bracket notation with the key name.")
    print()

    # Question 3
    print("Question 3/8: What will this set contain after running?")
    print()
    print('  colors = {"red", "blue", "red", "green", "blue"}')
    print()
    print('  a) {"red", "blue", "red", "green", "blue"}')
    print('  b) {"red", "blue", "green"}')
    print('  c) {"red", "green"}')
    print("  d) Error — duplicate values")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Sets automatically remove duplicates.")
    else:
        print('Incorrect. The answer is b) {"red", "blue", "green"}.')
        print("Sets do not allow duplicate values.")
    print()

    # Question 4
    print("Question 4/8: What happens if you try to change a tuple?")
    print()
    print("  point = (3, 5)")
    print("  point[0] = 10")
    print()
    print("  a) point becomes (10, 5)")
    print("  b) point becomes [10, 5]")
    print("  c) TypeError — tuples are immutable")
    print("  d) point becomes (10, 3, 5)")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! Tuples cannot be modified after creation.")
        print("That is their defining feature.")
    else:
        print("Incorrect. The answer is c) TypeError.")
        print("Tuples are immutable — they cannot be changed.")
    print()

    # Question 5
    print("Question 5/8: What does {} create in Python?")
    print()
    print("  a) An empty set")
    print("  b) An empty dictionary")
    print("  c) An empty list")
    print("  d) A SyntaxError")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! {} creates an empty dict, not a set.")
        print("To create an empty set, use set().")
    else:
        print("Incorrect. The answer is b) an empty dictionary.")
        print("This is a common gotcha. Use set() for an empty set.")
    print()

    # Question 6
    print("Question 6/8: What does person.get('salary') return if")
    print("'salary' is not a key in the dict?")
    print()
    print('  person = {"name": "Alice", "age": 30}')
    print()
    print("  a) 0")
    print("  b) Error")
    print("  c) None")
    print('  d) ""')
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! .get() returns None for missing keys instead")
        print("of raising a KeyError.")
    else:
        print("Incorrect. The answer is c) None.")
        print(".get() is the safe way to access dict keys — it returns")
        print("None instead of crashing.")
    print()

    # Question 7
    print("Question 7/8: Which collection would you use to store a list")
    print("of student names where order matters and duplicates are possible?")
    print()
    print("  a) Set")
    print("  b) Tuple")
    print("  c) Dictionary")
    print("  d) List")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "d":
        score += 1
        print("Correct! Lists are ordered, changeable, and allow duplicates —")
        print("perfect for a collection of names.")
    else:
        print("Incorrect. The answer is d) List.")
        print("Lists maintain order, allow duplicates, and are changeable.")
    print()

    # Question 8
    print("Question 8/8: What will fruits[-1] return?")
    print()
    print('  fruits = ["apple", "banana", "cherry"]')
    print()
    print('  a) "apple"')
    print('  b) "cherry"')
    print("  c) Error")
    print('  d) "banana"')
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Negative indexing counts from the end.")
        print("-1 gives you the last item.")
    else:
        print('Incorrect. The answer is b) "cherry".')
        print("In Python, -1 refers to the last element.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You have a strong grasp of Python collections.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/collections-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
