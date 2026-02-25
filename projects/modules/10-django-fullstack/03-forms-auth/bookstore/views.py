# ============================================================================
# Bookstore Views — Forms & Auth Project
# ============================================================================
# This file adds form handling and authentication views to the bookstore.
#
# New concepts:
# - @login_required: decorator that redirects anonymous users to the login page
# - form.is_valid(): validates submitted data and populates form.errors
# - form.save(): creates or updates a database object from form data
# - login() / logout(): Django functions that manage user sessions
# - redirect(): returns an HTTP redirect response to another URL
# ============================================================================

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, RegistrationForm
from .models import Book


# ----------------------------------------------------------------------------
# Book List View (same as Project 02)
# ----------------------------------------------------------------------------
def book_list(request):
    """List all books."""
    books = Book.objects.all()
    return render(request, "bookstore/book_list.html", {"books": books})


# ----------------------------------------------------------------------------
# Book Detail View (same as Project 02)
# ----------------------------------------------------------------------------
def book_detail(request, pk):
    """Display details for a single book."""
    book = get_object_or_404(Book, pk=pk)
    return render(request, "bookstore/book_detail.html", {"book": book})


# ----------------------------------------------------------------------------
# Add Book View — Demonstrates ModelForm and @login_required
#
# @login_required does two things:
# 1. If the user is logged in, the view runs normally.
# 2. If the user is NOT logged in, Django redirects to LOGIN_URL (from settings)
#    with a ?next= parameter so the user returns here after logging in.
#
# This view handles both GET (show the form) and POST (process the form):
# - GET: Create an empty BookForm and render it in the template.
# - POST: Create a BookForm with submitted data, validate it, and save.
#
# The pattern of checking request.method is standard in Django function-based
# views. Class-based views handle this automatically, but function-based views
# make the logic explicit and easier to learn.
# ----------------------------------------------------------------------------
@login_required
def add_book(request):
    """Show a form to add a new book, or process the submitted form.

    GET: Display an empty form.
    POST: Validate the form. If valid, save the book and redirect to the list.
          If invalid, re-display the form with error messages.
    """
    if request.method == "POST":
        # Bind the form to the submitted data (request.POST).
        # A "bound" form knows what data was submitted and can validate it.
        form = BookForm(request.POST)

        # is_valid() runs all validation:
        # 1. Field-level validation (type checking, max_length, required)
        # 2. Custom clean_<field>() methods (like our clean_price)
        # 3. The form's clean() method (for cross-field validation)
        #
        # If validation passes, cleaned data is available in form.cleaned_data.
        # If validation fails, errors are available in form.errors.
        if form.is_valid():
            # save() creates a new Book object in the database.
            # It uses form.cleaned_data to set the field values.
            form.save()

            # redirect() returns an HTTP 302 response that sends the browser
            # to the book list page. This follows the POST/Redirect/GET pattern,
            # which prevents duplicate submissions when the user refreshes.
            return redirect("book_list")
    else:
        # GET request: create an empty (unbound) form.
        form = BookForm()

    # Render the template with the form. If the form has errors (from a failed
    # POST), Django includes them in the template context automatically.
    return render(request, "bookstore/add_book.html", {"form": form})


# ----------------------------------------------------------------------------
# Registration View — Creating new user accounts
#
# This view uses Django's UserCreationForm (extended by our RegistrationForm)
# to create new user accounts. The form handles:
# - Username uniqueness checking
# - Password strength validation
# - Password confirmation matching
# - Secure password hashing (you never see or store the raw password)
# ----------------------------------------------------------------------------
def register_view(request):
    """Show a registration form, or create a new user account.

    After successful registration, the user is automatically logged in
    and redirected to the book list.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save() creates the User object with a hashed password.
            # Django never stores plaintext passwords.
            user = form.save()

            # login() creates a session for the new user so they are
            # immediately logged in after registration.
            login(request, user)
            return redirect("book_list")
    else:
        form = RegistrationForm()

    return render(request, "bookstore/register.html", {"form": form})


# ----------------------------------------------------------------------------
# Login View — Authenticating existing users
#
# Django provides a built-in LoginView class-based view, but we implement
# it as a function-based view here to make the logic explicit and learnable.
# In production, you might prefer Django's built-in views.
# ----------------------------------------------------------------------------
def login_view(request):
    """Show a login form, or authenticate the user.

    Uses Django's authenticate() function to verify credentials.
    On success, creates a session and redirects to LOGIN_REDIRECT_URL.
    On failure, re-displays the form with an error message.
    """
    from django.contrib.auth import authenticate

    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate() checks the username and password against the database.
        # It returns the User object if credentials are valid, or None if not.
        # The password is hashed and compared to the stored hash — Django
        # never compares plaintext passwords.
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login() creates a session. Django stores the session ID in a
            # cookie, and the session data (including the user ID) in the
            # database. On subsequent requests, Django reads the cookie and
            # loads the user automatically.
            login(request, user)

            # Check for a ?next= parameter. @login_required adds this so
            # users return to the page they originally tried to visit.
            next_url = request.GET.get("next", "/books/")
            return redirect(next_url)
        else:
            error_message = "Invalid username or password."

    return render(request, "bookstore/login.html", {"error": error_message})


# ----------------------------------------------------------------------------
# Logout View
#
# logout() clears the session. The user is no longer authenticated.
# We redirect to LOGOUT_REDIRECT_URL (defined in settings.py).
# ----------------------------------------------------------------------------
def logout_view(request):
    """Log the user out and redirect to the book list."""
    logout(request)
    return redirect("book_list")
