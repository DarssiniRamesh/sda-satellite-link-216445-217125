"""
Top-level ASGI entrypoint for ProtocolandCodingService.

This module exposes the FastAPI application instance as `app` so that
process managers like uvicorn or gunicorn can import `main:app`.

It re-exports the application from src.api.main to keep a clean package structure.

Environment:
    PORT (optional): The port uvicorn should bind to when launching via
        `python -m uvicorn main:app`. Allowed ports: 3000, 3001, 3002, 5000.
        Defaults to 3000 if not provided or invalid.

Usage:
    uvicorn main:app --host 0.0.0.0 --port ${PORT:-3000}
"""

from __future__ import annotations

import logging
import os
from typing import Final

# Import the actual FastAPI app from the package
try:
    from src.api.main import app as _app  # type: ignore
except Exception:  # pragma: no cover - defensive logging
    # Log the import error clearly without exposing internal details.
    logging.getLogger(__name__).error("Failed to import FastAPI app from src.api.main")
    raise

# Re-export symbol expected by uvicorn (main:app)
# PUBLIC_INTERFACE
app = _app
app.__doc__ = (
    "FastAPI application instance for the Protocol and Coding Service. "
    "Use `uvicorn main:app` to run."
)

# Explicit public API
__all__: Final = ["app"]


def _get_port_from_env() -> int:
    """
    Read PORT from the environment and validate against allowed ports.

    Returns:
        int: The validated port. Defaults to 3000 if unset or invalid.
    """
    allowed_ports = {3000, 3001, 3002, 5000}
    raw = os.environ.get("PORT")
    if not raw:
        return 3000
    try:
        port = int(raw)
    except (TypeError, ValueError):
        return 3000
    return port if port in allowed_ports else 3000


# If someone runs `python main.py` directly (not recommended in production),
# provide a sensible dev server bootstrap that binds to 0.0.0.0 and uses the
# validated PORT env variable.
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    port = _get_port_from_env()
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
