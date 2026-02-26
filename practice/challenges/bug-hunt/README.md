# Bug Hunt Challenges

Welcome to Bug Hunt — exercises where you become the debugger.

## How It Works

Each exercise contains a short Python program that **looks correct** but has
hidden bugs. Your job:

1. **Read the code** and the description of what it should do.
2. **Run the program** and observe the output (or the crash).
3. **Find every bug** — each file has 3-5 intentional mistakes.
4. **Fix the bugs** so the program works correctly.
5. **Check your work** against the solution in `solutions/`.

## Why Bug Hunting?

Reading and debugging code is a separate skill from writing it. Professional
developers spend more time reading code than writing it. These exercises train
your eye to spot common Python pitfalls before they bite you in your own
projects.

## Exercise List

| File | Topic | Difficulty |
|------|-------|------------|
| `01_off_by_one.py` | Index errors, range(), list boundaries | Beginner |
| `02_scope_confusion.py` | Local vs global, variable shadowing | Beginner |
| `03_mutable_defaults.py` | Mutable default args, aliasing | Intermediate |
| `04_key_and_attribute_errors.py` | Dict keys, None checks, attributes | Intermediate |
| `05_file_handling_bugs.py` | File I/O, modes, encoding, paths | Intermediate |
| `06_comparison_traps.py` | `is` vs `==`, floats, truthy/falsy | Intermediate |

## Tips

- Read the error messages carefully — Python tells you exactly what went wrong.
- Run the code in small pieces if a file is long.
- Add `print()` statements to inspect variables.
- Compare your fixes with the solutions only after you have tried on your own.
