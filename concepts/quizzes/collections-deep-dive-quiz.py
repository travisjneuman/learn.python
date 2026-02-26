"""
Quiz: Collections Deep Dive
Review: concepts/collections-deep-dive.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Collections Deep Dive")
    print("  Review: concepts/collections-deep-dive.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: What does Counter('mississippi') produce for")
    print("the letter 's'?")
    print()
    print("  a) 2")
    print("  b) 3")
    print("  c) 4")
    print("  d) 5")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! 'mississippi' has 4 s's.")
    else:
        print("Incorrect. The answer is c) 4.")
        print("Count the s's in 'mississippi': mi-ss-i-ss-ippi = 4.")
    print()

    # Question 2
    print("Question 2/12: What does Counter.most_common(2) return?")
    print()
    print("  a) The 2 least common items")
    print("  b) A list of the 2 most frequent (item, count) tuples")
    print("  c) The top 2 items as a dictionary")
    print("  d) Just the counts of the top 2 items")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! most_common(n) returns a list of (item, count) tuples.")
    else:
        print("Incorrect. The answer is b).")
        print("most_common(n) returns a list of the n most frequent")
        print("(element, count) pairs.")
    print()

    # Question 3
    print("Question 3/12: What does defaultdict(list) do when you access")
    print("a missing key?")
    print()
    print("  a) Raises a KeyError")
    print("  b) Returns None")
    print("  c) Creates the key with an empty list as the value")
    print("  d) Creates the key with value 0")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! defaultdict(list) automatically creates a new empty")
        print("list for any missing key.")
    else:
        print("Incorrect. The answer is c).")
        print("The factory function (list) is called to create the default value.")
    print()

    # Question 4
    print("Question 4/12: What is a gotcha with defaultdict?")
    print()
    print("  d = defaultdict(list)")
    print("  if d['missing_key']:")
    print("      pass")
    print()
    print("  a) It raises a KeyError")
    print("  b) It creates the key with an empty list just by checking it")
    print("  c) It returns True")
    print("  d) It deletes the key")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Accessing a missing key in defaultdict creates it.")
        print("Use 'key in d' to check without creating entries.")
    else:
        print("Incorrect. The answer is b).")
        print("Simply accessing d['missing_key'] creates the entry.")
        print("Use 'key in d' to check without side effects.")
    print()

    # Question 5
    print("Question 5/12: Can you modify a field of a namedtuple?")
    print()
    print("  Point = namedtuple('Point', ['x', 'y'])")
    print("  p = Point(3, 4)")
    print("  p.x = 5")
    print()
    print("  a) Yes, it works normally")
    print("  b) No, it raises an AttributeError because namedtuples are immutable")
    print("  c) Yes, but it creates a new tuple")
    print("  d) No, it raises a TypeError")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Namedtuples are immutable. Use _replace() to create")
        print("a modified copy instead.")
    else:
        print("Incorrect. The answer is b) AttributeError.")
        print("Use p._replace(x=5) to create a new namedtuple with a changed field.")
    print()

    # Question 6
    print("Question 6/12: What is the time complexity of deque.appendleft()")
    print("compared to list.insert(0, x)?")
    print()
    print("  a) Both are O(1)")
    print("  b) deque is O(1), list is O(n)")
    print("  c) Both are O(n)")
    print("  d) deque is O(n), list is O(1)")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! deque.appendleft() is O(1) because deque is optimized")
        print("for both ends. list.insert(0, x) is O(n) — it shifts every element.")
    else:
        print("Incorrect. The answer is b).")
        print("deque is O(1) at both ends; list.insert(0, x) is O(n).")
    print()

    # Question 7
    print("Question 7/12: What does deque(maxlen=5) do when you append")
    print("a 6th item?")
    print()
    print("  a) Raises an error")
    print("  b) Ignores the new item")
    print("  c) Automatically removes the oldest item from the other end")
    print("  d) Doubles the maxlen")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! A deque with maxlen automatically discards items")
        print("from the opposite end to stay within the limit.")
    else:
        print("Incorrect. The answer is c).")
        print("With maxlen, the deque acts as a fixed-size buffer, dropping")
        print("old items to make room for new ones.")
    print()

    # Question 8
    print("Question 8/12: How does OrderedDict differ from a regular dict")
    print("in Python 3.7+?")
    print()
    print("  a) Regular dicts do not maintain insertion order")
    print("  b) OrderedDict considers order in equality comparisons")
    print("  c) OrderedDict is faster")
    print("  d) There is no difference")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Both maintain insertion order, but OrderedDict")
        print("considers order when comparing equality. Regular dicts do not.")
    else:
        print("Incorrect. The answer is b).")
        print("OrderedDict([('a',1),('b',2)]) != OrderedDict([('b',2),('a',1)])")
        print("but {'a':1,'b':2} == {'b':2,'a':1}.")
    print()

    # Question 9
    print("Question 9/12: What does ChainMap do?")
    print()
    print("  a) Chains multiple lists together")
    print("  b) Groups dictionaries so lookups search each one in order")
    print("  c) Merges dictionaries into a single new dictionary")
    print("  d) Creates a linked list of maps")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! ChainMap searches multiple dictionaries in order,")
        print("returning the first match found.")
    else:
        print("Incorrect. The answer is b).")
        print("ChainMap groups dicts for layered lookups (e.g., CLI args,")
        print("user prefs, defaults) without merging them.")
    print()

    # Question 10
    print("Question 10/12: What does Counter support that regular dicts")
    print("do not?")
    print()
    print("  a) Key-value pairs")
    print("  b) Arithmetic operations like + and - between Counters")
    print("  c) Iteration")
    print("  d) String keys")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! You can add, subtract, intersect (&), and union (|)")
        print("Counters together.")
    else:
        print("Incorrect. The answer is b).")
        print("Counter supports +, -, &, | for combining counts.")
    print()

    # Question 11
    print("Question 11/12: Why does Counter([ [1,2], [3,4] ]) raise a")
    print("TypeError?")
    print()
    print("  a) Counter does not accept lists")
    print("  b) Lists are not hashable, and Counter keys must be hashable")
    print("  c) You can only count strings")
    print("  d) The list is too short")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Counter uses a dict internally, and dict keys must")
        print("be hashable. Lists are not hashable; use tuples instead.")
    else:
        print("Incorrect. The answer is b).")
        print("Convert lists to tuples: Counter([(1,2), (3,4)]).")
    print()

    # Question 12
    print("Question 12/12: Which collection type would you use for a")
    print("fixed-size 'recent items' buffer?")
    print()
    print("  a) Counter")
    print("  b) defaultdict")
    print("  c) deque with maxlen")
    print("  d) OrderedDict")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! deque(maxlen=n) automatically discards the oldest")
        print("items when the buffer is full.")
    else:
        print("Incorrect. The answer is c) deque with maxlen.")
        print("deque(maxlen=n) is perfect for sliding windows and")
        print("recent-items buffers.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You know the collections module well.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/collections-deep-dive.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
