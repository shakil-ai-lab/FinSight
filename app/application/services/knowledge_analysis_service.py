from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.models import AnalysisInsights, ExtractedKnowledge


class KnowledgeAnalysisService(ABC):
    """
    Defines the application capability responsible for
    analyzing extracted business knowledge.
    """

    @abstractmethod
    def analyze(
        self,
        knowledge: ExtractedKnowledge,
    ) -> AnalysisInsights:
        """
        Produce analytical insights from extracted knowledge.
        """
        raise NotImplementedError