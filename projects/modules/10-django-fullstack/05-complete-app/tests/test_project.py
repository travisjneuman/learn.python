"""
Tests for Project 05 — Complete App

These tests verify the complete bookstore application, which combines
HTML views (for browsers) and REST API views (for programmatic access).
Both share the same models and database.

Why test both HTML and API?
    The complete app serves two interfaces: HTML pages for human users
    and JSON endpoints for programs. A bug in shared code (models, forms)
    affects both. Testing both interfaces verifies the full application.

Run with: python manage.py test tests.test_project -v 2
(Run from the 05-complete-app/ directory)
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

from django.contrib.auth.models import User
from django.test import TestCase

from bookstore.models import Author, Book


class HTMLViewTest(TestCase):
    """Tests for the browser-facing HTML views.

    These use Django's test client which returns rendered HTML responses.
    """

    def setUp(self):
        """Create sample data for view tests."""
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            price="19.99",
        )

    def test_book_list_returns_200(self):
        """GET /books/ should return the book list page.

        WHY: The list page is the app's landing page. If it fails, users
        see a server error on their first visit.
        """
        response = self.client.get("/books/")

        self.assertEqual(response.status_code, 200)

    def test_book_list_includes_books(self):
        """The book list should include books from the database.

        WHY: The view uses select_related("author") for performance. If
        the query is wrong, the template might show no books or crash
        when accessing book.author.name.
        """
        response = self.client.get("/books/")

        self.assertIn("books", response.context)
        self.assertEqual(len(response.context["books"]), 1)

    def test_book_detail_returns_200(self):
        """GET /books/<pk>/ should return the detail page.

        WHY: Detail pages use get_object_or_404 with select_related.
        This test verifies the lookup and template rendering work together.
        """
        response = self.client.get(f"/books/{self.book.pk}/")

        self.assertEqual(response.status_code, 200)

    def test_book_detail_404_for_nonexistent(self):
        """GET /books/<pk>/ should return 404 for non-existent books."""
        response = self.client.get("/books/99999/")

        self.assertEqual(response.status_code, 404)


class AuthTest(TestCase):
    """Tests for authentication views.

    These verify the login, register, and logout flows work correctly
    with the complete app's URL configuration.
    """

    def test_register_creates_user_and_redirects(self):
        """Registration should create a user and redirect to book list.

        WHY: After registration, the user should be automatically logged
        in and redirected. If the redirect is missing, the user sees the
        registration form again, which is confusing.
        """
        response = self.client.post("/register/", {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_works(self):
        """Login with valid credentials should redirect.

        WHY: The login view uses Django's authenticate() function. If
        credentials are valid, it creates a session and redirects.
        """
        User.objects.create_user(username="user", password="Pass123!")

        response = self.client.post("/login/", {
            "username": "user",
            "password": "Pass123!",
        })

        self.assertEqual(response.status_code, 302)

    def test_login_fails_with_bad_password(self):
        """Login with wrong password should show error, not redirect.

        WHY: Security critical — bad credentials must be rejected.
        The response should stay on the login page (200) with an error.
        """
        User.objects.create_user(username="user", password="Pass123!")

        response = self.client.post("/login/", {
            "username": "user",
            "password": "WrongPass",
        })

        self.assertEqual(response.status_code, 200)

    def test_add_book_requires_login(self):
        """The add book page should redirect anonymous users to login.

        WHY: @login_required must actually enforce authentication. Without
        testing, a missing decorator would go unnoticed.
        """
        response = self.client.get("/add/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url.lower())

    def test_add_book_works_when_logged_in(self):
        """A logged-in user should be able to access the add book form.

        WHY: The form page should return 200 for authenticated users.
        If it returns 302 (redirect to login), the decorator is too
        restrictive or the login did not create a valid session.
        """
        User.objects.create_user(username="user", password="Pass123!")
        self.client.login(username="user", password="Pass123!")

        response = self.client.get("/add/")

        self.assertEqual(response.status_code, 200)

    def test_logout_redirects(self):
        """Logout should clear the session and redirect."""
        User.objects.create_user(username="user", password="Pass123!")
        self.client.login(username="user", password="Pass123!")

        response = self.client.get("/logout/")

        self.assertEqual(response.status_code, 302)


class ModelTest(TestCase):
    """Tests for the Author and Book models.

    These verify model behavior independent of views: __str__ methods,
    relationships, and ordering.
    """

    def test_author_str(self):
        """Author.__str__ should return the author's name.

        WHY: __str__ appears in the admin interface, in template output
        like {{ author }}, and in debugging. Getting it wrong makes the
        admin unusable.
        """
        author = Author.objects.create(name="Jane Austen")

        self.assertEqual(str(author), "Jane Austen")

    def test_book_str(self):
        """Book.__str__ should return 'title by author_name'."""
        author = Author.objects.create(name="Jane Austen")
        book = Book.objects.create(title="Emma", author=author, price="10.99")

        self.assertEqual(str(book), "Emma by Jane Austen")

    def test_author_books_relationship(self):
        """An author's books should be accessible via the reverse relation.

        WHY: The ForeignKey with related_name='books' creates a reverse
        relationship. author.books.all() should return all books by that
        author. If related_name is wrong, this would fail.
        """
        author = Author.objects.create(name="Author")
        Book.objects.create(title="Book 1", author=author, price="10.00")
        Book.objects.create(title="Book 2", author=author, price="15.00")

        self.assertEqual(author.books.count(), 2)
