from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True, frozen=True)
class GuidanceSummary:
    """
    Structured forward-looking guidance extracted from
    financial filings and earnings call transcripts.

    Purpose
    -------
    Represents management's expectations and outlook for
    future business performance.

    Created By
    ----------
    Knowledge Extraction Capability

    Consumed By
    -----------
    - Trend Analysis
    - Materiality Assessment
    - Decision Support
    - Analyst Brief Generation
    """

    company: str

    fiscal_year: int

    fiscal_quarter: Optional[int] = None

    revenue_guidance: Optional[str] = None

    earnings_guidance: Optional[str] = None

    margin_guidance: Optional[str] = None

    cash_flow_guidance: Optional[str] = None

    capital_expenditure_guidance: Optional[str] = None

    strategic_outlook: tuple[str, ...] = ()

    management_expectations: tuple[str, ...] = ()

    extracted_at: datetime = field(default_factory=datetime.utcnow)