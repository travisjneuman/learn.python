# ============================================================================
# Bookstore API Views — Complete App
# ============================================================================
# DRF ViewSets for the REST API. Same as Project 04.
# Separated from HTML views for clean organization.
# ============================================================================

from rest_framework import viewsets

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """API endpoint for Author CRUD operations."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """API endpoint for Book CRUD operations."""
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
