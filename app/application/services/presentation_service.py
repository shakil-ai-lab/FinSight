from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.models import DecisionResult

from app.domain.presentation import AnalystBrief


class PresentationService(ABC):
    """
    Defines the application capability responsible for
    presenting the final analyst report.
    """

    @abstractmethod
    def present(
        self,
        result: DecisionResult,
    ) -> AnalystBrief:
        """
        Produce the final analyst brief.
        """
        raise NotImplementedError