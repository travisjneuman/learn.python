"""API client for a public data service.

This module fetches data from several endpoints of a fictional API.
Each function works, but they are nearly identical copies of each other.
Your job is to eliminate the duplication.
"""

import json
import urllib.request
import urllib.error


BASE_URL = "https://jsonplaceholder.typicode.com"


def get_users():
    """Fetch all users."""
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "PythonClient/1.0")
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode("utf-8")
        result = json.loads(data)
        return result
    except urllib.error.HTTPError as e:
        print(f"HTTP error fetching users: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"URL error fetching users: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching users: {e}")
        return None


def get_posts():
    """Fetch all posts."""
    url = "https://jsonplaceholder.typicode.com/posts"
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "PythonClient/1.0")
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode("utf-8")
        result = json.loads(data)
        return result
    except urllib.error.HTTPError as e:
        print(f"HTTP error fetching posts: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"URL error fetching posts: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return None


def get_comments():
    """Fetch all comments."""
    url = "https://jsonplaceholder.typicode.com/comments"
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "PythonClient/1.0")
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode("utf-8")
        result = json.loads(data)
        return result
    except urllib.error.HTTPError as e:
        print(f"HTTP error fetching comments: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"URL error fetching comments: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return None


def get_todos():
    """Fetch all todos."""
    url = "https://jsonplaceholder.typicode.com/todos"
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "PythonClient/1.0")
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode("utf-8")
        result = json.loads(data)
        return result
    except urllib.error.HTTPError as e:
        print(f"HTTP error fetching todos: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"URL error fetching todos: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching todos: {e}")
        return None


def get_albums():
    """Fetch all albums."""
    url = "https://jsonplaceholder.typicode.com/albums"
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/json")
        req.add_header("User-Agent", "PythonClient/1.0")
        response = urllib.request.urlopen(req, timeout=10)
        data = response.read().decode("utf-8")
        result = json.loads(data)
        return result
    except urllib.error.HTTPError as e:
        print(f"HTTP error fetching albums: {e.code}")
        return None
    except urllib.error.URLError as e:
        print(f"URL error fetching albums: {e.reason}")
        return None
    except Exception as e:
        print(f"Error fetching albums: {e}")
        return None
