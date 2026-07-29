from __future__ import annotations

from dataclasses import dataclass

from app.application.models.extracted_knowledge import ExtractedKnowledge
from app.domain.presentation import AnalystBrief


@dataclass(frozen=True, slots=True)
class PresentationOutput:
    """
    Final output produced by the Presentation capability.

    Combines the executive analyst brief with the extracted
    factual knowledge required by the presentation layer.

    This model is intended to be consumed by UI applications
    (e.g. Streamlit dashboard) and report generators.
    """

    analyst_brief: AnalystBrief
    extracted_knowledge: ExtractedKnowledge