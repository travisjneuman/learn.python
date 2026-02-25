# ============================================================================
# Dockerfile — Docker Compose Web Service
# ============================================================================
# This Dockerfile builds the FastAPI web service. It is referenced by the
# "web" service in docker-compose.yml. The PostgreSQL database runs in a
# separate container (defined in docker-compose.yml as the "db" service).
#
# You do not build or run this Dockerfile directly. Instead, use:
#   docker compose up --build
# ============================================================================

# --------------------------------------------------------------------------
# Start from the official Python slim image.
# --------------------------------------------------------------------------
FROM python:3.12-slim

# --------------------------------------------------------------------------
# Set the working directory inside the container.
# --------------------------------------------------------------------------
WORKDIR /app

# --------------------------------------------------------------------------
# Copy and install dependencies first (layer caching).
# --------------------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------------------------------------------------
# Copy the application code.
# --------------------------------------------------------------------------
COPY . .

# --------------------------------------------------------------------------
# Document the port and set the startup command.
# --------------------------------------------------------------------------
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
