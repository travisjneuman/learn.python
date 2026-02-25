# Module 09 / Project 05 — Production Config

Home: [README](../../../../README.md)

## Focus

Environment variables, secrets management, health checks, structured logging, CORS, graceful shutdown, and non-root container users.

## Why this project exists

Building a Docker image is not the same as being production-ready. Production applications need proper configuration management (so secrets stay out of source code), structured logging (so you can debug issues in running containers), health checks (so orchestrators can restart failed containers), and security hardening (so a compromised container has minimal privileges). This project puts all those pieces together.

## Run

### Local development

```bash
cd projects/modules/09-docker-deployment/05-production-config

# Run with default settings (SQLite, debug logging)
DEBUG=true LOG_LEVEL=DEBUG python app.py
```

### With Docker Compose (recommended)

```bash
# Start the app and database
docker compose up --build

# In another terminal, check health status
docker compose ps
```

### Verify the endpoints

```bash
# Root endpoint — app metadata
curl http://127.0.0.1:8000/

# Health check — includes database status
curl http://127.0.0.1:8000/health

# Configuration — non-sensitive settings
curl http://127.0.0.1:8000/config
```

### Watch the logs

```bash
# Follow the web service logs
docker compose logs -f web
```

You will see structured log output like:

```
2024-01-15 14:30:00 | production-app | INFO | Starting production-app v1.0.0
2024-01-15 14:30:00 | production-app | INFO | Debug mode: False
2024-01-15 14:30:00 | production-app | INFO | Database tables verified
```

## Expected output

`GET /` returns:

```json
{"app": "production-app", "version": "1.0.0", "status": "running"}
```

`GET /health` returns:

```json
{"status": "healthy", "database": "connected", "version": "1.0.0"}
```

`GET /config` returns:

```json
{"app_name": "production-app", "version": "1.0.0", "debug": false, "log_level": "INFO", "workers": 2}
```

## Production deployment checklist

Before deploying to production, verify each item:

- [ ] All secrets come from environment variables, not source code.
- [ ] `.env` is in `.gitignore` (never committed).
- [ ] `DEBUG=false` in production.
- [ ] `LOG_LEVEL=INFO` or `WARNING` in production.
- [ ] `ALLOWED_ORIGINS` is restricted to your frontend domain(s).
- [ ] The container runs as a non-root user.
- [ ] Health checks are configured in the Dockerfile and docker-compose.yml.
- [ ] Restart policy is set (`unless-stopped` or `on-failure`).
- [ ] Resource limits are set (CPU and memory).
- [ ] Database credentials are unique per environment.

## Alter it

1. Add a `GET /ready` endpoint (separate from `/health`) that returns 503 if the database is not connected. This is a "readiness probe" used by Kubernetes.
2. Add a `REQUEST_TIMEOUT` setting to `config.py` and log it at startup.
3. Change `LOG_LEVEL` to `DEBUG` in docker-compose.yml and observe the additional log output.

## Break it

1. Remove the `DATABASE_URL` environment variable from docker-compose.yml. What happens when the app tries to connect to the database?
2. Change `USER appuser` to `USER root` in the Dockerfile. The app still works, but explain why this is a security risk.
3. Remove the `healthcheck` from the db service and the `condition: service_healthy` from the web service. Start the stack. Does the web service crash because the database is not ready?

## Fix it

1. Restore the `DATABASE_URL` environment variable. Without it, the app falls back to SQLite (the default in config.py), which is not what you want in production.
2. Restore `USER appuser`. Running as root inside a container gives an attacker full control if they exploit a vulnerability. Non-root users limit the damage.
3. Restore the health check and condition. Without them, the web service may start before PostgreSQL is ready, causing connection errors on the first few requests.

## Explain it

1. Why should configuration come from environment variables instead of hardcoded values?
2. What is the difference between a health check and a readiness check?
3. Why does the Dockerfile create a non-root user? What is the security risk of running as root?
4. What does `restart: unless-stopped` do? How is it different from `restart: always`?
5. Why does the `.env.example` file exist alongside `.env`? Why is `.env` not committed?

## Mastery check

You can move on when you can:

- configure a FastAPI application entirely through environment variables,
- explain why secrets must never appear in source code,
- set up Docker health checks and explain their purpose,
- describe why containers should run as non-root users,
- read structured logs and use them to diagnose issues.

---

## Related Concepts

- [Files and Paths](../../../../concepts/files-and-paths.md)
- [The Terminal Deeper](../../../../concepts/the-terminal-deeper.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Virtual Environments](../../../../concepts/virtual-environments.md)
- [Quiz: Files and Paths](../../../../concepts/quizzes/files-and-paths-quiz.py)

## Next

You have completed Module 09 — Docker & Deployment. You now have the skills to containerize any Python application and deploy it with confidence. Consider continuing to [Module 10 — Django Full-Stack](../../10-django-fullstack/) or [Module 12 — Cloud Deployment](../../12-cloud-deploy/).
