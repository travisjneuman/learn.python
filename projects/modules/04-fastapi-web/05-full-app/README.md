# Module 04 / Project 05 — Full App

Home: [README](../../../../README.md)

## Focus

Complete API with integration tests, custom error handling, CORS middleware, and OpenAPI documentation.

## Why this project exists

This project combines everything from Projects 01 through 04 into a production-quality API. You will add the finishing touches that separate a learning exercise from a deployable application: structured error handling, CORS headers for frontend clients, request logging, custom OpenAPI metadata, and a full test suite using FastAPI's TestClient.

## Run

```bash
cd projects/modules/04-fastapi-web/05-full-app
python app.py
```

Open **http://127.0.0.1:8000/docs** to see the fully documented API with tags, descriptions, and example responses.

To run the tests:

```bash
cd projects/modules/04-fastapi-web/05-full-app
pytest tests/ -v
```

Press `Ctrl+C` to stop the server.

## Expected output

The API works the same as Project 04, with additional polish:

- Custom error responses with consistent format
- CORS headers allowing frontend applications to connect
- Grouped endpoints in `/docs` (Users, Todos)
- All tests pass:

```text
tests/test_api.py::test_register_user PASSED
tests/test_api.py::test_register_duplicate_user PASSED
tests/test_api.py::test_login PASSED
tests/test_api.py::test_login_wrong_password PASSED
tests/test_api.py::test_create_todo PASSED
tests/test_api.py::test_list_todos PASSED
tests/test_api.py::test_update_todo PASSED
tests/test_api.py::test_delete_todo PASSED
tests/test_api.py::test_unauthorized_access PASSED
```

## Alter it

1. Add a `GET /todos/stats` endpoint that returns `{"total": N, "completed": M, "pending": P}` for the current user.
2. Add pagination to `GET /todos` with `skip` and `limit` query parameters (e.g., `GET /todos?skip=0&limit=10`).
3. Add a test for the stats endpoint and a test for pagination.

## Break it

1. Remove the `@app.exception_handler` decorators and send a request that triggers an unhandled error. Compare the error response format to the custom handler version.
2. Remove the CORS middleware and try to call the API from a browser-based JavaScript application (or just observe what headers are missing).
3. Delete the test database file between test runs. Do the tests still pass? Why or why not?

## Fix it

1. Restore the exception handlers. Custom handlers give clients consistent error formats they can parse reliably, instead of raw stack traces.
2. Restore the CORS middleware. Without it, browsers block requests from different origins (e.g., a React app on port 3000 calling an API on port 8000).
3. The tests should create a fresh test database each time (the test file already does this). If they do not, update the test setup to use a temporary database.

## Explain it

1. What is CORS and why does it exist? When would you need it versus when would you not?
2. What is the difference between FastAPI's TestClient and making real HTTP requests with `requests` or `httpx`?
3. Why do we use a separate test database instead of the real one?
4. What are OpenAPI tags and why do they matter for API documentation?

## Mastery check

You can move on when you can:

- build a full CRUD API with authentication from scratch,
- write integration tests that cover the happy path and error cases,
- explain what CORS middleware does and when you need it,
- describe why production APIs need custom error handlers.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Errors and Debugging](../../../../concepts/errors-and-debugging.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

You have completed Module 04. You now know how to build, secure, and test a FastAPI web application.

Suggested next steps:

- [Module 05 — Async Python](../../05-async-python/) to learn async/await patterns
- [Module 06 — Databases & ORM](../../06-databases-orm/) to go deeper with SQLAlchemy and migrations
- [Module 09 — Docker & Deployment](../../09-docker-deployment/) to containerize and deploy your API
