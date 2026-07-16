from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.knowledge import (
    GuidanceSummary,
    ManagementDiscussion,
    TranscriptAnalysis,
)


@dataclass(slots=True, frozen=True)
class CommunicationAnalysis:
    """
    Derived analysis of management's communication with
    investors across financial filings and earnings calls.

    Purpose
    -------
    Represents analytical observations about the quality,
    clarity, transparency, and confidence of management's
    communication.

    Created By
    ----------
    Knowledge Analysis Capability

    Consumed By
    -----------
    - Materiality Assessment
    - Analyst Brief Generation
    """

    management_discussion: ManagementDiscussion

    transcript_analysis: TranscriptAnalysis

    guidance_summary: Optional[GuidanceSummary] = None

    communication_quality: Optional[str] = None

    confidence_level: Optional[str] = None

    transparency_assessment: Optional[str] = None

    key_messages: tuple[str, ...] = ()

    notable_concerns: tuple[str, ...] = ()

    summary: Optional[str] = None

    analyzed_at: datetime = field(default_factory=datetime.utcnow)