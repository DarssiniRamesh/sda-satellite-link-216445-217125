"""
Shim module to expose the FastAPI application as 'main:app' for ASGI servers.

This allows running:
- uvicorn app.main:app
- uvicorn main:app
"""

# PUBLIC_INTERFACE
def get_app():
    """Return the FastAPI app instance from app.main."""
    from app.main import app
    return app

# Expose the ASGI app for uvicorn as 'main:app'
from app.main import app  # noqa: E402
