"""
Quiz: functools and itertools
Review: concepts/functools-and-itertools.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: functools and itertools")
    print("  Review: concepts/functools-and-itertools.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: What does @lru_cache do?")
    print()
    print("  a) Makes a function run in a separate thread")
    print("  b) Caches results so repeated calls with the same arguments")
    print("     return instantly")
    print("  c) Limits how many times a function can be called")
    print("  d) Logs function calls")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! lru_cache stores results in memory so the same")
        print("computation is never repeated.")
    else:
        print("Incorrect. The answer is b).")
        print("lru_cache is automatic memoization — it remembers results.")
    print()

    # Question 2
    print("Question 2/12: What does 'maxsize=128' mean in @lru_cache?")
    print()
    print("  a) Maximum input size")
    print("  b) Keeps the 128 most recent results in cache")
    print("  c) Maximum number of function calls")
    print("  d) Maximum argument value")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! maxsize controls how many results are cached.")
        print("Use maxsize=None for unlimited cache.")
    else:
        print("Incorrect. The answer is b).")
        print("It is an LRU (Least Recently Used) cache with a size limit.")
    print()

    # Question 3
    print("Question 3/12: What does functools.partial do?")
    print()
    print("  square = partial(power, exponent=2)")
    print()
    print("  a) Runs only part of a function")
    print("  b) Creates a new function with some arguments pre-filled")
    print("  c) Splits a function into two halves")
    print("  d) Makes a function partial (incomplete)")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! partial creates a new function with some arguments")
        print("already set, so you call it with fewer arguments.")
    else:
        print("Incorrect. The answer is b).")
        print("partial(power, exponent=2) creates a 'square' function.")
    print()

    # Question 4
    print("Question 4/12: What does functools.reduce do?")
    print()
    print("  a) Reduces the size of a list")
    print("  b) Applies a function cumulatively, reducing a sequence to one value")
    print("  c) Removes duplicates from a list")
    print("  d) Compresses data")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! reduce applies a two-argument function cumulatively.")
        print("reduce(lambda a, b: a + b, [1,2,3,4]) gives 10.")
    else:
        print("Incorrect. The answer is b).")
        print("reduce folds a sequence into a single value by applying a")
        print("function to pairs of elements.")
    print()

    # Question 5
    print("Question 5/12: What does @wraps(func) do in a decorator?")
    print()
    print("  a) Wraps the function in a try/except")
    print("  b) Copies the original function's name, docstring, etc. to the wrapper")
    print("  c) Makes the decorator reusable")
    print("  d) Prevents the function from being called directly")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Without @wraps, the decorated function would lose")
        print("its original __name__ and __doc__.")
    else:
        print("Incorrect. The answer is b).")
        print("@wraps preserves function metadata like __name__ and __doc__.")
    print()

    # Question 6
    print("Question 6/12: What does itertools.chain(a, b, c) do?")
    print()
    print("  a) Creates a linked list")
    print("  b) Combines multiple iterables into one sequential iterable")
    print("  c) Runs functions in sequence")
    print("  d) Merges dictionaries")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! chain yields items from the first iterable, then")
        print("the second, then the third, etc.")
    else:
        print("Incorrect. The answer is b).")
        print("chain([1,2], [3,4]) produces 1, 2, 3, 4.")
    print()

    # Question 7
    print("Question 7/12: What is a critical requirement for groupby to")
    print("work correctly?")
    print()
    print("  a) The data must be a list (not a generator)")
    print("  b) The data must be sorted by the grouping key")
    print("  c) The data must contain strings only")
    print("  d) The data must have no duplicates")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! groupby only groups consecutive items with the same")
        print("key. If data is not sorted, you get multiple groups for the")
        print("same key.")
    else:
        print("Incorrect. The answer is b) data must be sorted by key.")
        print("Always sort before groupby.")
    print()

    # Question 8
    print("Question 8/12: What does itertools.product(['a','b'], [1,2])")
    print("produce?")
    print()
    print("  a) [('a', 1), ('b', 2)]")
    print("  b) [('a', 1), ('a', 2), ('b', 1), ('b', 2)]")
    print("  c) ['a1', 'a2', 'b1', 'b2']")
    print("  d) [('a', 'b'), (1, 2)]")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! product gives all combinations (cartesian product).")
    else:
        print("Incorrect. The answer is b).")
        print("product creates every possible pair from the two iterables.")
    print()

    # Question 9
    print("Question 9/12: What is the difference between combinations")
    print("and permutations?")
    print()
    print("  a) combinations allows repeats, permutations does not")
    print("  b) combinations ignores order, permutations considers order")
    print("  c) They are the same thing")
    print("  d) permutations ignores order, combinations considers order")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! combinations('AB', 2) gives (A,B) only.")
        print("permutations('AB', 2) gives (A,B) and (B,A).")
    else:
        print("Incorrect. The answer is b).")
        print("Combinations: order does not matter. Permutations: order matters.")
    print()

    # Question 10
    print("Question 10/12: Why can you not use [start:stop] slicing on")
    print("a generator?")
    print()
    print("  a) Generators do not support indexing — use itertools.islice")
    print("  b) Generators only produce strings")
    print("  c) Slicing is a list-only feature")
    print("  d) You can — it works the same way")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "a":
        score += 1
        print("Correct! Generators are not subscriptable. Use islice(gen, start, stop)")
        print("to slice them.")
    else:
        print("Incorrect. The answer is a).")
        print("Use itertools.islice for slicing generators.")
    print()

    # Question 11
    print("Question 11/12: Why does @lru_cache fail if you pass a list")
    print("as an argument?")
    print()
    print("  a) Lists are too long")
    print("  b) Lists are not hashable, and cache keys must be hashable")
    print("  c) lru_cache only works with numbers")
    print("  d) Lists cannot be function arguments")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Cache keys are based on the arguments, which must")
        print("be hashable. Convert lists to tuples first.")
    else:
        print("Incorrect. The answer is b).")
        print("Use tuples instead of lists when calling cached functions.")
    print()

    # Question 12
    print("Question 12/12: What happens if you store groupby groups")
    print("without materializing them?")
    print()
    print("  groups = []")
    print("  for key, group in groupby(data, key_func):")
    print("      groups.append((key, group))")
    print()
    print("  a) It works correctly")
    print("  b) The group iterators are consumed when advancing to the next group")
    print("  c) It raises an error")
    print("  d) The groups are duplicated")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! You must materialize groups immediately with list(group).")
        print("The group iterator is invalidated when the next group starts.")
    else:
        print("Incorrect. The answer is b).")
        print("Use: groups = [(key, list(group)) for key, group in groupby(...)]")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You know functools and itertools well.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/functools-and-itertools.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
