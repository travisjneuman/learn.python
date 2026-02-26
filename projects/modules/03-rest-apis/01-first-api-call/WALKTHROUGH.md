# First API Call — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 15 minutes attempting it independently. The goal is to fetch JSON data from a public API, parse it into a Python dictionary, and print specific fields. If you can get a status code of 200 and print the title of the post, you are on the right track.

## Thinking Process

An API (Application Programming Interface) is a way for programs to talk to each other over the internet. Instead of getting back HTML (a webpage for humans), you get back JSON (structured data for programs). JSON looks like a Python dictionary: keys and values wrapped in curly braces. The `requests` library fetches the JSON just like it fetches HTML, and then `.json()` converts it into a real Python dict you can work with.

The workflow has three stages. First, send a GET request to the API endpoint. Second, check the status code to make sure it worked. Third, parse the JSON response and pull out the fields you care about. This is the exact same pattern you will use when working with any API — weather data, stock prices, social media, anything.

JSONPlaceholder is a free test API that returns fake blog posts, comments, and users. It exists specifically for learning. You cannot break it, and it always returns the same data, which makes it perfect for practicing.

## Step 1: Import the Libraries

**What to do:** Import `requests` for making HTTP requests and `json` for pretty-printing.

**Why:** `requests` handles the HTTP request. `json` is a standard library module — you only need it here for `json.dumps()`, which formats a dictionary as a nicely indented string. The actual JSON parsing is done by `response.json()`, which is a `requests` method.

```python
import requests
import json
```

**Predict:** You need `requests` for fetching data. Why do you also need `json`? Could you skip it? What would you lose?

## Step 2: Send a GET Request to the API

**What to do:** Call `requests.get()` with the JSONPlaceholder URL and store the response.

**Why:** This is identical to fetching a webpage — the only difference is that the server sends back JSON instead of HTML. The URL `https://jsonplaceholder.typicode.com/posts/1` returns a single blog post as JSON. The `/posts/1` part tells the API "give me post number 1."

```python
url = "https://jsonplaceholder.typicode.com/posts/1"
response = requests.get(url)
```

**Predict:** If you change `/posts/1` to `/posts/5`, what will change in the response? What if you use just `/posts` with no number?

## Step 3: Parse JSON into a Python Dictionary

**What to do:** Call `response.json()` to convert the JSON string into a Python dict.

**Why:** The response body arrives as a string of JSON text. `response.json()` parses that string and returns a Python dictionary (or list, depending on the API). Once you have a dict, you can access fields with square brackets just like any other dictionary. This is the key moment — raw text becomes structured data you can work with programmatically.

```python
data = response.json()

print("--- Raw JSON response ---")
print(json.dumps(data, indent=2))
```

`json.dumps()` converts the dictionary back into a formatted JSON string for display. The `indent=2` argument adds line breaks and indentation so you can actually read it. This is just for printing — `data` is still a regular Python dict.

**Predict:** What type is `data` after calling `.json()`? Is it a string, a list, or a dictionary? Try `print(type(data))`.

## Step 4: Access Individual Fields

**What to do:** Use dictionary bracket notation to pull out specific values from the response.

**Why:** The whole point of calling an API is to extract the data you need. The JSONPlaceholder post has four fields: `userId`, `id`, `title`, and `body`. You access each one with `data["field_name"]`, exactly like any Python dictionary.

```python
print("Status code :", response.status_code)
print("Post ID     :", data["id"])
print("User ID     :", data["userId"])
print("Title       :", data["title"])
print("Body preview:", data["body"][:20] + "...")
```

Two details to notice:

- **`data["body"][:20]`** is a slice that takes only the first 20 characters. The body is a long paragraph, so we just show a preview.
- **`response.status_code`** comes from the Response object, not from the JSON data. The status code is HTTP metadata; the JSON is the payload.

**Predict:** What happens if you try `data["nonexistent_field"]`? What error do you get?

## Step 5: Inspect Response Headers

**What to do:** Print the Content-Type header to confirm the response is JSON.

**Why:** The `Content-Type` header tells you the format of the response body. For an API that returns JSON, it should say `application/json`. If you see `text/html` instead, you are probably hitting a webpage, not an API. Checking this header is a quick sanity check when debugging API calls.

```python
print("\n--- Response headers (selected) ---")
print("Content-Type:", response.headers.get("Content-Type"))
```

**Predict:** What other headers does the server send? Try printing `response.headers` to see all of them. Can you find the server name?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `response.json()` raises `JSONDecodeError` | The response is not valid JSON (maybe HTML) | Check `response.status_code` first; check the URL |
| Using `response.text` instead of `response.json()` | Confusion between raw text and parsed data | `.text` gives you a string; `.json()` gives you a dict |
| `KeyError` when accessing a field | Typo in the field name or wrong API response | Print the full response first to see the actual field names |
| Not checking status code | Assuming every request returns valid JSON | Always check `response.status_code == 200` before parsing |

## Testing Your Solution

There are no pytest tests for this project — it makes live API calls. Run it and check the output:

```bash
python project.py
```

Expected output:
```text
--- Raw JSON response ---
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat ...",
  ...
}

--- Accessing individual fields ---
Status code : 200
Post ID     : 1
...
```

The data comes from JSONPlaceholder's fixed dataset, so the values should match every time.

## What You Learned

- **`response.json()`** parses a JSON response body into a Python dictionary — this is how you turn API data into something your code can work with.
- **JSON and Python dicts** are structurally similar (keys, values, nesting), which is why JSON is the default format for most APIs.
- **`json.dumps(data, indent=2)`** formats a dictionary as a readable JSON string — useful for debugging, not for data processing.
- **Response headers** like `Content-Type` tell you the format of the data before you try to parse it.
