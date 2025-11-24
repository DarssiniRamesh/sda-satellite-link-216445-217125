"""
Initialization module for top-level app package if used directly.
This file ensures 'app' is recognized as a package when importing relative modules.

Note: Uvicorn target for this service is 'main:app' from the service root,
not 'ProtocolandCodingService.app.main'.
"""
__all__ = []
