# ============================================================================
# Dockerfile — Production Configuration
# ============================================================================
# This Dockerfile combines everything from the previous projects:
#   - Multi-stage build (from Project 02) for a small image
#   - Non-root user for security
#   - HEALTHCHECK instruction for container health monitoring
#
# Build:
#   docker build -t production-app .
#
# Run:
#   docker run -p 8000:8000 --env-file .env.example production-app
# ============================================================================


# ==========================================================================
# Stage 1: builder — install dependencies
# ==========================================================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Create a virtual environment for clean dependency isolation.
RUN python -m venv /build/.venv
ENV PATH="/build/.venv/bin:$PATH"

# Install dependencies in the builder stage.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ==========================================================================
# Stage 2: production — final runtime image
# ==========================================================================
FROM python:3.12-slim

# --------------------------------------------------------------------------
# Create a non-root user.
#
# By default, Docker runs processes as root inside the container. This is a
# security risk: if an attacker exploits a vulnerability in your app, they
# have root access to the container (and potentially the host).
#
# Creating a dedicated user ("appuser") with no login shell and no home
# directory follows the principle of least privilege. The app runs with
# minimal permissions.
#
# --system    — creates a system user (no home directory, no login shell)
# --no-log-init — avoids creating a large lastlog file
# --------------------------------------------------------------------------
RUN useradd --system --no-log-init appuser

WORKDIR /app

# --------------------------------------------------------------------------
# Copy the virtual environment from the builder stage.
# --------------------------------------------------------------------------
COPY --from=builder /build/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# --------------------------------------------------------------------------
# Copy the application code.
# --------------------------------------------------------------------------
COPY . .

# --------------------------------------------------------------------------
# Change ownership of the app directory to the non-root user.
# The app needs to read its files but should not have write access to
# system files or other directories.
# --------------------------------------------------------------------------
RUN chown -R appuser:appuser /app

# --------------------------------------------------------------------------
# Switch to the non-root user.
# All subsequent instructions (and the CMD) run as "appuser."
# --------------------------------------------------------------------------
USER appuser

# --------------------------------------------------------------------------
# HEALTHCHECK — instruct Docker to periodically check if the container
# is healthy by making an HTTP request to the /health endpoint.
#
# --interval=30s   — check every 30 seconds.
# --timeout=10s    — fail if the check takes longer than 10 seconds.
# --start-period=5s — wait 5 seconds after startup before checking
#                     (gives the app time to initialize).
# --retries=3      — mark unhealthy after 3 consecutive failures.
#
# "curl -f" fails silently (returns non-zero exit code) on HTTP errors.
# If /health returns a non-200 status, the check fails.
#
# Install curl in a single RUN before switching to appuser, or use
# Python's urllib as shown here to avoid installing extra packages.
# --------------------------------------------------------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

EXPOSE 8000

# --------------------------------------------------------------------------
# CMD — start the application.
# In production, you typically run multiple workers to handle concurrent
# requests. The number of workers is configured via the WORKERS env var.
# --------------------------------------------------------------------------
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
