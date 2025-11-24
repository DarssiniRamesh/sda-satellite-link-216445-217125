"""
Shim entrypoint for FastAPI application within the ProtocolandCodingService container directory.

This file enables running the service from this directory (container root) with:
    uvicorn main:app --host 0.0.0.0 --port 3002

It imports `app` from the package-level FastAPI initialization.
"""

from ProtocolandCodingService.app.main import app

# PUBLIC_INTERFACE
def get_app():
    """
    Returns the FastAPI application instance.

    Useful for tooling that imports the app indirectly.
    """
    return app

# Expose 'app' at module level to support 'uvicorn main:app'
__all__ = ["app"]
