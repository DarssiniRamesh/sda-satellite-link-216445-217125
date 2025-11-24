"""
Application package initializer for ProtocolandCodingService.

Exposes:
- app: The FastAPI application instance created in app.main
- create_app: Factory function to create a new FastAPI app instance
"""

from .main import app, create_app  # re-export for convenience
