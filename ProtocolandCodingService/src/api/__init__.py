"""
API package for Protocol and Coding Service.

Exports:
    app (FastAPI): The FastAPI application instance.
    create_app (Callable): Factory to create a new FastAPI application instance.
"""

from __future__ import annotations

from .main import app, create_app

__all__ = ["app", "create_app"]
