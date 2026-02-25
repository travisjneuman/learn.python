"""
Project 02 — Parse HTML

This script fetches a page from books.toscrape.com, parses the HTML
with BeautifulSoup, and extracts the title and price of every book
on the page.

You will learn: BeautifulSoup basics, find(), find_all(), and
extracting text and attributes from HTML elements.
"""

import requests

# BeautifulSoup lives in the bs4 package.
# You installed it with: pip install beautifulsoup4
# The import name (bs4) is different from the package name (beautifulsoup4).
from bs4 import BeautifulSoup


def fetch_page(url):
    """Fetch a web page and return the response text, or None on failure."""
    print(f"Fetching {url} ...")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None

    return response.text


def parse_books(html):
    """
    Parse HTML and extract book titles and prices.

    BeautifulSoup turns raw HTML into a tree of objects you can search.
    Think of it like a map of the page — you can ask "find all the <h3> tags"
    or "find the element with class 'price_color'".

    Returns a list of tuples: [(title, price), ...]
    """

    # Create a BeautifulSoup object from the HTML string.
    # "lxml" is the parser — it reads the HTML and builds the tree.
    # Other options: "html.parser" (built-in, slower) or "html5lib" (very lenient).
    print("Parsing HTML with BeautifulSoup...")
    soup = BeautifulSoup(html, "lxml")

    books = []

    # Each book on the page is inside an <article> tag with class "product_pod".
    # find_all() returns a list of ALL matching elements.
    # find() returns only the FIRST match (or None if nothing matches).
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        # The book title is inside an <h3> tag, inside an <a> tag.
        # The title attribute on the <a> tag has the full title text.
        # We use find() here because there is only one <h3> per article.
        title_tag = article.find("h3")
        link_tag = title_tag.find("a")

        # The "title" attribute contains the full title.
        # link_tag["title"] gets an attribute, like href or title.
        # link_tag.text would give us the visible text, which is sometimes truncated.
        title = link_tag["title"]

        # The price is inside a <p> tag with class "price_color".
        # .text gives us the text content of the element, like "£51.77".
        price_tag = article.find("p", class_="price_color")
        price = price_tag.text.strip()

        books.append((title, price))

    return books


def display_books(books):
    """Print the list of books in a formatted table."""
    print(f"\nFound {len(books)} books on the page:\n")

    for i, (title, price) in enumerate(books, start=1):
        # Format each line so titles and prices line up in columns.
        # :<45 means left-align the title in a 45-character-wide column.
        print(f"  {i:>3}. {title:<45} {price}")


def main():
    url = "http://books.toscrape.com/"

    # Step 1: Fetch the raw HTML
    html = fetch_page(url)
    if html is None:
        return

    # Step 2: Parse the HTML and extract book data
    books = parse_books(html)

    # Step 3: Display the results
    if books:
        display_books(books)
    else:
        print("No books found. The page structure may have changed.")

    print(f"\nDone. Extracted {len(books)} books.")


if __name__ == "__main__":
    main()
