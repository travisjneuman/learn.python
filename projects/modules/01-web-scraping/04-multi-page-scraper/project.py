"""
Project 04 — Multi-Page Scraper

This script scrapes the first 3 pages of books.toscrape.com, collecting
book titles and prices from each page. It includes a 1-second delay
between requests to demonstrate rate limiting.

You will learn: constructing paginated URLs, looping over multiple pages,
rate limiting with time.sleep(), and aggregating results.
"""

import time

import requests
from bs4 import BeautifulSoup


# How many pages to scrape. Each page has 20 books.
# The site has 50 pages total, but we only scrape 3 to be respectful.
PAGES_TO_SCRAPE = 3

# WHY rate-limit yourself? -- Sending hundreds of requests per second can
# get your IP blocked and overloads the server. A 1-second delay is polite
# and shows respect for shared resources. Production scrapers use even more
# sophisticated throttling (adaptive delays, exponential backoff).
DELAY_BETWEEN_REQUESTS = 1


def fetch_page(url):
    """Fetch a single page and return the HTML, or None on failure."""
    response = requests.get(url)

    if response.status_code != 200:
        print(f"  Warning: got status {response.status_code} for {url}")
        return None

    return response.text


def extract_books_from_html(html):
    """
    Parse one page of HTML and return a list of dicts with title and price.

    This is the same extraction logic from previous projects, packaged
    as a reusable function. Each page has the same HTML structure.
    """
    soup = BeautifulSoup(html, "lxml")
    books = []

    for article in soup.find_all("article", class_="product_pod"):
        title = article.find("h3").find("a")["title"]
        price = article.find("p", class_="price_color").text.strip()

        books.append({"title": title, "price": price})

    return books


def scrape_multiple_pages(num_pages):
    """
    Scrape multiple pages and return all books combined.

    The pagination URLs on books.toscrape.com follow a pattern:
    - Page 1: http://books.toscrape.com/catalogue/page-1.html
    - Page 2: http://books.toscrape.com/catalogue/page-2.html
    - Page N: http://books.toscrape.com/catalogue/page-{N}.html

    We use an f-string to construct each URL dynamically.
    """
    all_books = []

    print(f"Scraping books from {num_pages} pages of books.toscrape.com...\n")

    for page_num in range(1, num_pages + 1):
        # Construct the URL for this page using an f-string.
        # f-strings let you embed variables directly in a string.
        url = f"http://books.toscrape.com/catalogue/page-{page_num}.html"
        print(f"Page {page_num}: {url}")

        # Fetch the page HTML
        html = fetch_page(url)

        if html is None:
            print(f"  Skipping page {page_num} due to fetch error.")
            continue

        # Extract books from this page
        page_books = extract_books_from_html(html)
        print(f"  Found {len(page_books)} books.", end="")

        # Add this page's books to our master list.
        # The += operator extends the list in place (same as .extend()).
        all_books += page_books

        # Rate limiting: sleep between requests, but not after the last page.
        # time.sleep() pauses the script for the given number of seconds.
        # This is polite — it gives the server time between our requests.
        if page_num < num_pages:
            print(f" Sleeping {DELAY_BETWEEN_REQUESTS} second...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
        else:
            print()  # Just a newline after the last page

    return all_books


def display_sample(books, sample_size=5):
    """Print a sample of books so the user can verify the data looks right."""
    print(f"\nSample (first {sample_size}):")

    for i, book in enumerate(books[:sample_size], start=1):
        print(f"  {i}. {book['title']} — {book['price']}")


def main():
    # Scrape the configured number of pages
    all_books = scrape_multiple_pages(PAGES_TO_SCRAPE)

    # Print summary
    print(f"\nTotal books collected: {len(all_books)}")

    if all_books:
        display_sample(all_books)
    else:
        print("No books were collected. Check the URLs and try again.")

    print("\nDone.")


if __name__ == "__main__":
    main()
