# Module 03 / Project 01 — First API Call

[README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Making a GET request with `requests.get()`
- Understanding response objects (status code, headers, body)
- Parsing JSON responses into Python dictionaries

## Why this project exists

Before you can build anything that talks to the internet, you need to understand the basic request-response cycle. This project strips it down to the simplest possible case: fetch one resource, look at what comes back, and pull out the pieces you care about.

## Run

```bash
cd projects/modules/03-rest-apis/01-first-api-call
python project.py
```

## Expected output

```text
--- Raw JSON response ---
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}

--- Accessing individual fields ---
Status code : 200
Post ID     : 1
User ID     : 1
Title       : sunt aut facere repellat provident occaecati excepturi optio reprehenderit
Body preview: quia et suscipit...

--- Response headers (selected) ---
Content-Type: application/json; charset=utf-8
```

## Alter it

1. Change the URL to fetch post `/posts/5` instead of `/posts/1`. Run again and compare the output.
2. Print the full `body` field instead of just the first 20 characters.
3. Add a line that prints the number of characters in the title.

## Break it

1. Change the URL to `https://jsonplaceholder.typicode.com/posts/99999` (a post that does not exist). What status code do you get? What does `response.json()` return?
2. Remove the `.json()` call and print `response.text` instead. What is the difference?
3. Change the URL to an invalid domain like `https://not-a-real-domain-xyz.com/posts/1`. What error do you get?

## Fix it

1. Add a check: if `response.status_code` is not 200, print a warning and skip the JSON parsing.
2. Wrap the `requests.get()` call in a `try/except` block that catches `requests.exceptions.ConnectionError` and prints a friendly message instead of a traceback.
3. After fixing, run with both a valid and invalid URL to confirm both paths work.

## Explain it

1. What does `response.json()` actually do under the hood?
2. What is the difference between `response.text` and `response.json()`?
3. Why does `requests.get()` return a Response object instead of just the data?
4. What HTTP method does `requests.get()` use, and what does that method mean?

## Mastery check

You can move on when you can:

- write a GET request from memory without looking at docs,
- explain what a status code of 200 means vs 404,
- extract any field from a JSON response,
- describe the difference between `.text` and `.json()`.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Classes and Objects](../../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Continue to [Query Parameters](../02-query-parameters/).
