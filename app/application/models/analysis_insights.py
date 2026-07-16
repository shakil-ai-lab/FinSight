from __future__ import annotations

from dataclasses import dataclass

from domain.analysis.communication_analysis import CommunicationAnalysis
from domain.analysis.consistency_analysis import ConsistencyAnalysis
from domain.analysis.quarter_comparison import QuarterComparison
from domain.analysis.trend_analysis import TrendAnalysis


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