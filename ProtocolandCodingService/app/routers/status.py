"""
Status and telemetry router.

Exposes:
- /telemetry: protocol telemetry and error statistics
- /status/verify: implementation verification details and capabilities
"""

from fastapi import APIRouter
from app.models.coding_profiles import TelemetryResponse
from app.routers.coding import get_telemetry_snapshot

router = APIRouter(tags=["health", "protocol"])


# PUBLIC_INTERFACE
@router.get(
    "/telemetry",
    summary="Get protocol telemetry and error statistics",
    response_model=TelemetryResponse,
)
def telemetry() -> TelemetryResponse:
    """Return telemetry counters."""
    s = get_telemetry_snapshot()
    return TelemetryResponse(
        frame_errors=s["frame_errors"],
        fec_errors=s["fec_errors"],
        arq_retries=s["arq_retries"],
        timestamps=s["timestamps"],
    )


# PUBLIC_INTERFACE
@router.get(
    "/status/verify",
    summary="Implementation verification and capabilities",
)
def status_verify() -> dict:
    """Return implementation metadata and basic acceptance criteria mapping."""
    return {
        "service": "ProtocolandCodingService",
        "version": "0.1.0",
        "capabilities": {
            "crc": ["CRC16", "CRC32"],
            "scrambler": "LFSR placeholder",
            "ldpc": ["NR-BaseGraph1", "NR-BaseGraph2"],
            "arq": {"window": True, "max_retx": True},
            "burst_mode": "validated (no physical timing gating in placeholder)",
        },
        "notes": "LDPC encode/decode are CPU placeholders; FPGA hooks present.",
    }
