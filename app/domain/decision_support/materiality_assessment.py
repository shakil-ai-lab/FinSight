from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.insights import (
    CommunicationAnalysis,
    ConsistencyAnalysis,
    QuarterComparison,
    TrendAnalysis,
)
from domain.knowledge import RiskAssessment


@dataclass(slots=True, frozen=True)
class MaterialityAssessment:
    """
    Prioritized assessment of the most significant findings
    identified during financial analysis.

    Purpose
    -------
    Represents the analytical conclusion about which
    business findings deserve the greatest attention from
    investors and decision makers.

    Created By
    ----------
    Decision Support Capability

    Consumed By
    -----------
    - Analyst Brief Generation
    """

    quarter_comparison: QuarterComparison

    trend_analysis: TrendAnalysis

    consistency_analysis: ConsistencyAnalysis

    communication_analysis: CommunicationAnalysis

    risk_assessment: RiskAssessment

    critical_findings: tuple[str, ...] = ()

    significant_findings: tuple[str, ...] = ()

    informational_findings: tuple[str, ...] = ()

    overall_assessment: Optional[str] = None

    recommendation: Optional[str] = None

    assessed_at: datetime = field(default_factory=datetime.utcnow)