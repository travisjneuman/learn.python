# Module 10 / Project 01 — Django Setup

Home: [README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

Creating a Django project from scratch: `startproject`, `startapp`, models, admin, migrations, and `runserver`.

## Why this project exists

Every Django application starts the same way: you run `startproject`, then `startapp`, define models, create migrations, and start the development server. This project walks you through that process step by step. Instead of running Django commands blindly, you will use a guided setup script that creates the project structure and explains every generated file along the way.

Understanding the file structure Django creates is essential. Each file has a specific purpose, and knowing what goes where will save you hours of confusion later.

## Run

```bash
cd projects/modules/10-django-fullstack/01-django-setup
python setup_guide.py
```

The script creates a Django project and app, then prints an explanation of every file it generated. After running it, explore the created directory structure.

To verify the generated project works:

```bash
cd demo_project
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open your browser to:

- **http://127.0.0.1:8000** — Django welcome page
- **http://127.0.0.1:8000/admin** — Django admin interface (log in with the superuser you created)

Press `Ctrl+C` to stop the server.

## Expected output

Running `setup_guide.py` prints explanations like:

```text
=== Django Project Setup Guide ===

[1/6] Creating project directory: demo_project/
  Created: demo_project/manage.py
    -> The command-line entry point for your Django project.
       Run migrations, start the server, create apps — all through manage.py.

  Created: demo_project/demo_project/settings.py
    -> The central configuration file. Database settings, installed apps,
       middleware, templates, and more are all configured here.
...
```

Running `python manage.py migrate` applies Django's built-in database tables:

```text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

## Alter it

1. Open `setup_guide.py` and add a new model field to the `Item` model (e.g., `description = models.TextField(blank=True)`). Re-run the script and verify the field appears.
2. Add a second model called `Category` with a `name` field. Add a `ForeignKey` from `Item` to `Category`.
3. Modify the script to also generate an `admin.py` that registers both models.

## Break it

1. In the generated `settings.py`, remove `'django.contrib.admin'` from `INSTALLED_APPS`. Try visiting `/admin`. What happens?
2. In the generated model, change `models.CharField(max_length=200)` to `models.CharField()` (remove max_length). Try running `makemigrations`. What error do you get?
3. Delete the generated `migrations/` directory and try running `migrate`. What happens?

## Fix it

1. Add `'django.contrib.admin'` back to `INSTALLED_APPS`. The admin interface requires this app.
2. Add `max_length=200` back. `CharField` requires a `max_length` argument. If you want unlimited text, use `TextField` instead.
3. Run `makemigrations` first to regenerate the migration files, then `migrate`. Django needs migration files to know what database changes to make.

## Explain it

1. What is the difference between a Django "project" and a Django "app"? Why does Django separate them?
2. What does `manage.py` do? How is it different from `django-admin`?
3. What are migrations? Why doesn't Django just read your models and create tables directly?
4. What does `INSTALLED_APPS` control? What happens if you define a model in an app that is not listed there?

## Mastery check

You can move on when you can:

- explain every file in a new Django project without looking at the guide,
- create a model, make migrations, and apply them from memory,
- access the admin interface and add/edit objects,
- describe what `settings.py` controls and find any setting by name.

---

## Related Concepts

- [Async Explained](../../../../concepts/async-explained.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [How Imports Work](../../../../concepts/how-imports-work.md)
- [Quiz: Async Explained](../../../../concepts/quizzes/async-explained-quiz.py)

## Next

Continue to [02-views-templates](../02-views-templates/).
