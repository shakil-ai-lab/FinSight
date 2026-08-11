from enum import Enum


class DocumentType(Enum):
    """Supported financial document types."""
    
    TEN_K = "10-K"
    TEN_Q = "10-Q"
    EARNINGS_TRANSCRIPT = "earnings_transcript"