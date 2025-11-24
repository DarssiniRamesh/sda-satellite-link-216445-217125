"""
Domain models for coding profiles, frame configuration, and validation.

These Pydantic models define the configuration structures used by the Protocol and Coding Service.
They include validation for coding rates, LDPC profiles, and burst mode constraints to align with
acceptance criteria in the API documentation.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field, validator


SUPPORTED_PROTOCOLS = {"SDA4-5GNR-LDPC"}
SUPPORTED_ENCODINGS = {"OOK-NRZ", "Manchester"}
SUPPORTED_RATES = {0.5, 0.66, 0.75, 0.8, 0.9}


# PUBLIC_INTERFACE
class FrameConfig(BaseModel):
    """Configuration for encoding/decoding a frame."""

    protocol: Literal["SDA4-5GNR-LDPC"] = Field(..., description="Protocol family.")
    rate: float = Field(..., description="Coding rate (e.g., 0.5, 0.66, 0.75, 0.8, 0.9).")
    encoding: Literal["OOK-NRZ", "Manchester"] = Field(..., description="Line encoding.")
    burst_mode: bool = Field(False, description="Enable burst mode operation.")
    max_burst_frames: Optional[int] = Field(
        None, description="When burst_mode=True, maximum frames per burst window."
    )
    ldpc_profile: Optional[str] = Field(
        default="NR-BaseGraph1",
        description="LDPC profile key (placeholder registry), e.g., NR-BaseGraph1/2.",
    )
    arq_window: int = Field(16, ge=1, le=1024, description="ARQ sliding window size.")
    arq_max_retx: int = Field(3, ge=0, le=16, description="Max ARQ retransmissions per PDU.")
    crc: Literal["CRC16", "CRC32"] = Field("CRC32", description="CRC type for error detection.")

    @validator("rate")
    def validate_rate(cls, v: float) -> float:
        if v not in SUPPORTED_RATES:
            raise ValueError(f"Unsupported coding rate {v}. Supported rates: {sorted(SUPPORTED_RATES)}")
        return v

    @validator("ldpc_profile")
    def validate_ldpc_profile(cls, v: Optional[str]) -> Optional[str]:
        # Basic placeholder set of valid names
        valid = {"NR-BaseGraph1", "NR-BaseGraph2"}
        if v is not None and v not in valid:
            raise ValueError(f"Unsupported LDPC profile '{v}'. Valid: {sorted(valid)}")
        return v

    @validator("max_burst_frames", always=True)
    def validate_burst_mode(cls, v: Optional[int], values) -> Optional[int]:
        if values.get("burst_mode", False):
            if v is None or v <= 0 or v > 4096:
                raise ValueError("When burst_mode=True, max_burst_frames must be in [1, 4096].")
        else:
            if v is not None:
                raise ValueError("max_burst_frames must be None when burst_mode=False.")
        return v


# PUBLIC_INTERFACE
class EncodeRequest(BaseModel):
    """Encode request containing hex payload and frame configuration."""

    payload: str = Field(..., description="Hex-encoded data payload.")
    config: FrameConfig = Field(..., description="Frame configuration.")


# PUBLIC_INTERFACE
class EncodeResponse(BaseModel):
    """Encode response returning hex-encoded frame."""

    frame: str = Field(..., description="Hex-encoded protocol frame.")


# PUBLIC_INTERFACE
class DecodeRequest(BaseModel):
    """Decode request containing hex-encoded frame."""

    frame: str = Field(..., description="Hex-encoded protocol frame.")


# PUBLIC_INTERFACE
class DecodeResponse(BaseModel):
    """Decode response containing decoded payload and status."""

    payload: str = Field(..., description="Hex-encoded decoded payload.")
    status: Literal["ok", "crc_error", "fec_fail", "arq_pending"] = Field(
        ..., description="Decode status outcome."
    )


# PUBLIC_INTERFACE
class ARQStatusResponse(BaseModel):
    """ARQ status for the sliding window and retransmission counters."""

    window: list[str] = Field(..., description="Window entries indicating seq and state.")
    retransmissions: int = Field(..., ge=0, description="Total retransmissions attempted.")


# PUBLIC_INTERFACE
class TelemetryResponse(BaseModel):
    """Telemetry counters and timestamps."""

    frame_errors: int = Field(..., ge=0, description="Frames with errors.")
    fec_errors: int = Field(..., ge=0, description="FEC decode failures.")
    arq_retries: int = Field(..., ge=0, description="ARQ retry count.")
    timestamps: list[str] = Field(
        ..., description="ISO8601 timestamps of last processed frames."
    )
