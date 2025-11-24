"""
LDPC encoder/decoder placeholder.

This module provides CPU placeholder methods and a simple profile registry. It includes
hooks where FPGA offloading would be integrated. For now, encoding/decoding are pass-through
to keep service functional and testable without hardware acceleration.
"""

from typing import Dict, Optional


_LDPC_PROFILES: Dict[str, Dict[str, int]] = {
    # Placeholder profiles
    "NR-BaseGraph1": {"n": 8448, "k": 4224},
    "NR-BaseGraph2": {"n": 8448, "k": 2816},
}


# PUBLIC_INTERFACE
def get_profile(name: str) -> Optional[Dict[str, int]]:
    """Return LDPC profile params if available."""
    return _LDPC_PROFILES.get(name)


# PUBLIC_INTERFACE
def cpu_ldpc_encode(data: bytes, profile: str) -> bytes:
    """CPU placeholder for LDPC encode. Just echo data for now."""
    _ = get_profile(profile)  # validate presence; not enforcing lengths here
    return data


# PUBLIC_INTERFACE
def cpu_ldpc_decode(data: bytes, profile: str) -> tuple[bytes, bool]:
    """CPU placeholder for LDPC decode. Returns data and success flag."""
    _ = get_profile(profile)
    return data, True


# PUBLIC_INTERFACE
def fpga_encode(data: bytes, profile: str) -> bytes:
    """Hook for FPGA encode offload - not implemented."""
    # In production, route to FPGA device driver/API.
    return cpu_ldpc_encode(data, profile)


# PUBLIC_INTERFACE
def fpga_decode(data: bytes, profile: str) -> tuple[bytes, bool]:
    """Hook for FPGA decode offload - not implemented."""
    return cpu_ldpc_decode(data, profile)
