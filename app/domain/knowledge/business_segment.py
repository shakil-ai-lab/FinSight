from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(slots=True, frozen=True)
class BusinessSegment:
    """
    Structured financial facts for a single business segment.

    Purpose
    -------
    Represents the financial performance of one operating
    segment extracted from company filings.

    Examples
    --------
    Apple
        - iPhone
        - Services
        - Mac

    Microsoft
        - Intelligent Cloud
        - Productivity and Business Processes

    Created By
    ----------
    Knowledge Extraction Capability

    Consumed By
    -----------
    - Trend Analysis
    - Quarter Comparison
    - Decision Support
    """

    name: str

    revenue: Optional[Decimal] = None

    operating_income: Optional[Decimal] = None

    growth_rate: Optional[Decimal] = None

    description: Optional[str] = None


@dataclass(slots=True, frozen=True)
class BusinessSegments:
    """
    Collection of business segments extracted from one or
    more source documents.

    Purpose
    -------
    Represents the complete segment-level view of a company
    for a reporting period.
    """

    company: str

    fiscal_year: int

    fiscal_quarter: Optional[int] = None

    segments: tuple[BusinessSegment, ...] = ()

    extracted_at: datetime = field(default_factory=datetime.utcnow)