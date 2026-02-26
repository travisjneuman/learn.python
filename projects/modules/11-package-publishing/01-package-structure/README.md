# Module 11 / Project 01 — Package Structure

Home: [README](../../../../README.md) · Module: [Package Publishing](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- The `src` layout for Python packages
- `pyproject.toml` configuration
- `__init__.py` and what it does
- Entry points (console scripts)

## Why this project exists

Before you can share your code as a pip-installable package, you need to structure it correctly. This project builds a real package from scratch and explains every file.

## Run

```bash
cd projects/modules/11-package-publishing/01-package-structure
python -m mymath.calculator
```

## Expected output

```text
mymath calculator v0.1.0
add(2, 3) = 5
subtract(10, 4) = 6
multiply(3, 7) = 21
divide(15, 4) = 3.75
```

## Project structure

```
01-package-structure/
├── pyproject.toml         # Package metadata and build config
├── README.md              # This file (also rendered on PyPI)
├── LICENSE                # MIT license
├── src/
│   └── mymath/
│       ├── __init__.py    # Makes mymath a package, exports version
│       ├── calculator.py  # Core math functions
│       └── statistics.py  # Mean, median, mode functions
└── tests/
    ├── test_calculator.py
    └── test_statistics.py
```

## Alter it

1. Add a new module `src/mymath/geometry.py` with `area_circle()` and `area_rectangle()`. Update `__init__.py` to export it.
2. Add a console script entry point in `pyproject.toml` so you can run `mymath-calc` from the command line.
3. Change the version to 0.2.0 and add a `__version__` attribute.

## Break it

1. Remove `__init__.py`. Can you still import mymath?
2. Put files directly in `mymath/` instead of `src/mymath/`. What changes?
3. Delete `pyproject.toml`. Can you still run the code? Can you build a package?

## Fix it

1. Restore `__init__.py` and verify imports work again.
2. If using flat layout, update `pyproject.toml` to find packages correctly.
3. Recreate `pyproject.toml` with the minimum required fields.

## Explain it

1. Why does the `src` layout exist? What problem does it solve?
2. What is the difference between a module and a package?
3. What does `__init__.py` do when you `import mymath`?
4. What is an entry point and why would you use one?

## Mastery check

You can move on when you can:
- create a package with the src layout from memory,
- explain what pyproject.toml fields are required,
- add a new module and export it from __init__.py,
- write tests for your package.

---

## Related Concepts

- [Errors and Debugging](../../../../concepts/errors-and-debugging.md)
- [How Imports Work](../../../../concepts/how-imports-work.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Quiz: Errors and Debugging](../../../../concepts/quizzes/errors-and-debugging-quiz.py)

## Next

[Project 02 — Build and Test](../02-build-and-test/)
