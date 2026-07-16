from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True, frozen=True)
class TranscriptAnalysis:
    """
    Structured knowledge extracted from an earnings call
    transcript.

    Purpose
    -------
    Represents significant discussion points identified
    during management presentations and analyst Q&A.

    Created By
    ----------
    Knowledge Extraction Capability

    Consumed By
    -----------
    - Consistency Analysis
    - Sentiment Analysis
    - Materiality Assessment
    - Analyst Brief Generation
    """

    company: str

    fiscal_year: int

    fiscal_quarter: Optional[int] = None

    key_topics: tuple[str, ...] = ()

    analyst_questions: tuple[str, ...] = ()

    management_responses: tuple[str, ...] = ()

    notable_announcements: tuple[str, ...] = ()

    unanswered_concerns: tuple[str, ...] = ()

    extracted_at: datetime = field(default_factory=datetime.utcnow)