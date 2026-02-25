# ============================================================================
# Dockerfile — CI Pipeline App
# ============================================================================
# Standard Python Dockerfile for the CI project. The GitHub Actions workflow
# builds this image in the "build" job to verify the Dockerfile is valid.
#
# Build locally:
#   docker build -t ci-app .
# ============================================================================

FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies (cached layer).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code.
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
