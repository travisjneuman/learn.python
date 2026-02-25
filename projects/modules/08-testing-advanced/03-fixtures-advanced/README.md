# Module 08 / Project 03 — Fixtures Advanced

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- `conftest.py` for sharing fixtures across test files
- Fixture scopes: `function`, `module`, `session`
- `tmp_path` for temporary file operations in tests
- `monkeypatch` for safely modifying environment variables and attributes

## Why this project exists

Real applications read configuration from environment variables, process files on disk, and combine multiple components. Testing these requires setup and teardown that would be tedious to repeat in every test function. Pytest fixtures let you define reusable setup code that runs automatically before each test. `conftest.py` lets you share fixtures across multiple test files. `tmp_path` gives you a fresh temporary directory for each test, and `monkeypatch` lets you safely override environment variables without affecting other tests.

## Run

```bash
cd projects/modules/08-testing-advanced/03-fixtures-advanced
pytest tests/ -v
```

## Expected output

```text
tests/test_processor.py::test_load_config_reads_env_vars PASSED
tests/test_processor.py::test_load_config_uses_defaults PASSED
tests/test_processor.py::test_process_file_uppercase PASSED
tests/test_processor.py::test_process_file_strips_whitespace PASSED
tests/test_processor.py::test_process_file_missing_file PASSED
tests/test_processor.py::test_save_results_creates_file PASSED
tests/test_processor.py::test_save_results_content PASSED
tests/test_processor.py::test_full_pipeline PASSED
```

All tests should pass. Each test gets its own temporary directory and environment, so they never interfere with each other.

## Alter it

1. Add a new fixture in `conftest.py` that creates a temporary directory with three text files of different sizes. Use it in a new test.
2. Change the `sample_config` fixture to use `scope="module"` instead of the default `scope="function"`. Run with `-v` and notice the setup/teardown happens less often.
3. Add a `monkeypatch` fixture that sets `APP_DEBUG=true` and verify that `load_config` reads it.

## Break it

1. Remove `conftest.py` and run the tests. What errors do you get? Why?
2. Create two fixtures with the same name in different files and see which one wins.
3. Use `monkeypatch.setenv` in a test, then check the environment variable in a different test. Is it still set? Why or why not?

## Fix it

1. Put `conftest.py` back and verify all tests pass again.
2. Rename one of the duplicate fixtures to avoid the conflict.
3. Understand why `monkeypatch` changes are automatically undone after each test (that is the whole point).

## Explain it

1. What is `conftest.py` and why is it special to pytest?
2. What is the difference between `scope="function"` and `scope="session"` for a fixture?
3. Why is `tmp_path` better than creating your own temporary directory manually?
4. How does `monkeypatch` differ from directly setting `os.environ`?

## Mastery check

You can move on when you can:

- Create a `conftest.py` with shared fixtures from memory.
- Explain the difference between function, module, and session scope.
- Use `tmp_path` to test code that reads and writes files.
- Use `monkeypatch` to test code that depends on environment variables.

## Next

[Project 04 — Property-Based Testing](../04-property-based/)
