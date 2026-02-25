# ============================================================================
# Dockerfile — First Dockerfile
# ============================================================================
# A Dockerfile is a recipe for building a container image. Each instruction
# adds a layer to the image. Docker caches layers, so unchanged layers are
# reused on subsequent builds (this makes rebuilds fast).
#
# Build this image:
#   docker build -t first-dockerfile .
#
# Run a container from the image:
#   docker run -p 8000:8000 first-dockerfile
# ============================================================================

# --------------------------------------------------------------------------
# FROM — choose the base image.
# Every Docker image starts from a parent image. python:3.12-slim is an
# official Python image based on Debian with unnecessary packages removed.
# "slim" means it is smaller than the full image (~150 MB vs ~900 MB).
#
# Why not python:3.12 (full)?   — Too large. Includes compilers and tools
#                                  you do not need at runtime.
# Why not python:3.12-alpine?   — Alpine uses musl libc instead of glibc.
#                                  Some Python packages (numpy, pandas) do
#                                  not have pre-built wheels for Alpine and
#                                  require compiling from source, which is
#                                  slow and error-prone.
# --------------------------------------------------------------------------
FROM python:3.12-slim

# --------------------------------------------------------------------------
# WORKDIR — set the working directory inside the container.
# All subsequent commands (COPY, RUN, CMD) execute relative to this path.
# If the directory does not exist, Docker creates it.
# This is like running "cd /app" at the start of a shell session.
# --------------------------------------------------------------------------
WORKDIR /app

# --------------------------------------------------------------------------
# COPY requirements.txt first (before copying the rest of the code).
# Docker caches each layer. If requirements.txt has not changed, Docker
# reuses the cached pip install layer and skips the slow download step.
# This is called "layer caching" and it makes rebuilds much faster.
# --------------------------------------------------------------------------
COPY requirements.txt .

# --------------------------------------------------------------------------
# RUN — execute a command during the build.
# pip install reads requirements.txt and installs the listed packages.
#
# --no-cache-dir  — do not store pip's download cache inside the image.
#                   The cache wastes space because you will never pip install
#                   again inside this image.
# --------------------------------------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------------------------------------------------
# COPY . . — copy the rest of your application code into the image.
# The first "." is the source (your project directory on the host).
# The second "." is the destination (/app inside the container, because
# WORKDIR is set to /app).
#
# This step is separate from COPY requirements.txt so that code changes
# do not invalidate the pip install cache layer.
# --------------------------------------------------------------------------
COPY . .

# --------------------------------------------------------------------------
# EXPOSE — document which port the container listens on.
# This does NOT actually publish the port. It is metadata for anyone
# reading the Dockerfile. The actual port mapping happens at runtime
# with "docker run -p 8000:8000".
# --------------------------------------------------------------------------
EXPOSE 8000

# --------------------------------------------------------------------------
# CMD — the default command to run when the container starts.
# This starts uvicorn, which serves the FastAPI application.
#
# --host 0.0.0.0  — listen on all network interfaces inside the container.
#                   Without this, the server only listens on 127.0.0.1
#                   (localhost inside the container), which is unreachable
#                   from the host machine.
# --port 8000     — match the EXPOSE declaration above.
#
# CMD uses the "exec form" (JSON array) instead of the "shell form"
# (plain string). The exec form runs uvicorn as PID 1, which means it
# receives shutdown signals (SIGTERM) directly. The shell form wraps the
# command in /bin/sh, which can swallow signals and prevent graceful
# shutdown.
# --------------------------------------------------------------------------
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
