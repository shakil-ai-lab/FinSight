from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class AnalysisType(Enum):
    """Supported analysis types."""

    ANNUAL = "annual"
    QUARTERLY = "quarterly"
    TRANSCRIPT = "transcript"
    COMPREHENSIVE = "comprehensive"


class DocumentType(Enum):
    """Supported financial document types."""

    TEN_K = "10-K"
    TEN_Q = "10-Q"
    EARNINGS_TRANSCRIPT = "earnings_transcript"


@dataclass(slots=True)
class AnalysisRequest:
    """
    Represents a business request to analyze a company.

    This is a Domain object.
    It contains business information only and is independent
    of FastAPI, SQLAlchemy, LangGraph, and LLM providers.
    """

    company: str
    analysis_type: AnalysisType
    fiscal_year: int

    ticker: Optional[str] = None
    fiscal_quarter: Optional[int] = None
    include_documents: list[DocumentType] = field(default_factory=list)

    created_at: datetime = field(default_factory=datetime.utcnow)