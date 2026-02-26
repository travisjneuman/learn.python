"""Module 03 / Project 05 — API Client Class.

Build a reusable API client using requests.Session that encapsulates
base URL, headers, error handling, and endpoint methods.
"""

import requests
import json


# WHY a client class instead of standalone functions? -- Encapsulating
# base_url, headers, and a Session in a class means callers don't repeat
# configuration on every call. The Session reuses TCP connections (HTTP
# keep-alive), avoiding the overhead of a new TLS handshake per request.
class JSONPlaceholderClient:
    """A reusable client for the JSONPlaceholder API.

    This class wraps requests.Session to provide:
    - A base URL that all requests build on (no repeating the domain)
    - Shared headers across all requests (set once in __init__)
    - Connection reuse (the Session keeps the TCP connection open)
    - Clean methods for each API endpoint
    - Internal error handling so callers get data or None, not exceptions

    Using a Session is more efficient than calling requests.get() directly
    because the underlying TCP connection is reused across requests instead
    of being opened and closed every time.
    """

    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        """Initialize the client with a base URL and a Session.

        The Session object is created once and reused for every request.
        We also set default headers that apply to all requests made
        through this client.
        """
        # Store the base URL. We strip trailing slashes so we can safely
        # append paths like /posts/1 without double slashes.
        self.base_url = base_url.rstrip("/")

        # Create a Session. This is the core of the client.
        # All requests go through this session, which means:
        # - TCP connections are reused (faster)
        # - Cookies are persisted automatically
        # - Headers set here apply to every request
        self.session = requests.Session()

        # Set default headers for all requests.
        self.session.headers.update({
            "User-Agent": "learn-python-module03-client/1.0",
            "Accept": "application/json",
        })

    def _build_url(self, path):
        """Build a full URL from the base URL and a path.

        Example: base="https://jsonplaceholder.typicode.com", path="/posts/1"
        Result:  "https://jsonplaceholder.typicode.com/posts/1"
        """
        return "{}{}".format(self.base_url, path)

    def get_post(self, post_id):
        """Fetch a single post by ID.

        Returns the post as a dictionary, or None if not found.
        Error handling is done internally so the caller does not need
        to worry about exceptions or status codes.
        """
        url = self._build_url("/posts/{}".format(post_id))

        try:
            response = self.session.get(url, timeout=10)

            # If the post does not exist, the API returns 404.
            # Instead of raising an exception, we return None.
            if response.status_code == 404:
                return None

            # For other errors (500, etc.), raise so the except catches it.
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as err:
            # RequestException is the base class for all requests errors.
            # Catching it here means connection errors, timeouts, and HTTP
            # errors are all handled the same way: log and return None.
            print("Error fetching post {}: {}".format(post_id, err))
            return None

    def get_posts(self, user_id=None, limit=10):
        """Fetch multiple posts, optionally filtered by user.

        Returns a list of post dictionaries. Returns an empty list
        if the request fails.
        """
        url = self._build_url("/posts")

        # Build query parameters. Only include userId if it was provided.
        params = {"_limit": limit}
        if user_id is not None:
            params["userId"] = user_id

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as err:
            print("Error fetching posts: {}".format(err))
            return []

    def create_post(self, title, body, user_id):
        """Create a new post via POST request.

        Returns the created post (with server-assigned ID) as a dictionary,
        or None if the request fails.

        Note: JSONPlaceholder accepts the data but does not actually save it.
        The returned ID will always be 101.
        """
        url = self._build_url("/posts")

        payload = {
            "title": title,
            "body": body,
            "userId": user_id,
        }

        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as err:
            print("Error creating post: {}".format(err))
            return None

    def close(self):
        """Close the underlying Session and release the connection.

        Call this when you are done using the client. Alternatively,
        use the client as a context manager (see __enter__/__exit__).
        """
        self.session.close()

    def __enter__(self):
        """Support using the client as a context manager: with Client() as c:"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the session when exiting the context manager."""
        self.close()
        # Return False so exceptions are not suppressed.
        return False


def main():
    """Demonstrate the JSONPlaceholder client."""

    # Using the client as a context manager ensures the session is closed
    # when we are done, even if an exception occurs.
    with JSONPlaceholderClient() as client:

        print("--- Using the JSONPlaceholder client ---")

        # Fetch a single post.
        print("\nFetching post 1...")
        post = client.get_post(1)
        if post:
            print("  Title:", post["title"])
            print("  Author user ID:", post["userId"])

        # Fetch posts by a specific user with a limit.
        print("\nFetching posts by user 2 (limit 3)...")
        posts = client.get_posts(user_id=2, limit=3)
        print("  Found {} posts:".format(len(posts)))
        for p in posts:
            print("    Post {}: {}".format(p["id"], p["title"]))

        # Create a new post.
        print("\nCreating a new post...")
        created = client.create_post(
            title="Testing the Client",
            body="This post was created through the client class.",
            user_id=1,
        )
        if created:
            print("  Created post with ID:", created["id"])
            print("  Title:", created["title"])
            print("  Body:", created["body"])

        # Fetch a post that does not exist.
        print("\nFetching a post that does not exist (ID 99999)...")
        missing = client.get_post(99999)
        if missing is None:
            print("  Result: None (post not found)")

        # Explain session reuse.
        print("\n--- Session reuse demonstration ---")
        print("The client reuses one TCP connection for all requests.")
        print("This is faster and more efficient than creating a new connection each time.")


if __name__ == "__main__":
    main()
