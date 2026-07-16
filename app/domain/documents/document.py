from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class DocumentType(Enum):
    """
    Supported financial document types.
    """

    TEN_K = "10-K"
    TEN_Q = "10-Q"
    EARNINGS_TRANSCRIPT = "earnings_transcript"


class DocumentSource(Enum):
    """
    Source from which a document was acquired.
    """

    EDGAR = "edgar"
    EARNINGS_CALL = "earnings_call"
    LOCAL_FILE = "local_file"
    MANUAL_UPLOAD = "manual_upload"


@dataclass(slots=True, frozen=True)
class SourceDocument:
    """
    Represents a financial document acquired for analysis.

    Purpose
    -------
    Acts as the canonical domain representation of a source
    document used throughout the analysis workflow.

    Created By
    ----------
    Document Acquisition Capability

    Consumed By
    -----------
    - Knowledge Extraction
    - Evidence Tracking
    - Analysis State
    """

    company: str

    document_type: DocumentType

    source: DocumentSource

    fiscal_year: int

    fiscal_quarter: Optional[int] = None

    filing_date: Optional[date] = None

    content: str = ""

    retrieved_at: datetime = field(default_factory=datetime.utcnow)