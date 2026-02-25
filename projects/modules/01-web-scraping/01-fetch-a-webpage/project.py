"""
Project 01 — Fetch a Webpage

This script fetches a web page using the requests library and prints
basic information about the response: status code, content type,
content length, and a preview of the HTML.

Target site: http://books.toscrape.com (a safe practice site for scraping)
"""

# The requests library makes HTTP requests simple.
# You installed it with: pip install requests
import requests


def fetch_page(url):
    """
    Fetch a web page and return the response object.

    requests.get() sends an HTTP GET request to the URL — the same kind
    of request your browser sends when you type a URL in the address bar.
    The response object contains the status code, headers, and body.
    """
    print(f"Fetching {url} ...")
    response = requests.get(url)
    return response


def display_response_info(response):
    """
    Print useful information about the HTTP response.

    Every HTTP response has:
    - A status code (200 = success, 404 = not found, 500 = server error)
    - Headers (metadata like content type, server name, etc.)
    - A body (the actual HTML, JSON, or other content)
    """

    # The status code tells you whether the request succeeded.
    # 200 means "OK" — the server found the page and sent it back.
    print(f"Status code: {response.status_code}")

    # Headers are key-value pairs the server sends with the response.
    # Content-Type tells you what kind of content came back (HTML, JSON, etc.)
    content_type = response.headers.get("Content-Type", "unknown")
    print(f"Content type: {content_type}")

    # response.text is the body of the response as a string.
    # For a web page, this is the raw HTML that the browser would render.
    # len() tells us how many characters are in the response.
    print(f"Content length: {len(response.text)} characters")

    # Print the first 500 characters so you can see what HTML looks like.
    # This is the same HTML your browser receives — it just renders it
    # as a pretty page instead of showing the raw tags.
    print()
    print("First 500 characters of the page:")
    print("-" * 50)
    print(response.text[:500])
    print("-" * 50)


def main():
    # books.toscrape.com is a website built specifically for people
    # learning web scraping. It is safe to scrape and will not block you.
    url = "http://books.toscrape.com/"

    # Step 1: Fetch the page
    response = fetch_page(url)

    # Step 2: Check if the request succeeded
    # Any status code in the 200s means success.
    # The most common success code is 200 ("OK").
    if response.status_code == 200:
        display_response_info(response)
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("This means the server could not return the page you asked for.")

    print("\nDone.")


# This pattern means: only run main() when this file is executed directly.
# If someone imports this file, main() will NOT run automatically.
# This is a Python convention you will see in almost every script.
if __name__ == "__main__":
    main()
