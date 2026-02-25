# Module 10 / Project 02 — Views & Templates

Home: [README](../../../../README.md)

## Focus

Function-based views, URL routing, Django templates, template tags, and static files.

## Why this project exists

Django follows the MTV pattern: Model-Template-View. You already know Models from Project 01. This project teaches you Views (the logic that handles requests) and Templates (the HTML that users see). Together, they turn your database models into a working web application.

Django's template language keeps logic out of your HTML. Instead of writing Python in your templates, you use simple tags like `{% for book in books %}` and `{{ book.title }}`. This separation makes templates readable and maintainable.

## Run

```bash
cd projects/modules/10-django-fullstack/02-views-templates
python manage.py migrate
python manage.py runserver
```

Then open your browser to:

- **http://127.0.0.1:8000/books/** — list of all books
- **http://127.0.0.1:8000/books/1/** — detail view for book with ID 1
- **http://127.0.0.1:8000/admin/** — admin interface to add books

Create a superuser first to add books through the admin:

```bash
python manage.py createsuperuser
```

Press `Ctrl+C` to stop the server.

## Expected output

Visiting `/books/` shows a page listing all books with their titles and authors. Visiting `/books/1/` shows a single book's full details including price and publication date. If no books exist yet, the list page shows "No books found."

## Alter it

1. Add a `GET /books/search/?q=python` view that filters books by title containing the search query. Use `Book.objects.filter(title__icontains=q)`.
2. Add an author field display to the book list page. Show both title and author on each row.
3. Create a base template (`base.html`) and make both pages extend it using `{% extends "bookstore/base.html" %}`.

## Break it

1. In `urls.py`, change `path("books/<int:pk>/", ...)` to `path("books/<pk>/", ...)` (remove `int:`). Visit `/books/abc/`. What happens?
2. In `book_list.html`, change `{% for book in books %}` to `{% for book in book %}` (wrong variable name). What does the page show?
3. Remove the `bookstore/` subdirectory from the templates path (move templates up one level). What error do you get?

## Fix it

1. Add `int:` back. The `<int:pk>` converter ensures Django only matches numeric URLs and returns 404 for non-numeric ones. Without it, your view receives a string and the database lookup may fail.
2. Fix the variable name back to `books`. Django templates fail silently on undefined variables, so you see an empty page instead of an error. This is intentional to prevent template errors from crashing your site.
3. Move templates back to `bookstore/templates/bookstore/`. Django uses this nested structure to avoid name collisions between apps. Two apps could both have a `book_list.html` — the app subdirectory prevents conflicts.

## Explain it

1. What is the difference between a "view" in Django and a "controller" in MVC frameworks? Why does Django call it MTV instead of MVC?
2. Why does Django require the `bookstore/templates/bookstore/` nested directory structure for templates?
3. What does `{% url 'book_detail' book.pk %}` do in a template? Why is it better than hardcoding `/books/1/`?
4. What is a "context" in Django views? How does data get from your view function to the template?

## Mastery check

You can move on when you can:

- create a view function, wire it to a URL, and render a template from memory,
- use `{% for %}`, `{% if %}`, `{{ variable }}`, and `{% url %}` in templates,
- explain why Django namespaces templates inside app subdirectories,
- pass data from a view to a template using the context dictionary.

## Next

Continue to [03-forms-auth](../03-forms-auth/).
