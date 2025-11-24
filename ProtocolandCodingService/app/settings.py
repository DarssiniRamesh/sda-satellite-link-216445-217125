"""
Application settings and configuration management.

Uses Pydantic v2 and pydantic-settings v2 to load configuration from environment
variables and an optional .env file. Provides sane defaults for local development.

Note:
- Field is imported from pydantic (v2)
- BaseSettings is imported from pydantic_settings (v2)
- No legacy pydantic.BaseSettings imports remain
- Unknown environment variables should NOT cause validation errors in preview envs
"""

from __future__ import annotations

import json
from typing import List, Optional, Sequence, Union

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


def _parse_list(value: Union[str, Sequence[str], None]) -> Optional[List[str]]:
    """
    Helper to coerce environment-provided values into a list of strings.

    Accepts:
    - None → None
    - list/tuple of str → list[str]
    - JSON-style list in a string (e.g., '["a","b"]') → list[str]
    - Comma-separated string (e.g., 'a,b,c') → ['a','b','c'] with whitespace trimmed
    - Empty string or string with only commas/whitespace → None
    """
    if value is None:
        return None

    # If already a sequence of strings (but not a str), normalize to list[str]
    if isinstance(value, (list, tuple)):
        # Filter out falsy or purely-whitespace entries and strip whitespace
        normalized = [str(v).strip() for v in value if str(v).strip() != ""]
        return normalized or None

    if isinstance(value, str):
        raw = value.strip()
        if raw == "":
            return None

        # Try to parse JSON-style list first
        if (raw.startswith("[") and raw.endswith("]")) or (raw.startswith("(") and raw.endswith(")")):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, (list, tuple)):
                    normalized = [str(v).strip() for v in parsed if str(v).strip() != ""]
                    return normalized or None
            except Exception:
                # fall through to comma parsing
                pass

        # Fallback: comma-separated handling
        parts = [p.strip() for p in raw.split(",")]
        # Remove empty entries
        parts = [p for p in parts if p != ""]
        return parts or None

    # Unknown type: coerce to string and split by commas as a conservative fallback
    coerced = str(value)
    parts = [p.strip() for p in coerced.split(",")]
    parts = [p for p in parts if p != ""]
    return parts or None


class AppSettings(BaseSettings):
    """
    Settings for the ProtocolandCodingService application.

    Values can be provided via environment variables or .env file.
    """

    # Core app metadata
    APP_NAME: str = Field("Protocol and Coding Service", description="Human-friendly app name")
    APP_DESCRIPTION: str = Field(
        "Handles synchronization, channel coding (5G NR LDPC), frame construction, "
        "scrambling, error control, and ARQ management for the SDA OCT system.",
        description="Application description for OpenAPI docs",
    )
    APP_VERSION: str = Field("0.1.0", description="Application version string")

    # Server bind configuration
    HOST: str = Field("0.0.0.0", description="Bind host for the server")
    PORT: int = Field(3002, description="Default port where the service runs")

    # Toggle for debug mode
    DEBUG: bool = Field(False, description="Enable debug features and verbose logs")

    # Optional fields commonly injected by preview environments; presence should not break settings
    backend_url: Optional[str] = Field(default=None, description="Preview env backend URL")
    frontend_url: Optional[str] = Field(default=None, description="Preview env frontend URL")
    ws_url: Optional[str] = Field(default=None, description="Preview env websocket URL")
    site_url: Optional[str] = Field(default=None, description="Site base URL for links/callbacks")

    # CORS settings: accept comma-separated or JSON-like lists from env
    allowed_origins: Optional[List[str]] = Field(
        default=None, description="CORS allowed origins list"
    )
    allowed_headers: Optional[List[str]] = Field(
        default=None, description="CORS allowed headers list"
    )
    allowed_methods: Optional[List[str]] = Field(
        default=None, description="CORS allowed methods list"
    )
    cors_max_age: Optional[int] = Field(default=None, description="CORS preflight max age")

    cookie_domain: Optional[str] = Field(default=None, description="Cookie domain for responses")
    trust_proxy: Optional[bool] = Field(default=None, description="Trust proxy headers for scheme/host")

    uvicorn_host: Optional[str] = Field(default=None, description="Override host for uvicorn")
    uvicorn_workers: Optional[int] = Field(default=None, description="Number of uvicorn workers")
    node_env: Optional[str] = Field(default=None, description="Node-style environment indicator")
    request_timeout_ms: Optional[int] = Field(default=None, description="Request timeout in ms")
    rate_limit_window_s: Optional[int] = Field(default=None, description="Rate limit window seconds")
    rate_limit_max: Optional[int] = Field(default=None, description="Max requests per window")

    # Pydantic v2 settings config pattern
    # - env_file and encoding supported by pydantic-settings v2
    # - extra="ignore" to avoid errors if unexpected env vars are present
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    # Validators to coerce list-like env inputs before Pydantic validates types
    @field_validator("allowed_origins", "allowed_headers", "allowed_methods", mode="before")
    @classmethod
    def _coerce_list_fields(cls, v):
        return _parse_list(v)


# PUBLIC_INTERFACE
def get_settings() -> AppSettings:
    """Return loaded application settings.

    Loads configuration from environment and optional .env file.
    Unknown environment variables are ignored to ensure preview environments do not fail.
    """
    return AppSettings()
