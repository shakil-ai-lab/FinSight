from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(slots=True, frozen=True)
class ManagementDiscussion:
    """
    Structured qualitative knowledge extracted from the
    Management Discussion & Analysis (MD&A) section of one
    or more financial documents.

    Purpose
    -------
    Represents management's explanation of the company's
    business performance during a reporting period.

    Created By
    ----------
    Knowledge Extraction Capability

    Consumed By
    -----------
    - Trend Analysis
    - Consistency Analysis
    - Materiality Assessment
    - Analyst Brief Generation
    """

    company: str

    fiscal_year: int

    fiscal_quarter: Optional[int] = None

    business_summary: Optional[str] = None

    performance_drivers: tuple[str, ...] = ()

    operational_highlights: tuple[str, ...] = ()

    strategic_initiatives: tuple[str, ...] = ()

    management_commentary: tuple[str, ...] = ()

    extracted_at: datetime = field(default_factory=datetime.utcnow)