"""
Project 03 — Extract Structured Data

This script fetches the books.toscrape.com homepage, extracts four fields
per book (title, price, rating, availability), and stores each book as
a dictionary. It then prints the data in a formatted table.

You will learn: building a list of dicts from scraped data, mapping CSS
classes to values, and formatting tabular output.
"""

import requests
from bs4 import BeautifulSoup


# This dictionary maps CSS class names to numeric star ratings.
# On books.toscrape.com, each book has a <p> tag with a class like
# "star-rating Three". We need to convert words to numbers.
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def fetch_page(url):
    """Fetch a page and return the HTML text, or None on failure."""
    print(f"Fetching {url} ...")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None

    return response.text


def extract_books(html):
    """
    Parse HTML and extract structured data for each book.

    Returns a list of dictionaries, where each dict has keys:
    - title: the full book title
    - price: the price string (e.g., "£51.77")
    - rating: integer 1–5
    - availability: "In stock" or "Out of stock"

    A list of dicts is the standard way to represent tabular data in Python.
    Each dict is one row, each key is a column. This structure works with
    csv.DictWriter, pandas DataFrames, and most data tools.
    """
    soup = BeautifulSoup(html, "lxml")
    print("Parsing page and extracting book data...")

    books = []
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        # --- Title ---
        # The full title is in the "title" attribute of the <a> tag inside <h3>.
        title_tag = article.find("h3").find("a")
        title = title_tag["title"]

        # --- Price ---
        # The price lives in a <p> tag with class "price_color".
        price_tag = article.find("p", class_="price_color")
        price = price_tag.text.strip()

        # --- Rating ---
        # The rating is encoded as a CSS class on a <p> tag.
        # The tag has two classes: "star-rating" and the rating word.
        # For example: <p class="star-rating Three">
        # We need the second class, which is the rating word.
        rating_tag = article.find("p", class_="star-rating")

        # rating_tag["class"] returns a list of classes, like ["star-rating", "Three"].
        # We grab the second one (index 1) and look it up in our mapping.
        rating_word = rating_tag["class"][1]
        rating = RATING_MAP.get(rating_word, 0)

        # --- Availability ---
        # The availability text is in a <p> tag with class "instock availability"
        # or "outofstock availability". We just grab the text.
        avail_tag = article.find("p", class_="availability")
        availability = avail_tag.text.strip()

        # Build a dictionary for this book and add it to the list.
        book = {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
        }
        books.append(book)

    return books


def display_table(books):
    """
    Print the list of books as a formatted table.

    We use Python string formatting to align columns. The format spec
    :<40 means left-align in a 40-character column. :>8 means right-align
    in an 8-character column.
    """
    # Print the header row
    print()
    print(f" {'#':>3}  {'Title':<40} {'Price':<8} {'Rating':<7} {'Available'}")
    print(f" {'---':>3}  {'-'*40} {'-'*8} {'-'*7} {'-'*9}")

    # Print each book as a row
    for i, book in enumerate(books, start=1):
        rating_str = f"{book['rating']} star"
        print(
            f" {i:>3}  {book['title']:<40} {book['price']:<8} "
            f"{rating_str:<7} {book['availability']}"
        )


def main():
    url = "http://books.toscrape.com/"

    # Step 1: Fetch the page
    html = fetch_page(url)
    if html is None:
        return

    # Step 2: Extract structured data
    books = extract_books(html)

    if not books:
        print("No books found. The page structure may have changed.")
        return

    # Step 3: Display the results
    display_table(books)

    # Print a summary
    print(f"\nExtracted {len(books)} books with {len(books[0])} fields each.")
    print("Done.")


if __name__ == "__main__":
    main()
