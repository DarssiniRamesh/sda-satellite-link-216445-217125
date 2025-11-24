"""
ARQ state machine implementing a simple sliding window and retransmission tracking.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, Optional
import time
import logging


logger = logging.getLogger(__name__)


@dataclass
class ArqPacket:
    seq: int
    payload_hex: str
    retx_count: int = 0
    acked: bool = False
    timestamp: float = field(default_factory=lambda: time.time())


# PUBLIC_INTERFACE
class ARQState:
    """ARQ sliding window state and operations."""

    def __init__(self, window_size: int = 16, max_retx: int = 3) -> None:
        self.window_size = window_size
        self.max_retx = max_retx
        self.base_seq = 0
        self.next_seq = 0
        self.window: Deque[ArqPacket] = deque(maxlen=window_size)
        self.sent: Dict[int, ArqPacket] = {}
        self.total_retx = 0

    def _in_window(self, seq: int) -> bool:
        return (seq - self.base_seq) % 65536 < self.window_size

    # PUBLIC_INTERFACE
    def push(self, payload_hex: str) -> int:
        """Queue a new packet in window if space allows, return sequence number."""
        if len(self.window) >= self.window_size:
            raise RuntimeError("ARQ window is full.")
        seq = self.next_seq & 0xFFFF
        pkt = ArqPacket(seq=seq, payload_hex=payload_hex)
        self.window.append(pkt)
        self.sent[seq] = pkt
        self.next_seq = (self.next_seq + 1) & 0xFFFF
        return seq

    # PUBLIC_INTERFACE
    def ack(self, seq: int) -> None:
        """Mark a packet as acked and slide the window if possible."""
        pkt = self.sent.get(seq)
        if not pkt:
            return
        pkt.acked = True
        # Slide window from base while contiguous ACKed
        while self.window and self.window[0].acked:
            head = self.window.popleft()
            self.sent.pop(head.seq, None)
            self.base_seq = (head.seq + 1) & 0xFFFF

    # PUBLIC_INTERFACE
    def mark_for_retx(self, seq: int) -> Optional[int]:
        """Mark packet for retransmission if under limit; return new retx count or None if drop."""
        pkt = self.sent.get(seq)
        if not pkt:
            return None
        if pkt.acked:
            return pkt.retx_count
        if pkt.retx_count >= self.max_retx:
            logger.warning("Dropping packet seq=%s after max_retx.", seq)
            # Drop and slide if head
            if self.window and self.window[0].seq == seq:
                self.window.popleft()
                self.sent.pop(seq, None)
                self.base_seq = (seq + 1) & 0xFFFF
            else:
                self.sent.pop(seq, None)
            return None
        pkt.retx_count += 1
        self.total_retx += 1
        return pkt.retx_count

    # PUBLIC_INTERFACE
    def status(self) -> dict:
        """Return window status for API exposure."""
        entries = []
        for pkt in list(self.window):
            state = "ACK" if pkt.acked else ("RETX" if pkt.retx_count > 0 else "TX")
            entries.append(f"seq={pkt.seq},state={state},retx={pkt.retx_count}")
        return {"window": entries, "retransmissions": self.total_retx}
