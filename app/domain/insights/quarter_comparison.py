from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional

from domain.knowledge import FinancialSnapshot


@dataclass(slots=True, frozen=True)
class QuarterComparison:
    """
    Derived comparison between two financial reporting periods.

    Purpose
    -------
    Represents the analytical differences between a current
    financial snapshot and a previous financial snapshot.

    Created By
    ----------
    Knowledge Analysis Capability

    Consumed By
    -----------
    - Trend Analysis
    - Materiality Assessment
    - Analyst Brief Generation
    """

    current: FinancialSnapshot

    previous: FinancialSnapshot

    revenue_change: Optional[Decimal] = None

    gross_margin_change: Optional[Decimal] = None

    operating_income_change: Optional[Decimal] = None

    net_income_change: Optional[Decimal] = None

    earnings_per_share_change: Optional[Decimal] = None

    operating_cash_flow_change: Optional[Decimal] = None

    summary: Optional[str] = None

    analyzed_at: datetime = field(default_factory=datetime.utcnow)