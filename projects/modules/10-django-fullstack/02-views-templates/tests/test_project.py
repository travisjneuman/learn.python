"""
Tests for Project 02 — Views & Templates

These tests verify Django views using Django's test framework. They test
the book_list and book_detail views by making HTTP requests through
Django's test client and checking the responses.

Why use django.test.TestCase?
    Django's TestCase wraps each test in a database transaction that is
    rolled back after the test. This means each test starts with a clean
    database without needing to manually delete data. It also provides
    self.client for making HTTP requests.

Run with: python manage.py test tests.test_project -v 2
(Run from the 02-views-templates/ directory)
"""

import os
import sys

import django
from django.conf import settings

# Configure Django settings before importing any Django modules.
# This is required when running tests outside of manage.py.
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()

from django.test import TestCase

from bookstore.models import Book


class BookListViewTest(TestCase):
    """Tests for the book_list view (GET /books/).

    These tests verify that the view returns the correct template and
    includes books from the database in the context.
    """

    def test_book_list_returns_200(self):
        """GET /books/ should return HTTP 200 (OK).

        WHY: A 200 response means the view function ran successfully and
        returned an HTML page. A 500 would mean a code error; a 404 would
        mean the URL pattern is not configured.
        """
        response = self.client.get("/books/")

        self.assertEqual(response.status_code, 200)

    def test_book_list_uses_correct_template(self):
        """The book list view should render the book_list.html template.

        WHY: Django can render any template. If the template name is wrong
        (typo, wrong directory), Django might render the wrong page or
        raise a TemplateDoesNotExist error.
        """
        response = self.client.get("/books/")

        self.assertTemplateUsed(response, "bookstore/book_list.html")

    def test_book_list_shows_books(self):
        """The book list should include books from the database.

        WHY: The view passes a 'books' queryset to the template. If the
        context variable name is wrong or the queryset is empty despite
        having data, the template would show nothing.
        """
        Book.objects.create(
            title="Test Book",
            author="Test Author",
            price=19.99,
        )

        response = self.client.get("/books/")

        # The response context contains the template variables.
        self.assertIn("books", response.context)
        self.assertEqual(len(response.context["books"]), 1)

    def test_book_list_empty(self):
        """The book list should work when no books exist.

        WHY: An empty database should not cause an error. The view should
        return a 200 with an empty queryset. The template should handle
        the "no books" case gracefully.
        """
        response = self.client.get("/books/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["books"]), 0)


class BookDetailViewTest(TestCase):
    """Tests for the book_detail view (GET /books/<pk>/).

    These tests verify that the view returns the correct book and
    handles non-existent books with a 404.
    """

    def setUp(self):
        """Create a test book for use in detail view tests.

        setUp runs before each test method, providing a fresh book
        with a known pk.
        """
        self.book = Book.objects.create(
            title="Django for Beginners",
            author="William Vincent",
            price=29.99,
        )

    def test_book_detail_returns_200(self):
        """GET /books/<pk>/ should return 200 for an existing book.

        WHY: The detail view uses get_object_or_404, which returns 200
        if the object exists. This test verifies the happy path.
        """
        response = self.client.get(f"/books/{self.book.pk}/")

        self.assertEqual(response.status_code, 200)

    def test_book_detail_uses_correct_template(self):
        """The detail view should render the book_detail.html template."""
        response = self.client.get(f"/books/{self.book.pk}/")

        self.assertTemplateUsed(response, "bookstore/book_detail.html")

    def test_book_detail_shows_correct_book(self):
        """The detail view should pass the correct book to the template.

        WHY: If the pk lookup is wrong, the view might return a different
        book or crash. This test verifies the template receives the book
        we requested.
        """
        response = self.client.get(f"/books/{self.book.pk}/")

        self.assertEqual(response.context["book"].pk, self.book.pk)
        self.assertEqual(response.context["book"].title, "Django for Beginners")

    def test_book_detail_404_for_nonexistent(self):
        """GET /books/<pk>/ should return 404 for a non-existent book.

        WHY: get_object_or_404 should raise Http404 when the book does
        not exist. Returning 200 with None would be a bug.
        """
        response = self.client.get("/books/99999/")

        self.assertEqual(response.status_code, 404)
