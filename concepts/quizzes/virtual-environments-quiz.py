"""
Quiz: Virtual Environments
Review: concepts/virtual-environments.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Virtual Environments")
    print("  Review: concepts/virtual-environments.md")
    print("=" * 60)
    print()

    score = 0
    total = 6

    # Question 1
    print("Question 1/6: What problem do virtual environments solve?")
    print()
    print("  a) They make Python run faster")
    print("  b) They isolate project dependencies so different projects")
    print("     can use different package versions without conflict")
    print("  c) They protect your code from viruses")
    print("  d) They let you run multiple Python scripts at once")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Each project gets its own isolated set of packages,")
        print("so version conflicts between projects are impossible.")
    else:
        print("Incorrect. The answer is b).")
        print("Virtual environments give each project its own private")
        print("package installation, preventing conflicts.")
    print()

    # Question 2
    print("Question 2/6: What command creates a virtual environment?")
    print()
    print("  a) pip install venv")
    print("  b) python -m venv .venv")
    print("  c) virtualenv create .venv")
    print("  d) python --venv .venv")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! python -m venv .venv creates a virtual environment")
        print("in a folder called .venv in your current directory.")
    else:
        print("Incorrect. The answer is b) python -m venv .venv")
        print("The -m flag runs the venv module as a script.")
    print()

    # Question 3
    print("Question 3/6: How do you know if your virtual environment")
    print("is activated?")
    print()
    print("  a) Python prints a message")
    print("  b) Your terminal prompt shows (.venv) at the beginning")
    print("  c) A new window opens")
    print("  d) The terminal changes color")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! When activated, your prompt changes to show")
        print("(.venv) — that is your confirmation.")
    else:
        print("Incorrect. The answer is b).")
        print("The (.venv) prefix on your terminal prompt means the")
        print("environment is active.")
    print()

    # Question 4
    print("Question 4/6: Should you commit the .venv/ folder to git?")
    print()
    print("  a) Yes, so teammates can use the same packages")
    print("  b) No — commit requirements.txt instead; teammates recreate")
    print("     the .venv from it")
    print("  c) Only if it is small")
    print("  d) Yes, but only on the main branch")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! .venv is large and machine-specific. Add it to")
        print(".gitignore. Share requirements.txt so others can recreate it.")
    else:
        print("Incorrect. The answer is b).")
        print("The .venv folder is not portable. requirements.txt is the")
        print("portable record of your dependencies.")
    print()

    # Question 5
    print("Question 5/6: What does 'pip freeze > requirements.txt' do?")
    print()
    print("  a) Installs packages from requirements.txt")
    print("  b) Deletes all installed packages")
    print("  c) Writes a list of all installed packages and their versions")
    print("     to requirements.txt")
    print("  d) Freezes the Python interpreter")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! pip freeze lists installed packages with exact")
        print("versions. The > redirects that list into a file.")
    else:
        print("Incorrect. The answer is c).")
        print("pip freeze outputs installed packages. > saves it to a file.")
        print("Use pip install -r requirements.txt to restore them.")
    print()

    # Question 6
    print("Question 6/6: What happens if you run 'pip install requests'")
    print("without activating a virtual environment?")
    print()
    print("  a) It installs into the project's .venv automatically")
    print("  b) It installs globally, affecting all projects on your system")
    print("  c) It fails with an error")
    print("  d) Nothing happens")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Without an active venv, pip installs globally.")
        print("Always check for (.venv) in your prompt before installing.")
    else:
        print("Incorrect. The answer is b).")
        print("Global installs can cause version conflicts between projects.")
        print("Always activate your venv first.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand virtual environments.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/virtual-environments.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
