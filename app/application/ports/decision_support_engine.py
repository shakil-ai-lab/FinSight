from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.models.analysis_insights import AnalysisInsights
from app.application.models.decision_result import DecisionResult
from app.application.models.extracted_knowledge import ExtractedKnowledge


class DecisionSupportEngine(ABC):
    """
    Contract for Decision Support implementations.
    """

    @abstractmethod
    def generate(
        self,
        knowledge: ExtractedKnowledge,
        insights: AnalysisInsights,
    ) -> DecisionResult:
        """
        Produce the final decision support result.
        """
        raise NotImplementedError