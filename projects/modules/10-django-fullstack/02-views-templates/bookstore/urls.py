# ============================================================================
# Bookstore URL Patterns
# ============================================================================
# This file defines URL patterns for the bookstore app. Each pattern maps
# a URL to a view function.
#
# These patterns are included by the project's root urls.py with:
#   path("books/", include("bookstore.urls"))
#
# So the full URLs become:
#   /books/       -> book_list view
#   /books/1/     -> book_detail view (for book with pk=1)
#
# The `name` argument lets you reference URLs by name instead of hardcoding
# paths. In templates: {% url 'book_detail' book.pk %}
# In Python: reverse("book_detail", args=[book.pk])
# ============================================================================

from django.urls import path

from . import views

urlpatterns = [
    # /books/ -> list all books
    # name="book_list" lets you reference this URL by name in templates and code.
    path("", views.book_list, name="book_list"),

    # /books/<int:pk>/ -> detail for one book
    # <int:pk> is a path converter. "int" ensures the value is a number.
    # "pk" is the parameter name passed to the view function.
    path("<int:pk>/", views.book_detail, name="book_detail"),
]
