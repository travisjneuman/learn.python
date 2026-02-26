# Refactoring 03 — Copy-Paste API Client

Open `messy.py`. This module fetches data from five endpoints of a JSON API. Each function is nearly identical — classic copy-paste programming.

The code works. But it has five copies of the same logic, no retry mechanism, a hardcoded base URL, and uses `print` for error reporting.

## Your mission

Eliminate the duplication and make this code maintainable. The tests in `tests/test_messy.py` must pass before and after every change.

## Refactoring goals

1. **DRY it up.** Extract the shared logic into a single helper function. Each endpoint function should be a one-liner that calls the helper.

2. **Extract configuration.** The base URL, timeout, and headers are hardcoded. Move them to module-level constants or a configuration dictionary.

3. **Add retry logic.** Network requests fail. Add a configurable retry mechanism (e.g., retry up to 3 times with a short delay). The helper function should handle this.

4. **Replace print with proper error handling.** Use `logging` for error messages. Raise custom exceptions (or return structured errors) instead of silently returning `None`.

5. **Add type hints and docstrings** to all functions.

## Stretch goals (optional)

- Create an `ApiClient` class that holds configuration and provides methods for each endpoint
- Add a simple caching mechanism (e.g., cache results for N seconds)
- Add support for query parameters (e.g., `get_posts(user_id=1)`)

## Process

```
1. Run tests (baseline)
2. Extract helper function -> tests pass
3. Replace each endpoint function -> tests pass after each one
4. Extract configuration -> tests pass
5. Add retry logic -> add new tests -> all pass
6. Replace print with logging -> tests pass
7. Add type hints and docstrings -> done
```

## What you are practicing

- Identifying and eliminating code duplication
- Designing reusable helper functions
- Adding resilience (retries) to network code
- Proper error handling and logging patterns
