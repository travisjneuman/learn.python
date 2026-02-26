# Module 12 / Project 02 — Deploy with Database

Home: [README](../../../../README.md) · Module: [Cloud Deployment](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Adding PostgreSQL to a cloud deployment
- Database connection strings (DATABASE_URL)
- Running migrations in production
- Data persistence across deploys

## Why this project exists

Most real apps need a database. Cloud platforms offer managed databases that handle backups, scaling, and maintenance. This project deploys a FastAPI app with a PostgreSQL database on Railway.

## Project files

```
02-deploy-with-database/
├── app.py              # FastAPI app with database CRUD
├── database.py         # SQLAlchemy setup reading DATABASE_URL
├── models.py           # ORM models
├── requirements.txt    # Includes psycopg2-binary
├── Procfile            # Start command
├── .env.example        # Template for local dev
└── notes.md
```

## Local development

```bash
cd projects/modules/12-cloud-deploy/02-deploy-with-database
pip install -r requirements.txt

# For local dev, SQLite is used when DATABASE_URL is not set.
python app.py
# Visit http://127.0.0.1:8000/docs
```

## Deploy with PostgreSQL

### 1. Add PostgreSQL on Railway

In your Railway project:
1. Click "New" → "Database" → "Add PostgreSQL."
2. Railway creates a managed Postgres instance.
3. Click the database service → "Variables" tab.
4. Copy the `DATABASE_URL` connection string.

### 2. Connect your app to the database

In your web service's Variables tab:
- Add `DATABASE_URL` with the value from the Postgres service.
- Railway can also auto-inject this if you link the services.

### 3. Deploy

Push your code. Railway rebuilds and connects to Postgres automatically.

### 4. Verify

```bash
# Create a todo via the API
curl -X POST https://your-app.up.railway.app/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Test from production"}'

# List todos
curl https://your-app.up.railway.app/todos
```

## Expected output

```json
{
  "id": 1,
  "title": "Test from production",
  "completed": false,
  "created_at": "2024-01-15T10:30:00"
}
```

## Alter it

1. Add a `/stats` endpoint that returns the total number of todos and how many are completed.
2. Switch from Railway Postgres to Render Postgres. What changes?
3. Add a seed command that pre-populates the database with sample data.

## Break it

1. Set DATABASE_URL to an invalid connection string. What error do you get?
2. Delete the Postgres service on Railway. Does the app still start?
3. Deploy without running migrations. What happens to new columns?

## Fix it

1. Fix the DATABASE_URL and redeploy.
2. Recreate the Postgres service and reconnect.
3. Add a startup event in FastAPI that runs `Base.metadata.create_all()`.

## Explain it

1. Why use PostgreSQL in production instead of SQLite?
2. What is a connection string and what are its parts?
3. Why should DATABASE_URL be an environment variable, not hardcoded?
4. What happens to your data when you redeploy the app?

## Mastery check

You can move on when you can:
- deploy an app with a managed database,
- configure DATABASE_URL via environment variables,
- verify data persists across deploys,
- explain why Postgres over SQLite in production.

---

## Related Concepts

- [Http Explained](../../../../concepts/http-explained.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Quiz: Http Explained](../../../../concepts/quizzes/http-explained-quiz.py)

## Next

[Project 03 — Production Checklist](../03-production-checklist/)
