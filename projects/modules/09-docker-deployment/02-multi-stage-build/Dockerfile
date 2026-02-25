# ============================================================================
# Dockerfile — Multi-Stage Build
# ============================================================================
# A multi-stage build uses multiple FROM instructions. Each FROM starts a
# new "stage." You can copy files from one stage to another but only the
# final stage ends up in the output image. This lets you install build tools
# in an early stage and produce a clean, minimal final image.
#
# Build:
#   docker build -t multi-stage-app .
#
# Compare sizes:
#   docker images single-stage-app
#   docker images multi-stage-app
# ============================================================================


# ==========================================================================
# Stage 1: builder
# ==========================================================================
# This stage installs Python dependencies into a virtual environment.
# The virtual environment makes it easy to copy only the installed packages
# (and nothing else) into the final stage.
#
# "AS builder" gives this stage a name so we can reference it later with
# COPY --from=builder.
# ==========================================================================
FROM python:3.12-slim AS builder

# --------------------------------------------------------------------------
# Set the working directory for the builder stage.
# --------------------------------------------------------------------------
WORKDIR /build

# --------------------------------------------------------------------------
# Create a virtual environment inside the builder stage.
# We install packages here so they live in a single directory (/build/.venv)
# that we can copy cleanly into the production stage.
# --------------------------------------------------------------------------
RUN python -m venv /build/.venv

# --------------------------------------------------------------------------
# Activate the virtual environment by prepending it to PATH.
# Every subsequent RUN command in this stage will use the venv's Python
# and pip instead of the system ones.
# --------------------------------------------------------------------------
ENV PATH="/build/.venv/bin:$PATH"

# --------------------------------------------------------------------------
# Copy and install dependencies in the builder stage.
# This stage has pip, setuptools, and all the tools needed to compile
# packages. None of these tools will be in the final image.
# --------------------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ==========================================================================
# Stage 2: production
# ==========================================================================
# This is the final stage. It starts from a clean python:3.12-slim image
# and copies only what is needed from the builder stage: the virtual
# environment (with installed packages) and the application code.
#
# The result is a smaller image because it does not contain:
# - pip, setuptools, or wheel
# - Build caches or temporary files from the install step
# - Anything from the builder stage that we did not explicitly copy
# ==========================================================================
FROM python:3.12-slim

# --------------------------------------------------------------------------
# Set the working directory for the production image.
# --------------------------------------------------------------------------
WORKDIR /app

# --------------------------------------------------------------------------
# Copy the virtual environment from the builder stage.
# --from=builder tells Docker to copy from the first stage, not from the
# build context (your local filesystem).
# --------------------------------------------------------------------------
COPY --from=builder /build/.venv /app/.venv

# --------------------------------------------------------------------------
# Add the virtual environment to PATH so Python finds the installed packages.
# --------------------------------------------------------------------------
ENV PATH="/app/.venv/bin:$PATH"

# --------------------------------------------------------------------------
# Copy the application code.
# --------------------------------------------------------------------------
COPY . .

# --------------------------------------------------------------------------
# Document the port and set the startup command.
# --------------------------------------------------------------------------
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
