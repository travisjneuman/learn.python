"""
Quiz: Generators and Iterators
Review: concepts/generators-and-iterators.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Generators and Iterators")
    print("  Review: concepts/generators-and-iterators.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: What keyword makes a function a generator?")
    print()
    print("  a) return")
    print("  b) yield")
    print("  c) generate")
    print("  d) next")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! yield pauses the function and produces a value.")
        print("The function resumes where it left off on the next call.")
    else:
        print("Incorrect. The answer is b) yield.")
        print("yield turns a regular function into a generator function.")
    print()

    # Question 2
    print("Question 2/12: What happens when you call a generator function?")
    print()
    print("  def count(n):")
    print("      for i in range(n):")
    print("          yield i")
    print()
    print("  result = count(5)")
    print()
    print("  a) It runs the function and returns a list")
    print("  b) It returns a generator object without running any code")
    print("  c) It prints the numbers 0-4")
    print("  d) It raises an error")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Calling a generator function does not execute it.")
        print("It returns a generator object. Code runs when you iterate.")
    else:
        print("Incorrect. The answer is b).")
        print("The function body does not run until you call next() or iterate.")
    print()

    # Question 3
    print("Question 3/12: What does next() do with a generator?")
    print()
    print("  a) Resets the generator to the beginning")
    print("  b) Advances to the next yield and returns the value")
    print("  c) Skips an item")
    print("  d) Closes the generator")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! next(gen) runs the generator until the next yield,")
        print("then returns the yielded value.")
    else:
        print("Incorrect. The answer is b).")
        print("next() advances to the next yield point and returns the value.")
    print()

    # Question 4
    print("Question 4/12: What exception is raised when a generator is")
    print("exhausted?")
    print()
    print("  a) GeneratorError")
    print("  b) ValueError")
    print("  c) StopIteration")
    print("  d) IndexError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! StopIteration signals that there are no more values.")
        print("For loops catch this automatically.")
    else:
        print("Incorrect. The answer is c) StopIteration.")
        print("This is the standard protocol for ending iteration.")
    print()

    # Question 5
    print("Question 5/12: How much memory does a generator expression use")
    print("compared to a list comprehension for 1 million items?")
    print()
    print("  a) About the same")
    print("  b) Roughly 100 bytes vs ~8 MB")
    print("  c) Generators use more memory")
    print("  d) It depends on the data type")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! A generator stores almost nothing (~100 bytes).")
        print("A list with 1M items uses ~8 MB. Generators compute on demand.")
    else:
        print("Incorrect. The answer is b).")
        print("Generators are lazy — they produce values one at a time,")
        print("using almost no memory regardless of sequence size.")
    print()

    # Question 6
    print("Question 6/12: What happens if you try to iterate over a")
    print("generator twice?")
    print()
    print("  gen = (x for x in range(3))")
    print("  list(gen)    # [0, 1, 2]")
    print("  list(gen)    # ???")
    print()
    print("  a) [0, 1, 2] again")
    print("  b) [] — empty, generators are exhausted after one pass")
    print("  c) An error")
    print("  d) [2, 1, 0] — reversed")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Generators can only be consumed once. The second")
        print("list(gen) returns an empty list.")
    else:
        print("Incorrect. The answer is b) empty list.")
        print("Generators are single-use. Create a new one to iterate again.")
    print()

    # Question 7
    print("Question 7/12: What is the syntax difference between a list")
    print("comprehension and a generator expression?")
    print()
    print("  a) Generators use {} instead of []")
    print("  b) Generators use () instead of []")
    print("  c) Generators use <> instead of []")
    print("  d) There is no syntax difference")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! [x for x in items] is a list comprehension.")
        print("(x for x in items) is a generator expression.")
    else:
        print("Incorrect. The answer is b) () instead of [].")
    print()

    # Question 8
    print("Question 8/12: What does 'yield from' do?")
    print()
    print("  def combined(n):")
    print("      yield from range(n)")
    print("      yield from range(n, 0, -1)")
    print()
    print("  a) Returns from a generator")
    print("  b) Delegates to another iterable, yielding all its values")
    print("  c) Creates a nested generator")
    print("  d) Yields the iterable itself as a single value")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! 'yield from iterable' yields each item from the")
        print("iterable, replacing a for loop with yield.")
    else:
        print("Incorrect. The answer is b).")
        print("yield from delegates to another iterable, yielding all its items.")
    print()

    # Question 9
    print("Question 9/12: What is a generator pipeline?")
    print()
    print("  a) A way to run generators in parallel")
    print("  b) Chaining generators where each one processes output from")
    print("     the previous one, without intermediate lists")
    print("  c) A generator that produces other generators")
    print("  d) A way to make generators faster")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Pipelines chain generators: read_lines() | filter()")
        print("| transform(). Each pulls one value at a time from the previous.")
    else:
        print("Incorrect. The answer is b).")
        print("Pipelines process data lazily through multiple stages without")
        print("loading everything into memory.")
    print()

    # Question 10
    print("Question 10/12: Can you index a generator with gen[3]?")
    print()
    print("  a) Yes, just like a list")
    print("  b) No — generators are not subscriptable")
    print("  c) Yes, but only for the first 10 items")
    print("  d) Yes, but it is slow")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Generators do not support indexing. Use")
        print("itertools.islice or convert to a list first.")
    else:
        print("Incorrect. The answer is b).")
        print("gen[3] raises TypeError. Use itertools.islice(gen, 3, 4).")
    print()

    # Question 11
    print("Question 11/12: What does gen.send(value) do?")
    print()
    print("  a) Sends a value to an external API")
    print("  b) Sends a value INTO the generator, resuming it at the yield")
    print("  c) Returns a value from the generator")
    print("  d) Resets the generator with a new starting value")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! send() resumes the generator and the sent value")
        print("becomes the result of the yield expression inside.")
    else:
        print("Incorrect. The answer is b).")
        print("send() enables two-way communication with a generator.")
    print()

    # Question 12
    print("Question 12/12: Why are generators essential for processing")
    print("large files?")
    print()
    print("  a) They read files faster than normal methods")
    print("  b) They process one line at a time without loading the entire")
    print("     file into memory")
    print("  c) They compress files automatically")
    print("  d) They can read binary files")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! A generator that yields lines one at a time can")
        print("process a 10 GB file using almost no memory.")
    else:
        print("Incorrect. The answer is b).")
        print("Generators enable streaming — processing data one piece at")
        print("a time without loading everything into memory.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand generators and iterators.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/generators-and-iterators.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
