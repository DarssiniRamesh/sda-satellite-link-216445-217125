"""
FastAPI application initialization for the ProtocolandCodingService.

Provides basic health and version endpoints and sets up logging and OpenAPI metadata.
"""

import logging
from logging import Logger
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .settings import get_settings

settings = get_settings()

# Basic logging configuration
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger: Logger = logging.getLogger("protocol-and-coding-service")

openapi_tags = [
    {"name": "health", "description": "Service liveness and readiness checks"},
    {"name": "meta", "description": "Service metadata and version information"},
]

# Create FastAPI app instance with metadata
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    openapi_tags=openapi_tags,
)


@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Returns liveness and basic readiness metadata.",
    response_model=dict,
    responses={200: {"description": "Service is healthy"}},
)
# PUBLIC_INTERFACE
def health() -> dict:
    """Health check endpoint returning basic service status."""
    return {"status": "ok", "service": settings.APP_NAME}


@app.get(
    "/version",
    tags=["meta"],
    summary="Version information",
    description="Returns application name and version.",
    response_model=dict,
    responses={200: {"description": "Version info"}},
)
# PUBLIC_INTERFACE
def version() -> dict:
    """Version endpoint returning app metadata."""
    return {"name": settings.APP_NAME, "version": settings.APP_VERSION}


# Root handler can provide a minimal welcome or redirect
@app.get(
    "/",
    tags=["meta"],
    summary="Root",
    description="Root endpoint returning a minimal service descriptor.",
    response_model=dict,
)
def root() -> JSONResponse:
    """Root endpoint providing a descriptor and helpful links."""
    return JSONResponse(
        {
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "openapi": "/openapi.json",
            "health": "/health",
        }
    )
