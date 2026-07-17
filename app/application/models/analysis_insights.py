from __future__ import annotations

from dataclasses import dataclass

from domain. insights import(
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

    This model represents the complete output of the
    Knowledge Analysis capability and serves as the
    contract between KnowledgeAnalysisService and
    DecisionSupportService.
    """

    quarter_comparison: QuarterComparison
    trend_analysis: TrendAnalysis
    consistency_analysis: ConsistencyAnalysis
    communication_analysis: CommunicationAnalysis