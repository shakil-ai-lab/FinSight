from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.knowledge import (
    FinancialSnapshot,
    ManagementDiscussion,
    GuidanceSummary,
)


@dataclass(slots=True, frozen=True)
class ConsistencyAnalysis:
    """
    Derived analysis measuring the consistency between
    financial performance and management communication.

    Purpose
    -------
    Represents analytical observations about whether
    management's narrative aligns with the underlying
    financial evidence.

    Created By
    ----------
    Knowledge Analysis Capability

    Consumed By
    -----------
    - Materiality Assessment
    - Analyst Brief Generation
    """

    financial_snapshot: FinancialSnapshot

    management_discussion: ManagementDiscussion

    guidance_summary: Optional[GuidanceSummary] = None

    consistency_score: Optional[int] = None

    supporting_observations: tuple[str, ...] = ()

    inconsistencies: tuple[str, ...] = ()

    summary: Optional[str] = None

    analyzed_at: datetime = field(default_factory=datetime.utcnow)