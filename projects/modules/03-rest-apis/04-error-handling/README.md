# Module 03 / Project 04 — Error Handling

[README](../../../../README.md)

## Focus

- Checking HTTP status codes and using `raise_for_status()`
- Handling connection errors, timeouts, and HTTP errors
- Implementing retries with exponential backoff
- Writing defensive code for unreliable networks

## Why this project exists

APIs fail. Networks drop. Servers return errors. If your code does not handle these cases, it crashes with an unhelpful traceback. This project teaches you how to make your API calls resilient by catching specific errors, retrying failed requests, and giving users clear feedback about what went wrong.

## Run

```bash
cd projects/modules/03-rest-apis/04-error-handling
python project.py
```

## Expected output

```text
--- Test 1: Successful request ---
Status: 200 OK
Title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit

--- Test 2: 404 Not Found ---
HTTP error: 404 Client Error: Not Found for url: https://jsonplaceholder.typicode.com/posts/99999

--- Test 3: Connection error (bad domain) ---
Connection error: could not reach https://not-a-real-domain-xyz.com/posts/1

--- Test 4: Timeout (very short limit) ---
Timeout: request to https://jsonplaceholder.typicode.com/posts took longer than 0.001s

--- Test 5: Retry with backoff ---
Attempt 1 of 3: requesting https://jsonplaceholder.typicode.com/posts/1
Success on attempt 1.
Title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
```

## Alter it

1. Change the retry function to attempt 5 times instead of 3. Increase the base delay to 2 seconds.
2. Add a test that uses `response.status_code` to check for a 200 before parsing JSON, without using `raise_for_status()`.
3. Add a test that catches `requests.exceptions.JSONDecodeError` by requesting a URL that returns non-JSON content (try `https://jsonplaceholder.typicode.com/` — the homepage returns HTML).

## Break it

1. Set the timeout to `0` (not `0.001`, literally `0`). What error do you get? Is it a timeout error or something else?
2. In the retry function, remove the `time.sleep()` call. What happens conceptually when retrying against a struggling server?
3. Catch all exceptions with a bare `except:` instead of specific exception types. Why is this dangerous?

## Fix it

1. After testing with `timeout=0`, add a guard: if timeout is less than or equal to 0, set it to a reasonable default (like 10 seconds) and print a warning.
2. Replace the bare `except:` with the specific exception types (`requests.exceptions.RequestException` as a catch-all for requests errors).
3. After fixing, verify that each error scenario prints a clear, specific message about what went wrong.

## Explain it

1. What is the difference between `response.raise_for_status()` and manually checking `response.status_code`?
2. Why does exponential backoff use increasing delays (1s, 2s, 4s) instead of a fixed delay?
3. What is the difference between a `ConnectionError` and a `Timeout` exception?
4. Why should you catch specific exceptions instead of using bare `except:`?

## Mastery check

You can move on when you can:

- name at least three types of request errors and their exception classes,
- implement a retry function with exponential backoff from memory,
- explain when to use `raise_for_status()` vs manual status checks,
- handle errors without crashing or printing raw tracebacks.

## Next

Continue to [API Client Class](../05-api-client-class/).
