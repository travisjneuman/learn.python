# Fetch a Webpage — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 15 minutes attempting it independently. The goal is to fetch a webpage with `requests.get()`, check the status code, and print some of the HTML content. If you can do that much, you are on the right track.

## Thinking Process

When you hear "fetch a webpage," think about what your browser does when you type a URL and press Enter. It sends an HTTP GET request to a server, the server sends back a response (status code, headers, and a body of HTML), and your browser renders the HTML into a visual page. Your Python script does the same thing, except instead of rendering the page, you inspect the raw response.

The `requests` library is Python's most popular tool for making HTTP requests. It wraps the messy details of HTTP into a clean, simple API. The response object it returns has everything: the status code (did it work?), the headers (metadata about the response), and the body text (the actual HTML). Your job is to call `requests.get()`, check whether the request succeeded, and display the interesting parts.

Start by thinking about what could go wrong. The server might not exist (connection error). The page might not exist (404 status). The server might be overloaded (500 status). Handling these cases is what separates a script that works from one that is actually useful.

## Step 1: Import requests and Define the URL

**What to do:** Import the `requests` library and choose a URL to fetch.

**Why:** The `requests` library does not come with Python — you installed it with `pip install requests`. The URL `http://books.toscrape.com/` is a website built specifically for scraping practice, so you will never get blocked or cause problems by fetching it.

```python
import requests

url = "http://books.toscrape.com/"
```

**Predict:** What happens if you try to run the script without installing `requests` first? What does the error message look like?

## Step 2: Send the GET Request

**What to do:** Call `requests.get(url)` and store the response object.

**Why:** `requests.get()` sends an HTTP GET request — the same type of request your browser sends when you visit a URL. The function returns a `Response` object that contains everything the server sent back. Think of it as an envelope: the status code is stamped on the outside, the headers are metadata inside the flap, and the body (HTML) is the letter inside.

```python
print(f"Fetching {url} ...")
response = requests.get(url)
```

**Predict:** After this line runs, `response` holds the entire server response. What type is `response`? Try `print(type(response))` to find out.

## Step 3: Check the Status Code

**What to do:** Read `response.status_code` and decide what to do based on its value.

**Why:** The status code tells you whether the request succeeded. 200 means "OK" — the server found the page and sent it back. 404 means "not found." 500 means the server had an internal error. Checking the status code before processing the response prevents you from trying to read HTML that does not exist.

```python
if response.status_code == 200:
    print(f"Status code: {response.status_code}")
    # Proceed to display the content
else:
    print(f"Request failed with status code: {response.status_code}")
```

**Predict:** If you change the URL to `http://books.toscrape.com/this-does-not-exist`, what status code will you get?

## Step 4: Inspect Headers and Content

**What to do:** Print the Content-Type header and a preview of the response body.

**Why:** Headers are metadata that the server sends along with the response. The `Content-Type` header tells you what kind of content came back (HTML, JSON, an image, etc.). The response body (`response.text`) is the actual content — in this case, raw HTML. Printing the first 500 characters gives you a preview without flooding your terminal.

```python
content_type = response.headers.get("Content-Type", "unknown")
print(f"Content type: {content_type}")
print(f"Content length: {len(response.text)} characters")

print("\nFirst 500 characters of the page:")
print("-" * 50)
print(response.text[:500])
print("-" * 50)
```

Two details to notice:

- **`response.headers.get("Content-Type", "unknown")`** uses `.get()` with a default value instead of direct bracket access. This prevents a crash if the header is missing.
- **`response.text[:500]`** is a string slice. It returns the first 500 characters. The full HTML of a webpage can be thousands of characters long.

**Predict:** What is the difference between `response.text` and `response.content`? Try printing both and look at the types.

## Step 5: Wrap It in a Function and Add a Main Guard

**What to do:** Organize your code into functions and add the `if __name__ == "__main__"` guard.

**Why:** Putting the logic in functions makes the code reusable — another script could import `fetch_page()` without running the whole program. The `__name__` guard ensures `main()` only runs when you execute the file directly, not when someone imports it.

```python
def fetch_page(url):
    print(f"Fetching {url} ...")
    response = requests.get(url)
    return response

def display_response_info(response):
    print(f"Status code: {response.status_code}")
    # ... rest of the display logic

def main():
    url = "http://books.toscrape.com/"
    response = fetch_page(url)
    if response.status_code == 200:
        display_response_info(response)
    else:
        print(f"Request failed with status code: {response.status_code}")
    print("\nDone.")

if __name__ == "__main__":
    main()
```

**Predict:** What happens if you import this file from another Python file? Does `main()` run?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `ModuleNotFoundError: No module named 'requests'` | `requests` is not installed | Run `pip install requests` in your terminal |
| Printing `response` instead of `response.text` | Confusion between the object and its content | `response` is the whole object; `.text` is the HTML string |
| Not checking the status code | Assuming every request succeeds | Always check `response.status_code` before processing |
| Using `response.content` when you want text | Mixing up bytes and strings | `.text` returns a string (decoded), `.content` returns raw bytes |

## Testing Your Solution

There are no pytest tests for this project — it is a script that fetches a live website. Run it and check the output:

```bash
python project.py
```

Expected output:
```text
Fetching http://books.toscrape.com/ ...
Status code: 200
Content type: text/html
Content length: 51696 characters
...
Done.
```

The exact character count may vary, but you should see status code 200 and recognizable HTML tags.

## What You Learned

- **`requests.get()`** sends an HTTP GET request and returns a Response object — the same kind of request your browser makes when you visit a URL.
- **Status codes** tell you whether a request succeeded (200), the page was not found (404), or the server had an error (500). Always check before processing.
- **`response.text`** gives you the response body as a string, while **`response.headers`** gives you the metadata the server sent back.
- **The `if __name__ == "__main__"` pattern** lets you write code that works both as a standalone script and as an importable module.
