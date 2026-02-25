# Module 03 / Project 05 — API Client Class

[README](../../../../README.md)

## Focus

- Building a reusable API client with `requests.Session`
- Encapsulating base URL, headers, and error handling in a class
- Writing methods that map to API endpoints
- Testing your client against a real API

## Why this project exists

Copy-pasting `requests.get()` calls with the same base URL and headers across your codebase is tedious and error-prone. Professional Python code wraps API interactions in a client class that handles the repetitive parts once. This project teaches you to build one, combining everything from the previous four projects into a clean, reusable design.

## Run

```bash
cd projects/modules/03-rest-apis/05-api-client-class
python project.py
```

To run the tests:

```bash
cd projects/modules/03-rest-apis/05-api-client-class
pytest tests/ -v
```

## Expected output

```text
--- Using the JSONPlaceholder client ---

Fetching post 1...
  Title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
  Author user ID: 1

Fetching posts by user 2 (limit 3)...
  Found 3 posts:
    Post 11: et ea vero quia laudantium deserunt
    Post 12: in quibusdam tempore odit est dolorem
    Post 13: dolorum ut in voluptas mollitia et saepe quo animi

Creating a new post...
  Created post with ID: 101
  Title: Testing the Client
  Body: This post was created through the client class.

Fetching a post that does not exist (ID 99999)...
  Result: None (post not found)

--- Session reuse demonstration ---
The client reuses one TCP connection for all requests.
This is faster and more efficient than creating a new connection each time.
```

## Alter it

1. Add a `get_comments(post_id)` method that fetches comments for a given post from `/posts/{id}/comments`. Print the commenter emails.
2. Add a `get_user(user_id)` method that fetches a user from `/users/{id}`. Print the user's name and email.
3. Change the default `limit` in `get_posts()` from 10 to 5 and add a `start` parameter for pagination.

## Break it

1. Change the `base_url` to `"https://jsonplaceholder.typicode.com"` (without trailing slash) and see if the URL joining still works.
2. Remove the `try/except` from inside `get_post()`. Call `get_post(99999)` and see what happens.
3. Create two separate `JSONPlaceholderClient` instances and check if they share the same session. (Hint: they should not.)

## Fix it

1. Make the URL joining work with or without a trailing slash by using `rstrip("/")` on the base URL in `__init__`.
2. Add the `try/except` back and make sure `get_post()` returns `None` for missing posts instead of crashing.
3. Add a `close()` method that calls `self.session.close()` and a `__enter__`/`__exit__` pair so the client can be used as a context manager (`with JSONPlaceholderClient() as client:`).

## Explain it

1. What is a `requests.Session` and why is it better than calling `requests.get()` directly for multiple requests?
2. What does the session reuse in terms of TCP connections, and why does that matter?
3. Why does the client return `None` instead of raising an exception when a post is not found?
4. How would you adapt this client class to work with a different API that requires an API key in the headers?

## Mastery check

You can move on when you can:

- write an API client class with Session from memory,
- explain the benefits of session reuse,
- add a new endpoint method to the client without guidance,
- write a test that exercises the client against the real API.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../../concepts/errors-and-debugging.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Go back to the [Module 03 index](../README.md). If you are ready for more, continue to [Module 04 — FastAPI Web Apps](../../04-fastapi-web/).
