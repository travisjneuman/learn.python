# ============================================================================
# Bookstore Views (API) — REST Framework Project
# ============================================================================
# This file uses DRF ViewSets instead of regular Django views.
#
# A ViewSet combines the logic for multiple related views into a single class:
# - list()    -> GET /api/books/       (list all)
# - create()  -> POST /api/books/      (create new)
# - retrieve()-> GET /api/books/1/     (get one)
# - update()  -> PUT /api/books/1/     (full update)
# - partial_update() -> PATCH /api/books/1/ (partial update)
# - destroy() -> DELETE /api/books/1/  (delete)
#
# ModelViewSet provides all six actions automatically. You just specify:
# - queryset: which objects to operate on
# - serializer_class: how to serialize/deserialize the data
#
# Comparison to FastAPI:
#   FastAPI @app.get("/books/")    ->  ViewSet.list()
#   FastAPI @app.post("/books/")   ->  ViewSet.create()
#   FastAPI @app.get("/books/{id}")->  ViewSet.retrieve()
# ============================================================================

from rest_framework import viewsets

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """API endpoint for Author CRUD operations.

    ModelViewSet provides all CRUD operations automatically:
    - GET /api/authors/      -> list all authors
    - POST /api/authors/     -> create a new author
    - GET /api/authors/1/    -> get author with id=1
    - PUT /api/authors/1/    -> update author with id=1
    - PATCH /api/authors/1/  -> partial update
    - DELETE /api/authors/1/ -> delete author with id=1

    You get all this by specifying just queryset and serializer_class.
    """

    # queryset: The base set of objects this viewset operates on.
    # .all() returns all authors. You can filter here to restrict access.
    queryset = Author.objects.all()

    # serializer_class: Which serializer to use for input/output.
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """API endpoint for Book CRUD operations.

    Same as AuthorViewSet but for Books. The serializer handles the
    author relationship: it accepts an author ID on input and includes
    both the author ID and author name on output.

    The queryset uses select_related("author") to optimize database queries.
    Without it, accessing book.author.name would trigger a separate SQL query
    for each book (the "N+1 query problem"). select_related() performs a
    SQL JOIN so all data is fetched in a single query.
    """

    # select_related("author") performs a JOIN to fetch author data in one query.
    # This avoids the N+1 problem: without it, listing 100 books would make
    # 101 queries (1 for books + 100 for each book's author).
    queryset = Book.objects.select_related("author").all()

    serializer_class = BookSerializer
