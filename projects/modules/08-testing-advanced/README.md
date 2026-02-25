# Module 08 — Advanced Testing

[README](../../../README.md) · Modules: [Index](../README.md)

## Overview

This module teaches advanced testing techniques that go beyond basic `assert` statements and simple test functions. You will learn to write tests that cover many inputs efficiently, isolate code from external dependencies, share setup across test files, discover edge cases automatically, and test full web applications end to end.

Testing is not an afterthought — it is how professional developers build confidence that their code works. The techniques in this module are used daily in production Python codebases around the world.

## Prerequisites

Complete **Level 3** before starting this module. You should be comfortable with:

- Packages and module imports
- Error handling with try/except
- Project structure (multiple files, `__init__.py`)
- Basic pytest usage (writing test functions, `assert`, running `pytest`)
- Classes and methods
- Working with files and environment variables

## Learning objectives

By the end of this module you will be able to:

1. Use `@pytest.mark.parametrize` to test a function against many inputs with a single test definition.
2. Mock external dependencies (APIs, databases, file systems) so tests run fast and without network access.
3. Write shared fixtures in `conftest.py` with different scopes, and use `tmp_path` and `monkeypatch`.
4. Use the Hypothesis library to automatically discover edge cases through property-based testing.
5. Write integration tests for a FastAPI web application using `TestClient`.

## Projects

| # | Project | What you learn |
|---|---------|----------------|
| 01 | [Parametrize](./01-parametrize/) | `@pytest.mark.parametrize`, test matrices, testing many inputs with one function |
| 02 | [Mocking](./02-mocking/) | `unittest.mock`, `@patch`, `MagicMock`, `side_effect` |
| 03 | [Fixtures Advanced](./03-fixtures-advanced/) | `conftest.py`, fixture scopes, `tmp_path`, `monkeypatch` |
| 04 | [Property-Based Testing](./04-property-based/) | Hypothesis library, `@given`, strategies, automatic edge case discovery |
| 05 | [Integration Testing](./05-integration-testing/) | FastAPI `TestClient`, full request/response cycle, API testing |

Work through them in order. Each project introduces a different testing technique.

## Setup

Create a virtual environment and install dependencies before starting:

```bash
cd projects/modules/08-testing-advanced
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

See [concepts/virtual-environments.md](../../../concepts/virtual-environments.md) for a full explanation of virtual environments.

## Dependencies

This module requires four packages (listed in `requirements.txt`):

- **pytest** — the standard Python test runner. You write functions that start with `test_`, use `assert`, and pytest finds and runs them automatically.
- **hypothesis** — a property-based testing library. Instead of writing specific test cases, you describe what kinds of inputs your function should handle and Hypothesis generates hundreds of examples automatically.
- **httpx** — a modern HTTP client that supports async requests. Used here for testing FastAPI applications.
- **fastapi** — a modern web framework for building APIs. Used in the integration testing project to give you a real app to test against.
