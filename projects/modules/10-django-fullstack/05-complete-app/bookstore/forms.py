# ============================================================================
# Bookstore Forms — Complete App
# ============================================================================
# Forms for creating books and registering users.
# Same as Project 03, adapted for the Author relationship.
# ============================================================================

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book


class BookForm(forms.ModelForm):
    """Form for creating and editing books.

    The author field renders as a dropdown (<select>) because it is a
    ForeignKey. Django automatically populates the dropdown with all Author
    objects from the database.
    """

    class Meta:
        model = Book
        fields = ["title", "author", "price", "published_date"]
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_price(self):
        """Ensure price is not negative."""
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price


class RegistrationForm(UserCreationForm):
    """User registration form with email field."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
