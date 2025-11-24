"""
ARQ configuration models.
"""

from pydantic import BaseModel, Field


# PUBLIC_INTERFACE
class ARQConfig(BaseModel):
    """Configuration for ARQ window and retransmissions."""

    window_size: int = Field(16, ge=1, le=1024, description="Sliding window size.")
    max_retx: int = Field(3, ge=0, le=16, description="Max retransmissions per packet.")
