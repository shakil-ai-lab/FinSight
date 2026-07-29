from __future__ import annotations

from app.application.models import (
    DecisionResult,
    ExtractedKnowledge,
    PresentationOutput,
)
from app.application.ports.presentation_engine import PresentationEngine

from app.domain.presentation import AnalystBrief


class PresentationService:
    """
    Application service responsible for producing the
    final presentation output.

    The Presentation capability combines the executive
    analyst brief with the extracted factual knowledge
    required by presentation clients such as the
    Streamlit dashboard.
    """

    def __init__(
        self,
        engine: PresentationEngine,
    ) -> None:
        self._engine = engine

    def present(
        self,
        knowledge: ExtractedKnowledge,
        result: DecisionResult,
    ) -> PresentationOutput:
        """
        Build the final presentation output.

        Parameters
        ----------
        knowledge
            Factual knowledge extracted from the source documents.

        result
            Investment decision produced by the Decision Support capability.

        Returns
        -------
        PresentationOutput
            Final application model consumed by the presentation layer.
        """

        analyst_brief: AnalystBrief = self._engine.present(result)

        return PresentationOutput(
            analyst_brief=analyst_brief,
            extracted_knowledge=knowledge,
        )