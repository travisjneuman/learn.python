# Module 08 / Project 01 — Parametrize

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- `@pytest.mark.parametrize` to run one test function with many different inputs
- Single-parameter and multi-parameter parametrize decorators
- The `ids` parameter for readable test output
- Testing utility functions with boundary values and edge cases

## Why this project exists

Writing a separate test function for every input you want to check is tedious and creates a wall of nearly identical code. `@pytest.mark.parametrize` solves this by letting you define one test function and feed it a table of inputs and expected outputs. Pytest runs it once per row, reporting each as a separate test case. This is how professional codebases test functions that must handle many different inputs.

## Run

```bash
cd projects/modules/08-testing-advanced/01-parametrize
pytest tests/test_utils.py -v
```

## Expected output

```text
tests/test_utils.py::test_validate_email[valid-user@example.com] PASSED
tests/test_utils.py::test_validate_email[valid-name.tag@domain.org] PASSED
tests/test_utils.py::test_validate_email[invalid-missing-at] PASSED
tests/test_utils.py::test_validate_email[invalid-empty-string] PASSED
...
tests/test_utils.py::test_celsius_to_fahrenheit[freezing] PASSED
tests/test_utils.py::test_celsius_to_fahrenheit[boiling] PASSED
...
tests/test_utils.py::test_is_palindrome[racecar-True] PASSED
tests/test_utils.py::test_is_palindrome[hello-False] PASSED
...
tests/test_utils.py::test_clamp[below-minimum] PASSED
tests/test_utils.py::test_clamp[above-maximum] PASSED
...
```

Each parametrized case appears as a separate test with a readable name. All should pass.

## Alter it

1. Add three more email test cases to `test_validate_email`: one with a `+` in the local part, one with multiple dots in the domain, and one with a missing domain.
2. Add a parametrize case for `celsius_to_fahrenheit` using absolute zero (-273.15 C = -459.67 F).
3. Add a new parametrized test for `clamp` where `min_val` equals `max_val`. What should happen when the range is a single point?

## Break it

1. Change one of the expected values in `test_celsius_to_fahrenheit` to be wrong (e.g., change 32.0 to 33.0). Run the tests and read the failure output carefully — pytest shows you exactly which parametrize case failed and what the actual vs expected values were.
2. Remove the `ids` parameter from one of the parametrize decorators and run with `-v`. Notice how the test names become less readable.
3. Add a duplicate test ID and see what pytest does.

## Fix it

1. Fix the broken expected value you changed above.
2. Add the `ids` back and verify the verbose output is readable again.
3. If any of your new test cases from "Alter it" fail, fix either the test or the function (decide which one is wrong first).

## Explain it

1. What is the difference between writing five separate test functions and one parametrized test with five cases?
2. What does the `ids` parameter do and why does it matter?
3. How does pytest report a failure in a parametrized test differently from a regular test?
4. When would you use multi-parameter parametrize (multiple arguments) vs single-parameter?

## Mastery check

You can move on when you can:

- Write a parametrized test from memory, without looking at examples.
- Explain what `ids` does and why you should use it.
- Add new test cases to an existing parametrized test in under a minute.
- Read pytest's parametrize failure output and understand which case failed and why.

---

## Related Concepts

- [Decorators Explained](../../../../concepts/decorators-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Quiz: Decorators Explained](../../../../concepts/quizzes/decorators-explained-quiz.py)

## Next

[Project 02 — Mocking](../02-mocking/)
