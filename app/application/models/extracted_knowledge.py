from __future__ import annotations

from dataclasses import dataclass

from domain.knowledge.business_segments import BusinessSegments
from domain.knowledge.financial_snapshot import FinancialSnapshot
from domain.knowledge.guidance_summary import GuidanceSummary
from domain.knowledge.risk_assessment import RiskAssessment
from domain.knowledge.transcript_analysis import TranscriptAnalysis


@dataclass(frozen=True, slots=True)
class ExtractedKnowledge:
    """
    Aggregates all knowledge extracted from the acquired documents.

    This model represents the complete output of the
    Knowledge Extraction capability and serves as the
    contract between KnowledgeExtractionService and
    KnowledgeAnalysisService.
    """

    financial_snapshot: FinancialSnapshot
    business_segments: BusinessSegments
    risk_assessment: RiskAssessment
    guidance_summary: GuidanceSummary
    transcript_analysis: TranscriptAnalysis