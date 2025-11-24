"""
Application settings and configuration management.

Uses Pydantic Settings v2 to load configuration from environment variables
and a .env file (if present). Provides sane defaults for local development.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """
    Settings for the ProtocolandCodingService application.

    Values can be provided via environment variables or .env file.
    """

    APP_NAME: str = Field("Protocol and Coding Service", description="Human-friendly app name")
    APP_DESCRIPTION: str = Field(
        "Handles synchronization, channel coding (5G NR LDPC), frame construction,"
        " scrambling, error control, and ARQ management for the SDA OCT system.",
        description="Application description for OpenAPI docs",
    )
    APP_VERSION: str = Field("0.1.0", description="Application version string")

    HOST: str = Field("0.0.0.0", description="Bind host for the server")
    PORT: int = Field(3002, description="Default port where the service runs")

    # Toggle for debug mode
    DEBUG: bool = Field(False, description="Enable debug features and verbose logs")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


# PUBLIC_INTERFACE
def get_settings() -> AppSettings:
    """Return loaded application settings."""
    return AppSettings()
