# Module 10 / Project 04 — REST Framework

Home: [README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

Django REST Framework (DRF) — serializers, viewsets, routers, and the browsable API.

## Why this project exists

Django's template system renders HTML for browsers, but modern applications often need a JSON API for mobile apps, single-page applications, or third-party integrations. Django REST Framework adds this capability to Django. If you used FastAPI in Module 04, DRF is Django's equivalent: it provides serializers (like Pydantic models), viewsets (like route handlers), and routers (like FastAPI's path decorators).

DRF also includes a browsable API — a web interface where you can interact with your API directly in the browser, similar to FastAPI's `/docs` page.

## Run

```bash
cd projects/modules/10-django-fullstack/04-rest-framework
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open your browser to:

- **http://127.0.0.1:8000/api/** — API root (browsable API)
- **http://127.0.0.1:8000/api/books/** — list all books (JSON)
- **http://127.0.0.1:8000/api/authors/** — list all authors (JSON)
- **http://127.0.0.1:8000/admin/** — add books and authors via admin

Press `Ctrl+C` to stop the server.

## Expected output

Visiting `/api/books/` in a browser shows DRF's browsable API with a list of books in JSON format. You can create new books using the form at the bottom of the page. Visiting `/api/books/1/` shows details for a single book.

Visiting `/api/books/?format=json` returns raw JSON:

```json
[
    {
        "id": 1,
        "title": "Django for Beginners",
        "author": 1,
        "author_name": "William Vincent",
        "price": "39.99",
        "published_date": "2024-01-15"
    }
]
```

## Alter it

1. Add a search filter: install `django-filter` and add `filterset_fields = ["author"]` to `BookViewSet`. Users can then filter books by author: `/api/books/?author=1`.
2. Add pagination: in `settings.py`, add `REST_FRAMEWORK = {"DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination", "PAGE_SIZE": 10}`.
3. Add a custom action to `BookViewSet` that returns only books under $20: use `@action(detail=False)` decorator.

## Break it

1. In `BookSerializer`, remove `author_name` from `fields`. Visit `/api/books/`. How does the response change?
2. In `urls.py`, comment out `router.register("books", ...)`. Visit `/api/books/`. What error do you get?
3. Remove `"rest_framework"` from `INSTALLED_APPS`. Try running the server. What happens?

## Fix it

1. Add `author_name` back. `SerializerMethodField` adds computed (read-only) fields to the API response. Removing it from `fields` removes it from the output.
2. Uncomment the router registration. DRF routers generate URL patterns automatically from viewsets. Without registration, the URL pattern does not exist.
3. Add `"rest_framework"` back. DRF must be in `INSTALLED_APPS` because it includes templates (for the browsable API), static files, and app configuration.

## Explain it

1. What is a serializer? How does it compare to Pydantic models in FastAPI?
2. What is the difference between a ViewSet and a regular Django view?
3. What does a DRF router do? How does it generate URL patterns from viewsets?
4. What is the browsable API? Why is it useful during development?

## Mastery check

You can move on when you can:

- create a serializer for any model with both model fields and computed fields,
- create a ViewSet with full CRUD operations,
- wire viewsets to URLs using a router,
- use the browsable API to test all CRUD operations.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Continue to [05-complete-app](../05-complete-app/).
