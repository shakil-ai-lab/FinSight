from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.models import (
    AnalysisInsights,
    ExtractedKnowledge,
)


class KnowledgeAnalyzer(ABC):
    """
    Application port responsible for generating analytical
    insights from extracted business knowledge.
    """

    @abstractmethod
    def analyze(
        self,
        knowledge: ExtractedKnowledge,
    ) -> AnalysisInsights:
        """
        Analyze extracted knowledge and return business insights.
        """
        ...