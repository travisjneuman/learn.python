"""
Quiz: Files and Paths
Review: concepts/files-and-paths.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Files and Paths")
    print("  Review: concepts/files-and-paths.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print("Question 1/7: What is the recommended way to open a file?")
    print()
    print("  a) f = open('data.txt')")
    print("  b) with open('data.txt') as f:")
    print("  c) file = File('data.txt')")
    print("  d) import 'data.txt'")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The 'with' statement automatically closes the file")
        print("when the block ends, even if an error occurs.")
    else:
        print("Incorrect. The answer is b) with open('data.txt') as f:")
        print("Using 'with' ensures the file is properly closed.")
    print()

    # Question 2
    print('Question 2/7: What does the "w" mode do in open("file.txt", "w")?')
    print()
    print("  a) Opens for reading only")
    print("  b) Opens for writing — creates or overwrites the file")
    print("  c) Opens for appending to the end")
    print("  d) Opens in binary mode")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! 'w' opens for writing. It creates the file if it")
        print("does not exist, or erases everything if it does.")
    else:
        print("Incorrect. The answer is b).")
        print("'w' = write (overwrite), 'a' = append, 'r' = read (default).")
    print()

    # Question 3
    print("Question 3/7: What does .strip() do when reading file lines?")
    print()
    print("  a) Removes the file extension")
    print("  b) Removes whitespace and newline characters from both ends")
    print("  c) Splits the line into words")
    print("  d) Converts the line to lowercase")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! strip() removes leading and trailing whitespace,")
        print("including the \\n newline at the end of each line.")
    else:
        print("Incorrect. The answer is b).")
        print("strip() removes whitespace from both ends of a string,")
        print("which is essential when reading lines from files.")
    print()

    # Question 4
    print("Question 4/7: What is the difference between an absolute path")
    print("and a relative path?")
    print()
    print("  a) Absolute paths are for Windows, relative for Mac")
    print("  b) Absolute paths start from the root; relative paths")
    print("     start from your current location")
    print("  c) They are the same thing")
    print("  d) Relative paths are faster")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! An absolute path is the full address from the root.")
        print("A relative path is relative to where you are now.")
    else:
        print("Incorrect. The answer is b).")
        print("Absolute: C:/Users/alice/data.txt")
        print("Relative: data.txt (from current directory)")
    print()

    # Question 5
    print("Question 5/7: What does .. mean in a file path?")
    print()
    print("  a) The current directory")
    print("  b) The home directory")
    print("  c) The parent directory (one level up)")
    print("  d) A hidden file")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! .. means 'go up one directory level.'")
        print("So ../data.txt means: go up one folder, then find data.txt.")
    else:
        print("Incorrect. The answer is c) the parent directory.")
        print(". = current directory, .. = one level up.")
    print()

    # Question 6
    print("Question 6/7: What does this pathlib code return?")
    print()
    print('  from pathlib import Path')
    print('  p = Path("data/sample.txt")')
    print('  print(p.suffix)')
    print()
    print('  a) "data"')
    print('  b) "sample"')
    print('  c) ".txt"')
    print('  d) "sample.txt"')
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! .suffix returns the file extension including")
        print("the dot.")
    else:
        print('Incorrect. The answer is c) ".txt".')
        print(".suffix gives the extension, .stem gives the name without")
        print("the extension, .name gives the full filename.")
    print()

    # Question 7
    print("Question 7/7: Why is this Windows path problematic in Python?")
    print()
    print('  path = "C:\\Users\\alice\\new_file.txt"')
    print()
    print("  a) Windows paths are not supported")
    print("  b) The backslash \\n is interpreted as a newline character")
    print("  c) It is too long")
    print("  d) Nothing is wrong")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! \\n in a regular string becomes a newline.")
        print("Use raw strings (r'...'), double backslashes, or forward slashes.")
    else:
        print("Incorrect. The answer is b).")
        print("Backslash is an escape character in Python strings.")
        print("\\n becomes a newline, \\t becomes a tab, etc.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand files and paths well.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/files-and-paths.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
