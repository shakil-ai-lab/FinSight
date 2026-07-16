from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class RiskSeverity(Enum):
    """
    Business-defined severity levels for an identified risk.
    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass(slots=True, frozen=True)
class Risk:
    """
    Structured representation of a single business risk
    extracted from one or more financial documents.

    Purpose
    -------
    Represents one identifiable risk that could materially
    affect the company's business or financial performance.

    Created By
    ----------
    Knowledge Extraction Capability

    Consumed By
    -----------
    - Materiality Assessment
    - Trend Analysis
    - Decision Support
    """

    title: str

    category: str

    description: str

    severity: RiskSeverity

    evidence: Optional[str] = None


@dataclass(slots=True, frozen=True)
class RiskAssessment:
    """
    Collection of business risks extracted from financial
    documents for a reporting period.

    Purpose
    -------
    Represents the overall risk profile of a company for
    a specific reporting period.
    """

    company: str

    fiscal_year: int

    fiscal_quarter: Optional[int] = None

    risks: tuple[Risk, ...] = ()

    overall_summary: Optional[str] = None

    extracted_at: datetime = field(default_factory=datetime.utcnow)