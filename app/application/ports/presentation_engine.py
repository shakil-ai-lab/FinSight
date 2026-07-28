from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.models.decision_result import DecisionResult
from app.domain.presentation import AnalystBrief


class PresentationEngine(ABC):
    """
    Contract for Presentation implementations.
    """

    @abstractmethod
    def present(
        self,
        result: DecisionResult,
    ) -> AnalystBrief:
        """
        Convert a DecisionResult into an AnalystBrief.
        """
        raise NotImplementedError