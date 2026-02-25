"""Module 03 / Project 04 — Error Handling.

Learn how to handle HTTP errors, connection failures, timeouts,
and implement retries with exponential backoff.
"""

import requests
import time


def test_successful_request():
    """A normal, successful request for baseline comparison."""
    print("--- Test 1: Successful request ---")

    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

    # raise_for_status() does nothing if the status code is 2xx (success).
    # If the status code is 4xx or 5xx, it raises an HTTPError exception.
    # This is a convenient way to check for errors without writing
    # if/else on the status code every time.
    response.raise_for_status()

    data = response.json()
    print("Status: {} OK".format(response.status_code))
    print("Title:", data["title"])


def test_404_not_found():
    """Request a resource that does not exist. The server returns 404."""
    print("\n--- Test 2: 404 Not Found ---")

    url = "https://jsonplaceholder.typicode.com/posts/99999"
    response = requests.get(url)

    try:
        # This will raise an HTTPError because the status code is 404.
        # The error message includes the status code, reason, and URL.
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        # HTTPError is raised for 4xx (client error) and 5xx (server error)
        # status codes. The exception object contains the response, so you
        # can still inspect it if needed.
        print("HTTP error:", err)


def test_connection_error():
    """Try to reach a server that does not exist."""
    print("\n--- Test 3: Connection error (bad domain) ---")

    url = "https://not-a-real-domain-xyz.com/posts/1"

    try:
        # ConnectionError is raised when the DNS lookup fails, the server
        # refuses the connection, or the network is unreachable.
        requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Connection error: could not reach", url)


def test_timeout():
    """Set an impossibly short timeout to trigger a timeout error."""
    print("\n--- Test 4: Timeout (very short limit) ---")

    url = "https://jsonplaceholder.typicode.com/posts"

    try:
        # The timeout parameter sets the maximum time (in seconds) to wait
        # for the server to respond. 0.001 seconds (1 millisecond) is too
        # short for any real network request, so this will always time out.
        #
        # In production code, a timeout of 5-30 seconds is typical.
        requests.get(url, timeout=0.001)
    except requests.exceptions.Timeout:
        print("Timeout: request to {} took longer than 0.001s".format(url))


def fetch_with_retry(url, max_attempts=3, base_delay=1):
    """Fetch a URL with automatic retries and exponential backoff.

    Exponential backoff means the delay between retries doubles each time:
    - Attempt 1 fails -> wait 1 second
    - Attempt 2 fails -> wait 2 seconds
    - Attempt 3 fails -> wait 4 seconds

    This prevents hammering a struggling server with rapid retries,
    giving it time to recover.

    Returns the Response object on success, or None if all attempts fail.
    """
    for attempt in range(1, max_attempts + 1):
        print("Attempt {} of {}: requesting {}".format(attempt, max_attempts, url))

        try:
            # Set a reasonable timeout for each attempt.
            response = requests.get(url, timeout=10)

            # Check for HTTP errors (4xx, 5xx).
            response.raise_for_status()

            # If we get here, the request succeeded.
            print("Success on attempt {}.".format(attempt))
            return response

        except requests.exceptions.ConnectionError:
            print("  Connection failed.")
        except requests.exceptions.Timeout:
            print("  Request timed out.")
        except requests.exceptions.HTTPError as err:
            print("  HTTP error: {}".format(err))

        # If this was the last attempt, don't sleep — just give up.
        if attempt < max_attempts:
            # Calculate delay: base_delay * 2^(attempt-1)
            # attempt 1 -> base_delay * 1 = 1s
            # attempt 2 -> base_delay * 2 = 2s
            # attempt 3 -> base_delay * 4 = 4s
            delay = base_delay * (2 ** (attempt - 1))
            print("  Retrying in {} seconds...".format(delay))
            time.sleep(delay)

    print("All {} attempts failed.".format(max_attempts))
    return None


def test_retry():
    """Demonstrate the retry function with a URL that should succeed."""
    print("\n--- Test 5: Retry with backoff ---")

    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = fetch_with_retry(url, max_attempts=3, base_delay=1)

    if response is not None:
        data = response.json()
        print("Title:", data["title"])
    else:
        print("Could not fetch the post after all retries.")


if __name__ == "__main__":
    test_successful_request()
    test_404_not_found()
    test_connection_error()
    test_timeout()
    test_retry()
