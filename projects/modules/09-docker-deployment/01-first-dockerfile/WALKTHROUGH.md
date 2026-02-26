# First Dockerfile — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 15 minutes attempting it independently. The goal is to write a Dockerfile that packages a FastAPI app into a container image, build the image, and run a container from it. If you can visit `http://127.0.0.1:8000` and see a JSON response from a running container, you are done.

## Thinking Process

Docker solves the "it works on my laptop" problem. Your app depends on a specific Python version, specific packages, and specific system configuration. When you ship the code to a server, any mismatch can cause failures. Docker packages your app, its dependencies, and its runtime environment into a single image that runs identically everywhere.

A Dockerfile is a recipe. Each instruction (FROM, COPY, RUN, CMD) adds a layer to the image, like stacking transparent sheets. Docker caches these layers, so if `requirements.txt` has not changed, the `pip install` layer is reused. This is why the order of instructions matters — you want the things that change least (base image, dependencies) at the top and the things that change most (your code) at the bottom.

The mental model is simple: you are building a tiny virtual computer that has only what your app needs, nothing more. The Dockerfile is the blueprint for that computer.

## Step 1: Write the FastAPI Application

**What to do:** Create `app.py` with a simple FastAPI app that has root and health endpoints.

**Why:** Before containerizing anything, make sure the app works locally. This is the same kind of FastAPI app you built in Module 04. The only new thing is `host="0.0.0.0"` — inside a container, `127.0.0.1` is unreachable from outside, so you must listen on all interfaces.

```python
from fastapi import FastAPI

app = FastAPI(title="First Dockerfile App", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello from Docker!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
```

Test it locally first: `python app.py`, then visit `http://127.0.0.1:8000`.

**Predict:** Why is the host `"0.0.0.0"` instead of `"127.0.0.1"`? What happens inside a container if you use `127.0.0.1`?

## Step 2: Choose a Base Image with FROM

**What to do:** Start the Dockerfile with a `FROM` instruction that specifies the Python base image.

**Why:** Every Docker image starts from a parent image. `python:3.12-slim` gives you Python 3.12 on a minimal Debian system. "Slim" means unnecessary tools (compilers, documentation) are removed, making the image smaller (~150 MB vs ~900 MB for the full image).

```dockerfile
FROM python:3.12-slim
```

Three common base image options:

- **`python:3.12`** — full image, ~900 MB, includes build tools
- **`python:3.12-slim`** — minimal image, ~150 MB, good default
- **`python:3.12-alpine`** — tiny image, ~50 MB, but compatibility issues with some packages

**Predict:** Why not always use Alpine for the smallest image? What breaks with packages like numpy or pandas on Alpine?

## Step 3: Set Working Directory and Install Dependencies

**What to do:** Set the working directory, copy `requirements.txt`, and run `pip install`.

**Why:** The order here is deliberate. You copy `requirements.txt` and install dependencies before copying your code. Docker caches each layer — if `requirements.txt` has not changed, Docker reuses the cached `pip install` layer. This means code-only changes do not trigger a slow reinstall of all packages.

```dockerfile
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

Three details to notice:

- **`WORKDIR /app`** sets the directory for all subsequent commands. If it does not exist, Docker creates it.
- **`COPY requirements.txt .`** copies just one file. The `.` means "current directory inside the container" (which is `/app`).
- **`--no-cache-dir`** tells pip not to store downloaded packages in a cache — that cache wastes space inside the image.

**Predict:** What happens to build speed if you swap the order and use `COPY . .` first, then `pip install`? What gets invalidated when you change a single line of code?

## Step 4: Copy Your Code and Configure the Container

**What to do:** Copy the rest of your application, document the port, and set the startup command.

**Why:** `COPY . .` copies everything in your project directory into the container. `EXPOSE` documents which port the app uses (but does not actually open it). `CMD` is the command that runs when the container starts.

```dockerfile
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Three details to notice:

- **`COPY . .`** is separate from the earlier `COPY requirements.txt .` to preserve layer caching.
- **`EXPOSE 8000`** is documentation only. The actual port mapping happens with `docker run -p`.
- **`CMD` uses the exec form** (JSON array) instead of shell form (plain string). The exec form runs uvicorn as PID 1, so it receives shutdown signals directly.

**Predict:** What is the difference between `EXPOSE 8000` in the Dockerfile and `-p 8000:8000` in the `docker run` command? Which one actually makes the port accessible?

## Step 5: Build and Run

**What to do:** Build the Docker image and run a container from it.

**Why:** Building converts the Dockerfile into an image — a snapshot of the filesystem with your app and all its dependencies. Running creates a container — a live instance of that image. Multiple containers can run from the same image.

```bash
# Build the image and tag it
docker build -t first-dockerfile .

# Run a container, mapping port 8000
docker run -p 8000:8000 first-dockerfile
```

The `-p 8000:8000` flag maps port 8000 on your machine to port 8000 inside the container. The format is `host_port:container_port`. If you use `-p 3000:8000`, you would visit `http://127.0.0.1:3000` on your machine, but the container still runs on 8000 internally.

**Predict:** After running the container, visit `http://127.0.0.1:8000`. Is the response any different from running the app locally without Docker?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| App unreachable from browser | Host is `127.0.0.1` instead of `0.0.0.0` | Use `--host 0.0.0.0` — container localhost is isolated |
| Slow rebuilds after code change | All files copied before pip install | Separate COPY: requirements first, then code |
| `pip install` runs every time | Single `COPY . .` before pip install | Copy only `requirements.txt` first, install, then copy everything |
| "Package not found" at runtime | Forgot to include dependency in requirements.txt | Run `pip freeze > requirements.txt` or add manually |

## Testing Your Solution

Build and run the container:

```bash
docker build -t first-dockerfile .
docker run -p 8000:8000 first-dockerfile
```

Visit these URLs:
- `http://127.0.0.1:8000` should return `{"message": "Hello from Docker!", "version": "1.0.0"}`
- `http://127.0.0.1:8000/health` should return `{"status": "healthy"}`
- `http://127.0.0.1:8000/docs` should show the interactive API documentation

Press `Ctrl+C` to stop the container.

## What You Learned

- **A Dockerfile** is a recipe that builds a container image layer by layer — each instruction (FROM, COPY, RUN, CMD) adds a layer that Docker caches for fast rebuilds.
- **Layer ordering matters** for caching: copy `requirements.txt` and install dependencies before copying code, so code changes do not invalidate the dependency cache.
- **`--host 0.0.0.0`** inside a container is required because the container has its own network namespace — `127.0.0.1` refers to the container's own loopback, not the host machine.
- **The difference between an image and a container** is like the difference between a class and an instance — the image is the blueprint, the container is a running copy of it.
