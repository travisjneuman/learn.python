# Deploy to Railway — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 15 minutes attempting it independently. The goal is to deploy a FastAPI app to Railway so it is accessible from any browser in the world. If you can get the app running locally first, you are halfway there.

## Thinking Process

Deployment is the bridge between "it runs on my laptop" and "anyone on the internet can use it." The app itself is a straightforward FastAPI server — you have built these before. The new skill here is configuring it for a cloud platform. Three things change when you move from local to cloud: configuration comes from environment variables (not hardcoded values), the port is assigned by the platform (not chosen by you), and the server must listen on `0.0.0.0` (not `127.0.0.1`).

Railway (and similar platforms like Render, Fly.io, and Heroku) follow a simple workflow: you push code to GitHub, the platform detects it, builds a container, and runs it. The `Procfile` tells Railway how to start your app. Environment variables control configuration without code changes. This is the Twelve-Factor App methodology in practice — the same code runs in development and production, with only environment variables changing.

Think of it like mailing a package. Locally, you hand the package directly to someone. In the cloud, you need an address (URL), a delivery method (Procfile), and instructions for the recipient (environment variables). The package contents (your code) stay the same.

## Step 1: Build the FastAPI App with Environment Variables

**What to do:** Create a FastAPI app that reads configuration from environment variables instead of hardcoded values.

**Why:** In production, you never hardcode configuration. The database URL, API keys, and even the app name come from environment variables. This lets you run the exact same code in development (local SQLite, debug mode) and production (cloud Postgres, production mode) by changing only environment variables.

```python
import os
from fastapi import FastAPI

APP_NAME = os.environ.get("APP_NAME", "my-fastapi-app")
APP_ENV = os.environ.get("APP_ENV", "development")
APP_VERSION = "1.0.0"
PORT = int(os.environ.get("PORT", 8000))

app = FastAPI(title=APP_NAME, version=APP_VERSION)
```

Two details to notice:

- **`os.environ.get("APP_ENV", "development")`** reads the environment variable with a default value. Locally, the default kicks in. On Railway, you set `APP_ENV=production`.
- **`PORT = int(os.environ.get("PORT", 8000))`** reads the port as a string and converts to int. Railway assigns the port automatically — you must not hardcode it.

**Predict:** What happens if you hardcode `port=8000` and deploy to Railway, but Railway assigns port 3000? Can anyone reach your app?

## Step 2: Create the Endpoints

**What to do:** Add root, health check, and info endpoints.

**Why:** The root endpoint confirms the app is running. The health check endpoint is what load balancers and monitoring tools ping to verify the app is alive. The info endpoint helps you debug deploys by showing the environment, version, and port.

```python
@app.get("/")
async def root():
    return {
        "message": "Hello from the cloud!",
        "environment": APP_ENV,
        "version": APP_VERSION,
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": APP_ENV}

@app.get("/info")
async def app_info():
    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "environment": APP_ENV,
        "port": PORT,
    }
```

The `/health` endpoint is not optional in production. Railway, Render, and Kubernetes all use health checks to decide if a container is healthy. If this endpoint stops responding, the platform restarts your app automatically.

**Predict:** After deploying, what value will `APP_ENV` show at the root endpoint? What about locally?

## Step 3: Create the Procfile

**What to do:** Create a `Procfile` that tells Railway how to start your app.

**Why:** The Procfile is a single-line configuration file that cloud platforms read to know which command starts your app. Without it, Railway has to guess — and it might guess wrong. The format is `<process type>: <command>`.

```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

Three details to notice:

- **`web:`** tells Railway this is a web process that receives HTTP traffic.
- **`--host 0.0.0.0`** listens on all interfaces — required in the cloud, just like in Docker.
- **`$PORT`** is an environment variable that Railway sets automatically. Your app must use it.

**Predict:** What happens if you omit the Procfile? Can Railway still deploy your app?

## Step 4: Create Supporting Files

**What to do:** Create `requirements.txt`, `runtime.txt`, and `.env.example`.

**Why:** `requirements.txt` lists your Python dependencies so Railway can install them. `runtime.txt` specifies the Python version. `.env.example` documents which environment variables your app expects (without containing actual values).

```text
# requirements.txt
fastapi>=0.100.0
uvicorn>=0.23.0
```

```text
# runtime.txt
python-3.12
```

```text
# .env.example
APP_NAME=my-fastapi-app
APP_ENV=development
```

**Predict:** What happens if you forget to include `uvicorn` in `requirements.txt`? When does the error appear — during build or at runtime?

## Step 5: Test Locally, Then Deploy

**What to do:** Verify the app works locally, push to GitHub, and deploy on Railway.

**Why:** Always test locally before deploying. Cloud debugging is slower and harder. Once the app works locally, deployment is just connecting Railway to your GitHub repo and setting environment variables.

```bash
# Test locally
pip install -r requirements.txt
python app.py
# Visit http://127.0.0.1:8000/docs
```

Deployment steps:

1. Push your code to a GitHub repository
2. Sign in to https://railway.app with your GitHub account
3. Click "New Project" and select "Deploy from GitHub repo"
4. Select your repository — Railway detects the Procfile and starts building
5. In the Railway dashboard, set environment variables: `APP_ENV=production`, `APP_NAME=my-fastapi-app`
6. Railway gives you a public URL — visit it to verify

```bash
# After deployment, verify with curl
curl https://your-app.up.railway.app/health
```

**Predict:** After pushing a code change to GitHub, what happens on Railway? Do you need to manually trigger a redeploy?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| App crashes on Railway but works locally | Hardcoded port instead of `$PORT` | Read PORT from `os.environ.get("PORT", 8000)` |
| "Application failed to respond" | Host is `127.0.0.1` instead of `0.0.0.0` | Use `--host 0.0.0.0` in the Procfile |
| Missing dependency error during build | Forgot to update `requirements.txt` | Add all dependencies: `pip freeze > requirements.txt` (then prune) |
| Secrets visible in GitHub | Committed `.env` file | Add `.env` to `.gitignore`; use `.env.example` as a template |

## Testing Your Solution

Test locally first:

```bash
python app.py
```

Visit these URLs:
- `http://127.0.0.1:8000` should return `{"message": "Hello from the cloud!", "environment": "development", "version": "1.0.0"}`
- `http://127.0.0.1:8000/health` should return `{"status": "healthy", ...}`
- `http://127.0.0.1:8000/info` should show app details including the port

After deploying to Railway, the same endpoints should work at your Railway URL, but `environment` should show `"production"`.

## What You Learned

- **Environment variables** are the standard way to configure apps in the cloud — they let you run the same code in development and production with different settings.
- **The Procfile** tells the cloud platform exactly how to start your app — without it, the platform has to guess, which often fails.
- **`--host 0.0.0.0`** and reading `$PORT`** are the two changes every app needs for cloud deployment — the platform assigns the port and routes traffic through its network.
- **The deployment workflow** is push to GitHub, connect to Railway, set environment variables, and verify — Railway handles building and running automatically.
