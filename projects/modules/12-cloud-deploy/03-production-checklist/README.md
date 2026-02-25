# Module 12 / Project 03 — Production Checklist

Home: [README](../../../../README.md) · Module: [Cloud Deployment](../README.md)

## Focus

- HTTPS and security headers
- Monitoring and alerting
- Structured logging
- Backup strategy
- Post-deploy verification

## Why this project exists

Deploying code is only half the battle. A production app needs monitoring, logging, backups, and security hardening. This project is a comprehensive checklist and reference for everything you need before going live.

## The production checklist

### Security

- [ ] HTTPS enforced (Railway/Render handle this automatically)
- [ ] CORS configured to allow only your frontend domain
- [ ] No secrets in source code (use environment variables)
- [ ] API rate limiting in place
- [ ] Input validation on all endpoints (Pydantic handles this)
- [ ] SQL injection prevented (parameterized queries / ORM)
- [ ] Authentication on sensitive endpoints

### Monitoring

- [ ] Health check endpoint (`/health`) returns database status
- [ ] Uptime monitoring set up (UptimeRobot, Better Uptime — free tiers)
- [ ] Error tracking configured (Sentry — free tier for small projects)
- [ ] Response time monitoring

### Logging

- [ ] Structured logging (JSON format) instead of print()
- [ ] Log levels used correctly (DEBUG, INFO, WARNING, ERROR)
- [ ] Request/response logging for debugging
- [ ] No sensitive data in logs (passwords, tokens, etc.)

### Database

- [ ] Automated backups enabled (Railway/Render do this)
- [ ] Connection pooling configured
- [ ] Migrations tested before deploy
- [ ] Rollback plan documented

### Deployment

- [ ] CI/CD pipeline runs tests before deploy
- [ ] Environment variables documented (.env.example)
- [ ] Zero-downtime deploys (Railway handles this)
- [ ] Rollback procedure tested

## Project files

```
03-production-checklist/
├── app.py              # Production-hardened FastAPI app
├── config.py           # Configuration from environment
├── logging_config.py   # Structured logging setup
├── requirements.txt
├── .env.example
└── notes.md
```

## Run

```bash
cd projects/modules/12-cloud-deploy/03-production-checklist
pip install -r requirements.txt
python app.py
```

## Alter it

1. Add Sentry integration for error tracking (sign up for free at sentry.io).
2. Add a `/metrics` endpoint that returns request counts and average response times.
3. Set up UptimeRobot to ping your `/health` endpoint every 5 minutes.

## Break it

1. Remove CORS middleware and try to call the API from a different domain.
2. Remove rate limiting and send 1000 requests in 1 second.
3. Log a user's password by accident. Find it in the logs.

## Fix it

1. Add CORS middleware with strict origin rules.
2. Add rate limiting middleware or use a reverse proxy.
3. Add a log sanitizer that redacts sensitive fields.

## Explain it

1. Why is HTTPS important and how does it work at a high level?
2. What is the difference between monitoring and logging?
3. Why should you use structured (JSON) logging instead of plain text?
4. What is a connection pool and why does it matter for databases?

## Mastery check

You can move on when you can:
- deploy a production-hardened FastAPI app,
- set up monitoring and error tracking,
- configure structured logging,
- explain each item on the production checklist.

---

## Related Concepts

- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Collections Explained](../../../../concepts/quizzes/collections-explained-quiz.py)

## Next

Go back to [Module index](../README.md) or return to the [Modules overview](../../modules/README.md).
