"""
Top-level ASGI entrypoint for ProtocolandCodingService.

- Exposes `app` imported from src.api.main so `uvicorn main:app` works.
- When executed directly, runs uvicorn bound to 0.0.0.0 on the port from env PORT,
  defaulting to 5000 per project standard.

Usage:
    uvicorn main:app --host 0.0.0.0 --port ${PORT:-5000}
"""

from __future__ import annotations

import logging
import os
from typing import Final

# Import the actual FastAPI app from the package
try:
    from src.api.main import app as _app  # type: ignore
except Exception:  # pragma: no cover - defensive logging
    logging.getLogger(__name__).error("Failed to import FastAPI app from src.api.main")
    raise

# Re-export symbol expected by uvicorn (main:app)
# PUBLIC_INTERFACE
app = _app
app.__doc__ = (
    "FastAPI application instance for the Protocol and Coding Service. "
    "Use `uvicorn main:app` to run."
)
# Note: Swagger UI is available at /docs and OpenAPI JSON at /openapi.json by default.

# Explicit public API
__all__: Final = ["app"]


def _get_port_from_env() -> int:
    """
    Read PORT from the environment and validate against allowed ports.

    Returns:
        int: The validated port. Defaults to 5000 if unset or invalid.
    """
    allowed_ports = {3000, 3001, 3002, 5000}
    raw = os.environ.get("PORT")
    if not raw:
        return 5000
    try:
        port = int(raw)
    except (TypeError, ValueError):
        return 5000
    return port if port in allowed_ports else 5000


# If someone runs `python main.py` directly (not recommended in production),
# provide a sensible dev server bootstrap that binds to 0.0.0.0 and uses the
# validated PORT env variable.
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    port = _get_port_from_env()
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
