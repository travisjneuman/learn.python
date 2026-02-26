"""
Quiz: Jupyter Notebooks
Review: concepts/jupyter-notebooks.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Jupyter Notebooks")
    print("  Review: concepts/jupyter-notebooks.md")
    print("=" * 60)
    print()

    score = 0
    total = 10

    # Question 1
    print("Question 1/10: What are the two main types of cells in a")
    print("Jupyter notebook?")
    print()
    print("  a) Input and Output")
    print("  b) Code and Markdown")
    print("  c) Python and HTML")
    print("  d) Text and Image")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Code cells run Python, Markdown cells contain")
        print("formatted text for documentation.")
    else:
        print("Incorrect. The answer is b) Code and Markdown.")
    print()

    # Question 2
    print("Question 2/10: What keyboard shortcut runs a cell and moves")
    print("to the next one?")
    print()
    print("  a) Ctrl+Enter")
    print("  b) Shift+Enter")
    print("  c) Alt+Enter")
    print("  d) Tab+Enter")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Shift+Enter runs the current cell and advances.")
        print("Ctrl+Enter runs the cell but stays on it.")
    else:
        print("Incorrect. The answer is b) Shift+Enter.")
    print()

    # Question 3
    print("Question 3/10: What does the magic command %timeit do?")
    print()
    print("  a) Shows the current time")
    print("  b) Measures how long a line of code takes to run")
    print("  c) Sets a timer for the notebook session")
    print("  d) Counts the number of cells")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! %timeit runs a line multiple times and reports the")
        print("average execution time. %%timeit does the same for a full cell.")
    else:
        print("Incorrect. The answer is b).")
        print("%timeit benchmarks code by running it many times.")
    print()

    # Question 4
    print("Question 4/10: What is the danger of running cells out of order?")
    print()
    print("  a) The notebook crashes")
    print("  b) Variables may not exist or may have unexpected values")
    print("  c) Cells cannot be run out of order")
    print("  d) The kernel restarts")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Running cells out of order can reference undefined")
        print("variables or use stale values. Use 'Restart & Run All' to verify.")
    else:
        print("Incorrect. The answer is b).")
        print("Notebooks let you run cells in any order, which can create")
        print("confusing state. Always test with 'Restart & Run All'.")
    print()

    # Question 5
    print("Question 5/10: What is 'hidden state' in a notebook?")
    print()
    print("  a) Encrypted variables")
    print("  b) Variables that exist in memory from deleted cells")
    print("  c) Private class attributes")
    print("  d) Environment variables")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! If you delete a cell that defined a variable, the")
        print("variable still exists in memory until you restart the kernel.")
    else:
        print("Incorrect. The answer is b).")
        print("Deleting a cell does not remove its variables from memory.")
        print("'Restart & Run All' catches this problem.")
    print()

    # Question 6
    print("Question 6/10: How do you run a shell command from a notebook?")
    print()
    print("  a) shell('command')")
    print("  b) Prefix with ! like !pip install requests")
    print("  c) Use the os module only")
    print("  d) You cannot run shell commands")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! The ! prefix runs shell commands directly from a")
        print("code cell. Example: !pip install requests")
    else:
        print("Incorrect. The answer is b) prefix with !.")
        print("!command runs it in the system shell from within the notebook.")
    print()

    # Question 7
    print("Question 7/10: Why are .ipynb files problematic for git?")
    print()
    print("  a) Git cannot track them")
    print("  b) They are JSON with embedded output, creating messy diffs")
    print("  c) They are too large to commit")
    print("  d) Git corrupts them")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! .ipynb files are JSON that includes cell outputs")
        print("(images, data), making git diffs hard to read.")
        print("Use nbstripout or jupytext to solve this.")
    else:
        print("Incorrect. The answer is b).")
        print("Clear output before committing, or use nbstripout.")
    print()

    # Question 8
    print("Question 8/10: What is the recommended first step when sharing")
    print("a notebook?")
    print()
    print("  a) Export to PDF")
    print("  b) Run 'Restart & Run All' to verify it works from scratch")
    print("  c) Delete all markdown cells")
    print("  d) Convert to a .py file")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! 'Restart & Run All' ensures the notebook works")
        print("from a clean state with no hidden dependencies.")
    else:
        print("Incorrect. The answer is b).")
        print("Always verify with 'Restart & Run All' before sharing.")
    print()

    # Question 9
    print("Question 9/10: When should you use a .py script instead of")
    print("a notebook?")
    print()
    print("  a) When exploring data interactively")
    print("  b) When building reusable tools, library code, or production code")
    print("  c) When creating visualizations")
    print("  d) When teaching")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Notebooks are for exploration and presentation.")
        print("Scripts are for reusable, production, and library code.")
    else:
        print("Incorrect. The answer is b).")
        print("Start in a notebook, then extract reusable code into .py files.")
    print()

    # Question 10
    print("Question 10/10: What is JupyterLite?")
    print()
    print("  a) A lightweight version of Python")
    print("  b) A Jupyter environment that runs entirely in the browser")
    print("     with no installation")
    print("  c) A command-line only version of Jupyter")
    print("  d) A paid version of JupyterLab")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! JupyterLite runs in the browser using Pyodide")
        print("(Python compiled to WebAssembly) — no server needed.")
    else:
        print("Incorrect. The answer is b).")
        print("JupyterLite is browser-based, using WebAssembly. Great for")
        print("quick experiments without installing anything.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand Jupyter notebooks well.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/jupyter-notebooks.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
