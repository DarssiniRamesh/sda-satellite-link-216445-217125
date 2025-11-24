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
# 1) Prefer relative import (works when CWD is the service directory and the package is local)
# 2) Fallback to absolute import (works when running from repo root)
# 3) If both fail, add parent to sys.path and retry absolute import
app = None  # will be set by one of the import paths

# Try relative import first to support `uvicorn main:app` from service dir
try:
    from app.main import app as _app  # type: ignore
    app = _app
except Exception:
    # Try absolute import (works when running from repo root)
    try:
        from ProtocolandCodingService.app.main import app as _app  # type: ignore
        app = _app
    except Exception:
        # As a last resort, ensure the parent of the service directory is on sys.path
        service_dir = Path(__file__).resolve().parent
        parent_dir = service_dir.parent
        if str(parent_dir) not in sys.path:
            sys.path.append(str(parent_dir))
        # Retry absolute import after fixing sys.path
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
__all__ = ["app"]
