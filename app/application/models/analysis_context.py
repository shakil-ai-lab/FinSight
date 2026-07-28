from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.application.models import ExtractedKnowledge


@dataclass(frozen=True, slots=True)
class AnalysisContext:
    """
    Contains all information available for analysis.

    The context is designed to grow as FinSight evolves
    from single-document analysis to multi-document
    equity research.
    """

    current_knowledge: ExtractedKnowledge

    previous_knowledge: Optional[ExtractedKnowledge] = None