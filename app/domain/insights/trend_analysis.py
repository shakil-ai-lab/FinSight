from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.insights import QuarterComparison


@dataclass(slots=True, frozen=True)
class TrendAnalysis:
    """
    Derived long-term trends identified from one or more
    quarter comparisons.

    Purpose
    -------
    Represents analytical observations about how the
    company's business performance has evolved over time.

    Created By
    ----------
    Knowledge Analysis Capability

    Consumed By
    -----------
    - Materiality Assessment
    - Analyst Brief Generation
    """

    comparisons: tuple[QuarterComparison, ...]

    revenue_trend: Optional[str] = None

    margin_trend: Optional[str] = None

    earnings_trend: Optional[str] = None

    cash_flow_trend: Optional[str] = None

    business_momentum: Optional[str] = None

    key_observations: tuple[str, ...] = ()

    summary: Optional[str] = None

    analyzed_at: datetime = field(default_factory=datetime.utcnow)