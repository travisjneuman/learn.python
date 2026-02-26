# Level 3 / Project 01 - Package Layout Starter
Home: [README](../../../README.md)

> **Try in Browser:** [Practice similar concepts online](../../browser/level-2.html?ex=1) — browser exercises cover Level 2 topics

## Before You Start

Recall these prerequisites before diving in:
- Can you use `try/except` to handle a `FileNotFoundError`?
- Can you import a function from another file? (`from mymodule import my_function`)
- Can you use `pathlib.Path` to check if a path is a file or directory?

**Estimated time:** 30 minutes

## Focus
- project layout and import boundaries

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/01-package-layout-starter
python project.py scan .
python project.py validate .
python project.py init .
pytest -q
```

## Expected terminal output
```text
{"name": "01-package-layout-starter", "modules": [...]}
8 passed
```

## Expected artifacts
- Package info JSON on stdout
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that scans a directory and returns a summary of file types.

**Step 1: Use pathlib to iterate files.**

```python
from pathlib import Path
from collections import Counter

def scan_file_types(directory):
    path = Path(directory)
    if not path.is_dir():
        raise ValueError(f"Not a directory: {directory}")
    extensions = Counter()
    for item in path.rglob("*"):
        if item.is_file():
            ext = item.suffix or "(no extension)"
            extensions[ext] += 1
    return dict(extensions.most_common())
```

**Step 2: Think about the structure.** `scan_file_types("my_project")` returns `{".py": 12, ".md": 3, ".txt": 1}`.

**Step 3: Think about edge cases.** Empty directory returns `{}`. Non-existent directory should raise an error, not silently return empty.

**The thought process:** Validate input first (is it a directory?). Use `pathlib` for cross-platform path handling. Use `Counter` for counting. This is the same approach the package layout scanner uses.

## Design First
Before writing code, sketch your approach in `notes.md`:
- What functions or classes do you need?
- What data structures will you use?
- What's the flow from input to output?
- What could go wrong?

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Try adding support for nested packages — what flag or argument would make sense?
2. What other metadata could the scanner generate beyond what it already does?
3. Add a useful metric to the report output.

## Break it (required) — Core
1. Try pointing the scanner at something unexpected — what breaks first?
2. Can you create a situation where imports get confused?
3. What happens when the input is not what the tool expects?

## Fix it (required) — Core
1. Add input validation for the most obvious failure case you found.
2. Improve how the tool handles the import issue you discovered.
3. Make the tool resilient to permission problems.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What makes a directory a Python package (hint: `__init__.py`)?
2. What is `__all__` and how does it control `from package import *`?
3. Why use `@dataclass` instead of writing `__init__` manually?
4. What is the difference between a module and a package?

## Mastery check
You can move on when you can:
- create a Python package from scratch with proper structure,
- explain what `__init__.py` does and when it is optional (Python 3.3+),
- describe how `from package import module` resolves the import,
- use dataclasses for structured data instead of plain dicts.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Package Layout Starter. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am confused about the difference between a Python module and a package. Can you explain with a simple directory structure example?"
- "Can you explain what `__init__.py` does and why Python packages need it?"

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-cli-arguments-workbench/README.md) |
|:---|:---:|---:|
