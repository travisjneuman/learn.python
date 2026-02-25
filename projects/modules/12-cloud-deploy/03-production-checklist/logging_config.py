"""
Structured Logging — JSON-formatted logs for production.

Why structured logging?
- Plain text logs ("Error: something broke") are hard to search.
- JSON logs ({"level": "error", "message": "..."}) can be parsed by
  log aggregation tools (CloudWatch, Datadog, etc.).
- Each log entry has a timestamp, level, and context.
"""

import json
import logging
import sys
from datetime import datetime

from config import APP_NAME, APP_ENV, LOG_LEVEL, LOG_FORMAT


class JSONFormatter(logging.Formatter):
    """Formats log records as JSON for production log aggregation."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "app": APP_NAME,
            "environment": APP_ENV,
        }

        # Add exception info if present.
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add any extra fields passed via the "extra" parameter.
        for key in ("request_id", "method", "path", "status_code", "duration_ms"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        return json.dumps(log_entry)


def setup_logging():
    """Configure logging for the application."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # Remove existing handlers.
    root_logger.handlers.clear()

    # Create a handler that writes to stdout (cloud platforms capture stdout).
    handler = logging.StreamHandler(sys.stdout)

    if LOG_FORMAT == "json":
        handler.setFormatter(JSONFormatter())
    else:
        # Plain text format for local development.
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        ))

    root_logger.addHandler(handler)

    return root_logger
