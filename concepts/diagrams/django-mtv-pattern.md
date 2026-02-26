# Django MTV Pattern — Diagrams

[<- Back to Diagram Index](../../guides/DIAGRAM_INDEX.md)

## Overview

These diagrams show how Django processes requests through its Model-Template-View architecture, how the ORM maps Python classes to database tables, and how the admin interface fits into the stack.

## Request Through the MTV Stack

Django's MTV (Model-Template-View) pattern is similar to MVC, but Django calls the controller a "View" and the presentation layer a "Template." Every request flows through URL routing to a view, which coordinates models and templates.

```mermaid
flowchart TD
    CLIENT["Browser Request<br/>GET /blog/42/"] --> WSGI["WSGI Server (Gunicorn)<br/>Passes request to Django"]
    WSGI --> MW_IN["Middleware (request phase)<br/>SecurityMiddleware, SessionMiddleware,<br/>AuthenticationMiddleware"]
    MW_IN --> URLS["URL Resolver<br/>urls.py: path('blog/&lt;int:pk&gt;/', views.post_detail)"]
    URLS --> VIEW["View Function / Class<br/>def post_detail(request, pk):"]

    VIEW --> MODEL["Model Layer<br/>Post.objects.get(pk=42)"]
    MODEL --> DB["Database<br/>SELECT * FROM blog_post WHERE id=42"]
    DB --> MODEL
    MODEL --> VIEW

    VIEW --> TEMPLATE["Template Layer<br/>post_detail.html"]
    TEMPLATE --> RENDER["Template Engine<br/>Render HTML with context"]
    RENDER --> VIEW

    VIEW --> MW_OUT["Middleware (response phase)<br/>Add headers, CSRF token"]
    MW_OUT --> CLIENT2["Browser receives HTML"]

    style WSGI fill:#4a9eff,stroke:#2670c2,color:#fff
    style URLS fill:#cc5de8,stroke:#9c36b5,color:#fff
    style VIEW fill:#ff922b,stroke:#e8590c,color:#fff
    style MODEL fill:#51cf66,stroke:#27ae60,color:#fff
    style TEMPLATE fill:#ffd43b,stroke:#f59f00,color:#000
```

**Key points:**
- The View is the coordinator: it fetches data from Models and passes it to Templates
- URL routing maps URL patterns to view functions using `urls.py`
- Middleware processes every request/response (authentication, security, sessions)
- Templates receive a context dictionary and render HTML

## Django ORM: Model to Database

The ORM translates Python class definitions into database tables. Each model field becomes a column, and relationships become foreign keys or junction tables.

```mermaid
flowchart LR
    subgraph PYTHON ["Python Model Classes"]
        AUTHOR["class Author(Model):<br/>    name = CharField()<br/>    email = EmailField()"]
        POST["class Post(Model):<br/>    title = CharField()<br/>    body = TextField()<br/>    author = ForeignKey(Author)<br/>    tags = ManyToManyField(Tag)"]
        TAG["class Tag(Model):<br/>    name = CharField()"]
    end

    subgraph DATABASE ["Database Tables"]
        T_AUTHOR["blog_author<br/>id | name | email"]
        T_POST["blog_post<br/>id | title | body | author_id"]
        T_TAG["blog_tag<br/>id | name"]
        T_M2M["blog_post_tags<br/>post_id | tag_id"]
    end

    AUTHOR -->|"makemigrations<br/>migrate"| T_AUTHOR
    POST -->|"ForeignKey"| T_POST
    TAG --> T_TAG
    POST -->|"ManyToMany<br/>auto junction table"| T_M2M
    T_POST ---|"author_id FK"| T_AUTHOR
    T_M2M ---|"post_id FK"| T_POST
    T_M2M ---|"tag_id FK"| T_TAG

    style PYTHON fill:#51cf66,stroke:#27ae60,color:#fff
    style DATABASE fill:#4a9eff,stroke:#2670c2,color:#fff
```

**Key points:**
- Each Model class maps to one database table, named `appname_modelname`
- `ForeignKey` creates a column with a foreign key constraint
- `ManyToManyField` automatically creates a junction table
- `makemigrations` generates SQL; `migrate` applies it to the database

## Django Admin and Management Flow

The admin interface auto-generates CRUD pages for your models. Management commands let you run tasks from the terminal.

```mermaid
flowchart TD
    subgraph ADMIN ["Django Admin (auto-generated)"]
        REGISTER["admin.py<br/>admin.site.register(Post, PostAdmin)"]
        LIST["List View<br/>Search, filter, pagination"]
        DETAIL["Detail View<br/>Edit form with validation"]
        ACTIONS["Bulk Actions<br/>Delete selected, custom actions"]
    end

    subgraph MANAGE ["manage.py Commands"]
        MIGRATE["python manage.py migrate<br/>Apply database schema"]
        CREATE["python manage.py createsuperuser<br/>Create admin account"]
        SHELL["python manage.py shell<br/>Interactive ORM access"]
        CUSTOM["python manage.py seed_data<br/>Custom management commands"]
    end

    subgraph LAYERS ["How Admin Uses MTV"]
        ADMIN_VIEW["Admin Views<br/>(built-in class-based views)"]
        ADMIN_MODEL["Your Models<br/>(reads fields, relationships)"]
        ADMIN_TEMPLATE["Admin Templates<br/>(overridable)"]
    end

    REGISTER --> LIST
    LIST --> DETAIL
    LIST --> ACTIONS
    ADMIN_VIEW --> ADMIN_MODEL
    ADMIN_VIEW --> ADMIN_TEMPLATE

    style ADMIN fill:#cc5de8,stroke:#9c36b5,color:#fff
    style MANAGE fill:#ff922b,stroke:#e8590c,color:#fff
    style LAYERS fill:#51cf66,stroke:#27ae60,color:#fff
```

**Key points:**
- Registering a model in `admin.py` gives you a full CRUD interface for free
- The admin reads your model fields to auto-generate forms and list displays
- `ModelAdmin` classes let you customize search, filters, display columns, and inline editing
- Management commands extend `manage.py` for custom CLI tasks (seeding data, cleanup jobs)

---

| [Back to Diagram Index](../../guides/DIAGRAM_INDEX.md) |
|:---:|
