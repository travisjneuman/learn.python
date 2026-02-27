"""
Quiz: Collections — Lists, Dicts, Sets, Tuples
Review: concepts/collections-explained.md
"""

from _quiz_helpers import normalize_answer, ask_true_false, ask_code_completion


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Collections — Lists, Dicts, Sets, Tuples")
    print("  Review: concepts/collections-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 11

    # Question 1
    print("Question 1/11: What will this code print?")
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
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! append() adds one item, so the list now has")
        print("4 elements.")
    else:
        print("Incorrect. The answer is b) 4.")
        print("append() adds one element. len() counts the total items.")
    print()

    # Question 2
    print("Question 2/11: How do you access the value 'Denver' from this dict?")
    print()
    print('  person = {"name": "Alice", "city": "Denver"}')
    print()
    print('  a) person[1]')
    print('  b) person["city"]')
    print('  c) person.city')
    print('  d) person("city")')
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Dictionaries use keys in square brackets")
        print("to access values.")
    else:
        print('Incorrect. The answer is b) person["city"].')
        print("Dicts use bracket notation with the key name.")
    print()

    # Question 3
    print("Question 3/11: What will this set contain after running?")
    print()
    print('  colors = {"red", "blue", "red", "green", "blue"}')
    print()
    print('  a) {"red", "blue", "red", "green", "blue"}')
    print('  b) {"red", "blue", "green"}')
    print('  c) {"red", "green"}')
    print("  d) Error — duplicate values")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Sets automatically remove duplicates.")
    else:
        print('Incorrect. The answer is b) {"red", "blue", "green"}.')
        print("Sets do not allow duplicate values.")
    print()

    # Question 4
    print("Question 4/11: What happens if you try to change a tuple?")
    print()
    print("  point = (3, 5)")
    print("  point[0] = 10")
    print()
    print("  a) point becomes (10, 5)")
    print("  b) point becomes [10, 5]")
    print("  c) TypeError — tuples are immutable")
    print("  d) point becomes (10, 3, 5)")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Tuples cannot be modified after creation.")
        print("That is their defining feature.")
    else:
        print("Incorrect. The answer is c) TypeError.")
        print("Tuples are immutable — they cannot be changed.")
    print()

    # Question 5
    print("Question 5/11: What does {} create in Python?")
    print()
    print("  a) An empty set")
    print("  b) An empty dictionary")
    print("  c) An empty list")
    print("  d) A SyntaxError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! {} creates an empty dict, not a set.")
        print("To create an empty set, use set().")
    else:
        print("Incorrect. The answer is b) an empty dictionary.")
        print("This is a common gotcha. Use set() for an empty set.")
    print()

    # Question 6
    print("Question 6/11: What does person.get('salary') return if")
    print("'salary' is not a key in the dict?")
    print()
    print('  person = {"name": "Alice", "age": 30}')
    print()
    print("  a) 0")
    print("  b) Error")
    print("  c) None")
    print('  d) ""')
    print()
    answer = normalize_answer(input("Your answer: "))
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
    print("Question 7/11: Which collection would you use to store a list")
    print("of student names where order matters and duplicates are possible?")
    print()
    print("  a) Set")
    print("  b) Tuple")
    print("  c) Dictionary")
    print("  d) List")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "d":
        score += 1
        print("Correct! Lists are ordered, changeable, and allow duplicates —")
        print("perfect for a collection of names.")
    else:
        print("Incorrect. The answer is d) List.")
        print("Lists maintain order, allow duplicates, and are changeable.")
    print()

    # Question 8
    print("Question 8/11: What will fruits[-1] return?")
    print()
    print('  fruits = ["apple", "banana", "cherry"]')
    print()
    print('  a) "apple"')
    print('  b) "cherry"')
    print("  c) Error")
    print('  d) "banana"')
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Negative indexing counts from the end.")
        print("-1 gives you the last item.")
    else:
        print('Incorrect. The answer is b) "cherry".')
        print("In Python, -1 refers to the last element.")
    print()

    # Question 9 — true/false
    if ask_true_false(
        question_num=9,
        total=total,
        statement="Lists and tuples can both contain items of different types.",
        correct=True,
        explanation_correct="Both lists and tuples are heterogeneous — they can hold ints, strings, booleans, and more in the same collection.",
        explanation_incorrect="Python lists and tuples can both store mixed types: [1, 'hello', True] and (1, 'hello', True) are both valid.",
    ):
        score += 1

    # Question 10 — true/false
    if ask_true_false(
        question_num=10,
        total=total,
        statement="Dictionary keys must be unique, but values can repeat.",
        correct=True,
        explanation_correct="Each key appears once. If you assign to the same key again, it overwrites the old value. Values have no such restriction.",
        explanation_incorrect="Keys are unique identifiers. Assigning to an existing key replaces the value. Multiple keys can share the same value.",
    ):
        score += 1

    # Question 11 — code completion
    if ask_code_completion(
        question_num=11,
        total=total,
        prompt="Remove the last item from a list and store it in a variable:",
        code_lines=[
            "fruits = ['apple', 'banana', 'cherry']",
            "last = fruits.____()",
        ],
        correct_answers=["pop"],
        explanation_correct="pop() removes and returns the last item from the list.",
        explanation_incorrect="The pop() method removes the last item and returns it. del and remove() work differently.",
        case_sensitive=True,
    ):
        score += 1

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
