from __future__ import annotations

from dataclasses import dataclass

from app.domain.knowledge import (
    BusinessSegments,
    FinancialSnapshot,
    GuidanceSummary,
    RiskAssessment,
    TranscriptAnalysis,
    ManagementDiscussion,
)

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
    management_discussion: ManagementDiscussion
    risk_assessment: RiskAssessment
    guidance_summary: GuidanceSummary
    transcript_analysis: TranscriptAnalysis