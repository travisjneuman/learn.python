# Module 08 / Project 02 — Mocking

[README](../../../../README.md) · [Module Index](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- `unittest.mock.patch` to replace external dependencies during tests
- `MagicMock` for creating fake objects with any attributes or methods
- `side_effect` for simulating errors and varying responses
- `return_value` for controlling what a mock returns

## Why this project exists

Real applications talk to external services — APIs, databases, file systems. You cannot run tests that depend on a live weather API: the tests would be slow, flaky (what if the API is down?), and non-deterministic (weather changes). Mocking lets you replace the real API call with a fake one that returns exactly what you tell it to. Your tests run in milliseconds, work offline, and test your logic without testing someone else's server.

## Run

```bash
cd projects/modules/08-testing-advanced/02-mocking
pytest tests/test_weather.py -v
```

## Expected output

```text
tests/test_weather.py::test_get_temperature_success PASSED
tests/test_weather.py::test_get_temperature_city_not_found PASSED
tests/test_weather.py::test_get_temperature_api_error PASSED
tests/test_weather.py::test_get_temperature_timeout PASSED
tests/test_weather.py::test_get_forecast_success PASSED
tests/test_weather.py::test_get_forecast_returns_correct_days PASSED
tests/test_weather.py::test_get_temperature_different_cities PASSED
```

All tests should pass without making any real HTTP requests.

## Alter it

1. Add a new method `get_humidity(city)` to `WeatherService` and write a mocked test for it.
2. Change one of the mocked responses to return a different temperature and verify the test still checks the right thing.
3. Add a test that verifies `requests.get` was called with the correct URL (use `mock.assert_called_once_with`).

## Break it

1. Remove the `@patch` decorator from one test and run it. What happens when the test tries to call the real API?
2. Change the patch target to the wrong module path (e.g., `@patch("requests.get")` instead of `@patch("project.requests.get")`). Why does this matter?
3. Make a mock return a response without a `.json()` method and see what error your code raises.

## Fix it

1. Put the `@patch` decorator back and verify the test passes again.
2. Fix the patch target so it points to the right location.
3. Add proper error handling in `WeatherService` for responses that do not have the expected JSON structure.

## Explain it

1. Why do we patch `project.requests.get` instead of just `requests.get`?
2. What is the difference between `return_value` and `side_effect`?
3. What happens if you forget to patch an external dependency in a test?
4. How does `MagicMock` know what attributes and methods to have?

## Mastery check

You can move on when you can:

- Write a `@patch` decorator from memory and explain the target path.
- Use `side_effect` to simulate both exceptions and varying return values.
- Explain why mocking makes tests faster and more reliable.
- Verify that a mock was called with specific arguments.

---

## Related Concepts

- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Quiz: Classes and Objects](../../../../concepts/quizzes/classes-and-objects-quiz.py)

## Next

[Project 03 — Fixtures Advanced](../03-fixtures-advanced/)
