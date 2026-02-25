# Module 01 / Project 01 — Fetch a Webpage

[README](../../../../README.md) · [Module Index](../README.md)

## Focus

- `requests.get()` to fetch a URL
- HTTP status codes (200, 404, etc.)
- Inspecting `response.text`, `response.status_code`, and `response.headers`

## Why this project exists

Before you can scrape data from any website, you need to know how to fetch a page and understand what comes back. This project teaches you the fundamentals of making HTTP requests in Python. You will see the raw HTML that your browser normally renders for you, and you will learn to check whether a request succeeded or failed.

## Run

```bash
cd projects/modules/01-web-scraping/01-fetch-a-webpage
python project.py
```

## Expected output

```text
Fetching http://books.toscrape.com/ ...
Status code: 200
Content type: text/html
Content length: 51696 characters

First 500 characters of the page:
--------------------------------------------------
<!DOCTYPE html>
<!--[if lt IE 7]>      <html lang="en-us" ...
(HTML content continues)
--------------------------------------------------
Done.
```

The exact character count and HTML will vary, but you should see status code 200 and recognizable HTML.

## Alter it

1. Change the URL to `http://books.toscrape.com/catalogue/page-2.html` and run again. What changes? What stays the same?
2. Add a line that prints `response.headers` to see all the HTTP headers the server sent back. Pick two headers and look up what they mean.
3. Add a check: if the status code is not 200, print a warning message instead of the page content.

## Break it

1. Change the URL to `http://books.toscrape.com/this-page-does-not-exist`. What status code do you get?
2. Change the URL to `http://definitely-not-a-real-website-abc123.com`. What error do you get? (Hint: it is not a status code — it is a Python exception.)
3. Remove the `import requests` line and run the script. Read the error message carefully.

## Fix it

1. Wrap the `requests.get()` call in a try/except block that catches `requests.exceptions.RequestException`. Print a friendly error message instead of a traceback.
2. After fetching, check `response.status_code`. If it is 404, print "Page not found" and exit early. If it is anything other than 200, print the status code as a warning.
3. Put the import back if you removed it.

## Explain it

1. What is an HTTP status code and what does 200 mean?
2. What is the difference between `response.text` and `response.content`?
3. Why might `requests.get()` raise an exception instead of returning a response?
4. What does the `Content-Type` header tell you?

## Mastery check

You can move on when you can:

- Fetch any URL and check whether it succeeded, from memory.
- Explain what a status code is without looking it up.
- Handle both HTTP errors (404) and connection errors (no internet) gracefully.
- Describe what `response.text` contains.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

[Project 02 — Parse HTML](../02-parse-html/)
