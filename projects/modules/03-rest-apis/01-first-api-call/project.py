"""Module 03 / Project 01 — First API Call.

Learn how to fetch data from a REST API using requests.get(),
inspect the response object, and parse JSON into a Python dictionary.
"""

# requests is the most popular HTTP library for Python.
# You installed it with: pip install requests
import requests

# json is part of the standard library. We use it here only for
# pretty-printing (indent=2), not for parsing — requests handles that.
import json


def fetch_single_post():
    """Fetch one post from JSONPlaceholder and explore the response."""

    # The URL points to a single post resource.
    # JSONPlaceholder provides 100 fake posts at /posts/1 through /posts/100.
    url = "https://jsonplaceholder.typicode.com/posts/1"

    # requests.get() sends an HTTP GET request and returns a Response object.
    # The Response object contains everything the server sent back:
    # status code, headers, body, encoding, and more.
    response = requests.get(url)

    # --- Raw JSON response ---
    # response.json() parses the response body from a JSON string into
    # a Python dictionary (or list, depending on what the API returns).
    # This only works if the server actually sent JSON — otherwise it raises
    # a JSONDecodeError.
    data = response.json()

    print("--- Raw JSON response ---")
    # json.dumps() converts the dictionary BACK into a formatted string.
    # indent=2 makes it human-readable. This is just for display.
    print(json.dumps(data, indent=2))

    # --- Accessing individual fields ---
    # Once parsed, `data` is a plain Python dict. You access fields with
    # square brackets, just like any dictionary.
    print("\n--- Accessing individual fields ---")
    print("Status code :", response.status_code)
    print("Post ID     :", data["id"])
    print("User ID     :", data["userId"])
    print("Title       :", data["title"])

    # Slice the body to show just the first 20 characters as a preview.
    print("Body preview:", data["body"][:20] + "...")

    # --- Response headers ---
    # The server sends metadata in HTTP headers. response.headers is a
    # case-insensitive dictionary. Content-Type tells you the format of
    # the response body.
    print("\n--- Response headers (selected) ---")
    print("Content-Type:", response.headers.get("Content-Type"))


# This guard ensures the code below only runs when you execute this file
# directly (python project.py). If another file imports this module,
# the code below will NOT run. This is a Python best practice.
if __name__ == "__main__":
    fetch_single_post()
