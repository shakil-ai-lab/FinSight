from __future__ import annotations

from abc import ABC, abstractmethod

from application.models import AnalysisInsights, DecisionResult


class DecisionSupportService(ABC):
    """
    Defines the application capability responsible for
    evaluating the significance of analytical insights.
    """

    @abstractmethod
    def assess(
        self,
        insights: AnalysisInsights,
    ) -> DecisionResult:
        """
        Produce the decision support result from
        analytical insights.
        """
        raise NotImplementedError