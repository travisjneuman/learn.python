"""Module 03 / Project 03 — POST and Auth.

Learn how to send POST requests with JSON bodies, set custom headers,
and understand the difference between GET and POST.
"""

import requests
import json


def create_post():
    """Send a POST request to create a new resource.

    POST sends data TO the server. The server processes it and (usually)
    creates a new resource. JSONPlaceholder accepts the data and returns
    what it would have created, but does not actually save it.

    Key concept: use the json= parameter (not data=) to send JSON.
    When you use json=, requests automatically:
      1. Serializes the dict to a JSON string
      2. Sets the Content-Type header to application/json
    """
    url = "https://jsonplaceholder.typicode.com/posts"

    # The data we want to send. This is a plain Python dictionary.
    new_post = {
        "title": "My First API Post",
        "body": "This post was created by a Python script using requests.",
        "userId": 1,
    }

    # json= tells requests to serialize this dict as JSON and set
    # the correct Content-Type header. This is the preferred approach.
    response = requests.post(url, json=new_post)

    print("--- POST: Creating a new post ---")
    print("Status code:", response.status_code)

    # The server responds with the created resource, including the new ID.
    created = response.json()
    print("Server response:")
    print(json.dumps(created, indent=2))
    print("The server assigned ID:", created["id"])


def get_with_custom_headers():
    """Send a GET request with custom HTTP headers.

    Headers are metadata sent with every HTTP request. Common uses:
    - User-Agent: identifies your client (browser, script, bot)
    - Accept: tells the server what format you want back
    - Authorization: sends credentials (API keys, tokens)

    Some APIs require specific headers. Even when they don't, setting a
    descriptive User-Agent is good practice — it helps API owners know
    who is calling their service.
    """
    url = "https://jsonplaceholder.typicode.com/posts/1"

    # Custom headers are passed as a dictionary.
    headers = {
        "User-Agent": "learn-python-module03/1.0",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    print("\n--- GET with custom headers ---")
    print("Status code:", response.status_code)

    # response.request gives you access to the Request object that was
    # actually sent. This lets you inspect what headers your client used.
    print("Request headers we sent:")
    print("  User-Agent:", response.request.headers.get("User-Agent"))
    print("  Accept:", response.request.headers.get("Accept"))
    print("Post title:", data["title"])


def compare_get_and_post():
    """Demonstrate the fundamental difference between GET and POST.

    GET: retrieves data. Does not change anything on the server.
         Parameters go in the URL (query string).
         Safe to repeat — calling it twice gives the same result.

    POST: sends data to create something new. Changes server state.
          Data goes in the request body (not the URL).
          NOT safe to repeat blindly — calling it twice might create duplicates.
    """
    print("\n--- GET vs POST comparison ---")

    # GET retrieves an existing resource.
    get_response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    print("GET /posts/1  -> status {}, method retrieves existing data".format(
        get_response.status_code
    ))

    # POST creates a new resource.
    post_response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json={"title": "test", "body": "test", "userId": 1},
    )
    print("POST /posts   -> status {}, method creates new data".format(
        post_response.status_code
    ))

    print("Key difference: GET reads, POST writes.")


if __name__ == "__main__":
    create_post()
    get_with_custom_headers()
    compare_get_and_post()
