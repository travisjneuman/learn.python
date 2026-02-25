# ============================================================================
# Bookstore HTML URL Patterns — Complete App
# ============================================================================
# URL patterns for browser-facing HTML views.
# ============================================================================

from django.urls import path

from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("<int:pk>/", views.book_detail, name="book_detail"),
    path("add/", views.add_book, name="add_book"),
]
