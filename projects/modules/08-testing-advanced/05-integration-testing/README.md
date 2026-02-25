# Module 08 / Project 05 — Integration Testing

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- Testing a FastAPI application with `TestClient`
- Full request/response cycle testing (create, read, update, delete)
- Testing error cases: 404, invalid input
- `conftest.py` fixtures for fresh app instances

## Why this project exists

Unit tests check individual functions in isolation. Integration tests check that the whole system works together — that HTTP requests reach the right endpoint, data is stored and retrieved correctly, and error responses have the right status codes. This project gives you a simple FastAPI todo API and teaches you to test it from the outside, the same way a real client would use it. This is the closest thing to "clicking through the app" but automated and repeatable.

## Run

```bash
cd projects/modules/08-testing-advanced/05-integration-testing
pytest tests/ -v
```

## Expected output

```text
tests/test_integration.py::test_list_todos_empty PASSED
tests/test_integration.py::test_create_todo PASSED
tests/test_integration.py::test_create_todo_returns_id PASSED
tests/test_integration.py::test_get_todo_not_found PASSED
tests/test_integration.py::test_create_and_retrieve_todo PASSED
tests/test_integration.py::test_delete_todo PASSED
tests/test_integration.py::test_delete_nonexistent_todo PASSED
tests/test_integration.py::test_create_todo_invalid_input PASSED
tests/test_integration.py::test_full_crud_flow PASSED
```

All tests should pass. Each test gets a fresh app instance so they do not interfere with each other.

## Alter it

1. Add a `PUT /todos/{todo_id}` endpoint that updates a todo's title and done status. Write integration tests for it.
2. Add a test that creates five todos and verifies that `GET /todos` returns all five.
3. Add a `GET /todos?done=true` query parameter that filters completed todos. Write tests for the filter.

## Break it

1. Remove the `conftest.py` file and import TestClient directly in each test without the fixture. Create a todo in one test and try to read it in another. What happens?
2. Change the `POST /todos` endpoint to not return the created todo. What tests break?
3. Change the todo ID generation to always return 1. What tests break?

## Fix it

1. Put `conftest.py` back and verify each test gets an isolated app instance.
2. Restore the POST response to include the full todo object.
3. Fix the ID generation so each todo gets a unique ID.

## Explain it

1. What is the difference between a unit test and an integration test?
2. Why does each test need a fresh app instance (a fresh `client` fixture)?
3. What does `TestClient` do under the hood — does it start a real server?
4. Why do we test error cases (404, invalid input) and not just the happy path?

## Mastery check

You can move on when you can:

- Write a TestClient-based integration test from memory.
- Test the full CRUD cycle (create, read, update, delete) for any resource.
- Test error responses and verify status codes.
- Explain why test isolation matters for integration tests.

## Next

Congratulations — you have completed Module 08. You now have a professional-grade testing toolkit: parametrize for coverage, mocking for isolation, fixtures for setup, Hypothesis for edge cases, and integration tests for confidence. Go back to [Module Index](../README.md) and pick your next module.
