"""
Root entrypoint for the ProtocolandCodingService FastAPI application.

This file allows running the app from the repository root with:
    uvicorn main:app --reload --port 3002

It imports the FastAPI app instance from the ProtocolandCodingService package.
The package includes an __init__.py to allow absolute imports to work consistently.
"""

# Prefer local service package import first, then fallback to absolute package
try:
    from ProtocolandCodingService.app.main import app  # type: ignore
except Exception:
    # If running inside the service dir by accident, try the relative import path
    try:
        from ProtocolandCodingService.app.main import app  # type: ignore
    except Exception as e:
        raise e

# PUBLIC_INTERFACE
def get_app():
    """
    Returns the FastAPI application instance.

    Useful for external tooling that needs to import the app object indirectly.
    """
    return app

# Expose 'app' at module level to support 'uvicorn main:app'
__all__ = ["app"]
