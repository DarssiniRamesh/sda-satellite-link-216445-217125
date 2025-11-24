"""
Root entrypoint for the ProtocolandCodingService FastAPI application.

This file allows running the app from the repository root with:
    uvicorn main:app --reload --port 3002

It imports the FastAPI app instance from the ProtocolandCodingService package.
The package includes an __init__.py to allow absolute imports to work consistently.
"""
import sys
from pathlib import Path

# Robust import strategy similar to service-level shim
app = None
try:
    # Prefer import via local package path if executed from inside service dir by mistake
    from ProtocolandCodingService.app.main import app as _app  # type: ignore
    app = _app
except Exception:
    try:
        # Try relative import from service subpackage if local layout changes
        from ProtocolandCodingService.app.main import app as _app  # type: ignore
        app = _app
    except Exception:
        # Append parent of this file to sys.path and retry absolute import
        root_dir = Path(__file__).resolve().parent
        if str(root_dir) not in sys.path:
            sys.path.append(str(root_dir))
        from ProtocolandCodingService.app.main import app as _app  # type: ignore
        app = _app

# PUBLIC_INTERFACE
def get_app():
    """
    Returns the FastAPI application instance.

    Useful for external tooling that needs to import the app object indirectly.
    """
    return app

# Expose 'app' at module level to support 'uvicorn main:app'
__all__ = ["app"]
