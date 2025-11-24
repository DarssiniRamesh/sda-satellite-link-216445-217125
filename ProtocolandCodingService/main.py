"""
ASGI entrypoint for ProtocolandCodingService.

This module exposes the FastAPI application as `app` so that process managers
and the preview orchestrator can launch the service with:

    uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"

It re-exports the application created in src.api.main without altering ports or behavior.
"""

from __future__ import annotations

# Re-export the FastAPI application instance for ASGI servers.
from src.api.main import app  # noqa: F401  (public re-export)
