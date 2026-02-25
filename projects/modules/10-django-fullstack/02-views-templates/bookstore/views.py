# ============================================================================
# Bookstore Views — Views & Templates Project
# ============================================================================
# Views are Python functions that receive an HTTP request and return an HTTP
# response. In Django's MTV pattern:
#   - Model: defines data (models.py)
#   - Template: defines presentation (HTML files)
#   - View: defines logic (this file)
#
# Each view function:
# 1. Receives a request object (contains HTTP method, headers, user, etc.)
# 2. Queries the database using model methods
# 3. Passes data to a template via a "context" dictionary
# 4. Returns an HttpResponse (usually rendered HTML)
#
# The render() shortcut combines steps 3 and 4: it loads a template, fills
# in the context variables, and returns the result as an HttpResponse.
# ============================================================================

from django.shortcuts import get_object_or_404, render

from .models import Book


# ----------------------------------------------------------------------------
# View 1: Book List
#
# URL: /books/
# Purpose: Display all books in the database.
#
# Book.objects.all() returns a QuerySet — a lazy database query. Django does
# not actually hit the database until the template iterates over the queryset.
# This is efficient: if you never use the data, the query never runs.
#
# The context dictionary {"books": books} makes the queryset available in the
# template as the variable name "books".
# ----------------------------------------------------------------------------
def book_list(request):
    """List all books in the bookstore.

    The template receives a 'books' variable containing all Book objects,
    ordered by published_date (newest first, as defined in the model's Meta).
    """
    books = Book.objects.all()

    # render() takes three arguments:
    # 1. The request object (required by Django's template engine)
    # 2. The template path (relative to any templates/ directory)
    # 3. The context dictionary (variables available in the template)
    return render(request, "bookstore/book_list.html", {"books": books})


# ----------------------------------------------------------------------------
# View 2: Book Detail
#
# URL: /books/<pk>/
# Purpose: Display a single book's full details.
#
# get_object_or_404() is a shortcut that does two things:
# 1. Tries to find a Book with the given primary key (pk)
# 2. If not found, raises an Http404 exception (shows a 404 page)
#
# Without this shortcut, you would need a try/except block:
#   try:
#       book = Book.objects.get(pk=pk)
#   except Book.DoesNotExist:
#       raise Http404("Book not found")
#
# The pk parameter comes from the URL pattern: books/<int:pk>/
# Django extracts the number from the URL and passes it as a keyword argument.
# ----------------------------------------------------------------------------
def book_detail(request, pk):
    """Display details for a single book.

    Args:
        request: The HTTP request object.
        pk: The primary key of the book (from the URL).

    Returns:
        Rendered HTML with the book's full details, or a 404 page if the
        book does not exist.
    """
    book = get_object_or_404(Book, pk=pk)
    return render(request, "bookstore/book_detail.html", {"book": book})
