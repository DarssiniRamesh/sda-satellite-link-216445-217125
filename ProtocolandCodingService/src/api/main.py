"""FastAPI application factory and default app instance for Protocol and Coding Service."""

from __future__ import annotations

from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    application = FastAPI(
        title="Protocol and Coding Service",
        description=(
            "Handles synchronization, channel coding (5G NR LDPC FEC), frame construction, "
            "scrambling, error control, and ARQ management. Exposes protocol processing and "
            "frame handling interfaces."
        ),
        version="0.1.0",
        openapi_tags=[
            {"name": "Health", "description": "Service health and liveness checks."},
        ],
        # Explicitly enable default documentation endpoints
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Log OpenAPI/docs URLs on startup for discoverability in preview/local environments
    logger = logging.getLogger(__name__)

    @application.on_event("startup")
    async def _log_docs_urls() -> None:
        port = os.getenv("PORT") or "5000"
        host = "0.0.0.0"
        try:
            p = int(port)
            if not (1 <= p <= 65535):
                port = "5000"
        except ValueError:
            port = "5000"
        logger.info("Protocol and Coding Service started")
        logger.info("Swagger UI: http://%s:%s/docs", host, port)
        logger.info("OpenAPI JSON: http://%s:%s/openapi.json", host, port)

    @application.get("/", tags=["Health"], summary="Health Check", description="Simple health check endpoint.")
    # PUBLIC_INTERFACE
    def health_check() -> dict[str, str]:
        """Health check endpoint.

        Returns:
            dict[str, str]: JSON payload indicating service health.
        """
        return {"message": "Healthy"}

    @application.get("/health", tags=["Health"], summary="Readiness/Health probe", description="Ready probe for orchestrators.")
    # PUBLIC_INTERFACE
    def readiness() -> dict[str, str]:
        """Readiness endpoint for liveness probes and readiness checks."""
        return {"status": "ok"}

    return application


# Expose a module-level symbol `app`
# PUBLIC_INTERFACE
app: Final[FastAPI] = create_app()
__all__: Final = ["app", "create_app"]
