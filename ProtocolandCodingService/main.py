"""
Shim entrypoint for FastAPI application within the ProtocolandCodingService container directory.

This file enables running the service from this directory (service root) with:
    uvicorn main:app --host 0.0.0.0 --port 3002

It ensures `app` is imported from the FastAPI initialization module regardless of
whether the process is started from the repo root or from the service directory,
and even in environments where package resolution may not be pre-configured.
"""

import sys
from pathlib import Path

# Robust import strategy:
# 1) Prefer import from local package when CWD is service dir (from app.main)
# 2) If that fails, append parent to sys.path and try absolute package import
# 3) Final fallback: try absolute import without modifying sys.path
app = None  # will be set by one of the import paths

try:
    # Prefer local import so `uvicorn main:app` works directly inside service directory
    from app.main import app as _app  # type: ignore
    app = _app
except Exception:
    try:
        # Ensure the parent of this service directory is on sys.path, then import absolutely
        service_dir = Path(__file__).resolve().parent
        parent_dir = service_dir.parent
        if str(parent_dir) not in sys.path:
            sys.path.append(str(parent_dir))
        from ProtocolandCodingService.app.main import app as _app  # type: ignore
        app = _app
    except Exception:
        # Final attempt: absolute import without sys.path modification
        from ProtocolandCodingService.app.main import app as _app  # type: ignore
        app = _app


# PUBLIC_INTERFACE
def get_app():
    """
    Returns the FastAPI application instance.

    Useful for tooling that imports the app indirectly.
    """
    return app

# Expose 'app' at module level to support 'uvicorn main:app'
# This is required by the Dockerfile CMD and local run instructions.
__all__ = ["app"]
