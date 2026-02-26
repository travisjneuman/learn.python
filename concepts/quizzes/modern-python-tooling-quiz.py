"""
Quiz: Modern Python Tooling
Review: concepts/modern-python-tooling.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Modern Python Tooling")
    print("  Review: concepts/modern-python-tooling.md")
    print("=" * 60)
    print()

    score = 0
    total = 11

    # Question 1
    print("Question 1/11: What does 'uv' replace in the Python toolchain?")
    print()
    print("  a) Python itself")
    print("  b) pip, venv, pip-tools, and pyenv")
    print("  c) pytest and ruff")
    print("  d) VS Code")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! uv is a single tool that replaces pip, venv,")
        print("pip-tools, and pyenv. It is written in Rust and very fast.")
    else:
        print("Incorrect. The answer is b).")
        print("uv handles package management, virtual environments, lock files,")
        print("and Python version management in one tool.")
    print()

    # Question 2
    print("Question 2/11: How fast is uv compared to pip?")
    print()
    print("  a) About the same speed")
    print("  b) 2-3x faster")
    print("  c) 10-100x faster")
    print("  d) Slower but more reliable")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! uv is written in Rust and is 10-100x faster than")
        print("pip for most operations.")
    else:
        print("Incorrect. The answer is c) 10-100x faster.")
        print("uv's speed comes from parallel downloads, caching, and Rust.")
    print()

    # Question 3
    print("Question 3/11: What does 'ruff' replace?")
    print()
    print("  a) pip and venv")
    print("  b) flake8 (linter), black (formatter), and isort (import sorter)")
    print("  c) pytest and mypy")
    print("  d) git and GitHub")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! ruff is a single tool that replaces flake8, black,")
        print("and isort — all much faster because ruff is written in Rust.")
    else:
        print("Incorrect. The answer is b).")
        print("ruff check replaces flake8, ruff format replaces black.")
    print()

    # Question 4
    print("Question 4/11: What command formats Python code with ruff?")
    print()
    print("  a) ruff lint .")
    print("  b) ruff format .")
    print("  c) ruff fix .")
    print("  d) ruff style .")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! 'ruff format .' formats all Python files.")
        print("'ruff check .' is for linting.")
    else:
        print("Incorrect. The answer is b) ruff format .")
        print("format = formatting, check = linting.")
    print()

    # Question 5
    print("Question 5/11: What is pyproject.toml?")
    print()
    print("  a) A Python script that configures projects")
    print("  b) The modern config file that replaces setup.py and")
    print("     scattered config files")
    print("  c) A template for Python projects")
    print("  d) A TOML file that only ruff uses")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! pyproject.toml consolidates project metadata, dependencies,")
        print("and tool configuration in one standard file.")
    else:
        print("Incorrect. The answer is b).")
        print("pyproject.toml replaces setup.py, setup.cfg, and per-tool")
        print("config files with a single standard file.")
    print()

    # Question 6
    print("Question 6/11: What Python 3.11+ feature shows the exact")
    print("expression that caused an error?")
    print()
    print("  a) Colored tracebacks")
    print("  b) Fine-grained error locations with underline indicators")
    print("  c) Auto-suggestions for fixes")
    print("  d) Error codes")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Python 3.11+ underlines the exact problematic")
        print("expression in error messages, not just the line.")
    else:
        print("Incorrect. The answer is b).")
        print("Python 3.11 shows arrows pointing to the exact sub-expression")
        print("that caused the error.")
    print()

    # Question 7
    print("Question 7/11: What does f'{x=}' print when x = 42?")
    print()
    print("  a) 42")
    print("  b) x=42")
    print("  c) x: 42")
    print("  d) {x=42}")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The = inside an f-string shows the expression and")
        print("its value. Very useful for debugging.")
    else:
        print("Incorrect. The answer is b) x=42.")
        print("f'{x=}' is shorthand for f'x={x}'.")
    print()

    # Question 8
    print("Question 8/11: What built-in module (Python 3.11+) parses")
    print("TOML files without third-party libraries?")
    print()
    print("  a) json")
    print("  b) tomllib")
    print("  c) configparser")
    print("  d) yaml")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! tomllib was added in Python 3.11 for reading TOML")
        print("files, including pyproject.toml.")
    else:
        print("Incorrect. The answer is b) tomllib.")
        print("tomllib reads TOML files. Open the file in 'rb' mode.")
    print()

    # Question 9
    print("Question 9/11: What does 'pip audit' do?")
    print()
    print("  a) Checks code for bugs")
    print("  b) Scans installed packages for known security vulnerabilities")
    print("  c) Audits your Python version")
    print("  d) Checks license compliance")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! pip-audit checks your dependencies against known")
        print("vulnerability databases.")
    else:
        print("Incorrect. The answer is b).")
        print("pip audit scans for known CVEs in your installed packages.")
    print()

    # Question 10
    print("Question 10/11: What is the risk of mixing pip and uv in the")
    print("same environment?")
    print()
    print("  a) It corrupts the virtual environment")
    print("  b) It can cause confusion about what is installed, though both")
    print("     work with the same .venv")
    print("  c) It is completely safe — no risk")
    print("  d) pip stops working after installing uv")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Both tools write to the same .venv, so they are")
        print("compatible, but mixing them can cause confusion. Pick one.")
    else:
        print("Incorrect. The answer is b).")
        print("They are compatible but can cause confusion. Stick with one.")
    print()

    # Question 11
    print("Question 11/11: What is the pip equivalent of 'uv venv'?")
    print()
    print("  a) pip create venv")
    print("  b) python -m venv .venv")
    print("  c) pip install venv")
    print("  d) pip venv create")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! 'uv venv' replaces 'python -m venv .venv'.")
        print("The rest of the workflow stays the same.")
    else:
        print("Incorrect. The answer is b) python -m venv .venv.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You know the modern Python toolchain.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/modern-python-tooling.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
