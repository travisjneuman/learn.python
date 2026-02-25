# Module 12 — Cloud Deployment

Home: [README](../../../README.md) · Modules: [Index](../README.md)

## Prerequisites

- Module 04 complete (FastAPI Web Apps)
- Module 09 complete (Docker & Deployment)

## What you will learn

- Deploying a Python app to a cloud platform
- Connecting to a managed PostgreSQL database
- Environment variables and secrets management
- Production readiness checklist

## Why cloud deployment matters

A web app that only runs on your laptop is a prototype. To share it with the world, you need to deploy it to a server that runs 24/7. This module walks through deploying a FastAPI app to a cloud platform with a real database.

## Platform choice

These projects use [Railway](https://railway.app) as the primary platform because it has a free tier, supports Python directly, and requires minimal configuration. Instructions for [Render](https://render.com) are included as alternatives.

## Projects

| # | Project | Focus |
|---|---------|-------|
| 01 | [Deploy to Railway](./01-deploy-to-railway/) | Push a FastAPI app live, environment config |
| 02 | [Deploy with Database](./02-deploy-with-database/) | PostgreSQL on Railway/Render, connection strings |
| 03 | [Production Checklist](./03-production-checklist/) | HTTPS, monitoring, logging, backup strategy |

## Related concepts

- [concepts/virtual-environments.md](../../../concepts/virtual-environments.md)
- [concepts/http-explained.md](../../../concepts/http-explained.md)
