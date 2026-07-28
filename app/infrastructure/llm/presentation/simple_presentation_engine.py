from __future__ import annotations

from app.application.models.decision_result import DecisionResult
from app.application.ports.presentation_engine import PresentationEngine

from app.domain.presentation import AnalystBrief


class SimplePresentationEngine(PresentationEngine):
    """
    Deterministic Presentation implementation.

    Converts a DecisionResult into an AnalystBrief without
    invoking an LLM.
    """

    def present(
        self,
        result: DecisionResult,
    ) -> AnalystBrief:

        assessment = result.materiality_assessment

        return AnalystBrief(
            materiality_assessment=assessment,
            executive_summary=assessment.overall_assessment or "",
            investment_highlights=assessment.significant_findings,
            key_risks=assessment.critical_findings,
            recommendation=assessment.recommendation or "",
        )