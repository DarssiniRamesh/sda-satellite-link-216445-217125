from __future__ import annotations

import os
from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings for ProtocolandCodingService."""
    APP_NAME: str = Field(default="ProtocolandCodingService", description="Service name")
    APP_VERSION: str = Field(default="0.1.0", description="Service version")
    APP_DESCRIPTION: str = Field(
        default="Protocol processing: framing, 5G NR LDPC FEC, CRC, ARQ, and telemetry.",
        description="Short description for service",
    )
    PORT: int = Field(default=int(os.getenv("PORT", "8000")), description="Port (metadata only)")
    CORS_ALLOW_ORIGINS: List[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
        description="Allowed CORS origins",
    )


@lru_cache()
def get_settings() -> Settings:
    """
    PUBLIC_INTERFACE
    Returns cached Settings instance loaded from environment variables.
    """
    return Settings()
