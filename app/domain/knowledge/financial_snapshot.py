from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(slots=True, frozen=True)
class FinancialSnapshot:
    """
    Structured financial facts extracted from one or more
    source documents.

    Purpose
    -------
    Represents the core financial position of a company
    for a reporting period.

    Created By
    ----------
    Knowledge Extraction Capability

    Consumed By
    -----------
    - Knowledge Analysis
    - Decision Support
    - Analyst Brief Generation
    """

    company: str

    fiscal_year: int

    fiscal_quarter: Optional[int] = None

    revenue: Optional[Decimal] = None

    gross_margin: Optional[Decimal] = None

    operating_income: Optional[Decimal] = None

    net_income: Optional[Decimal] = None

    earnings_per_share: Optional[Decimal] = None

    operating_cash_flow: Optional[Decimal] = None

    extracted_at: datetime = field(default_factory=datetime.utcnow)