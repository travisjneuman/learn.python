"""
Quiz: Regex Explained
Review: concepts/regex-explained.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Regex Explained")
    print("  Review: concepts/regex-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: Why should you use raw strings (r'...') for regex?")
    print()
    print("  a) They run faster")
    print("  b) They prevent Python from interpreting backslashes before")
    print("     the regex engine sees them")
    print("  c) They are required by the re module")
    print("  d) They support Unicode")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Without r, Python interprets \\b as backspace instead")
        print("of a regex word boundary.")
    else:
        print("Incorrect. The answer is b).")
        print("Raw strings pass backslashes through to the regex engine unchanged.")
    print()

    # Question 2
    print("Question 2/12: What does \\d+ match?")
    print()
    print("  a) Exactly one digit")
    print("  b) One or more digits")
    print("  c) Zero or more digits")
    print("  d) Only the digit 0")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! \\d matches one digit, + means 'one or more'.")
        print("So \\d+ matches '5', '42', '12345', etc.")
    else:
        print("Incorrect. The answer is b) one or more digits.")
        print("\\d = digit, + = one or more.")
    print()

    # Question 3
    print("Question 3/12: What is the difference between re.match() and")
    print("re.search()?")
    print()
    print("  a) match() is case-insensitive, search() is case-sensitive")
    print("  b) match() only checks the beginning of the string,")
    print("     search() finds a match anywhere")
    print("  c) match() returns all matches, search() returns the first")
    print("  d) They are the same")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! re.match(r'\\d+', 'hello 42') is None because the")
        print("string does not START with digits. re.search() finds '42'.")
    else:
        print("Incorrect. The answer is b).")
        print("match = beginning only. search = anywhere in the string.")
    print()

    # Question 4
    print("Question 4/12: What does re.findall() return?")
    print()
    print("  a) The first match as a string")
    print("  b) A match object")
    print("  c) A list of all matching strings")
    print("  d) True or False")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! findall returns a list of all non-overlapping matches.")
    else:
        print("Incorrect. The answer is c) a list of all matching strings.")
        print("re.findall(r'\\d+', 'a1 b22 c333') returns ['1', '22', '333'].")
    print()

    # Question 5
    print("Question 5/12: What does the ? quantifier mean?")
    print()
    print("  a) Exactly one")
    print("  b) Zero or one (optional)")
    print("  c) One or more")
    print("  d) Zero or more")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! ? means the preceding element is optional.")
        print("colou?r matches both 'color' and 'colour'.")
    else:
        print("Incorrect. The answer is b) zero or one.")
        print("? makes something optional — it can appear 0 or 1 times.")
    print()

    # Question 6
    print("Question 6/12: What do parentheses () create in a regex?")
    print()
    print("  a) Optional groups")
    print("  b) Capturing groups that extract parts of the match")
    print("  c) Comments")
    print("  d) Alternation")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Groups let you extract specific parts of a match.")
        print("Use match.group(1), match.group(2), etc. to access them.")
    else:
        print("Incorrect. The answer is b) capturing groups.")
        print("(\\d{4})-(\\d{2}) captures the year and month separately.")
    print()

    # Question 7
    print("Question 7/12: What does \\b match?")
    print()
    print("  a) A backspace character")
    print("  b) A word boundary (the edge between a word and non-word character)")
    print("  c) A blank line")
    print("  d) A bold marker")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! \\bcat\\b matches 'cat' as a whole word, not 'catalog'.")
        print("Use raw strings (r'\\b') so Python does not interpret \\b as backspace.")
    else:
        print("Incorrect. The answer is b) a word boundary.")
        print("\\b prevents matching inside longer words.")
    print()

    # Question 8
    print("Question 8/12: What is the difference between greedy and lazy")
    print("matching?")
    print()
    print("  text = '<b>bold</b> and <b>more</b>'")
    print()
    print("  a) Greedy matches as much as possible, lazy matches as little")
    print("  b) Greedy is faster, lazy is slower")
    print("  c) Greedy matches one character, lazy matches all")
    print("  d) They produce the same result")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "a":
        score += 1
        print("Correct! <b>.*</b> (greedy) matches '<b>bold</b> and <b>more</b>'.")
        print("<b>.*?</b> (lazy, with ?) matches just '<b>bold</b>'.")
    else:
        print("Incorrect. The answer is a).")
        print("Add ? after a quantifier to make it lazy: *? +? ??")
    print()

    # Question 9
    print("Question 9/12: What does re.sub() do?")
    print()
    print("  a) Searches for a pattern")
    print("  b) Replaces all matches of a pattern with a replacement string")
    print("  c) Subtracts patterns")
    print("  d) Creates a sub-pattern")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! re.sub(pattern, replacement, text) replaces all matches.")
        print("re.sub(r'\\d', 'X', 'abc123') gives 'abcXXX'.")
    else:
        print("Incorrect. The answer is b).")
        print("sub = substitute. It replaces pattern matches with new text.")
    print()

    # Question 10
    print("Question 10/12: What does the re.IGNORECASE flag do?")
    print()
    print("  a) Ignores whitespace in the pattern")
    print("  b) Makes matching case-insensitive")
    print("  c) Ignores errors")
    print("  d) Ignores empty matches")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! With re.IGNORECASE, 'python' matches 'Python',")
        print("'PYTHON', 'python', etc.")
    else:
        print("Incorrect. The answer is b) case-insensitive matching.")
    print()

    # Question 11
    print("Question 11/12: What happens if re.search() finds no match?")
    print()
    print("  a) Returns an empty string")
    print("  b) Returns None")
    print("  c) Raises an exception")
    print("  d) Returns False")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! search() returns None when no match is found.")
        print("Always check 'if match:' before calling match.group().")
    else:
        print("Incorrect. The answer is b) None.")
        print("Calling .group() on None raises AttributeError. Always check first.")
    print()

    # Question 12
    print("Question 12/12: Why would you use re.compile()?")
    print()
    print("  a) To convert regex to a different format")
    print("  b) To precompile a pattern for faster reuse in loops")
    print("  c) To check if a pattern is valid")
    print("  d) To compile Python code")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! re.compile() creates a reusable pattern object.")
        print("This is faster when the same pattern is used many times.")
    else:
        print("Incorrect. The answer is b).")
        print("Compiled patterns avoid recompiling on every call in a loop.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand regular expressions well.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/regex-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
