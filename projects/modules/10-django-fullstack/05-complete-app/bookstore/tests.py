# ============================================================================
# Bookstore Tests — Complete App
# ============================================================================
# Django's test framework builds on Python's unittest module with additions:
#
# - TestCase: each test runs in a transaction that is rolled back after the test,
#   so test data never leaks between tests.
# - self.client: a test HTTP client that simulates browser requests without
#   needing a running server. It can GET, POST, and check responses.
# - A separate test database is created and destroyed for each test run.
#
# Run tests with:
#   python manage.py test
#
# Run a specific test class:
#   python manage.py test bookstore.tests.BookModelTest
#
# Run a specific test method:
#   python manage.py test bookstore.tests.BookModelTest.test_book_str
# ============================================================================

from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book


class BookModelTest(TestCase):
    """Tests for the Book and Author models.

    setUp() runs before each test method. It creates test data that
    every test in this class can use. Because Django rolls back the
    transaction after each test, this data is recreated fresh every time.
    """

    def setUp(self):
        """Create test data: one author and one book."""
        self.author = Author.objects.create(
            name="Test Author",
            bio="A test biography.",
        )
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            price=Decimal("29.99"),
            published_date=date(2024, 1, 15),
        )

    def test_book_str(self):
        """The __str__ method should return 'Title by Author'."""
        self.assertEqual(str(self.book), "Test Book by Test Author")

    def test_author_str(self):
        """The __str__ method should return the author's name."""
        self.assertEqual(str(self.author), "Test Author")

    def test_book_author_relationship(self):
        """A book's author should be accessible, and the reverse too."""
        # Forward: book -> author
        self.assertEqual(self.book.author, self.author)

        # Reverse: author -> books (using related_name="books")
        self.assertIn(self.book, self.author.books.all())

    def test_book_default_ordering(self):
        """Books should be ordered by published_date descending."""
        older_book = Book.objects.create(
            title="Older Book",
            author=self.author,
            price=Decimal("19.99"),
            published_date=date(2020, 6, 1),
        )
        books = list(Book.objects.all())
        # Newest first (2024 before 2020)
        self.assertEqual(books[0], self.book)
        self.assertEqual(books[1], older_book)


class BookViewTest(TestCase):
    """Tests for the HTML views.

    self.client is Django's test client. It simulates HTTP requests
    without starting a real server. You can check:
    - response.status_code: the HTTP status code
    - response.context: the template context variables
    - response.content: the raw HTML bytes
    - response.templates: which templates were rendered
    """

    def setUp(self):
        """Create test data and a test user."""
        self.author = Author.objects.create(name="View Author")
        self.book = Book.objects.create(
            title="View Test Book",
            author=self.author,
            price=Decimal("24.99"),
        )
        # Create a user for testing protected views.
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def test_book_list_status(self):
        """GET /books/ should return 200."""
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)

    def test_book_list_contains_book(self):
        """The book list page should contain our test book's title."""
        response = self.client.get(reverse("book_list"))
        self.assertContains(response, "View Test Book")

    def test_book_detail_status(self):
        """GET /books/<pk>/ should return 200 for an existing book."""
        response = self.client.get(reverse("book_detail", args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_404(self):
        """GET /books/99999/ should return 404 for a non-existent book."""
        response = self.client.get(reverse("book_detail", args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_add_book_requires_login(self):
        """GET /books/add/ should redirect to login for anonymous users."""
        response = self.client.get(reverse("add_book"))
        # 302 means redirect. Django sends anonymous users to the login page.
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_add_book_authenticated(self):
        """Logged-in users should be able to access the add book form."""
        # self.client.login() authenticates the test client.
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("add_book"))
        self.assertEqual(response.status_code, 200)


class BookAPITest(TestCase):
    """Tests for the REST API endpoints.

    These tests verify that the DRF viewsets return correct JSON responses.
    The test client can also interact with API endpoints.
    """

    def setUp(self):
        """Create test data for API tests."""
        self.author = Author.objects.create(name="API Author")
        self.book = Book.objects.create(
            title="API Test Book",
            author=self.author,
            price=Decimal("34.99"),
            published_date=date(2024, 3, 1),
        )

    def test_api_book_list(self):
        """GET /api/books/ should return a list of books as JSON."""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, 200)

        # response.json() parses the JSON response body.
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "API Test Book")
        self.assertEqual(data[0]["author_name"], "API Author")

    def test_api_book_detail(self):
        """GET /api/books/<pk>/ should return a single book."""
        response = self.client.get(f"/api/books/{self.book.pk}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "API Test Book")

    def test_api_create_book(self):
        """POST /api/books/ should create a new book."""
        response = self.client.post(
            "/api/books/",
            data={
                "title": "New API Book",
                "author": self.author.pk,
                "price": "19.99",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)  # 201 Created
        self.assertEqual(Book.objects.count(), 2)

    def test_api_author_list(self):
        """GET /api/authors/ should return a list of authors."""
        response = self.client.get("/api/authors/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "API Author")
