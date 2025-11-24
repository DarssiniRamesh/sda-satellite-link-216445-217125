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

# Try absolute import first (works when running from repository root)
try:
    from ProtocolandCodingService.app.main import app  # type: ignore
except Exception:
    # Try relative package import when running from the service directory
    try:
        from app.main import app  # type: ignore
    except Exception:
        # As a last resort, ensure the parent of the service directory is on sys.path
        # so that absolute import works even when invoked from within the service dir.
        service_dir = Path(__file__).resolve().parent
        parent_dir = service_dir.parent
        if str(parent_dir) not in sys.path:
            sys.path.append(str(parent_dir))
        # Retry absolute import after fixing sys.path
        from ProtocolandCodingService.app.main import app  # type: ignore

# PUBLIC_INTERFACE
def get_app():
    """
    Returns the FastAPI application instance.

    Useful for tooling that imports the app indirectly.
    """
    return app

# Expose 'app' at module level to support 'uvicorn main:app'
__all__ = ["app"]
