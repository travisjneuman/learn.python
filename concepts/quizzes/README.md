# Concept Quizzes

Interactive terminal quizzes that test your understanding of each concept doc in `concepts/`.

## How to Run

Each quiz is a standalone Python script with zero dependencies. Run any quiz from the repo root or the `concepts/quizzes/` directory:

```bash
python concepts/quizzes/what-is-a-variable-quiz.py
python concepts/quizzes/how-loops-work-quiz.py
python concepts/quizzes/functions-explained-quiz.py
# ... etc.
```

No virtual environment or pip install needed -- every quiz uses only the Python standard library.

## What They Test

Each quiz matches one concept doc and tests *understanding*, not memorization. You will see questions like "What will this code print?" and "Which approach is correct?" rather than "What page covers X?"

## Quiz List

| Quiz Script | Concept Doc | Topics |
|---|---|---|
| `what-is-a-variable-quiz.py` | `what-is-a-variable.md` | Naming rules, assignment vs comparison, scope |
| `how-loops-work-quiz.py` | `how-loops-work.md` | for/while loops, range(), common pitfalls |
| `functions-explained-quiz.py` | `functions-explained.md` | def, return, parameters, default values |
| `collections-explained-quiz.py` | `collections-explained.md` | Lists, dicts, sets, tuples, mutability |
| `files-and-paths-quiz.py` | `files-and-paths.md` | open(), with, read/write modes, pathlib |
| `errors-and-debugging-quiz.py` | `errors-and-debugging.md` | Error types, tracebacks, debugging strategy |
| `types-and-conversions-quiz.py` | `types-and-conversions.md` | str/int/float/bool, truthy/falsy, conversion |
| `how-imports-work-quiz.py` | `how-imports-work.md` | import, from, packages, search path |
| `classes-and-objects-quiz.py` | `classes-and-objects.md` | self, __init__, methods, inheritance |
| `decorators-explained-quiz.py` | `decorators-explained.md` | @syntax, wrapping, functools.wraps |
| `virtual-environments-quiz.py` | `virtual-environments.md` | venv, activate, requirements.txt |
| `the-terminal-deeper-quiz.py` | `the-terminal-deeper.md` | Pipes, redirects, env vars, shortcuts |
| `http-explained-quiz.py` | `http-explained.md` | Methods, status codes, headers, JSON |
| `api-basics-quiz.py` | `api-basics.md` | REST conventions, requests, auth |
| `async-explained-quiz.py` | `async-explained.md` | async/await, event loop, gather |

## Format

Each quiz has 5-8 questions mixing multiple choice and short answer. You get immediate feedback after every question with a brief explanation, plus a final score and percentage.

## Recommended Order

Follow the concept docs in curriculum order:

1. Variables
2. Loops
3. Functions
4. Collections
5. Files and Paths
6. Errors and Debugging
7. Types and Conversions
8. Imports
9. Classes and Objects
10. Decorators
11. Virtual Environments
12. The Terminal (Deeper)
13. HTTP
14. API Basics
15. Async
