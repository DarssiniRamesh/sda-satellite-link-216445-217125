from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ARQState:
    """
    Sliding window ARQ state with wrap-around and retransmission control.

    Requirements:
    - REQ-ARQ-WINDOW: enforce max window size
    - REQ-ARQ-RETX: enforce retransmission count per packet
    - REQ-ARQ-WRAP: 16-bit sequence wrap-around behavior
    """

    window_size: int = 16
    max_retx: int = 3
    base_seq: int = 0  # oldest outstanding (16-bit space)
    next_seq: int = 0
    retransmissions: int = 0
    window: Dict[int, str] = field(default_factory=dict)  # seq -> payload_hex
    retx_count: Dict[int, int] = field(default_factory=dict)  # seq -> count

    def _in_window(self, seq: int) -> bool:
        """Return True if seq is within the current window starting at base_seq."""
        distance = (seq - self.base_seq) & 0xFFFF
        return distance < self.window_size

    # PUBLIC_INTERFACE
    def push(self, payload_hex: str) -> int:
        """Add a new payload into the ARQ window and assign a sequence number.

        Raises:
            RuntimeError: if the window is full (REQ-ARQ-WINDOW).
        """
        if len(self.window) >= self.window_size:
            raise RuntimeError("REQ-ARQ-WINDOW: window full")
        seq = self.next_seq & 0xFFFF
        # If the seq would not be in the window relative to base (extreme edge), slide base cautiously
        if not self._in_window(seq) and self.window:
            # Avoid overrun; this condition shouldn't generally occur with size checks,
            # but keep a defensive realignment.
            self.base_seq = seq
        self.window[seq] = payload_hex
        self.retx_count.setdefault(seq, 0)
        self.next_seq = (self.next_seq + 1) & 0xFFFF
        return seq

    # PUBLIC_INTERFACE
    def ack(self, seq: int) -> None:
        """Acknowledge a sequence number and slide the window as needed."""
        if seq in self.window:
            del self.window[seq]
            self.retx_count.pop(seq, None)
            self._recompute_base()

    def _recompute_base(self) -> None:
        """Recompute base_seq to the oldest outstanding seq (closest to current base)."""
        if not self.window:
            self.base_seq = self.next_seq
            return
        # Choose the outstanding seq with the smallest forward distance from current base
        candidates = list(self.window.keys())
        candidates.sort(key=lambda s: (s - self.base_seq) & 0xFFFF)
        self.base_seq = candidates[0]

    # PUBLIC_INTERFACE
    def mark_for_retx(self, seq: int) -> int | None:
        """Mark a sequence for retransmission if below limit.

        Returns:
            int | None: The new retransmission count, or None if dropped/unknown.

        Behavior:
        - If seq unknown, returns None (treated as dropped).
        - If exceeding max_retx, remove from window (REQ-ARQ-RETX).
        """
        if seq not in self.window:
            return None
        count = self.retx_count.get(seq, 0) + 1
        if count > self.max_retx:
            # Drop packet after exceeding limit
            del self.window[seq]
            self.retx_count.pop(seq, None)
            return None
        self.retx_count[seq] = count
        self.retransmissions += 1
        return count

    # PUBLIC_INTERFACE
    def status(self) -> Dict[str, object]:
        """Return a window status snapshot.

        Returns:
            dict: { "window": [ "seq_hex:retx_count", ...], "retransmissions": int }
        """
        entries = [f"{s:04x}:{self.retx_count.get(s, 0)}" for s in sorted(self.window.keys())]
        return {"window": entries, "retransmissions": self.retransmissions}
