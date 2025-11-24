"""
Frame layout models and helpers.

Defines simple placeholder structures for preamble and header formatting to construct
hex-encoded frames. Real implementation would align exactly with SDA OCT header fields.
"""

from pydantic import BaseModel, Field
from typing import Optional


# PUBLIC_INTERFACE
class Preamble(BaseModel):
    """Frame preamble parameters."""

    sync: str = Field("A5A5A5A5", description="Hex sync word for preamble.")
    version: int = Field(1, ge=0, le=255, description="Protocol version byte.")


# PUBLIC_INTERFACE
class Header(BaseModel):
    """Frame header minimal placeholder."""

    seq: int = Field(..., ge=0, le=65535, description="Sequence number.")
    length: int = Field(..., ge=0, description="Payload length in bytes.")
    flags: int = Field(0, ge=0, le=255, description="Bit flags for ARQ/fragmentation.")
    fec: str = Field("LDPC", description="FEC type identifier.")
    crc_type: str = Field("CRC32", description="CRC used for payload.")


def build_header_bytes(header: Header) -> bytes:
    """
    Build a minimal header byte array. This is a simplified format:
    [seq_hi, seq_lo, len_hi, len_lo, flags, fec_tag_byte, crc_tag_byte]
    """
    seq_hi = (header.seq >> 8) & 0xFF
    seq_lo = header.seq & 0xFF
    length = header.length
    len_hi = (length >> 8) & 0xFF
    len_lo = length & 0xFF
    flags_b = header.flags & 0xFF
    # Simplified tag mapping
    fec_tag = 0x01 if header.fec == "LDPC" else 0x00
    crc_tag = 0x02 if header.crc_type == "CRC32" else 0x01
    return bytes([seq_hi, seq_lo, len_hi, len_lo, flags_b, fec_tag, crc_tag])


def build_preamble_bytes(preamble: Preamble) -> bytes:
    """
    Build preamble as version + sync bytes.
    """
    try:
        sync_bytes = bytes.fromhex(preamble.sync)
    except ValueError as exc:
        raise ValueError("Invalid preamble sync hex.") from exc
    version_b = bytes([preamble.version & 0xFF])
    return version_b + sync_bytes
