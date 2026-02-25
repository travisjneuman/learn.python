"""
Tests for Project 04 — REST Framework

These tests verify the DRF API endpoints for Authors and Books using
Django's test framework. DRF's APIClient provides a convenient way to
make JSON requests and inspect responses.

Why test REST APIs?
    APIs are contracts. If an endpoint changes its response format, URL,
    or status code, all clients (frontends, mobile apps, other services)
    break. Tests lock down the API contract so changes are intentional.

Run with: python manage.py test tests.test_project -v 2
(Run from the 04-rest-framework/ directory)
"""

import os
import sys

import django
from django.conf import settings

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()

from django.test import TestCase
from rest_framework.test import APIClient

from bookstore.models import Author, Book


class AuthorAPITest(TestCase):
    """Tests for the Author API endpoints.

    These test the full CRUD lifecycle: create, list, retrieve, update, delete.
    """

    def setUp(self):
        """Create an API client and a sample author."""
        self.client = APIClient()
        self.author = Author.objects.create(name="Jane Austen", bio="English novelist")

    def test_list_authors(self):
        """GET /api/authors/ should return a list of all authors.

        WHY: The list endpoint is the entry point for API consumers. If it
        returns wrong data or the wrong format, nothing else works.
        """
        response = self.client.get("/api/authors/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Jane Austen")

    def test_create_author(self):
        """POST /api/authors/ should create a new author.

        WHY: API creation must validate input (required fields, types) and
        return the created object with its generated ID. This test verifies
        the full serialization -> validation -> save -> response cycle.
        """
        response = self.client.post("/api/authors/", {
            "name": "Charles Dickens",
            "bio": "Victorian era novelist",
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Charles Dickens")
        self.assertIn("id", response.data)
        self.assertEqual(Author.objects.count(), 2)

    def test_retrieve_author(self):
        """GET /api/authors/{id}/ should return a single author.

        WHY: Detail endpoints let API consumers fetch specific resources.
        The response should include all serialized fields.
        """
        response = self.client.get(f"/api/authors/{self.author.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Jane Austen")
        self.assertEqual(response.data["bio"], "English novelist")

    def test_delete_author(self):
        """DELETE /api/authors/{id}/ should remove the author.

        WHY: Deletion is destructive and must actually remove the resource.
        If it silently fails, stale data accumulates in the database.
        """
        response = self.client.delete(f"/api/authors/{self.author.pk}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Author.objects.count(), 0)


class BookAPITest(TestCase):
    """Tests for the Book API endpoints.

    These tests verify that the Author-Book relationship is handled
    correctly in the API: accepting author ID on input and including
    author_name on output.
    """

    def setUp(self):
        """Create an API client, a sample author, and a sample book."""
        self.client = APIClient()
        self.author = Author.objects.create(name="Jane Austen")
        self.book = Book.objects.create(
            title="Pride and Prejudice",
            author=self.author,
            price="12.99",
        )

    def test_list_books(self):
        """GET /api/books/ should return all books with author_name included.

        WHY: The BookSerializer includes a computed author_name field via
        SerializerMethodField. This test verifies the serializer includes it.
        """
        response = self.client.get("/api/books/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Pride and Prejudice")
        self.assertEqual(response.data[0]["author_name"], "Jane Austen")

    def test_create_book_with_author_id(self):
        """POST /api/books/ should accept an author ID and create the book.

        WHY: The API consumer sends an author ID (integer), not the author
        object. The serializer must resolve this to the actual Author instance.
        If the ForeignKey handling is wrong, creation fails.
        """
        response = self.client.post("/api/books/", {
            "title": "Sense and Sensibility",
            "author": self.author.pk,
            "price": "10.99",
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Sense and Sensibility")
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book_includes_author_name(self):
        """GET /api/books/{id}/ should include both author ID and author_name.

        WHY: The detail response must include the computed author_name field.
        If get_author_name is broken, the field might be missing or null.
        """
        response = self.client.get(f"/api/books/{self.book.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["author"], self.author.pk)
        self.assertEqual(response.data["author_name"], "Jane Austen")

    def test_book_404_for_nonexistent(self):
        """GET /api/books/{id}/ should return 404 for non-existent books.

        WHY: ModelViewSet handles this automatically, but we verify it
        works correctly and returns the expected status code.
        """
        response = self.client.get("/api/books/99999/")

        self.assertEqual(response.status_code, 404)
