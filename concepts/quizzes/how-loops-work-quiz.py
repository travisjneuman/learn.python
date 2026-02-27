"""
Quiz: How Loops Work
Review: concepts/how-loops-work.md
"""

from _quiz_helpers import normalize_answer, ask_true_false, ask_code_completion


def run_quiz():
    print("=" * 60)
    print("  QUIZ: How Loops Work")
    print("  Review: concepts/how-loops-work.md")
    print("=" * 60)
    print()

    score = 0
    total = 10

    # Question 1
    print("Question 1/10: What does range(5) produce?")
    print()
    print("  a) 1, 2, 3, 4, 5")
    print("  b) 0, 1, 2, 3, 4")
    print("  c) 0, 1, 2, 3, 4, 5")
    print("  d) 1, 2, 3, 4")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! range(5) starts at 0 and stops before 5,")
        print("giving you 0, 1, 2, 3, 4.")
    else:
        print("Incorrect. The answer is b) 0, 1, 2, 3, 4.")
        print("range() starts at 0 by default and stops BEFORE the number.")
    print()

    # Question 2
    print("Question 2/10: What will this code print?")
    print()
    print('  for letter in "Hi":')
    print("      print(letter)")
    print()
    print("  a) Hi")
    print("  b) H then i (on separate lines)")
    print("  c) H i")
    print("  d) Error")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! A for loop over a string goes through each")
        print("character one at a time.")
    else:
        print("Incorrect. The answer is b). A for loop iterates over")
        print("each character in the string individually.")
    print()

    # Question 3
    print("Question 3/10: When should you use a while loop instead of")
    print("a for loop?")
    print()
    print("  a) When you know exactly how many times to repeat")
    print("  b) When you are going through a list")
    print("  c) When you do not know when to stop")
    print("  d) Always — while loops are better")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Use while when you are waiting for a condition")
        print("to change, and you don't know how many iterations that takes.")
    else:
        print("Incorrect. The answer is c). While loops are for when you")
        print("don't know the number of iterations in advance.")
    print()

    # Question 4
    print("Question 4/10: What is wrong with this code?")
    print()
    print("  count = 1")
    print("  while count <= 5:")
    print("      print(count)")
    print()
    print("  a) count should start at 0")
    print("  b) The condition should be count < 5")
    print("  c) count is never updated, so it loops forever")
    print("  d) Nothing is wrong")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Without count = count + 1 inside the loop,")
        print("count stays at 1 forever, creating an infinite loop.")
    else:
        print("Incorrect. The answer is c). The loop never updates count,")
        print("so the condition is always True, causing an infinite loop.")
    print()

    # Question 5
    print("Question 5/10: What does range(2, 8, 2) produce?")
    print()
    print("  a) 2, 4, 6, 8")
    print("  b) 2, 4, 6")
    print("  c) 2, 3, 4, 5, 6, 7")
    print("  d) 2, 8, 2")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! range(2, 8, 2) starts at 2, steps by 2, and")
        print("stops before 8: 2, 4, 6.")
    else:
        print("Incorrect. The answer is b) 2, 4, 6.")
        print("The third argument is the step. range stops BEFORE 8.")
    print()

    # Question 6
    print("Question 6/10: How many times does this loop print?")
    print()
    print("  for i in range(3):")
    print('      print("hello")')
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "3":
        score += 1
        print("Correct! range(3) produces 0, 1, 2 — three values,")
        print("so the loop runs three times.")
    else:
        print("Incorrect. The answer is 3.")
        print("range(3) gives 0, 1, 2 — that is three iterations.")
    print()

    # Question 7
    print("Question 7/10: Why is it dangerous to modify a list while")
    print("looping over it?")
    print()
    print("  a) It causes a SyntaxError")
    print("  b) It can skip items or produce unpredictable behavior")
    print("  c) Python automatically prevents it")
    print("  d) It deletes the list")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Removing items shifts the indexes, causing the")
        print("loop to skip items or behave unpredictably.")
    else:
        print("Incorrect. The answer is b). Modifying a list during")
        print("iteration can skip items. Build a new list instead.")
    print()

    # Question 8 — true/false
    if ask_true_false(
        question_num=8,
        total=total,
        statement="A for loop and a while loop can always be used interchangeably.",
        correct=False,
        explanation_correct="While they can often achieve the same result, for loops are best when you know the number of iterations, and while loops are best when you are waiting for a condition.",
        explanation_incorrect="For loops iterate over a known sequence. While loops repeat until a condition becomes false. They have different strengths.",
    ):
        score += 1

    # Question 9 — code completion
    if ask_code_completion(
        question_num=9,
        total=total,
        prompt="Complete the loop so it prints numbers 0 through 4:",
        code_lines=[
            "for i in ____(5):",
            "    print(i)",
        ],
        correct_answers=["range"],
        explanation_correct="range(5) produces 0, 1, 2, 3, 4.",
        explanation_incorrect="The range() function generates a sequence of numbers.",
        case_sensitive=True,
    ):
        score += 1

    # Question 10 — code completion
    if ask_code_completion(
        question_num=10,
        total=total,
        prompt="What keyword exits a loop immediately?",
        code_lines=[
            "while True:",
            "    user = input('Type quit to exit: ')",
            "    if user == 'quit':",
            "        ____",
        ],
        correct_answers=["break"],
        explanation_correct="break exits the nearest enclosing loop right away.",
        explanation_incorrect="The break keyword stops the loop and continues with the code after it.",
        case_sensitive=True,
    ):
        score += 1

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand loops thoroughly.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/how-loops-work.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
