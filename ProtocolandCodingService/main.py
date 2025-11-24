"""
Shim entrypoint for FastAPI application within the ProtocolandCodingService container directory.

This file enables running the service from this directory (container root) with:
    uvicorn main:app --host 0.0.0.0 --port 3002

It imports `app` from the package-level FastAPI initialization.
The import is resilient whether started from the repository root or from the
ProtocolandCodingService folder to avoid ModuleNotFoundError issues.
"""

# Attempt absolute import (works when running from repo root)
try:
    from ProtocolandCodingService.app.main import app  # type: ignore
except Exception:
    # Fallback to local package import when running inside ProtocolandCodingService/
    from app.main import app  # type: ignore

# PUBLIC_INTERFACE
def get_app():
    """
    Returns the FastAPI application instance.

    Useful for tooling that imports the app indirectly.
    """
    return app

# Expose 'app' at module level to support 'uvicorn main:app'
__all__ = ["app"]
