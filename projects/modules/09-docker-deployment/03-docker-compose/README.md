# Module 09 / Project 03 — Docker Compose

Home: [README](../../../../README.md)

## Focus

Using `docker-compose.yml` to run a multi-service stack: app + database, with networking, volumes, and environment variables.

## Why this project exists

Real applications rarely run alone. They need databases, caches, queues, and other services. Docker Compose lets you define all these services in a single file and start them together with one command. Docker Compose also creates a private network so your services can find each other by name. This project teaches you to orchestrate a FastAPI application with a PostgreSQL database.

## Run

```bash
cd projects/modules/09-docker-deployment/03-docker-compose

# Start both services (web app + database)
docker compose up --build
```

Docker Compose will:

1. Build the web service image from the Dockerfile.
2. Pull the `postgres:16` image from Docker Hub (first time only).
3. Create a private network for both services.
4. Start the database, then start the web app.

Once you see `Uvicorn running on http://0.0.0.0:8000`, visit:

- http://127.0.0.1:8000 — root endpoint
- http://127.0.0.1:8000/docs — interactive API docs (try creating items here)
- http://127.0.0.1:8000/items — list all items

### Create some data

Use the `/docs` page or curl:

```bash
# Create an item
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "description": "A useful widget"}'

# List all items
curl http://127.0.0.1:8000/items
```

### Stop the services

```bash
# Stop containers (data is preserved in the volume)
docker compose down

# Stop containers AND delete the database volume
docker compose down -v
```

## Expected output

Visiting http://127.0.0.1:8000 returns:

```json
{"message": "Hello from Docker Compose!", "database": "PostgreSQL"}
```

After creating an item, `GET /items` returns:

```json
[{"id": 1, "name": "Widget", "description": "A useful widget"}]
```

## Alter it

1. Add a `DELETE /items/{item_id}` endpoint that removes an item from the database. Rebuild with `docker compose up --build`.
2. Add a `redis:7` service to `docker-compose.yml`. You do not need to connect it to the app yet -- just get it running alongside the other services.
3. Change the database port mapping from `"5432:5432"` to `"5433:5432"` and connect to it from your host on port 5433.

## Break it

1. Change the `DATABASE_URL` in the web service's environment to use the wrong hostname (e.g., `wronghost` instead of `db`). What error do you get?
2. Remove the `volumes` section entirely. Run `docker compose up`, create some items, then `docker compose down` and `docker compose up` again. Are the items still there? Why not?
3. Remove `depends_on: - db` from the web service. Run `docker compose up`. Does the web service start before the database is ready?

## Fix it

1. Restore `db` as the hostname. Docker Compose registers each service name as a DNS hostname on the shared network.
2. Restore the `volumes` section. Without a named volume, PostgreSQL stores data inside the container's filesystem, which is destroyed when the container is removed.
3. Restore `depends_on`. While it does not guarantee the database is *ready*, it ensures the database container *starts* first.

## Explain it

1. How does the web service find the database using the hostname `db`? What creates this DNS entry?
2. What is a named volume? Where does Docker store the actual data on disk?
3. What happens to the data when you run `docker compose down` vs `docker compose down -v`?
4. Why do the `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` values need to match the `DATABASE_URL`?

## Mastery check

You can move on when you can:

- write a `docker-compose.yml` with two services from scratch,
- explain how Docker networking connects services by name,
- demonstrate that data persists across restarts with named volumes,
- describe what `depends_on` does and does not guarantee.

## Next

Continue to [04-ci-github-actions](../04-ci-github-actions/).
