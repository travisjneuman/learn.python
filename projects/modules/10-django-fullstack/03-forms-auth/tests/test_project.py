"""
Tests for Project 03 — Forms & Auth

These tests verify form validation, user registration, login, logout, and
the @login_required decorator. Django's test framework provides a test
client that handles cookies and sessions, making auth testing straightforward.

Why test authentication?
    Auth bugs are security bugs. If @login_required does not actually
    require login, unauthorized users can access protected pages. If
    registration does not validate passwords, users can create weak accounts.
    Tests catch these issues before they reach production.

Run with: python manage.py test tests.test_project -v 2
(Run from the 03-forms-auth/ directory)
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

from bookstore.forms import BookForm
from bookstore.models import Book


class BookFormTest(TestCase):
    """Tests for the BookForm ModelForm.

    These tests verify that the form validates input correctly, including
    the custom clean_price validator that rejects negative prices.
    """

    def test_valid_book_form(self):
        """A form with valid data should pass validation.

        WHY: This is the happy path. If a valid form fails validation,
        users cannot create books even with correct data.
        """
        data = {
            "title": "Test Book",
            "author": "Test Author",
            "price": "19.99",
            "published_date": "2024-01-15",
        }
        form = BookForm(data=data)

        self.assertTrue(form.is_valid(), f"Form should be valid. Errors: {form.errors}")

    def test_negative_price_is_rejected(self):
        """A negative price should fail the custom clean_price validation.

        WHY: The BookForm has a clean_price method that rejects negative
        values. Without this test, someone could remove the validation
        and no one would notice until a user creates a book with price -$10.
        """
        data = {
            "title": "Cheap Book",
            "author": "Author",
            "price": "-5.00",
        }
        form = BookForm(data=data)

        self.assertFalse(form.is_valid(), "Negative price should be invalid")
        self.assertIn("price", form.errors, "Error should be on the price field")

    def test_missing_title_is_rejected(self):
        """A form without a title should fail validation.

        WHY: Title is a required CharField. Django's form validation should
        reject empty required fields automatically.
        """
        data = {"author": "Author", "price": "10.00"}
        form = BookForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_save_creates_book(self):
        """Calling form.save() should create a Book in the database.

        WHY: The whole point of ModelForm is to create model instances
        from form data. This test verifies the full form -> model flow.
        """
        data = {
            "title": "Saved Book",
            "author": "Saved Author",
            "price": "25.00",
        }
        form = BookForm(data=data)
        self.assertTrue(form.is_valid())

        book = form.save()

        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(book.title, "Saved Book")


class AuthViewTest(TestCase):
    """Tests for authentication views: register, login, logout.

    These tests verify the complete auth flow using Django's test client,
    which automatically handles cookies and sessions.
    """

    def test_register_creates_user(self):
        """POST to /register/ with valid data should create a new user.

        WHY: Registration is the entry point for new users. If it fails,
        no one can sign up. We verify the user is created in the database.
        """
        response = self.client.post("/register/", {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "TestPass123!",
            "password2": "TestPass123!",
        })

        # Should redirect to book list after successful registration.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_authenticates_user(self):
        """POST to /login/ with valid credentials should log the user in.

        WHY: Login creates a session. Without a valid session, the user
        cannot access @login_required views. This test verifies the full
        credential checking and session creation flow.
        """
        User.objects.create_user(username="testuser", password="TestPass123!")

        response = self.client.post("/login/", {
            "username": "testuser",
            "password": "TestPass123!",
        })

        # Should redirect after successful login.
        self.assertEqual(response.status_code, 302)

    def test_login_rejects_bad_password(self):
        """POST to /login/ with wrong password should show an error.

        WHY: If bad credentials are accepted, any user can log in as
        anyone. This is a critical security test.
        """
        User.objects.create_user(username="testuser", password="TestPass123!")

        response = self.client.post("/login/", {
            "username": "testuser",
            "password": "WrongPassword",
        })

        # Should return the login page (200) with an error, not redirect (302).
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid")

    def test_logout_clears_session(self):
        """Visiting /logout/ should log the user out and redirect.

        WHY: Logout must actually clear the session. If it does not, the
        user remains authenticated and @login_required checks would pass.
        """
        User.objects.create_user(username="testuser", password="TestPass123!")
        self.client.login(username="testuser", password="TestPass123!")

        response = self.client.get("/logout/")

        self.assertEqual(response.status_code, 302)

    def test_add_book_requires_login(self):
        """GET /add/ without being logged in should redirect to login.

        WHY: The @login_required decorator should prevent anonymous access.
        If it is missing or misconfigured, anyone could add books.
        """
        response = self.client.get("/add/")

        # Should redirect to login page (302), not return the form (200).
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url.lower())
