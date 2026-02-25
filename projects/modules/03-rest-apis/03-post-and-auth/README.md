# Module 03 / Project 03 — POST and Auth

[README](../../../../README.md)

## Focus

- Sending POST requests with `requests.post()`
- Sending a JSON body with the `json` parameter
- Setting custom HTTP headers
- Understanding the difference between GET and POST

## Why this project exists

Reading data is only half the story. Most APIs also let you create, update, and delete resources. This project teaches you how to send data to an API and how to attach headers that identify your client. JSONPlaceholder accepts POST requests and returns what the server would have created, so you can practice without any risk.

## Run

```bash
cd projects/modules/03-rest-apis/03-post-and-auth
python project.py
```

## Expected output

```text
--- POST: Creating a new post ---
Status code: 201
Server response:
{
  "title": "My First API Post",
  "body": "This post was created by a Python script using requests.",
  "userId": 1,
  "id": 101
}
The server assigned ID: 101

--- GET with custom headers ---
Status code: 200
Request headers we sent:
  User-Agent: learn-python-module03/1.0
  Accept: application/json
Post title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit

--- GET vs POST comparison ---
GET /posts/1  -> status 200, method retrieves existing data
POST /posts   -> status 201, method creates new data
Key difference: GET reads, POST writes.
```

## Alter it

1. Change the POST body to include your own title and body text. Verify the server echoes back what you sent.
2. Add a custom header called `X-Request-Source` with the value `"python-learner"`. Print the request headers to confirm it was sent.
3. Try sending a POST with an empty body (`json={}`). What does the server return?

## Break it

1. Use `requests.post()` but pass the data as `data={"title": "test"}` instead of `json={"title": "test"}`. What happens to the Content-Type header? Does the response change?
2. Send a POST to `/posts/1` (an existing resource URL). What status code do you get?
3. Remove the `json` parameter entirely from the POST call. What does the server return?

## Fix it

1. When using `data=` instead of `json=`, manually set the `Content-Type` header to `application/json` and use `json.dumps()` on the body. Verify the server responds the same as before.
2. Add a check after the POST: if `status_code` is not 201, print a warning with the actual status code.
3. After fixing, run both the correct and broken versions to confirm the difference.

## Explain it

1. What is the difference between the `json=` parameter and the `data=` parameter in `requests.post()`?
2. What does HTTP status code 201 mean, and how does it differ from 200?
3. Why would you set a custom `User-Agent` header when making API requests?
4. JSONPlaceholder returns `id: 101` for every POST. Why is that, and how would a real API differ?

## Mastery check

You can move on when you can:

- send a POST request with a JSON body from memory,
- explain the difference between GET and POST,
- set custom headers on a request,
- describe what `json=` does compared to `data=`.

## Next

Continue to [Error Handling](../04-error-handling/).
