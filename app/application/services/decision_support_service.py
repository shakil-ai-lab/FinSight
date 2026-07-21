from __future__ import annotations



from app.application.models import AnalysisInsights, DecisionResult


class DecisionSupportService:
    """
    Defines the application capability responsible for
    evaluating the significance of analytical insights.
    """

   
    def assess(
        self,
        insights: AnalysisInsights,
    ) -> DecisionResult:
        """
        Produce the decision support result from
        analytical insights.
        """
        raise NotImplementedError