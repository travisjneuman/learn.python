# Module 10 / Project 05 — Complete App

Home: [README](../../../../README.md)

## Focus

A full CRUD application combining models, views, templates, Django REST Framework, authentication, and tests.

## Why this project exists

This project ties together everything from Projects 01 through 04 into a single, complete application. It demonstrates how Django's components work together in a real project: models define the data, views handle logic, templates render HTML for browsers, DRF serializers serve JSON for API clients, and Django's auth system controls access.

The addition of tests is critical. Django includes a test framework built on Python's `unittest` that provides a test client for simulating HTTP requests, database isolation between tests, and helpers for common assertions. Writing tests ensures your application works correctly and continues to work as you make changes.

## Run

```bash
cd projects/modules/10-django-fullstack/05-complete-app
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open your browser to:

- **http://127.0.0.1:8000/books/** — browse all books (HTML)
- **http://127.0.0.1:8000/books/add/** — add a book (requires login)
- **http://127.0.0.1:8000/api/books/** — REST API (JSON, browsable)
- **http://127.0.0.1:8000/api/authors/** — REST API for authors
- **http://127.0.0.1:8000/admin/** — Django admin interface
- **http://127.0.0.1:8000/register/** — create a user account
- **http://127.0.0.1:8000/login/** — log in

To run the tests:

```bash
python manage.py test
```

Press `Ctrl+C` to stop the server.

## Expected output

Running `python manage.py test` shows:

```text
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.XXXs

OK
Destroying test database for alias 'default'...
```

The application serves both an HTML interface (for browsers) and a JSON API (for programmatic access). Both share the same models and database.

## Alter it

1. Add an `edit_book` view and template. The URL should be `/books/<pk>/edit/`. Use `BookForm(request.POST, instance=book)` to pre-fill and update. Protect with `@login_required`. Add a test for it.
2. Add a `delete_book` view with a confirmation template. Add a test that verifies deletion works and that anonymous users cannot delete.
3. Add a `/api/books/<pk>/reviews/` nested endpoint using DRF. Create a `Review` model with `book` (ForeignKey), `rating` (1-5), and `text` fields. Write tests for the new API.

## Break it

1. In `tests.py`, change an `assertEqual` assertion to check for the wrong value. Run the tests. Read the failure output and understand what Django tells you.
2. Remove `select_related("author")` from the `BookViewSet` queryset. The app still works, but run the tests — do they still pass? (Yes, but performance degrades silently. This is why N+1 query detection tools exist.)
3. Comment out the CSRF middleware in `settings.py`. Submit a form. What changes?

## Fix it

1. Fix the assertion back to the correct value. Test failure output shows the expected vs actual values, which makes debugging straightforward.
2. Add `select_related("author")` back. The tests pass either way because correctness is not affected — only performance. In production, tools like `django-debug-toolbar` or `nplusone` detect these issues.
3. Uncomment the CSRF middleware. Without it, your site is vulnerable to Cross-Site Request Forgery attacks. The middleware and `{% csrf_token %}` work together to verify that POST requests originate from your site.

## Explain it

1. How does Django's test framework create an isolated database for each test run? What happens to data created during tests?
2. What is the purpose of `self.client` in Django tests? How does it differ from a real browser?
3. How do the HTML views and the DRF API views share the same models? What are the advantages of serving both interfaces?
4. Looking at the full application, what would you need to add to make it production-ready? (Think: security, deployment, performance.)

## Mastery check

You can move on when you can:

- build a Django app from scratch with models, views, templates, and DRF,
- write tests for models, views, and API endpoints,
- explain how Django's components fit together (MTV + DRF + auth),
- describe what makes this a "full-stack" application.

## Next

Congratulations on completing Module 10! You now have full-stack Django skills.

Return to the [Module Index](../README.md) to choose your next module.
