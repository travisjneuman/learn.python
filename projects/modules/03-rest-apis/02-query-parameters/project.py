"""Module 03 / Project 02 — Query Parameters.

Learn how to pass query parameters to filter and paginate API results.
Covers two approaches: the params dict and the URL string.
"""

import requests


def fetch_posts_by_user_params_dict(user_id):
    """Fetch all posts by a specific user using the params dict approach.

    The params dict is the preferred way to pass query parameters.
    requests will URL-encode the values and append them to the URL
    automatically: /posts?userId=3
    """
    url = "https://jsonplaceholder.typicode.com/posts"

    # Pass parameters as a dictionary. requests turns this into
    # ?userId=3 appended to the URL. This approach is cleaner and
    # handles special characters (spaces, &, =) automatically.
    params = {"userId": user_id}
    response = requests.get(url, params=params)
    posts = response.json()

    print("--- Method 1: params dict ---")
    print("Fetching posts by user {} (using params dict)...".format(user_id))
    print("Found {} posts by user {}.".format(len(posts), user_id))

    # Show a preview of the first 3 posts.
    for post in posts[:3]:
        print("  Post {}: {}".format(post["id"], post["title"]))
    if len(posts) > 3:
        print("  (showing first 3)")

    return posts


def fetch_posts_by_user_url_string(user_id):
    """Fetch all posts by a specific user using a URL string.

    This approach puts the query parameters directly in the URL.
    It works but is harder to maintain — you have to handle URL encoding
    yourself and the URL becomes harder to read with many parameters.
    """
    # Here we build the URL string ourselves. For simple cases this is
    # fine, but with multiple parameters or special characters, the
    # params dict approach is safer.
    url = "https://jsonplaceholder.typicode.com/posts?userId={}".format(user_id)

    response = requests.get(url)
    posts = response.json()

    print("\n--- Method 2: URL string ---")
    print("Fetching posts by user {} (using URL string)...".format(user_id))
    print("Found {} posts by user {}.".format(len(posts), user_id))

    return posts


def paginate_posts(page_size, num_pages):
    """Fetch posts in pages using _start and _limit parameters.

    JSONPlaceholder supports pagination with:
    - _start: the index to start from (0-based)
    - _limit: how many items to return

    Other APIs might use page/per_page or offset/limit instead.
    The concept is the same: fetch a slice of the full dataset.
    """
    url = "https://jsonplaceholder.typicode.com/posts"

    print("\n--- Pagination ---")

    for page_num in range(1, num_pages + 1):
        # _start is 0-based. Page 1 starts at 0, page 2 starts at page_size, etc.
        start = (page_num - 1) * page_size

        params = {
            "_start": start,
            "_limit": page_size,
        }

        response = requests.get(url, params=params)
        posts = response.json()

        # Build a comma-separated string of post IDs for display.
        ids = ", ".join(str(post["id"]) for post in posts)
        print("Page {}: fetched {} posts (IDs: {})".format(page_num, len(posts), ids))


if __name__ == "__main__":
    # Fetch posts by user 3 using both methods.
    fetch_posts_by_user_params_dict(3)
    fetch_posts_by_user_url_string(3)

    # Paginate through posts, 5 per page, 3 pages.
    paginate_posts(page_size=5, num_pages=3)
