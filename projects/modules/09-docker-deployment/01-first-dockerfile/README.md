# Module 09 / Project 01 — First Dockerfile

Home: [README](../../../../README.md)

## Focus

Writing a Dockerfile, building an image, and running a container.

## Why this project exists

Docker packages your application and all its dependencies into a single image that runs the same way on every machine. No more "it works on my laptop" problems. This project teaches you the fundamental Docker workflow: write a Dockerfile, build an image, run a container. Every deployment pipeline in the industry starts here.

## Run

### Without Docker (verify the app works locally first)

```bash
cd projects/modules/09-docker-deployment/01-first-dockerfile
python app.py
```

Visit http://127.0.0.1:8000 to confirm it works, then stop the server with `Ctrl+C`.

### With Docker

**Step 1 — Build the image.** This reads the Dockerfile and creates an image named `first-dockerfile`:

```bash
docker build -t first-dockerfile .
```

You will see Docker execute each instruction. The first build downloads the base image and installs dependencies (slow). Subsequent builds reuse cached layers (fast).

**Step 2 — Run a container from the image:**

```bash
docker run -p 8000:8000 first-dockerfile
```

The `-p 8000:8000` flag maps port 8000 on your machine to port 8000 inside the container.

**Step 3 — Visit your app:**

- http://127.0.0.1:8000 — root endpoint
- http://127.0.0.1:8000/health — health check
- http://127.0.0.1:8000/docs — interactive API docs

**Step 4 — Stop the container** with `Ctrl+C`.

### Useful Docker commands

```bash
docker images                    # list all images on your machine
docker ps                        # list running containers
docker ps -a                     # list all containers (including stopped)
docker rm <container_id>         # remove a stopped container
docker rmi first-dockerfile      # remove the image
```

## Expected output

Visiting http://127.0.0.1:8000 returns:

```json
{"message": "Hello from Docker!", "version": "1.0.0"}
```

Visiting http://127.0.0.1:8000/health returns:

```json
{"status": "healthy"}
```

## Alter it

1. Add a `GET /info` endpoint that returns `{"container": True, "python_version": "3.12"}`. Rebuild the image and verify.
2. Change the `CMD` in the Dockerfile to run on port 9000. Update the `EXPOSE` instruction and the `docker run` command to match.
3. Add a `--name my-app` flag to `docker run` so you can refer to the container by name instead of ID.

## Break it

1. Remove the `COPY requirements.txt .` and `RUN pip install` lines from the Dockerfile. Rebuild and try to run. What error do you get?
2. Change `--host 0.0.0.0` to `--host 127.0.0.1` in the CMD instruction. Rebuild and run. Can you reach the app from your browser? Why not?
3. Swap the order of `COPY requirements.txt .` and `COPY . .` so all files are copied in one step. Does it still work? What happens to build caching when you change only `app.py`?

## Fix it

1. Restore the `COPY requirements.txt` and `RUN pip install` lines. The app cannot start without its dependencies installed in the image.
2. Change the host back to `0.0.0.0`. Inside a container, `127.0.0.1` only accepts connections from inside the container itself, not from the host machine.
3. Separate the two COPY steps again. With a single COPY, every code change invalidates the pip install cache and forces a slow reinstall.

## Explain it

1. What is the difference between a Docker image and a Docker container?
2. Why does the Dockerfile copy `requirements.txt` and run `pip install` before copying the rest of the code?
3. What does `-p 8000:8000` mean in the `docker run` command? What happens if you use `-p 3000:8000`?
4. Why does the CMD use `--host 0.0.0.0` instead of `--host 127.0.0.1`?

## Mastery check

You can move on when you can:

- write a Dockerfile from scratch without looking at this one,
- build an image and run a container with port mapping,
- explain why layer order matters for build caching,
- describe the difference between EXPOSE and `-p`.

## Next

Continue to [02-multi-stage-build](../02-multi-stage-build/).
