"""
Root entrypoint for the ProtocolandCodingService FastAPI application.

This file allows running the app from the repository root with:
    uvicorn main:app --reload --port 3002

It imports the FastAPI app instance from the ProtocolandCodingService package.
"""

from ProtocolandCodingService.app.main import app

# PUBLIC_INTERFACE
def get_app():
    """
    Returns the FastAPI application instance.

    Useful for external tooling that needs to import the app object indirectly.
    """
    return app

# Expose 'app' at module level to support 'uvicorn main:app'
__all__ = ["app"]
