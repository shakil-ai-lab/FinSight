from __future__ import annotations

from app.application.models import (
    AnalysisInsights,
    ExtractedKnowledge,
)
from app.application.ports import KnowledgeAnalyzer


class KnowledgeAnalysisService:
    """
    Application service responsible for coordinating
    the Knowledge Analysis capability.
    """

    def __init__(
        self,
        analyzer: KnowledgeAnalyzer,
    ) -> None:
        self._analyzer = analyzer

    def analyze(
        self,
        knowledge: ExtractedKnowledge,
    ) -> AnalysisInsights:
        return self._analyzer.analyze(knowledge)