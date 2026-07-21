from __future__ import annotations



from app.application.models import DecisionResult

from app.domain.presentation import AnalystBrief


class PresentationService:
    """
    Defines the application capability responsible for
    presenting the final analyst report.
    """

    
    def present(
        self,
        result: DecisionResult,
    ) -> AnalystBrief:
        """
        Produce the final analyst brief.
        """
        raise NotImplementedError