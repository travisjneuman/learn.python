"""
Quiz: The Terminal — Going Deeper
Review: concepts/the-terminal-deeper.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: The Terminal — Going Deeper")
    print("  Review: concepts/the-terminal-deeper.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print("Question 1/7: What does the pipe symbol | do in the terminal?")
    print()
    print("  a) Separates two unrelated commands")
    print("  b) Sends the output of one command as input to the next")
    print("  c) Runs two commands at the same time")
    print("  d) Creates a new file")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! The pipe connects commands. The output of the")
        print("left command becomes the input of the right command.")
    else:
        print("Incorrect. The answer is b).")
        print("Example: ls | wc -l counts files by piping the file list")
        print("into the line counter.")
    print()

    # Question 2
    print("Question 2/7: What is the difference between > and >> ?")
    print()
    print("  a) > is for text files, >> is for binary files")
    print("  b) > overwrites the file, >> appends to the end")
    print("  c) > creates a file, >> deletes a file")
    print("  d) They do the same thing")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! > writes output to a file (replacing contents).")
        print(">> adds output to the end of an existing file.")
    else:
        print("Incorrect. The answer is b).")
        print("> overwrites, >> appends. Use >> to add to logs without")
        print("losing previous content.")
    print()

    # Question 3
    print("Question 3/7: What does Ctrl+C do in the terminal?")
    print()
    print("  a) Copies text to clipboard")
    print("  b) Clears the screen")
    print("  c) Stops the currently running command")
    print("  d) Closes the terminal")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! Ctrl+C sends an interrupt signal that stops the")
        print("current process. Essential for stopping infinite loops.")
    else:
        print("Incorrect. The answer is c).")
        print("Ctrl+C interrupts the running command. It does not copy")
        print("text in the terminal (that is different from GUI copy).")
    print()

    # Question 4
    print("Question 4/7: What does this command do?")
    print()
    print("  export API_KEY='abc123'")
    print()
    print("  a) Installs the API_KEY package")
    print("  b) Sets an environment variable for the current session")
    print("  c) Saves API_KEY permanently to a file")
    print("  d) Sends abc123 to an API")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! export sets an environment variable that programs")
        print("can read. It lasts only for the current terminal session.")
    else:
        print("Incorrect. The answer is b).")
        print("export creates a temporary environment variable. Programs")
        print("read it with os.environ in Python.")
    print()

    # Question 5
    print("Question 5/7: What does && do between commands?")
    print()
    print("  python -m pytest && echo 'All tests passed!'")
    print()
    print("  a) Runs both commands regardless of success")
    print("  b) Runs the second command only if the first succeeds")
    print("  c) Runs both commands at the same time")
    print("  d) Combines the output of both commands")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! && means 'run the next command only if the")
        print("previous one succeeded (exit code 0).'")
    else:
        print("Incorrect. The answer is b).")
        print("&& is conditional: the second command runs only on success.")
        print("Use ; to run regardless, || to run only on failure.")
    print()

    # Question 6
    print("Question 6/7: Why should .env files not be committed to git?")
    print()
    print("  a) They are too large")
    print("  b) They contain secrets like API keys and passwords")
    print("  c) Git cannot read .env files")
    print("  d) They slow down the repository")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! .env files contain sensitive configuration like")
        print("API keys and database passwords. Add .env to .gitignore.")
    else:
        print("Incorrect. The answer is b).")
        print("Committing secrets to git is a security risk. Anyone")
        print("with access to the repo can see them.")
    print()

    # Question 7
    print("Question 7/7: What does the 'which python' command show you?")
    print()
    print("  a) The version of Python installed")
    print("  b) The file path where the python command lives")
    print("  c) A list of all Python packages")
    print("  d) Whether Python is installed")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! 'which' shows the full path to the command.")
        print("Useful for checking if you are using the right Python")
        print("(system vs virtual environment).")
    else:
        print("Incorrect. The answer is b).")
        print("'which python' might show /usr/bin/python or .venv/bin/python,")
        print("telling you exactly which Python you are using.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You are comfortable with advanced terminal use.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/the-terminal-deeper.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
