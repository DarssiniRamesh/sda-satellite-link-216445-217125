from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from app.routers.coding import router as coding_router
from app.routers.arq import router as arq_router
from app.routers.sync import router as sync_router
from app.routers.status import router as status_router


# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance with metadata, middleware, and routers.
    """
    app = FastAPI(
        title="Protocol and Coding Service",
        description=(
            "Handles synchronization, channel coding (5G NR LDPC FEC), frame construction "
            "(preamble, header, payload), scrambling, error control (CRC-16, CRC-32), and "
            "ARQ management for the SDA Satellite Link system. Exposes health and protocol endpoints."
        ),
        version="0.1.0",
        openapi_tags=[
            {"name": "health", "description": "Basic service health and readiness endpoints."},
            {"name": "protocol", "description": "Protocol processing and coding interfaces."},
        ],
    )

    # Allow cross-origin requests from any origin by default (can be restricted via env/config later)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(coding_router)
    app.include_router(arq_router)
    app.include_router(sync_router)
    app.include_router(status_router)

    @app.get(
        "/health",
        tags=["health"],
        summary="Health check",
        description="Returns a simple health status to indicate the service is up.",
        responses={
            200: {
                "description": "Service is healthy.",
                "content": {
                    "application/json": {
                        "example": {"status": "ok", "service": "ProtocolandCodingService"}
                    }
                },
            }
        },
    )
    # PUBLIC_INTERFACE
    def health() -> Dict[str, str]:
        """Health check endpoint.

        Returns:
            dict: A JSON object indicating service health.
        """
        return {"status": "ok", "service": "ProtocolandCodingService"}

    return app


# Expose the ASGI application for uvicorn with import path 'app.main:app'
app = create_app()
