"""
ARQ router exposing status and simple management endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.models.arq_config import ARQConfig
from app.models.coding_profiles import ARQStatusResponse

from app.services.arq_state import ARQState

router = APIRouter(prefix="/arq", tags=["protocol"])

# Global ARQ state (in-memory)
_ARQ = ARQState()


# PUBLIC_INTERFACE
@router.get(
    "/status",
    summary="Get ARQ window and retransmission status",
    response_model=ARQStatusResponse,
)
def arq_status() -> ARQStatusResponse:
    """Return ARQ state including window entries and retransmissions."""
    s = _ARQ.status()
    return ARQStatusResponse(window=s["window"], retransmissions=s["retransmissions"])


# PUBLIC_INTERFACE
@router.post(
    "/configure",
    summary="Configure ARQ window and max retransmissions",
    response_model=ARQStatusResponse,
)
def arq_configure(cfg: ARQConfig) -> ARQStatusResponse:
    """Update ARQ window configuration."""
    # Reinitialize ARQ with new settings (drops old window)
    global _ARQ  # noqa: PLW0603
    _ARQ = ARQState(window_size=cfg.window_size, max_retx=cfg.max_retx)
    s = _ARQ.status()
    return ARQStatusResponse(window=s["window"], retransmissions=s["retransmissions"])


# PUBLIC_INTERFACE
@router.post(
    "/enqueue",
    summary="Enqueue a payload for ARQ managed transmission and get sequence number",
)
def arq_enqueue(payload_hex: str) -> dict:
    """Push a payload into ARQ window and return assigned sequence number."""
    payload_hex = payload_hex.strip().lower()
    if not payload_hex or any(c not in "0123456789abcdef" for c in payload_hex):
        raise HTTPException(status_code=400, detail="payload_hex must be lowercase hex string.")
    try:
        seq = _ARQ.push(payload_hex)
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"seq": seq}


# PUBLIC_INTERFACE
@router.post(
    "/ack",
    summary="Acknowledge a sequence number",
)
def arq_ack(seq: int) -> dict:
    """Mark a given sequence as acknowledged and slide window as needed."""
    seq = seq & 0xFFFF
    _ARQ.ack(seq)
    return {"status": "ok"}


# PUBLIC_INTERFACE
@router.post(
    "/nack",
    summary="Negative acknowledge a sequence number, triggering retransmission if allowed",
)
def arq_nack(seq: int) -> dict:
    """Mark for retransmission; if over limit, packet is dropped."""
    seq = seq & 0xFFFF
    result = _ARQ.mark_for_retx(seq)
    if result is None:
        return {"status": "dropped"}
    return {"status": "retx", "count": result}
