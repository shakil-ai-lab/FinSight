from __future__ import annotations

from app.application.models.analysis_insights import AnalysisInsights
from app.application.models.decision_result import DecisionResult
from app.application.models.extracted_knowledge import ExtractedKnowledge
from app.application.ports.decision_support_engine import (
    DecisionSupportEngine,
)


class DecisionSupportService:
    """
    Application service responsible for executing the
    Decision Support capability.

    Responsibilities
    ----------------
    - Coordinate the Decision Support workflow.
    - Delegate reasoning to the configured DecisionSupportEngine.
    """

    def __init__(
        self,
        decision_support_engine: DecisionSupportEngine,
    ) -> None:
        self._decision_support_engine = decision_support_engine

    def generate_decision_support(
        self,
        knowledge: ExtractedKnowledge,
        insights: AnalysisInsights,
    ) -> DecisionResult:
        """
        Generate the final decision support result.

        Parameters
        ----------
        knowledge:
            Structured financial knowledge extracted from
            source documents.

        insights:
            Analytical insights produced by the Knowledge
            Analysis capability.

        Returns
        -------
        DecisionResult
            Final decision support output.
        """

        return self._decision_support_engine.generate(
            knowledge=knowledge,
            insights=insights,
        )