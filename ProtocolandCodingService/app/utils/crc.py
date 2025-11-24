"""
CRC utility functions supporting CRC-16 (IBM) and CRC-32 (IEEE 802.3).

Security notes:
- Avoids any dynamic code execution.
- Operates purely on bytes.
"""

from typing import Literal


CRC16_POLY = 0xA001  # bit-reflected 0x8005
CRC32_POLY = 0xEDB88320  # bit-reflected 0x04C11DB7


def _crc16_ibm(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ CRC16_POLY
            else:
                crc >>= 1
            crc &= 0xFFFF
    return crc & 0xFFFF


def _crc32_ieee(data: bytes) -> int:
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ CRC32_POLY
            else:
                crc >>= 1
            crc &= 0xFFFFFFFF
    return (~crc) & 0xFFFFFFFF


# PUBLIC_INTERFACE
def compute_crc(data: bytes, kind: Literal["CRC16", "CRC32"] = "CRC32") -> int:
    """Compute CRC over data for the requested kind."""
    if kind == "CRC16":
        return _crc16_ibm(data)
    return _crc32_ieee(data)
