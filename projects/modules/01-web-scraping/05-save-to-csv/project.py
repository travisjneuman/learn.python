"""
Project 05 — Save to CSV

This script scrapes 2 pages of books.toscrape.com, deduplicates the
results by title, and writes the data to a CSV file using csv.DictWriter.

This is the capstone project for Module 01. It combines fetching, parsing,
structured extraction, pagination, and file output into one pipeline.

You will learn: csv.DictWriter, deduplication by key, and verifying output files.
"""

import csv
import os
import time

import requests
from bs4 import BeautifulSoup


# Configuration
PAGES_TO_SCRAPE = 2
DELAY_BETWEEN_REQUESTS = 1
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "books.csv")

# WHY define fields as a constant? -- DictWriter needs the field list to
# write the header row AND to order columns consistently. Defining it once
# as a constant prevents header-data mismatches if you add a new field.
CSV_FIELDS = ["title", "price", "rating", "availability"]

# Map CSS class names to numeric star ratings (same as project 03).
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def fetch_page(url):
    """Fetch a single page. Returns HTML text or None on failure."""
    response = requests.get(url)

    if response.status_code != 200:
        print(f"  Warning: status {response.status_code} for {url}")
        return None

    return response.text


def extract_books_from_html(html):
    """
    Extract all books from one page of HTML.

    Returns a list of dicts, each with keys matching CSV_FIELDS:
    title, price, rating, availability.
    """
    soup = BeautifulSoup(html, "lxml")
    books = []

    for article in soup.find_all("article", class_="product_pod"):
        # Title
        title = article.find("h3").find("a")["title"]

        # Price
        price = article.find("p", class_="price_color").text.strip()

        # Rating (convert CSS class to integer)
        rating_tag = article.find("p", class_="star-rating")
        rating_word = rating_tag["class"][1]
        rating = RATING_MAP.get(rating_word, 0)
        rating_str = f"{rating} star"

        # Availability
        availability = article.find("p", class_="availability").text.strip()

        books.append({
            "title": title,
            "price": price,
            "rating": rating_str,
            "availability": availability,
        })

    return books


def scrape_pages(num_pages):
    """Scrape multiple pages and return a combined list of book dicts."""
    all_books = []

    print(f"Scraping books from {num_pages} pages of books.toscrape.com...")

    for page_num in range(1, num_pages + 1):
        url = f"http://books.toscrape.com/catalogue/page-{page_num}.html"

        html = fetch_page(url)
        if html is None:
            print(f"  Page {page_num}: failed to fetch. Skipping.")
            continue

        page_books = extract_books_from_html(html)
        print(f"  Page {page_num}: fetched {len(page_books)} books.", end="")
        all_books.extend(page_books)

        # Rate limit between requests (not after the last one)
        if page_num < num_pages:
            print(f" Sleeping {DELAY_BETWEEN_REQUESTS} second...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
        else:
            print()

    return all_books


def deduplicate(books, key="title"):
    """
    Remove duplicate books based on a key field.

    We use a set to track which titles we have already seen.
    Sets have O(1) lookup, so this is efficient even for large lists.

    If two books have the same title, we keep the first one and skip
    the rest. This is a simple deduplication strategy.
    """
    seen = set()
    unique = []

    for book in books:
        if book[key] not in seen:
            seen.add(book[key])
            unique.append(book)

    return unique


def write_csv(books, filepath, fields):
    """
    Write a list of dicts to a CSV file using csv.DictWriter.

    csv.DictWriter is better than manually joining strings because:
    1. It handles commas inside values (wraps them in quotes).
    2. It handles quotes inside values (escapes them).
    3. It writes a proper header row.
    4. It maps dict keys to columns automatically.
    """

    # Create the output directory if it does not exist.
    # exist_ok=True means "don't raise an error if it already exists."
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Open the file for writing. newline="" is required on Windows to prevent
    # extra blank lines between rows. It is harmless on macOS/Linux.
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)

        # writeheader() writes the column names as the first row.
        writer.writeheader()

        # writerows() writes all the dicts at once.
        # Each dict becomes one row. The keys must match fieldnames.
        writer.writerows(books)

    print(f"Wrote {len(books)} rows to {filepath}")


def preview_books(books, count=3):
    """Print a few rows so the user can verify the data looks right."""
    print(f"\nPreview (first {count} rows):")
    for book in books[:count]:
        print(f"  {book['title']}, {book['price']}, {book['rating']}, {book['availability']}")


def main():
    # Step 1: Scrape multiple pages
    all_books = scrape_pages(PAGES_TO_SCRAPE)

    if not all_books:
        print("No books collected. Nothing to write.")
        return

    print(f"\nCollected {len(all_books)} books total.")

    # Step 2: Deduplicate by title
    unique_books = deduplicate(all_books, key="title")
    removed = len(all_books) - len(unique_books)

    if removed > 0:
        print(f"After deduplication: {len(unique_books)} unique books ({removed} duplicates removed).")
    else:
        print(f"After deduplication: {len(unique_books)} unique books.")

    # Step 3: Write to CSV
    print(f"\nWriting to {OUTPUT_FILE}...")
    write_csv(unique_books, OUTPUT_FILE, CSV_FIELDS)

    # Step 4: Preview
    preview_books(unique_books)

    print("\nDone.")


if __name__ == "__main__":
    main()
