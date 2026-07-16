from __future__ import annotations

from dataclasses import dataclass

from domain.decision.materiality_assessment import MaterialityAssessment


@dataclass(frozen=True, slots=True)
class DecisionResult:
    """
    Represents the output of the Decision Support capability.

    This model serves as the contract between
    DecisionSupportService and PresentationService.
    """

    materiality_assessment: MaterialityAssessment