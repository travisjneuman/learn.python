# Module 10 / Project 03 — Forms & Auth

Home: [README](../../../../README.md)

## Focus

Django's ModelForm system, form validation, user registration, login/logout, and the `@login_required` decorator.

## Why this project exists

Most web applications need two things: data entry forms and user accounts. Django provides both out of the box. ModelForm automatically generates HTML form fields from your model definitions, with built-in validation. The auth system gives you user registration, login, logout, password hashing, and access control without writing any of it yourself.

In FastAPI (Module 04), you built authentication from scratch with JWT tokens and password hashing. Django's approach is different: it provides a complete, battle-tested auth system that you configure rather than build.

## Run

```bash
cd projects/modules/10-django-fullstack/03-forms-auth
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open your browser to:

- **http://127.0.0.1:8000/books/** — list all books
- **http://127.0.0.1:8000/books/add/** — add a new book (requires login)
- **http://127.0.0.1:8000/register/** — create a new user account
- **http://127.0.0.1:8000/login/** — log in
- **http://127.0.0.1:8000/logout/** — log out

Press `Ctrl+C` to stop the server.

## Expected output

Visiting `/books/add/` while not logged in redirects you to `/login/`. After logging in, the form appears with fields for title, author, price, and published date. Submitting a valid form creates the book and redirects to the book list. Submitting invalid data (e.g., negative price) shows error messages inline.

## Alter it

1. Add an edit view: `GET /books/<pk>/edit/` shows the form pre-filled with existing data. `POST` updates the book. Use `BookForm(request.POST, instance=book)` to bind the form to an existing object.
2. Add a delete view: `GET /books/<pk>/delete/` shows a confirmation page. `POST` deletes the book. Protect it with `@login_required`.
3. Add a "remember me" checkbox to the login form that extends the session duration.

## Break it

1. Remove `{% csrf_token %}` from the book form template. Try submitting the form. What error do you get?
2. In `RegistrationForm`, remove the `email` field from `Meta.fields`. Try registering a user. What happens to the email field?
3. Remove `@login_required` from the `add_book` view. Can anonymous users now add books?

## Fix it

1. Add `{% csrf_token %}` back. Django requires CSRF tokens in all POST forms to prevent Cross-Site Request Forgery attacks. The token proves the form was served by your site, not by a malicious third party.
2. Add `email` back to `Meta.fields`. Django forms only display fields listed in `fields`. Removing a field from the list means it is not rendered and not validated.
3. Add `@login_required` back. Without it, any visitor can add books. The decorator checks `request.user.is_authenticated` and redirects to the login page if the user is not logged in.

## Explain it

1. What is the difference between a regular `Form` and a `ModelForm`? When would you use each?
2. What is CSRF? How does `{% csrf_token %}` protect against it?
3. How does `@login_required` work? Where does it redirect unauthenticated users?
4. What does `form.is_valid()` check? What happens to errors when validation fails?

## Mastery check

You can move on when you can:

- create a ModelForm from any model and render it in a template,
- explain what CSRF protection is and why forms need the token,
- implement login, logout, and registration using Django's auth system,
- use `@login_required` to protect views from anonymous users.

## Next

Continue to [04-rest-framework](../04-rest-framework/).
