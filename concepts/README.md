# Concepts — Quick Reference

Plain-language explanations of Python concepts. Use these when you need to understand something a project introduces.

## Core Concepts (start here)

- [What is a Variable?](./what-is-a-variable.md)
- [How Loops Work](./how-loops-work.md)
- [Functions Explained](./functions-explained.md)
- [Collections: Lists, Dicts, Sets](./collections-explained.md)
- [Files and Paths](./files-and-paths.md)
- [Errors and Debugging](./errors-and-debugging.md)
- [Reading Error Messages](./reading-error-messages.md) — traceback anatomy, 10 most common errors
- [Types and Conversions](./types-and-conversions.md)

## Intermediate Concepts (after Level 2)

- [How Imports Work](./how-imports-work.md) — modules, packages, `__init__.py`
- [Classes and Objects](./classes-and-objects.md) — OOP basics, `self`, inheritance
- [Decorators Explained](./decorators-explained.md) — `@` syntax, wrapping functions
- [Virtual Environments](./virtual-environments.md) — venv, pip, requirements.txt
- [The Terminal — Going Deeper](./the-terminal-deeper.md) — pipes, redirects, env vars

## Advanced Concepts (after Level 3)

- [HTTP Explained](./http-explained.md) — requests, responses, status codes, headers
- [API Basics](./api-basics.md) — REST, JSON, endpoints, authentication
- [Async Explained](./async-explained.md) — async/await, event loops, concurrency

## Modern Python (Level 1+)

- [Type Hints Explained](./type-hints-explained.md) — annotations, Optional, Union, Protocol
- [Dataclasses Explained](./dataclasses-explained.md) — @dataclass, fields, frozen, the easy way to create classes
- [Match/Case Explained](./match-case-explained.md) — structural pattern matching (Python 3.10+)
- [Modern Python Tooling](./modern-python-tooling.md) — uv, ruff, pyproject.toml

## How to use these

- Read the concept page before or during a project
- Each page has: explanation, code example, common mistakes
- Come back to these whenever you forget how something works

---

## Practice Tools

| Tool | Description | How to use |
|------|-------------|------------|
| **Concept Quizzes** | Interactive terminal quizzes for each concept | `python concepts/quizzes/<name>-quiz.py` |
| **Flashcard Decks** | Spaced repetition cards organized by level | `python practice/flashcards/review-runner.py` |
| **Coding Challenges** | Short focused exercises (beginner + intermediate) | See `practice/challenges/README.md` |
| **Diagnostic Assessments** | Test your readiness before starting a level | `python tools/diagnose.py` |

### Available Quizzes

Each concept doc has a matching quiz in `concepts/quizzes/`:

- [Api Basics](quizzes/api-basics-quiz.py)
- [Async Explained](quizzes/async-explained-quiz.py)
- [Classes And Objects](quizzes/classes-and-objects-quiz.py)
- [Collections Explained](quizzes/collections-explained-quiz.py)
- [Dataclasses Explained](quizzes/dataclasses-explained-quiz.py)
- [Decorators Explained](quizzes/decorators-explained-quiz.py)
- [Errors And Debugging](quizzes/errors-and-debugging-quiz.py)
- [Files And Paths](quizzes/files-and-paths-quiz.py)
- [Functions Explained](quizzes/functions-explained-quiz.py)
- [How Imports Work](quizzes/how-imports-work-quiz.py)
- [How Loops Work](quizzes/how-loops-work-quiz.py)
- [Http Explained](quizzes/http-explained-quiz.py)
- [Match Case Explained](quizzes/match-case-explained-quiz.py)
- [Reading Error Messages](quizzes/reading-error-messages-quiz.py)
- [The Terminal Deeper](quizzes/the-terminal-deeper-quiz.py)
- [Type Hints Explained](quizzes/type-hints-explained-quiz.py)
- [Types And Conversions](quizzes/types-and-conversions-quiz.py)
- [Virtual Environments](quizzes/virtual-environments-quiz.py)
- [What Is A Variable](quizzes/what-is-a-variable-quiz.py)
