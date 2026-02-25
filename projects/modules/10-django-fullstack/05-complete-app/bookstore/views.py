# ============================================================================
# Bookstore Views — Complete App
# ============================================================================
# This file contains both HTML views (for browser access) and auth views.
# The DRF API views are in views_api.py for clean separation.
#
# HTML views render templates for human users.
# API views (in views_api.py) return JSON for programmatic access.
# Both share the same models and database.
# ============================================================================

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, RegistrationForm
from .models import Book


# ---- HTML Views (browser-facing) ----

def book_list(request):
    """List all books (HTML page)."""
    books = Book.objects.select_related("author").all()
    return render(request, "bookstore/book_list.html", {"books": books})


def book_detail(request, pk):
    """Display a single book's details (HTML page)."""
    book = get_object_or_404(Book.objects.select_related("author"), pk=pk)
    return render(request, "bookstore/book_detail.html", {"book": book})


@login_required
def add_book(request):
    """Show form to add a book (GET) or process submitted form (POST)."""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookstore/add_book.html", {"form": form})


# ---- Authentication Views ----

def register_view(request):
    """Register a new user account."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("book_list")
    else:
        form = RegistrationForm()
    return render(request, "bookstore/register.html", {"form": form})


def login_view(request):
    """Log in an existing user."""
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "/books/")
            return redirect(next_url)
        else:
            error_message = "Invalid username or password."
    return render(request, "bookstore/login.html", {"error": error_message})


def logout_view(request):
    """Log out the current user."""
    logout(request)
    return redirect("book_list")
