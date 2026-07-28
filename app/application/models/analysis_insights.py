from __future__ import annotations

from typing import Optional

from dataclasses import dataclass

from app.domain.insights import(
    CommunicationAnalysis,
    ConsistencyAnalysis,
    QuarterComparison,
    TrendAnalysis,
)


@dataclass(frozen=True, slots=True)
class AnalysisInsights:
    """
    Aggregates all analytical insights generated from
    extracted business knowledge.
    """

    consistency_analysis: ConsistencyAnalysis
    communication_analysis: CommunicationAnalysis

    quarter_comparison: Optional[QuarterComparison] = None
    trend_analysis: Optional[TrendAnalysis] = None