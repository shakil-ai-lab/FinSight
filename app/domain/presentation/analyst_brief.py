from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.decision_support import MaterialityAssessment


@dataclass(slots=True, frozen=True)
class AnalystBrief:
    """
    Executive-level summary produced from the completed
    financial analysis workflow.

    Purpose
    -------
    Represents the final presentation of analytical
    conclusions for investors, executives, or decision
    makers.

    Created By
    ----------
    Presentation Capability

    Consumed By
    -----------
    - API Layer
    - Streamlit UI
    - PDF Report Generator
    """

    materiality_assessment: MaterialityAssessment

    executive_summary: str

    investment_highlights: tuple[str, ...] = ()

    key_risks: tuple[str, ...] = ()

    recommendation: str = ""

    generated_at: datetime = field(default_factory=datetime.utcnow)