# ============================================================================
# Bookstore Forms — Forms & Auth Project
# ============================================================================
# Django forms handle two things:
# 1. Rendering HTML form fields from Python definitions
# 2. Validating submitted data and reporting errors
#
# ModelForm is a special form that generates fields automatically from a model.
# Instead of defining each field by hand, you point it at a model and list
# which fields to include. Django creates the form fields, validates data
# types, and can save directly to the database with form.save().
# ============================================================================

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Book


class BookForm(forms.ModelForm):
    """A form for creating and editing Book objects.

    ModelForm automatically generates form fields based on the Book model:
    - title -> TextInput (from CharField)
    - author -> TextInput (from CharField)
    - price -> NumberInput (from DecimalField)
    - published_date -> DateInput (from DateField)

    Validation happens automatically based on model field constraints:
    - title and author: required, max 300/200 chars
    - price: must be a valid decimal, max 6 digits
    - published_date: must be a valid date (optional because blank=True)
    """

    class Meta:
        # model: Which model to generate the form from.
        model = Book

        # fields: Which model fields to include in the form.
        # You can also use "__all__" for all fields, but explicit is better.
        # Listing fields protects against accidentally exposing sensitive fields.
        fields = ["title", "author", "price", "published_date"]

        # widgets: Override the default HTML widget for specific fields.
        # DateInput with type="date" renders a browser-native date picker.
        widgets = {
            "published_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_price(self):
        """Custom validation for the price field.

        clean_<fieldname> methods run after Django's built-in validation.
        They receive the cleaned (type-converted) value and can add custom rules.

        This method ensures the price is not negative. If validation fails,
        raise forms.ValidationError with a user-friendly message. Django
        attaches this error to the price field in the template.
        """
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price


class RegistrationForm(UserCreationForm):
    """A user registration form that extends Django's built-in UserCreationForm.

    UserCreationForm provides:
    - username field
    - password1 field (the password)
    - password2 field (password confirmation)
    - Password validation (minimum length, not too common, not all numeric)

    We add an email field because UserCreationForm does not include one by default.
    """

    # Add an email field. required=True makes it mandatory.
    email = forms.EmailField(required=True)

    class Meta:
        # Use Django's built-in User model.
        model = User

        # Include username, email, and both password fields.
        fields = ["username", "email", "password1", "password2"]
