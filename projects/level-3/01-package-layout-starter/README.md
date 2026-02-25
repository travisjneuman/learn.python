# Level 3 / Project 01 - Package Layout Starter
Home: [README](../../../README.md)

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

## Alter it (required)
1. Add a `--recursive` flag to scan nested packages.
2. Add a `pyproject.toml` generator alongside `__init__.py`.
3. Count lines of code per module and include in the report.

## Break it (required)
1. Point the scanner at a directory with no `.py` files.
2. Create a circular import between two modules — does validation catch it?
3. Scan a file (not a directory) — what error appears?

## Fix it (required)
1. Add a check that the path is a directory, not a file.
2. Improve circular import detection heuristic.
3. Handle permission errors when scanning directories.

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

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-cli-arguments-workbench/README.md) |
|:---|:---:|---:|
